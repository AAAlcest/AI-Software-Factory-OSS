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
        stack.enter_context(patch.object(subject, "source_identity", return_value=(VIEWER, NEW)))
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
        self.assertEqual(plan["prior_sha"], OLD)
        self.assertEqual(plan["changed_managed"], ["templates/STAFF_OFFICE_TEMPLATE.md"])
        self.assertEqual(set(plan["changes"]), {
            "templates/STAFF_OFFICE_TEMPLATE.md", subject.PROVENANCE, subject.LOCK,
        })
        updated = json.loads(plan["changes"][subject.PROVENANCE])
        self.assertEqual(updated["private_extension"], "preserved")
        self.assertEqual(updated["source_sha"], NEW)
        self.assertEqual(updated["managed_scope"], "EXPLICIT_PARTIAL_FRAMEWORK_UPGRADE")
        new_lock = json.loads(plan["changes"][subject.LOCK])
        self.assertEqual(set(new_lock["files"]), set(subject.MANAGED))
        self.assertEqual(new_lock["source_sha"], NEW)
        self.assertEqual(raw[subject.PROVENANCE], json.dumps({
            "upstream": subject.UPSTREAM, "upstream_repository_id": subject.UPSTREAM_ID,
            "source_ref": "refs/tags/v1.6.0", "source_sha": OLD, "license": "MIT",
            "status": "COPIED_FRAMEWORK_NOT_OPERATING_AUTHORITY",
            "private_extension": "preserved",
        }).encode())
        journal.assert_called_once_with("FAKE_TOKEN", DEST, 42, ref=BASE)
        conflict.assert_called_once()

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
        plan = {"source_sha": NEW, "prior_sha": OLD, "changed_managed": [],
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
