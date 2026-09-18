"""Synthetic offline tests. No token, network, or real Issue write is performed."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("documentation_journal", ROOT / "scripts/documentation_journal.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

A, B, C = "a" * 40, "b" * 40, "c" * 40
CFG = {"repository": "example/factory", "repository_id": 42, "notice_issue": 26,
       "writer_login": "github-actions[bot]", "default_branch": "main",
       "baseline_sha": A, "since": "2026-01-01T00:00:00Z", "paths": ["docs/*", "*.md", "templates/*"]}


def change(path="docs/guide.md", status="M", old=None):
    return {"status": status, "old": old or path, "new": path, "old_blob": A, "new_blob": B}


def pr(head=B, state="open", body="", base=A, base_ref="main", number=1):
    return {"number": number, "base": {"repo": {"id": 42}, "sha": base, "ref": base_ref},
            "head": {"repo": {"id": 43}, "sha": head}, "state": state, "body": body,
            "user": {"login": "contributor"}, "draft": False, "merged": False,
            "updated_at": "2026-01-02T00:00:00Z"}


def snap(p=None, changes=None):
    changes = [change()] if changes is None else changes
    return m.candidate(p or pr(), changes, A)


class FakeAPI:
    def __init__(self):
        self.rows, self.posts = [], 0
        self.lost, self.fail, self.patch_fail = False, False, False
        self.prs, self.timeline = [], []
        self.tip = C
        self.after = None

    def pages(self, path):
        if path.startswith("/issues/26/comments"):
            return copy.deepcopy(self.rows)
        if path.startswith("/pulls?"):
            return copy.deepcopy(self.prs)
        if path.endswith("/pulls"):
            return []
        if path.endswith("/timeline"):
            return copy.deepcopy(self.timeline)
        raise AssertionError(path)

    def call(self, path, method="GET", data=None):
        if method == "POST":
            if self.fail:
                raise m.Gap("API POST HTTP 403")
            self.posts += 1
            row = {"id": len(self.rows) + 1, "body": data["body"],
                   "user": {"login": "github-actions[bot]", "type": "Bot"}}
            self.rows.append(row)
            if self.lost:
                self.lost = False
                raise m.Gap("API POST transport/decoding failure")
            return copy.deepcopy(row)
        if path.startswith("/issues/comments/"):
            row = next(r for r in self.rows if r["id"] == int(path.rsplit("/", 1)[1]))
            if method == "PATCH":
                if self.patch_fail:
                    raise m.Gap("API PATCH HTTP 503")
                row["body"] = data["body"]
            return copy.deepcopy(row)
        if path.startswith("/actions/runs/"):
            return {"id": 1, "path": m.WRITER, "repository": {"id": 42},
                    "head_branch": "main", "event": "push"}
        if path.startswith("/git/ref"):
            return {"object": {"sha": self.tip}}
        if path.startswith("/commits/"):
            return {"author": {"login": "author"}}
        if path.startswith("/pulls/"):
            p = next(p for p in self.prs if p["number"] == int(path.split("/")[2]))
            result = copy.deepcopy(p)
            if self.after:
                self.after(p)
                self.after = None
            return result
        raise AssertionError((path, method))


class FakeGit:
    def __init__(self):
        self.missing, self.diffs = set(), {B: [change()], C: [change(status="D")]}
        self.revisions = [B, C]
    def ensure(self, ref):
        if ref in self.missing:
            raise m.Gap("Git object unavailable")
    exists = ensure
    def fetch_pr(self, number, ref):
        self.ensure(ref)
    def commits(self, base, tip):
        self.ensure(base)
        return [] if base == tip else self.revisions
    def parents(self, ref):
        return [A if ref == B else B]
    def changes(self, base, ref):
        self.ensure(ref)
        return self.diffs.get(ref, [])
    def merge_base(self, base, head):
        return A
    def timestamp(self, ref):
        return "2026-01-02T00:00:00+00:00"


def event(key="k"):
    return {"key": key, "lane": "main", "commit": B, "kind": "INTEGRATED_COMMIT", "docs_digest": "d"}


class SnapshotTests(unittest.TestCase):
    def test_same_snapshot_no_duplicate(self):
        first = m.next_candidate(42, 1, snap(), None)
        self.assertIsNone(m.next_candidate(42, 1, snap(), first))
    def test_a_b_a_preserved(self):
        first = m.next_candidate(42, 1, snap(), None)
        second = m.next_candidate(42, 1, snap(pr(head=C)), first)
        third = m.next_candidate(42, 1, snap(), second)
        self.assertNotEqual(first["key"], third["key"])
        self.assertEqual(third["previous"], second["key"])
    def test_same_head_metadata_correction(self):
        first = m.next_candidate(42, 1, snap(), None)
        second = m.next_candidate(42, 1, snap(pr(body="Logical role: Engineer\nReason: clarify")), first)
        self.assertIsNotNone(second)
        self.assertEqual(second["role"], "DECLARED (see PR)")
    def test_same_head_target_correction(self):
        first = m.next_candidate(42, 1, snap(), None)
        self.assertIsNotNone(m.next_candidate(42, 1, snap(pr(base_ref="stable")), first))
    def test_base_tip_only_does_not_post(self):
        first = m.next_candidate(42, 1, snap(), None)
        self.assertIsNone(m.next_candidate(42, 1, snap(pr(base=C)), first))
    def test_clear_is_not_withdrawal(self):
        first = m.next_candidate(42, 1, snap(), None)
        second = m.next_candidate(42, 1, snap(pr(head=C), []), first)
        self.assertEqual(second["kind"], "DOC_DELTA_CLEARED")
        self.assertTrue(second["ever_had_docs"])
    def test_never_docs_no_post(self):
        self.assertIsNone(m.next_candidate(42, 1, snap(changes=[]), None))
    def test_close_is_withdrawal(self):
        self.assertEqual(m.next_candidate(42, 1, snap(pr(state="closed")), None)["kind"], "WITHDRAWN")
    def test_unknown_not_invented(self):
        self.assertEqual(snap()["role"], "UNKNOWN")
    def test_raw_reason_not_copied(self):
        self.assertNotIn("private@example.invalid", m.canonical(snap(pr(body="Reason: private@example.invalid"))))
    def test_invalid_sha(self):
        with self.assertRaises(m.Gap):
            m.sha("HEAD; echo unsafe")
    def test_escaping(self):
        value = m.safe("<script>@all [bad](x) `code`\n|stuff|")
        self.assertNotIn("<script>", value)
        self.assertNotIn("@all", value)
        self.assertNotIn("[bad]", value)
        self.assertNotIn("\n", value)


class ReceiptTests(unittest.TestCase):
    def test_roundtrip(self):
        self.assertEqual(m.unpack(m.pack({"text": "<!-- @all -->"})), {"text": "<!-- @all -->"})
    def test_bad_marker(self):
        self.assertIsNone(m.unpack("not-a-marker"))
        self.assertIsNone(m.unpack("<!-- documentation-journal:v1 a -->\n"))
    def test_post_readback_and_rerun(self):
        api = FakeAPI()
        journal = m.Journal(api, CFG, 1, True)
        journal.write(event(), [change()])
        m.Journal(api, CFG, 2, True).write(event(), [change()])
        self.assertEqual(api.posts, 1)
    def test_lost_post_response_no_duplicate(self):
        api = FakeAPI()
        api.lost = True
        journal = m.Journal(api, CFG, 1, True)
        journal.write(event(), [change()])
        self.assertIn("k", journal.events)
        self.assertEqual(api.posts, 1)
    def test_failed_post_explicit(self):
        api = FakeAPI()
        api.fail = True
        with self.assertRaises(m.Gap):
            m.Journal(api, CFG, 1, True).write(event(), [change()])
    def test_dryrun_no_remote_mutation(self):
        api = FakeAPI()
        m.Journal(api, CFG, 1, False).write(event(), [change()])
        self.assertEqual(api.rows, [])
    def test_forged_human_marker_ignored(self):
        api = FakeAPI()
        api.rows.append({"id": 1, "user": {"login": "attacker", "type": "User"},
          "body": m.pack({"kind": "event", "repository_id": 42, "run_id": 1,
                          "event": event(), "part": 0, "total": 1})})
        journal = m.Journal(api, CFG, 1, True)
        self.assertEqual(journal.events, {})
        journal.write(event(), [change()])
        self.assertEqual(api.posts, 1)
    def test_multiple_parts_verified(self):
        api = FakeAPI()
        journal = m.Journal(api, CFG, 1, True)
        journal.write(event(), [change(f"docs/{i}.md") for i in range(81)])
        self.assertEqual(api.posts, 3)
        self.assertIn("k", journal.events)
    def test_partial_parts_resume(self):
        api = FakeAPI()
        journal = m.Journal(api, CFG, 1, True)
        real = api.call
        def fail_second(path, method="GET", data=None):
            if method == "POST" and api.posts == 1:
                raise m.Gap("API POST HTTP 503")
            return real(path, method, data)
        api.call = fail_second
        changes = [change(f"docs/{i}.md") for i in range(41)]
        with self.assertRaises(m.Gap):
            journal.write(event(), changes)
        api.call = real
        m.Journal(api, CFG, 2, True).write(event(), changes)
        self.assertEqual(api.posts, 2)
    def test_state_update_not_new_comment(self):
        api = FakeAPI()
        journal = m.Journal(api, CFG, 1, True)
        state = {"last_run": {"result": "COMPLETE", "observed_at": "now"}, "gaps": {}}
        journal.save(state)
        journal.save(state)
        self.assertEqual(api.posts, 1)


class ReconcileTests(unittest.TestCase):
    def run_journal(self, api=None, git=None):
        api, git = api or FakeAPI(), git or FakeGit()
        j = m.Journal(api, CFG, 1, True)
        return m.reconcile(api, git, j, CFG), j, api
    def test_direct_and_revert_both_recorded(self):
        state, journal, api = self.run_journal()
        self.assertEqual(state["last_run"]["result"], "COMPLETE")
        self.assertEqual(len(journal.events), 2)
        self.assertEqual({e["commit"] for e in journal.events.values()}, {B, C})
        count = api.posts
        self.run_journal(api)
        self.assertEqual(api.posts, count)
    def test_no_docs_no_event(self):
        git = FakeGit()
        git.diffs = {}
        state, journal, _ = self.run_journal(git=git)
        self.assertEqual(journal.events, {})
        self.assertEqual(state["main_covered"], C)
    def test_missing_revision_other_lane_continues(self):
        git, api = FakeGit(), FakeAPI()
        git.missing.add(B)
        api.prs = [pr(head=C)]
        state, journal, _ = self.run_journal(api, git)
        self.assertEqual(state["main_covered"], A)
        self.assertEqual(state["last_run"]["result"], "PARTIAL")
        self.assertTrue(any(e.get("commit") == C for e in journal.events.values()))
        self.assertTrue(any(e.get("pr") == 1 for e in journal.events.values()))
        git.missing.clear()
        state, journal, _ = self.run_journal(api, git)
        self.assertEqual(state["last_run"]["result"], "COMPLETE")
        self.assertEqual(state["main_covered"], C)
    def test_candidate_and_unknown_validation(self):
        api = FakeAPI()
        api.prs = [pr()]
        _, journal, _ = self.run_journal(api)
        candidate = next(e for e in journal.events.values() if e["lane"] == "pr:1")
        self.assertEqual(candidate["delivery"], "CANDIDATE_UNMERGED")
        self.assertIn("UNKNOWN", candidate["validation"])
    def test_snapshot_race_leaves_gap(self):
        api = FakeAPI()
        api.prs = [pr()]
        api.after = lambda p: p.update(head={"sha": C, "repo": {"id": 43}})
        state, journal, _ = self.run_journal(api)
        self.assertEqual(state["last_run"]["result"], "PARTIAL")
        self.assertFalse(any(e["lane"] == "pr:1" for e in journal.events.values()))
    def test_closed_and_reopened_between_polls(self):
        api = FakeAPI()
        api.prs = [pr()]
        api.timeline = [{"id": 7, "event": "closed", "created_at": "2026-01-02T00:00:00Z"},
                        {"id": 8, "event": "reopened", "created_at": "2026-01-02T01:00:00Z"}]
        _, journal, _ = self.run_journal(api)
        kinds = {e["kind"] for e in journal.events.values()}
        self.assertTrue({"CLOSED", "REOPENED"}.issubset(kinds))
    def test_old_unavailable_head_not_erased_by_new(self):
        api, git = FakeAPI(), FakeGit()
        api.prs = [pr()]
        git.missing.add(B)
        self.run_journal(api, git)
        api.prs = [pr(head=C)]
        state, journal, _ = self.run_journal(api, git)
        self.assertIn("pr:1:" + B, state["gaps"])
        self.assertTrue(any(e.get("snapshot", {}).get("head") == C for e in journal.events.values()))
    def test_post_pending_retry_after_head_changed(self):
        api = FakeAPI()
        api.prs = [pr()]
        real = api.call
        def fail_candidate(path, method="GET", data=None):
            marker = m.unpack((data or {}).get("body", "")) or {}
            if method == "POST" and marker.get("event", {}).get("lane") == "pr:1":
                raise m.Gap("API POST HTTP 503")
            return real(path, method, data)
        api.call = fail_candidate
        state, _, _ = self.run_journal(api)
        self.assertTrue(state["pending"])
        api.call = real
        api.prs = [pr(head=C)]
        state, journal, _ = self.run_journal(api)
        self.assertFalse(state["pending"])
        self.assertEqual(state["last_run"]["result"], "COMPLETE")
        self.assertEqual({e["snapshot"]["head"] for e in journal.events.values() if e["lane"] == "pr:1"}, {B, C})
    def test_rewritten_baseline_fails_closed(self):
        git = FakeGit()
        git.missing.add(A)
        state, _, _ = self.run_journal(git=git)
        self.assertEqual(state["main_covered"], A)
        self.assertIn("main-scan", state["gaps"])


class GitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.run_git("init", "-q")
        self.run_git("config", "user.name", "Synthetic Author")
        self.run_git("config", "user.email", "synthetic@example.invalid")
        (self.root / "base.txt").write_text("base")
        self.commit()
        self.base = self.run_git("rev-parse", "HEAD")
        self.git = m.Git(self.root, "example/factory", ["docs/*"])
    def tearDown(self):
        self.tmp.cleanup()
    def run_git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True, text=True).stdout.strip()
    def commit(self):
        self.run_git("add", ".")
        self.run_git("commit", "-qm", "Synthetic test")
        return self.run_git("rev-parse", "HEAD")
    def test_rename_outside_boundary(self):
        (self.root / "docs").mkdir()
        (self.root / "docs/a.txt").write_text("reference\n" * 10)
        first = self.commit()
        (self.root / "docs/a.txt").rename(self.root / "outside.txt")
        second = self.commit()
        diff = self.git.changes(first, second)
        self.assertEqual(len(diff), 1)
        self.assertTrue(diff[0]["status"].startswith("R"))
        self.assertEqual(diff[0]["new"], "outside.txt")
    def test_zero_net_diff_keeps_two_revisions(self):
        (self.root / "docs").mkdir()
        (self.root / "docs/a.txt").write_text("a")
        first = self.commit()
        (self.root / "docs/a.txt").unlink()
        second = self.commit()
        self.assertEqual(self.git.changes(self.base, second), [])
        self.assertEqual(self.git.commits(self.base, second), [first, second])
        self.assertTrue(self.git.changes(self.base, first))
        self.assertTrue(self.git.changes(first, second))
    def test_git_does_not_run_textconv(self):
        (self.root / "docs").mkdir()
        (self.root / "docs/a.txt").write_text("a")
        (self.root / ".gitattributes").write_text("*.txt diff=bad\n")
        self.run_git("config", "diff.bad.textconv", "nonexistent-dangerous-command")
        head = self.commit()
        self.assertEqual(len(self.git.changes(self.base, head)), 1)
    def test_large_diff_no_rest_file_cap(self):
        (self.root / "docs").mkdir()
        for i in range(3001):
            (self.root / f"docs/{i}.txt").write_text("a")
        head = self.commit()
        self.assertEqual(len(self.git.changes(self.base, head)), 3001)


class PaginationTests(unittest.TestCase):
    def test_reads_more_than_one_page(self):
        api = m.API("example/factory", "not-used")
        api.call = lambda path: list(range(100)) if path.endswith("&page=1") else [100]
        self.assertEqual(len(api.pages("/pulls?state=all")), 101)
    def test_list_shape_failure(self):
        api = m.API("example/factory", "not-used")
        api.call = lambda path: {"message": "not a list"}
        with self.assertRaises(m.Gap):
            api.pages("/pulls")
    def test_wrong_workflow_cannot_write(self):
        api = FakeAPI()
        api.call = lambda path: {"id": 42, "full_name": "example/factory", "default_branch": "main", "private": False}
        with patch.dict(os.environ, {"GITHUB_REPOSITORY": "example/factory", "GITHUB_WORKFLOW_REF": "fork/workflow@branch"}):
            with self.assertRaises(m.Gap):
                m.validate_environment(api, CFG)


if __name__ == "__main__":
    unittest.main()
