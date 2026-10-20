"""Public-safe, synthetic/mocked tests; NEVER mutate a real private Factory."""
from __future__ import annotations

import base64
from contextlib import ExitStack
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import update_private_factory as subject  # noqa: E402

OLD = "a" * 40
NEW = "b" * 40
BASE = "c" * 40
VIEWER = {"login": "sample-user", "id": 7}
DEST = "sample-user/Private-Factory"
REPO = {
    "id": 42, "full_name": DEST, "owner": VIEWER, "private": True,
    "fork": False, "parent": None, "default_branch": "main",
    "permissions": {"push": True},
}



class SourceIdentityReleaseTagTests(unittest.TestCase):
    """No GitHub access: exact official main/tag source identity contracts."""

    def probe(self, *, branch="main", tag_points=None, api_sha=NEW,
              remote_sha=NEW, repo_override=None, origin=None,
              dirty=False, tag_type=None, viewer=None, local_head=NEW):
        wanted = subject.bootstrap.RELEASE_TAG
        ref_name = "refs/heads/main" if branch == "main" else f"refs/tags/{wanted}"
        commands = {
            ("git", "status", "--porcelain"): " M docs/README.md" if dirty else "",
            ("git", "rev-parse", "--show-toplevel"): str(subject.ROOT),
            ("git", "remote", "get-url", "origin"):
                origin or f"https://github.com/{subject.UPSTREAM}.git",
            ("git", "rev-parse", "HEAD"): local_head,
            ("git", "branch", "--show-current"): branch,
            ("git", "tag", "--points-at", "HEAD"):
                wanted if tag_points is None else tag_points,
            ("git", "ls-remote", "origin", ref_name):
                f"{remote_sha}\t{ref_name}",
        }
        seen = []
        def process(args, **kwargs):
            seen.append(("git", tuple(args)))
            if tuple(args) not in commands:
                raise AssertionError(("unexpected git command", args))
            return commands[tuple(args)]
        def api(_token, path, method="GET", payload=None, missing_ok=False):
            self.assertEqual(method, "GET")
            seen.append(("api", path))
            if path == f"/repos/{subject.UPSTREAM}":
                return {
                    "id": subject.UPSTREAM_ID, "full_name": subject.UPSTREAM,
                    "private": False, "default_branch": "main", **(repo_override or {}),
                }
            if path == f"/repos/{subject.UPSTREAM}/git/ref/{ref_name.removeprefix('refs/')}":
                return {"object": {"sha": api_sha,
                    "type": tag_type if tag_type is not None else "commit"}}
            if path == "/user":
                return viewer or VIEWER
            raise AssertionError(("unexpected API call", path))
        with patch.object(subject.bootstrap, "process", side_effect=process), \
             patch.object(subject.bootstrap, "api", side_effect=api):
            result = subject.source_identity("FAKE_TOKEN")
        return result, seen

    def test_main_requires_exact_local_remote_and_api_main_tip(self):
        got, seen = self.probe()
        self.assertEqual(got, (VIEWER, NEW, "refs/heads/main"))
        self.assertIn(("api", f"/repos/{subject.UPSTREAM}/git/ref/heads/main"), seen)
        for option in ({"remote_sha": OLD}, {"api_sha": OLD},
                       {"dirty": True},
                       {"origin": "https://github.com/fake/another.git"},
                       {"repo_override": {"id": 12345}},
                       {"repo_override": {"private": True}},
                       {"branch": "feature/preview"}):
            with self.subTest(option=option), self.assertRaises(subject.UpgradeError):
                self.probe(**option)

    def test_detached_release_tag_requires_triple_equality(self):
        got, seen = self.probe(branch="")
        self.assertEqual(got, (VIEWER, NEW,
                               f"refs/tags/{subject.bootstrap.RELEASE_TAG}"))
        self.assertIn(("git", ("git", "tag", "--points-at", "HEAD")), seen)
        self.assertIn(("api", f"/repos/{subject.UPSTREAM}/git/ref/tags/"
                                f"{subject.bootstrap.RELEASE_TAG}"), seen)

        for option in ({"tag_points": "v1.6.0"}, {"tag_points": ""},
                       {"api_sha": OLD}, {"remote_sha": OLD},
                       {"tag_type": "tag"},  # no unsupported annotated-tag fallback
                       {"dirty": True},
                       {"repo_override": {"default_branch": "other"}},
                       {"local_head": "bad_sha"}):
            with self.subTest(option=option), self.assertRaises(subject.UpgradeError):
                self.probe(branch="", **option)

    def test_other_branch_never_becomes_current_release(self):
        with self.assertRaisesRegex(subject.UpgradeError, "official main or"):
            self.probe(branch="release/v1.7.0-rc")



