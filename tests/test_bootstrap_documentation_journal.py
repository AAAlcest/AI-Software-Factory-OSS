"""Offline, synthetic fork bootstrap checks; independent of installed config."""

import importlib.util
import json
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
    "permissions": {"push": True, "admin": True},
}
HEAD = "a" * 40
ACTOR_ID = 7
SOURCE_CONFIG = {
    "repository": subject.UPSTREAM, "repository_id": subject.UPSTREAM_ID,
    "default_branch": "main", "notice_issue": 26,
    "baseline_sha": "b" * 40, "since": "2026-09-18T19:33:42Z",
    "paths": ["*.md"],
}
SOURCE_WORKFLOW = """name: Documentation journal
on:
  push:
    branches: [main]
  workflow_run:
    workflows: [Documentation journal signal]
    types: [completed]
  workflow_dispatch:
    inputs:
      dry_run:
        type: boolean
        default: true
concurrency:
  group: documentation-journal-${{ github.repository_id }}-26
jobs:
  record:
    if: github.repository_id == '1358307744' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@sha
        with:
          ref: refs/heads/main
"""
SOURCE_README_EN = """**Documentation notice:** https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/26
The [journal is active in this repository](https://example.test): records asynchronously.
"""
SOURCE_README_ZH = """**文档公告墙：**https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/26
[本仓自动日志已启用](https://example.test)：异步记录。
"""


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.fixture = Path(self.temp.name)
        contents = {
            subject.CONFIG: json.dumps(SOURCE_CONFIG),
            subject.WORKFLOW: SOURCE_WORKFLOW,
            Path("README.md"): SOURCE_README_EN,
            Path("README.zh-CN.md"): SOURCE_README_ZH,
        }
        for path, content in contents.items():
            (self.fixture / path).parent.mkdir(parents=True, exist_ok=True)
            (self.fixture / path).write_text(content, encoding="utf-8")
        root_patch = patch.object(subject, "ROOT", self.fixture)
        root_patch.start()
        self.addCleanup(root_patch.stop)

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
        self.assertIn("branches: [main]", writer)
        self.assertIn("ref: refs/heads/main", writer)
        for name in ("README.md", "README.zh-CN.md"):
            readme = files[Path(name)]
            self.assertIn("https://github.com/synthetic-user/AI-Software-Factory-OSS/issues/17", readme)
            self.assertNotIn("https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/26", readme)
            self.assertIn("NOT_ACTIVATED" if name == "README.md" else "尚未启用", readme)

    def test_origin_parser_accepts_exact_github_remote_only(self):
        for url in ("https://github.com/synthetic-user/AI-Software-Factory-OSS.git",
                    "git@github.com:synthetic-user/AI-Software-Factory-OSS.git",
                    "ssh://git@github.com/synthetic-user/AI-Software-Factory-OSS.git"):
            self.assertEqual(subject.origin_repository(url), FORK["full_name"])
        for url in ("https://example.com/owner/repo.git", "https://github.com/owner/repo/extra",
                    "https://attacker@github.com/owner/repo.git"):
            with self.assertRaises(subject.BootstrapError):
                subject.origin_repository(url)

    def test_preflight_binds_origin_api_and_checkout(self):
        replies = {
            ("git", "status", "--porcelain"): "",
            ("git", "remote", "get-url", "origin"):
                "https://github.com/synthetic-user/AI-Software-Factory-OSS.git",
            ("git", "branch", "--show-current"): "main",
            ("git", "rev-parse", "HEAD"): HEAD,
            ("git", "ls-remote", "origin", "refs/heads/main"):
                f"{HEAD}\trefs/heads/main",
            ("gh", "api", "user"): json.dumps({"id": ACTOR_ID, "login": "synthetic-user"}),
        }
        def fake_command(*args):
            self.assertNotEqual(args[:3], ("gh", "repo", "view"))
            return replies[args]
        def fake_api(repo, method="GET", path="", payload=None, info=FORK, tip=HEAD):
            self.assertEqual(repo, FORK["full_name"])
            return {"object": {"sha": tip}} if path else info
        with patch.object(subject, "command", side_effect=fake_command), \
             patch.object(subject, "api", side_effect=fake_api):
            self.assertEqual(subject.preflight()[1:], (HEAD, ACTOR_ID))
        # A second fork at the same commit must not be accepted as this origin.
        with patch.object(subject, "command", side_effect=fake_command), \
             patch.object(subject, "api", side_effect=lambda *a, **k: fake_api(*a, **k, info={**FORK, "full_name": "other/fork"})):
            with self.assertRaises(subject.BootstrapError):
                subject.preflight()
        # API and origin tips must both match the local checkout.
        with patch.object(subject, "command", side_effect=fake_command), \
             patch.object(subject, "api", side_effect=lambda *a, **k: fake_api(*a, **k, tip="c" * 40)):
            with self.assertRaises(subject.BootstrapError):
                subject.preflight()
        replies[("git", "remote", "get-url", "origin")] = "https://github.com/AAAlcest/AI-Software-Factory-OSS.git"
        with patch.object(subject, "command", side_effect=fake_command), \
             patch.object(subject, "api", return_value={**FORK, "full_name": subject.UPSTREAM,
                                                         "fork": False}) as api:
            with self.assertRaises(subject.BootstrapError):
                subject.preflight()
            self.assertEqual(api.call_args.args[0], subject.UPSTREAM)

    def test_preflight_rejects_nonfork_private_missing_access_and_nonmain(self):
        replies = {
            ("git", "status", "--porcelain"): "",
            ("git", "remote", "get-url", "origin"):
                "https://github.com/synthetic-user/AI-Software-Factory-OSS.git",
        }
        with patch.object(subject, "command", side_effect=lambda *a: replies[a]):
            for change in ({"fork": False}, {"private": True},
                           {"permissions": {"push": False, "admin": True}},
                           {"parent": {"full_name": "other/repo"}},
                           {"default_branch": "trunk"}):
                with self.subTest(change=change), patch.object(subject, "api", return_value={**FORK, **change}):
                    with self.assertRaises(subject.BootstrapError):
                        subject.preflight()
        with self.assertRaises(subject.BootstrapError):
            subject.candidate_files({**FORK, "default_branch": "trunk"}, HEAD, 17,
                                    datetime.now(timezone.utc))

    def test_preflight_allows_disabled_issues_for_admin(self):
        replies = {
            ("git", "status", "--porcelain"): "",
            ("git", "remote", "get-url", "origin"):
                "https://github.com/synthetic-user/AI-Software-Factory-OSS.git",
            ("git", "branch", "--show-current"): "main",
            ("git", "rev-parse", "HEAD"): HEAD,
            ("git", "ls-remote", "origin", "refs/heads/main"):
                f"{HEAD}\trefs/heads/main",
            ("gh", "api", "user"): json.dumps({"id": ACTOR_ID, "login": "synthetic-user"}),
        }
        disabled = {**FORK, "has_issues": False,
                    "permissions": {"push": True, "admin": True}}
        def fake_api(repo, method="GET", path="", payload=None):
            return {"object": {"sha": HEAD}} if path else disabled
        with patch.object(subject, "command", side_effect=lambda *a: replies[a]), \
             patch.object(subject, "api", side_effect=fake_api):
            self.assertEqual(subject.preflight()[0]["has_issues"], False)

    def test_preflight_rejects_disabled_issues_without_admin(self):
        replies = {
            ("git", "status", "--porcelain"): "",
            ("git", "remote", "get-url", "origin"):
                "https://github.com/synthetic-user/AI-Software-Factory-OSS.git",
        }
        disabled = {**FORK, "has_issues": False,
                    "permissions": {"push": True, "admin": False}}
        with patch.object(subject, "command", side_effect=lambda *a: replies[a]), \
             patch.object(subject, "api", return_value=disabled):
            with self.assertRaisesRegex(subject.BootstrapError, "admin access"):
                subject.preflight()

    def test_enable_issues_is_scoped_and_read_back(self):
        disabled = {**FORK, "has_issues": False,
                    "permissions": {"push": True, "admin": True}}
        enabled = {**disabled, "has_issues": True}
        calls = []
        def fake_api(repo, method="GET", path="", payload=None):
            calls.append((repo, method, path, payload))
            if method == "PATCH":
                return enabled
            return enabled
        with patch.object(subject, "api", side_effect=fake_api):
            result = subject.enable_issues(FORK["full_name"], disabled)
        self.assertTrue(result["has_issues"])
        self.assertEqual(calls[0], (FORK["full_name"], "PATCH", "", {"has_issues": True}))
        self.assertEqual(calls[1][:3], (FORK["full_name"], "GET", ""))

    def test_disabled_issues_dry_run_does_not_mutate(self):
        disabled = {**FORK, "has_issues": False,
                    "permissions": {"push": True, "admin": True}}
        with patch.object(subject, "preflight", return_value=(disabled, HEAD, ACTOR_ID)), \
             patch.object(subject, "existing_notice") as existing, \
             patch.object(subject, "candidate_files", return_value={}) as candidate, \
             patch.object(subject, "enable_issues") as enable, \
             patch.object(subject, "api") as api, \
             patch.object(sys, "argv", ["bootstrap_documentation_journal.py"]):
            subject.main()
            existing.assert_not_called()
            candidate.assert_called_once()
            enable.assert_not_called()
            api.assert_not_called()

    def test_notice_is_explicitly_inactive_and_local(self):
        body = subject.notice_body(FORK["full_name"], HEAD)
        self.assertIn(subject.MARKER, body)
        self.assertIn("NOT_ACTIVATED", body)
        self.assertIn(HEAD, body)
        self.assertNotIn("AAAlcest/AI-Software-Factory-OSS/issues/26", body)

    def test_existing_notice_requires_same_authenticated_creator(self):
        item = {"number": 17, "state": "open", "locked": False,
                "user": {"id": ACTOR_ID}, "body": subject.MARKER,
                "html_url": "https://github.com/example/fork/issues/17"}
        with patch.object(subject, "command", return_value=json.dumps([[item]])):
            self.assertEqual(subject.existing_notice("example/fork", ACTOR_ID)["number"], 17)
        for changed in ({"locked": True}, {"user": {"id": 999}}):
            with patch.object(subject, "command", return_value=json.dumps([[{**item, **changed}]])):
                with self.assertRaises(subject.BootstrapError):
                    subject.existing_notice("example/fork", ACTOR_ID)

    def test_default_invocation_is_read_only(self):
        with patch.object(subject, "preflight", return_value=(FORK, HEAD, ACTOR_ID)), \
             patch.object(subject, "existing_notice", return_value=None), \
             patch.object(subject, "candidate_files", return_value={}) as candidate, \
             patch.object(subject, "api") as api, \
             patch.object(sys, "argv", ["bootstrap_documentation_journal.py"]):
            subject.main()
            candidate.assert_called_once()
            api.assert_not_called()

    def test_generated_fork_layout_does_not_break_bootstrap_tests(self):
        files = subject.candidate_files(FORK, HEAD, 17, datetime.now(timezone.utc))
        for path, content in files.items():
            (self.fixture / path).write_text(content, encoding="utf-8")
        # The test's source inputs are independent from the generated repository.
        # An installed fork's normal test discovery must not re-adapt this layout.
        self.assertEqual(json.loads((self.fixture / subject.CONFIG).read_text())["repository_id"], 42)
        self.assertEqual(SOURCE_CONFIG["repository_id"], subject.UPSTREAM_ID)

    def test_apply_writes_only_fork_files_after_own_notice_creation(self):
        notice = {"number": 17,
                  "html_url": "https://github.com/synthetic-user/AI-Software-Factory-OSS/issues/17"}
        with patch.object(subject, "preflight", return_value=(FORK, HEAD, ACTOR_ID)), \
             patch.object(subject, "existing_notice", return_value=None), \
             patch.object(subject, "api", return_value=notice) as api, \
             patch.object(sys, "argv", ["bootstrap_documentation_journal.py", "--apply"]):
            subject.main()
            api.assert_called_once()
            self.assertEqual(api.call_args.args[:3], (FORK["full_name"], "POST", "/issues"))
            self.assertIn(subject.MARKER, api.call_args.args[3]["body"])
        cfg = json.loads((self.fixture / subject.CONFIG).read_text(encoding="utf-8"))
        self.assertEqual(cfg["notice_issue"], 17)
        self.assertEqual(cfg["repository_id"], 42)
        self.assertIn("vars.DOCUMENTATION_JOURNAL_ENABLED == 'true'",
                      (self.fixture / subject.WORKFLOW).read_text(encoding="utf-8"))
        self.assertEqual(sorted(str(p.relative_to(self.fixture)) for p in self.fixture.rglob("*") if p.is_file()),
                         sorted(str(p) for p in (subject.CONFIG, subject.WORKFLOW,
                                                 Path("README.md"), Path("README.zh-CN.md"))))


if __name__ == "__main__":
    unittest.main()
