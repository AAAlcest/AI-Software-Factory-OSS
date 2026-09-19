"""Offline, synthetic fork bootstrap checks. No GitHub Issue or file is written."""

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "bootstrap_documentation_journal", ROOT / "scripts/bootstrap_documentation_journal.py"
)
subject = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(subject)

FORK = {
    "full_name": "synthetic-user/AI-Software-Factory-OSS", "id": 42,
    "default_branch": "main", "fork": True, "private": False,
    "parent": {"full_name": subject.UPSTREAM}, "has_issues": True,
    "permissions": {"push": True},
}
HEAD = "a" * 40


class BootstrapTests(unittest.TestCase):
    def test_candidate_is_fork_scoped_and_write_gated(self):
        files = subject.candidate_files(
            FORK, HEAD, 17, datetime(2026, 9, 19, tzinfo=timezone.utc)
        )
        cfg = json.loads(files[subject.CONFIG])
        self.assertEqual((cfg["repository"], cfg["repository_id"], cfg["notice_issue"]),
                         (FORK["full_name"], 42, 17))
        self.assertEqual(cfg["baseline_sha"], HEAD)
        self.assertEqual(cfg["since"], "2026-09-19T00:00:00Z")
        writer = files[subject.WORKFLOW]
        self.assertIn("github.repository_id == '42'", writer)
        self.assertIn("vars.DOCUMENTATION_JOURNAL_ENABLED == 'true'", writer)
        self.assertIn("github.event_name == 'workflow_dispatch' && inputs.dry_run", writer)
        self.assertNotIn("github.repository_id == '1358307744'", writer)
        self.assertIn("documentation-journal-${{ github.repository_id }}-17", writer)
        for name in ("README.md", "README.zh-CN.md"):
            readme = files[Path(name)]
            self.assertIn("https://github.com/synthetic-user/AI-Software-Factory-OSS/issues/17", readme)
            self.assertNotIn("https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/26", readme)
            self.assertIn("NOT_ACTIVATED" if name == "README.md" else "尚未启用", readme)

    def test_preflight_rejects_nonfork_private_and_missing_access(self):
        replies = {
            ("git", "status", "--porcelain"): "",
            ("gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"):
                FORK["full_name"],
            ("git", "branch", "--show-current"): "main",
            ("git", "rev-parse", "HEAD"): HEAD,
            ("git", "ls-remote", "origin", "refs/heads/main"):
                f"{HEAD}\trefs/heads/main",
        }
        with patch.object(subject, "command", side_effect=lambda *a: replies[a]):
            for change in ({"fork": False}, {"private": True},
                           {"has_issues": False}, {"permissions": {"push": False}},
                           {"parent": {"full_name": "other/repo"}}):
                with self.subTest(change=change), patch.object(subject, "api", return_value={**FORK, **change}):
                    with self.assertRaises(subject.BootstrapError):
                        subject.preflight()
            with patch.object(subject, "api", return_value=FORK):
                self.assertEqual(subject.preflight()[1], HEAD)

    def test_notice_is_explicitly_inactive_and_local(self):
        body = subject.notice_body(FORK["full_name"], HEAD)
        self.assertIn(subject.MARKER, body)
        self.assertIn("NOT_ACTIVATED", body)
        self.assertIn(HEAD, body)
        self.assertNotIn("AAAlcest/AI-Software-Factory-OSS/issues/26", body)

    def test_existing_notice_reused_and_locked_notice_rejected(self):
        item = {"number": 17, "state": "open", "locked": False,
                "body": subject.MARKER, "html_url": "https://github.com/example/fork/issues/17"}
        with patch.object(subject, "command", return_value=json.dumps([[item]])):
            self.assertEqual(subject.existing_notice("example/fork")["number"], 17)
        with patch.object(subject, "command", return_value=json.dumps([[{**item, "locked": True}]])):
            with self.assertRaises(subject.BootstrapError):
                subject.existing_notice("example/fork")

    def test_default_invocation_is_read_only(self):
        with patch.object(subject, "preflight", return_value=(FORK, HEAD)), \
             patch.object(subject, "existing_notice", return_value=None), \
             patch.object(subject, "candidate_files", return_value={}) as candidate, \
             patch.object(subject, "api") as api, \
             patch.object(sys, "argv", ["bootstrap_documentation_journal.py"]):
            subject.main()
            candidate.assert_called_once()
            api.assert_not_called()

    def test_apply_writes_only_fork_files_after_own_notice_creation(self):
        with tempfile.TemporaryDirectory() as temp:
            fixture = Path(temp)
            for path in (subject.CONFIG, subject.WORKFLOW,
                         Path("README.md"), Path("README.zh-CN.md")):
                (fixture / path).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, fixture / path)
            notice = {"number": 17, "html_url": "https://github.com/synthetic-user/AI-Software-Factory-OSS/issues/17"}
            with patch.object(subject, "ROOT", fixture), \
                 patch.object(subject, "preflight", return_value=(FORK, HEAD)), \
                 patch.object(subject, "existing_notice", return_value=None), \
                 patch.object(subject, "api", return_value=notice) as api, \
                 patch.object(sys, "argv", ["bootstrap_documentation_journal.py", "--apply"]):
                subject.main()
                api.assert_called_once()
                self.assertEqual(api.call_args.args[:3], (FORK["full_name"], "POST", "/issues"))
                self.assertIn(subject.MARKER, api.call_args.args[3]["body"])
            cfg = json.loads((fixture / subject.CONFIG).read_text(encoding="utf-8"))
            self.assertEqual(cfg["notice_issue"], 17)
            self.assertEqual(cfg["repository_id"], 42)
            self.assertIn("vars.DOCUMENTATION_JOURNAL_ENABLED == 'true'",
                          (fixture / subject.WORKFLOW).read_text(encoding="utf-8"))
            self.assertEqual(sorted(str(p.relative_to(fixture)) for p in fixture.rglob("*") if p.is_file()),
                             sorted(str(p) for p in (subject.CONFIG, subject.WORKFLOW,
                                                     Path("README.md"), Path("README.zh-CN.md"))))


if __name__ == "__main__":
    unittest.main()
