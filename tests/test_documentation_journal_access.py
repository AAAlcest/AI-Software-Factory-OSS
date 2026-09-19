"""Offline regression checks for the Human-approved unlocked notice policy."""
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("journal_access_subject", ROOT / "scripts/documentation_journal.py")
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


class NoticeAccessTests(unittest.TestCase):
    def setUp(self):
        self.cfg = {"repository": "example/factory", "repository_id": 123,
                    "default_branch": "main", "notice_issue": 26}
        self.repo = {"id": 123, "full_name": "example/factory",
                     "default_branch": "main", "private": False}
        self.notice = {"state": "open", "locked": False}
        self.calls = []
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        event = Path(self.tmp.name) / "event.json"
        event.write_text("{}", encoding="utf-8")
        self.env = {"GITHUB_REPOSITORY": "example/factory", "GITHUB_EVENT_NAME": "schedule",
                    "GITHUB_EVENT_PATH": str(event),
                    "GITHUB_WORKFLOW_REF": "example/factory/" + m.WRITER + "@refs/heads/main"}

    def validate(self):
        subject = self
        class ReadOnlyAPI:
            def call(self, path, method="GET", data=None):
                subject.calls.append((path, method))
                if method != "GET":
                    raise AssertionError("validation must not mutate access or comments")
                if path == "":
                    return subject.repo
                if path == "/issues/26":
                    return subject.notice
                raise AssertionError("unexpected destination")
        with patch.dict(os.environ, self.env, clear=True):
            m.validate_environment(ReadOnlyAPI(), self.cfg)

    def test_open_unlocked_notice_is_accepted(self):
        self.validate()
        self.assertEqual(self.calls, [("", "GET"), ("/issues/26", "GET")])

    def test_relocked_notice_stops_without_unlocking(self):
        self.notice["locked"] = True
        with self.assertRaisesRegex(m.Gap, "open and unlocked"):
            self.validate()
        self.assertTrue(all(method == "GET" for _, method in self.calls))

    def test_closed_notice_is_rejected(self):
        self.notice["state"] = "closed"
        with self.assertRaises(m.Gap):
            self.validate()

    def test_missing_or_nonboolean_lock_state_is_rejected(self):
        for value in (None, 0, "false", ""):
            with self.subTest(value=value):
                self.notice["locked"] = value
                with self.assertRaises(m.Gap):
                    self.validate()
        self.notice.pop("locked")
        with self.assertRaises(m.Gap):
            self.validate()

    def test_private_repository_is_still_rejected(self):
        self.repo["private"] = True
        with self.assertRaisesRegex(m.Gap, "visibility mismatch"):
            self.validate()
        self.assertEqual(self.calls, [("", "GET")])

    def test_explicit_private_visibility_and_exact_notice_target(self):
        self.cfg["visibility"] = "private"
        self.repo["private"] = True
        self.notice["repository_url"] = "https://api.github.com/repos/example/factory"
        self.validate()
        self.notice["repository_url"] = "https://api.github.com/repos/other/factory"
        with self.assertRaisesRegex(m.Gap, "private notice target mismatch"):
            self.validate()
        self.repo["private"] = False
        with self.assertRaisesRegex(m.Gap, "visibility mismatch"):
            self.validate()

    def test_unknown_visibility_fails_closed(self):
        self.cfg["visibility"] = "unknown"
        with self.assertRaisesRegex(m.Gap, "unsupported configured visibility"):
            self.validate()

    def test_private_git_fetch_uses_same_repo_askpass_and_sanitizes_failure(self):
        seen = []
        def fake_run(args, **kwargs):
            seen.append((args, kwargs))
            raise subprocess.CalledProcessError(1, args, stderr=b"SECRET_CANARY")
        with patch("subprocess.run", side_effect=fake_run):
            git = m.Git(ROOT, "example/factory", ["*.md"], "private", "SECRET_CANARY")
            with self.assertRaisesRegex(m.Gap, "Git object unavailable") as failure:
                git.run("fetch", "https://github.com/example/factory.git", "a" * 40)
        self.assertNotIn("SECRET_CANARY", str(failure.exception))
        args, kwargs = seen[0]
        self.assertNotIn("SECRET_CANARY", " ".join(args))
        self.assertIn("https://github.com/example/factory.git", args)
        self.assertEqual(kwargs["env"]["GITHUB_TOKEN"], "SECRET_CANARY")
        self.assertEqual(kwargs["env"]["GIT_CONFIG_GLOBAL"], os.devnull)

    def test_private_git_without_repository_token_stops(self):
        git = m.Git(ROOT, "example/factory", ["*.md"], "private", "")
        with self.assertRaisesRegex(m.Gap, "authentication unavailable"):
            git.run("fetch", "https://github.com/example/factory.git", "a" * 40)

    def test_wrong_repository_is_still_rejected(self):
        self.repo["id"] = 456
        with self.assertRaisesRegex(m.Gap, "identity"):
            self.validate()

    def test_candidate_workflow_cannot_become_writer(self):
        self.env["GITHUB_WORKFLOW_REF"] = "example/factory/" + m.WRITER + "@refs/heads/candidate"
        with self.assertRaisesRegex(m.Gap, "default branch"):
            self.validate()


if __name__ == "__main__":
    unittest.main()