class UpgradePlanTests(unittest.TestCase):
    def synthetic(self, *, lock=False, edited=None, prior=OLD, ancestry=True,
                  missing=None, bad_provenance=False):
        """Return a hermetic synthetic plan; private network calls are patched."""
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        old = {p: ("old:" + p + "\n").encode() for p in subject.MANAGED}
        new = dict(old)
        new["templates/STAFF_OFFICE_TEMPLATE.md"] = b"new: staff notes template\n"
        for p, value in new.items():
            fp = root / p
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_bytes(value)
        provenance = {
            "upstream": "other/foreign" if bad_provenance else subject.UPSTREAM,
            "upstream_repository_id": subject.UPSTREAM_ID,
            "source_ref": "refs/tags/v1.6.0",
            "source_sha": prior, "license": "MIT",
            "status": "COPIED_FRAMEWORK_NOT_OPERATING_AUTHORITY",
            "private_extension": "preserved",  # never logged or overwritten
        }
        raw = {
            "instance.json": b'{"mode":"INSTANCE"}',
            subject.PROVENANCE: json.dumps(provenance).encode(),
        }
        for p, value in old.items():
            raw[p] = (b"locally edited!" if p == edited else value)
        if missing:
            raw.pop(missing, None)
        if lock:
            raw[subject.LOCK] = subject.json_bytes({
                "schema_version": 1, "upstream": subject.UPSTREAM,
                "repository_id": subject.UPSTREAM_ID, "source_sha": prior,
                "files": {p: subject.digest(v) for p, v in old.items()},
            })

        def read(_token, _dest, path, *, optional=False, ref="main"):
            self.assertEqual(ref, BASE)
            if path not in raw and optional:
                return None
            if path not in raw:
                raise subject.UpgradeError("A required managed/identity file is missing.")
            return raw[path]

        stack = ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(patch.object(subject, "ROOT", root))
        stack.enter_context(patch.object(subject, "source_identity", return_value=(VIEWER, NEW, "refs/heads/main")))
        stack.enter_context(patch.object(subject, "target_identity", return_value=REPO))
        stack.enter_context(patch.object(subject, "target_tip", return_value=BASE))
        stack.enter_context(patch.object(subject, "get_bytes", side_effect=read))
        # Both old/new source bytes are Git objects. The new content is not
        # taken from ROOT's platform-dependent working-tree line endings.
        stack.enter_context(patch.object(
            subject, "historical_bytes",
            side_effect=lambda sha, p: old[p] if sha == prior else new[p],
        ))
        stack.enter_context(patch.object(subject, "is_ancestor", return_value=ancestry))
        journal = stack.enter_context(patch.object(subject, "verify_journal"))
        conflict = stack.enter_context(patch.object(subject, "no_conflicting_upgrade"))
        return root, raw, journal, conflict

    def test_legacy_upgrade_is_tiny_explicit_and_preserves_private_provenance(self):
        _root, raw, journal, conflict = self.synthetic()
        plan = subject.build_plan("FAKE_TOKEN", DEST)
        self.assertTrue(plan["legacy_without_lock"])
        self.assertEqual(plan["base_sha"], BASE)
        self.assertEqual(plan["source_sha"], NEW)
        self.assertEqual(plan["source_ref"], "refs/heads/main")

        self.assertEqual(plan["prior_sha"], OLD)
        self.assertEqual(plan["changed_managed"], ["templates/STAFF_OFFICE_TEMPLATE.md"])
        self.assertEqual(set(plan["changes"]), {
            "templates/STAFF_OFFICE_TEMPLATE.md", subject.PROVENANCE, subject.LOCK,
        })
        updated = json.loads(plan["changes"][subject.PROVENANCE])
        self.assertEqual(updated["private_extension"], "preserved")
        self.assertEqual(updated["source_sha"], NEW)
        self.assertEqual(updated["source_ref"], "refs/heads/main")
        self.assertEqual(updated["managed_scope"], "EXPLICIT_PARTIAL_FRAMEWORK_UPGRADE")
        new_lock = json.loads(plan["changes"][subject.LOCK])
        self.assertEqual(set(new_lock["files"]), set(subject.MANAGED))
        self.assertEqual(new_lock["source_sha"], NEW)
        self.assertEqual(new_lock["source_ref"], "refs/heads/main")
        self.assertEqual(raw[subject.PROVENANCE], json.dumps({
            "upstream": subject.UPSTREAM, "upstream_repository_id": subject.UPSTREAM_ID,
            "source_ref": "refs/tags/v1.6.0", "source_sha": OLD, "license": "MIT",
            "status": "COPIED_FRAMEWORK_NOT_OPERATING_AUTHORITY",
            "private_extension": "preserved",
        }).encode())
        journal.assert_called_once_with("FAKE_TOKEN", DEST, 42, ref=BASE)
        conflict.assert_called_once()

    def test_tag_source_ref_is_preserved_in_private_provenance_and_lock(self):
        # Private GitHub operations are fully mocked by the existing synthetic fixture.
        self.synthetic()
        release_ref = f"refs/tags/{subject.bootstrap.RELEASE_TAG}"
        with patch.object(subject, "source_identity",
                          return_value=(VIEWER, NEW, release_ref)):
            plan = subject.build_plan("FAKE_TOKEN", DEST)
        self.assertEqual(plan["source_ref"], release_ref)
        self.assertEqual(json.loads(plan["changes"][subject.PROVENANCE])["source_ref"],
                         release_ref)
        self.assertEqual(json.loads(plan["changes"][subject.LOCK])["source_ref"],
                         release_ref)

    def test_explicit_old_lock_source_ref_cannot_disagree_with_provenance(self):
        _root, raw, _, _ = self.synthetic(lock=True)
        previous = json.loads(raw[subject.LOCK])
        previous["source_ref"] = "refs/heads/foreign"
        raw[subject.LOCK] = subject.json_bytes(previous)
        with self.assertRaisesRegex(subject.UpgradeError, "lock conflicts"):
            subject.build_plan("FAKE_TOKEN", DEST)

    def test_existing_lock_revalidation_and_bad_lock_stop(self):
        _root, raw, _, _ = self.synthetic(lock=True)
        self.assertFalse(subject.build_plan("t", DEST)["legacy_without_lock"])
        data = json.loads(raw[subject.LOCK])
        data["files"][subject.MANAGED[0]] = "0" * 64
        raw[subject.LOCK] = subject.json_bytes(data)
        with self.assertRaisesRegex(subject.UpgradeError, "hash mismatch"):
            subject.build_plan("t", DEST)

    def test_modified_or_deleted_managed_file_cannot_be_overwritten(self):
        self.synthetic(edited="templates/STAFF_OFFICE_TEMPLATE.md")
        with self.assertRaisesRegex(subject.UpgradeError, "conflict"):
            subject.build_plan("t", DEST)
        # Run the missing-file case with a new independent synthetic fixture.
        self.synthetic(missing="scripts/validate_instance.py")
        with self.assertRaisesRegex(subject.UpgradeError, "required managed"):
            subject.build_plan("t", DEST)

    def test_missing_wrong_or_unverifiable_provenance_stops(self):
        _root, raw, _, _ = self.synthetic()
        raw.pop(subject.PROVENANCE)
        with self.assertRaisesRegex(subject.UpgradeError, "required managed/identity file"):
            subject.build_plan("t", DEST)
        self.synthetic(bad_provenance=True)
        with self.assertRaisesRegex(subject.UpgradeError, "Foreign"):
            subject.build_plan("t", DEST)
        self.synthetic(ancestry=False)
        with self.assertRaisesRegex(subject.UpgradeError, "unverified"):
            subject.build_plan("t", DEST)

    def test_bounded_scope_never_manages_instance_or_journal_files(self):
        self.assertEqual(set(subject.MANAGED), {
            "scripts/validate_instance.py",
            "templates/STAFF_OFFICE_TEMPLATE.md",
            "templates/PROJECT_ROOM_TEMPLATE.md",
        })
        forbidden = ("projects/", "offices/", ".github/", "README.md", "instance.json",
                     "state.json", "authority.json", "CURRENT.md", "AGENTS.md")
        self.assertTrue(all(not any(p.startswith(f) for f in forbidden) for p in subject.MANAGED))

    def test_clean_crlf_checkout_normalizes_blobs_across_successive_upgrades(self):
        """Clean core.autocrlf=true working files must never be written as CRLF blobs."""
        with tempfile.TemporaryDirectory(prefix="synthetic-upgrade-crlf-") as tmp:
            history = Path(tmp) / "synthetic-history"
            work = Path(tmp) / "crlf-checkout"
            history.mkdir()

            def git(root, *args):
                return subprocess.run(
                    ["git", "-C", str(root), *args], capture_output=True,
                    text=True, check=True, timeout=30,
                ).stdout.strip()

            def git_blob(root, sha, path):
                return subprocess.run(
                    ["git", "-C", str(root), "show", f"{sha}:{path}"],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    check=True, timeout=30,
                ).stdout

            git(history, "init", "-b", "main")
            git(history, "config", "core.autocrlf", "false")
            git(history, "config", "user.name", "Synthetic Test")
            git(history, "config", "user.email", "synthetic@example.invalid")
            for path in subject.MANAGED:
                p = history / path
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(("v1:" + path + "\n").encode())
            git(history, "add", ".")
            git(history, "commit", "-m", "synthetic v1")
            oldsha = git(history, "rev-parse", "HEAD")
            managed_path = "templates/STAFF_OFFICE_TEMPLATE.md"
            (history / managed_path).write_bytes(b"synthetic v2 template\n")
            git(history, "add", ".")
            git(history, "commit", "-m", "synthetic v2")
            v2 = git(history, "rev-parse", "HEAD")

            subprocess.run(
                ["git", "clone", "-c", "core.autocrlf=true",
                 str(history), str(work)], check=True, capture_output=True,
                text=True, timeout=30,
            )
            git(work, "config", "core.autocrlf", "true")
            git(work, "checkout", "-f", "main")
            self.assertEqual(git(work, "status", "--porcelain"), "")
            self.assertIn(b"\r\n", (work / managed_path).read_bytes())
            self.assertNotIn(b"\r\n", git_blob(work, v2, managed_path))

            raw = {
                "instance.json": b'{"mode":"INSTANCE"}',
                subject.PROVENANCE: subject.json_bytes({
                    "upstream": subject.UPSTREAM,
                    "upstream_repository_id": subject.UPSTREAM_ID,
                    "source_sha": oldsha,
                    "source_ref": "refs/heads/main",
                    "license": "MIT",
                    "status": "COPIED_FRAMEWORK_NOT_OPERATING_AUTHORITY",
                }),
            }
            raw.update({p: git_blob(work, oldsha, p) for p in subject.MANAGED})
            source_tip = [v2]

            def read(_token, _dest, path, *, optional=False, ref="main"):
                self.assertEqual(ref, BASE)
                if path not in raw and optional:
                    return None
                if path not in raw:
                    raise subject.UpgradeError("Required file missing.")
                return raw[path]

            with patch.object(subject, "ROOT", work), \
                 patch.object(subject, "source_identity",
                              side_effect=lambda _token: (VIEWER, source_tip[0], "refs/heads/main")), \
                 patch.object(subject, "target_identity", return_value=REPO), \
                 patch.object(subject, "target_tip", return_value=BASE), \
                 patch.object(subject, "get_bytes", side_effect=read), \
                 patch.object(subject, "verify_journal"), \
                 patch.object(subject, "no_conflicting_upgrade"):
                first = subject.build_plan("FAKE_TOKEN", DEST)
                self.assertEqual(first["prior_sha"], oldsha)
                self.assertEqual(first["changed_managed"], [managed_path])
                self.assertEqual(first["changes"][managed_path],
                                 git_blob(work, v2, managed_path))
                self.assertNotIn(b"\r\n", first["changes"][managed_path])
                first_lock = json.loads(first["changes"][subject.LOCK])
                for p in subject.MANAGED:
                    self.assertEqual(first_lock["files"][p],
                                     subject.digest(git_blob(work, v2, p)))
                # Model a private, separately accepted PR without touching a real repo.
                raw.update(first["changes"])
                git(work, "config", "user.name", "Synthetic Test")
                git(work, "config", "user.email", "synthetic@example.invalid")
                (work / managed_path).write_bytes(b"synthetic v3 template\r\n")
                git(work, "add", managed_path)
                git(work, "commit", "-m", "synthetic v3")
                v3 = git(work, "rev-parse", "HEAD")
                source_tip[0] = v3
                self.assertEqual(git(work, "status", "--porcelain"), "")
                self.assertIn(b"\r\n", (work / managed_path).read_bytes())

                # The next preview must accept the prior normalized Git blobs.
                second = subject.build_plan("FAKE_TOKEN", DEST)
                self.assertEqual(second["prior_sha"], v2)
                self.assertEqual(second["source_sha"], v3)
                self.assertEqual(second["changed_managed"], [managed_path])
                self.assertEqual(second["changes"][managed_path],
                                 git_blob(work, v3, managed_path))
                self.assertNotIn(b"\r\n", second["changes"][managed_path])

    def test_private_target_rejects_wrong_owner_public_fork_or_default_branch(self):
        subject.target_identity
        valid = dict(REPO)
        with patch.object(subject.bootstrap, "api", return_value=valid):
            self.assertEqual(subject.target_identity("t", DEST, VIEWER), valid)
        for changed in (
            {"private": False}, {"fork": True}, {"parent": {"id": 1}},
            {"default_branch": "master"}, {"owner": {"id": 8}},
            {"id": "not-number"}, {"permissions": {"push": False}},
        ):
            with self.subTest(changed=changed):
                with patch.object(subject.bootstrap, "api", return_value={**valid, **changed}):
                    with self.assertRaises(subject.UpgradeError):
                        subject.target_identity("t", DEST, VIEWER)
        with patch.object(subject.bootstrap, "api") as api:
            for wrong in ("other-owner/Private-Factory", "sample-user/../../evil",
                          "Private-Factory", "sample-user/private.git"):
                with self.assertRaises(subject.UpgradeError):
                    subject.target_identity("t", wrong, VIEWER)
            api.assert_not_called()

    def test_private_journal_identity_conflict_stops(self):
        config = {
            "repository": DEST, "repository_id": 42, "visibility": "private",
            "default_branch": "main", "notice_issue": 17,
            "baseline_sha": OLD, "cadence_mode": "manual",
        }
        with patch.object(subject, "get_bytes", return_value=subject.json_bytes(config)):
            subject.verify_journal("t", DEST, 42)
        for changed in ({"repository": "other/private"}, {"visibility": "public"},
                        {"repository_id": 43}, {"notice_issue": 0},
                        {"baseline_sha": "garbage"}, {"cadence_mode": "unknown"}):
            with self.subTest(changed=changed), patch.object(
                subject, "get_bytes", return_value=subject.json_bytes({**config, **changed})
            ):
                with self.assertRaisesRegex(subject.UpgradeError, "binding"):
                    subject.verify_journal("t", DEST, 42)

    def test_conflicting_upgrade_branch_or_private_pr_stops(self):
        def get(_token, path, method="GET", payload=None, missing_ok=False):
            if "/git/ref/heads/factory-upgrade/" in path:
                return None
            if "/pulls?" in path:
                return [{"head": {"ref": "factory-upgrade/old-to-new"}}]
            raise AssertionError(path)
        with patch.object(subject.bootstrap, "api", side_effect=get):
            with self.assertRaisesRegex(subject.UpgradeError, "existing private upgrade PR"):
                subject.no_conflicting_upgrade("t", DEST, "factory-upgrade/abc-to-def")

    def test_preview_only_never_uses_mutation_path(self):
        plan = {"source_sha": NEW, "source_ref": "refs/heads/main",
                "prior_sha": OLD, "changed_managed": [],
                "legacy_without_lock": True}
        with patch("sys.argv", ["update_private_factory.py", "--repository", DEST]), \
             patch.object(subject.bootstrap, "process", return_value="FAKE_TOKEN") as proc, \
             patch.object(subject, "build_plan", return_value=plan), \
             patch.object(subject, "commit_private_candidate") as apply, \
             patch("builtins.print") as output:
            self.assertEqual(subject.main(), 0)
        proc.assert_called_once_with(["gh", "auth", "token"])
        apply.assert_not_called()
        self.assertEqual(json.loads(output.call_args.args[0])["status"], "PREVIEW_ONLY")


