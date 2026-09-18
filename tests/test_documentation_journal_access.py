"""Offline regression checks for the Human-approved unlocked notice policy."""
import importlib.util
import os
from pathlib import Path
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
        with self.assertRaisesRegex(m.Gap, "public boundary"):
            self.validate()
        self.assertEqual(self.calls, [("", "GET")])

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