class UpgradeApplyTests(unittest.TestCase):
    def test_apply_creates_only_private_draft_branch_and_pr(self):
        plan = {
            "dest": DEST, "source_sha": NEW, "prior_sha": OLD,
            "base_sha": BASE, "branch": "factory-upgrade/aaaa-to-bbbb",
            "target_id": 42, "viewer_id": 7,
            "changes": {
                subject.PROVENANCE: b'{"source_sha":"new"}',
                subject.LOCK: b'{"files":{}}',
                "templates/STAFF_OFFICE_TEMPLATE.md": b"public-safe template\n",
            },
            "changed_managed": ["templates/STAFF_OFFICE_TEMPLATE.md"],
        }
        created = []
        blob_number = [0]
        def api(_token, path, method="GET", payload=None, missing_ok=False):
            if method == "GET":
                if path == "/user":
                    return VIEWER
                if path == f"/repos/{DEST}":
                    return REPO
                if path.endswith("/git/ref/heads/" + plan["branch"]):
                    return None
                if path.endswith("/git/commits/" + BASE):
                    return {"tree": {"sha": "d" * 40}}
                if path.endswith("/pulls/31"):
                    return {"head": {"sha": "f" * 40}, "base": {"ref": "main"}, "draft": True}
            created.append((path, method, payload))
            if path.endswith("/git/blobs"):
                blob_number[0] += 1
                self.assertEqual(base64.b64decode(payload["content"]), plan["changes"][
                    sorted(plan["changes"])[blob_number[0] - 1]
                ])
                return {"sha": f"{blob_number[0]:040x}"}
            if path.endswith("/git/trees"):
                self.assertEqual(payload["base_tree"], "d" * 40)
                self.assertEqual(set(x["path"] for x in payload["tree"]), set(plan["changes"]))
                return {"sha": "e" * 40}
            if path.endswith("/git/commits"):
                self.assertEqual(payload["parents"], [BASE])
                return {"sha": "f" * 40}
            if path.endswith("/git/refs"):
                self.assertEqual(payload["ref"], "refs/heads/" + plan["branch"])
                return {"ref": payload["ref"]}
            if path.endswith("/pulls"):
                self.assertEqual(payload["draft"], True)
                self.assertEqual(payload["base"], "main")
                self.assertNotIn("PRIVATE_SECRET", json.dumps(payload))
                return {"number": 31}
            raise AssertionError((path, method))
        with patch.object(subject, "target_tip", return_value=BASE), \
             patch.object(subject.bootstrap, "api", side_effect=api):
            self.assertEqual(subject.commit_private_candidate("PRIVATE_SECRET", plan), 31)
        self.assertTrue(created)
        self.assertTrue(all(path.startswith(f"/repos/{DEST}/") for path, _, _ in created))
        self.assertFalse(any("git/ref/heads/main" in path for path, _, _ in created))
        self.assertTrue(all(method == "POST" for _, method, _ in created))
        self.assertFalse(any("variable" in path or "/contents" in path for path, _, _ in created))
        self.assertTrue(all("PRIVATE_SECRET" not in json.dumps(payload) for _, _, payload in created))

    def test_apply_rebinds_private_identity_before_first_mutation(self):
        """An unchanged main SHA is not evidence of unchanged private visibility."""
        plan = {
            "dest": DEST, "source_sha": NEW, "prior_sha": OLD,
            "base_sha": BASE, "branch": "factory-upgrade/aaaa-to-bbbb",
            "target_id": 42, "viewer_id": 7,
            "changes": {subject.LOCK: b'{"files":{}}'},
            "changed_managed": [],
        }
        cases = {
            "became-public": ({"private": False}, VIEWER),
            "became-fork": ({"fork": True}, VIEWER),
            "wrong-repository-id": ({"id": 43}, VIEWER),
            "wrong-owner-id": ({"owner": {"id": 8}}, VIEWER),
            "lost-push-permission": ({"permissions": {"push": False}}, VIEWER),
            "authenticated-account-changed": ({}, {"login": "other-user", "id": 9}),
        }
        for label, (changed, viewer) in cases.items():
            with self.subTest(case=label):
                writes = []
                reads = []
                def api(_token, path, method="GET", payload=None, missing_ok=False):
                    if method != "GET":
                        writes.append((path, method))
                        raise AssertionError("A preflight identity drift must never POST.")
                    reads.append(path)
                    if path == "/user":
                        return viewer
                    if path == f"/repos/{DEST}":
                        return {**REPO, **changed}
                    if path.endswith("/git/ref/heads/" + plan["branch"]):
                        return None
                    if path.endswith("/git/commits/" + BASE):
                        return {"tree": {"sha": "d" * 40}}
                    raise AssertionError(("unexpected GET", path))
                with patch.object(subject, "target_tip", return_value=BASE), \
                     patch.object(subject.bootstrap, "api", side_effect=api):
                    with self.assertRaises(subject.UpgradeError):
                        subject.commit_private_candidate("FAKE_TOKEN", plan)
                self.assertEqual(writes, [], label)
                self.assertIn("/user", reads)

    def test_apply_accepts_only_the_original_verified_repo_and_owner_ids(self):
        """The saved plan's immutable identities are part of the write gate."""
        plan = {
            "dest": DEST, "source_sha": NEW, "prior_sha": OLD,
            "base_sha": BASE, "branch": "factory-upgrade/aaaa-to-bbbb",
            "target_id": 999, "viewer_id": 7,
            "changes": {subject.LOCK: b'{"files":{}}'},
        }
        writes = []
        def api(_token, path, method="GET", payload=None, missing_ok=False):
            if method != "GET":
                writes.append(path)
                raise AssertionError("Unexpected write.")
            if path == "/user":
                return VIEWER
            if path == f"/repos/{DEST}":
                return REPO
            if path.endswith("/git/ref/heads/" + plan["branch"]):
                return None
            if path.endswith("/git/commits/" + BASE):
                return {"tree": {"sha": "d" * 40}}
            raise AssertionError(path)
        with patch.object(subject, "target_tip", return_value=BASE), \
             patch.object(subject.bootstrap, "api", side_effect=api):
            with self.assertRaisesRegex(subject.UpgradeError, "repository ID changed"):
                subject.commit_private_candidate("FAKE_TOKEN", plan)
        self.assertEqual(writes, [])

    def test_main_moved_means_zero_writes(self):
        with patch.object(subject, "target_tip", return_value="d" * 40), \
             patch.object(subject.bootstrap, "api") as api:
            with self.assertRaisesRegex(subject.UpgradeError, "moved"):
                subject.commit_private_candidate("t", {"dest": DEST, "base_sha": BASE})
            api.assert_not_called()

    def test_branch_conflict_means_zero_mutations(self):
        with patch.object(subject, "target_tip", return_value=BASE), \
             patch.object(subject.bootstrap, "api", return_value={"object": {"sha": BASE}}) as api:
            with self.assertRaisesRegex(subject.UpgradeError, "appeared"):
                subject.commit_private_candidate("t", {
                    "dest": DEST, "base_sha": BASE, "branch": "factory-upgrade/old-to-new",
                })
            self.assertEqual(api.call_count, 1)
            self.assertEqual(api.call_args.args[1].split("/git/ref/heads/")[0],
                             f"/repos/{DEST}")


if __name__ == "__main__":
    unittest.main()
