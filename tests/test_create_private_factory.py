"""Public-safe offline tests; never create a real GitHub repository."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("private_bootstrap", ROOT / "scripts/create_private_factory.py")
subject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subject)
HEAD = "a" * 40
VIEWER = {"id": 7, "login": "example-user"}
DEST = "example-user/Private-Factory"


class PrivateFactoryTests(unittest.TestCase):
    def test_default_cli_is_read_only(self):
        with patch("sys.argv", ["create_private_factory.py", "--repository", "Private-Factory"]), \
             patch.object(subject, "process", return_value="secret-in-memory") as command, \
             patch.object(subject, "source_and_target", return_value=(VIEWER, HEAD, DEST)), \
             patch.object(subject, "apply") as apply, \
             patch("builtins.print") as output:
            subject.main()
        command.assert_called_once_with(["gh", "auth", "token"])
        apply.assert_not_called()
        self.assertIn("No writes performed", output.call_args.args[0])

    def source(self, origin=f"https://github.com/{subject.UPSTREAM}.git", branch="main",
               remote=HEAD, existing=None):
        replies = {
            ("git", "status", "--porcelain"): "",
            ("git", "rev-parse", "--show-toplevel"): str(ROOT),
            ("git", "remote", "get-url", "origin"): origin,
            ("git", "rev-parse", "HEAD"): HEAD,
            ("git", "branch", "--show-current"): branch,
            ("git", "ls-remote", "origin", "refs/heads/main"): f"{remote}\trefs/heads/main",
        }
        calls = []
        def command(args, **_):
            calls.append(("local", tuple(args)))
            return replies[tuple(args)]
        def api(_token, path, **_):
            calls.append(("remote", path))
            if path == f"/repos/{subject.UPSTREAM}":
                return {"id": subject.UPSTREAM_ID, "full_name": subject.UPSTREAM,
                        "private": False, "default_branch": "main"}
            if path.endswith("/git/ref/heads/main"):
                return {"object": {"sha": HEAD}}
            if path == "/user":
                return VIEWER
            if path == f"/repos/{DEST}":
                return existing
            raise AssertionError(path)
        with patch.object(subject, "process", side_effect=command), patch.object(subject, "api", side_effect=api):
            return subject.source_and_target("token", "Private-Factory"), calls

    def test_exact_upstream_and_absent_destination(self):
        result, calls = self.source()
        self.assertEqual(result, (VIEWER, HEAD, DEST))
        self.assertEqual(calls[-1], ("remote", f"/repos/{DEST}"))
        with self.assertRaisesRegex(subject.BootstrapError, "exists"):
            self.source(existing={"id": 99})
        with self.assertRaisesRegex(subject.BootstrapError, "origin"):
            self.source(origin="https://github.com/other/repo.git")
        with self.assertRaisesRegex(subject.BootstrapError, "exact OSS main"):
            self.source(branch="candidate")
        with self.assertRaisesRegex(subject.BootstrapError, "tips differ"):
            self.source(remote="b" * 40)

    def test_destination_readback_rejects_public_fork_or_wrong_identity(self):
        row = {"id": 42, "full_name": DEST, "owner": VIEWER, "private": True,
               "fork": False, "default_branch": "main"}
        for mutation in ({"private": False}, {"fork": True}, {"id": 43},
                         {"owner": {"id": 9}}, {"default_branch": "master"}):
            with self.subTest(mutation=mutation), patch.object(subject, "api", return_value={**row, **mutation}):
                with self.assertRaisesRegex(subject.BootstrapError, "readback failed"):
                    subject.verify_destination("token", DEST, 42, 7, "main")

    def test_generated_starter_is_lean_blocked_and_provenanced(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subject.staged_source(root, HEAD)
            names = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
            self.assertIn("LICENSE", names)
            self.assertIn("instance.json", names)
            self.assertIn("scripts/documentation_journal.py", names)
            self.assertFalse(any(n.startswith("examples/") for n in names))
            self.assertFalse(any(n.startswith("tests/") and n != "tests/test_documentation_journal.py" for n in names))
            self.assertEqual(json.loads((root / "SOURCE_PROVENANCE.json").read_text())["source_sha"], HEAD)
            self.assertEqual(json.loads((root / "authority.json").read_text())["status"], "UNKNOWN")
            result = subprocess.run(["python", "-B", "scripts/validate_instance.py", "--root", str(root)],
                                    cwd=root, text=True, capture_output=True)
            self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "BLOCKED")

    def test_private_journal_is_bound_and_disabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subject.staged_source(root, HEAD)
            subject.journal_files(root, DEST, 42, 17, HEAD)
            cfg = json.loads((root / subject.CONFIG).read_text())
            self.assertEqual((cfg["repository"], cfg["repository_id"], cfg["visibility"],
                              cfg["notice_issue"], cfg["baseline_sha"]),
                             (DEST, 42, "private", 17, HEAD))
            writer = (root / subject.WRITER).read_text()
            self.assertIn("github.repository_id == '42'", writer)
            self.assertIn("vars.DOCUMENTATION_JOURNAL_ENABLED == 'true'", writer)
            self.assertIn("github.event_name == 'workflow_dispatch' && inputs.dry_run", writer)
            self.assertNotIn("github.repository_id == '1358307744'", writer)
            self.assertIn(f"https://github.com/{DEST}/issues/17", (root / "README.md").read_text())

    def test_issues_enablement_is_scoped_and_read_back(self):
        row = {"id": 42, "full_name": DEST, "owner": VIEWER, "private": True,
               "fork": False, "has_issues": False, "permissions": {"admin": True}}
        calls = []
        def fake_api(_token, path, method="GET", payload=None):
            calls.append((path, method, payload))
            return None
        with patch.object(subject, "api", side_effect=fake_api), \
             patch.object(subject, "verify_destination", return_value={**row, "has_issues": True}):
            self.assertTrue(subject.ensure_issues("token", DEST, row, 42, 7)["has_issues"])
        self.assertEqual(calls, [(f"/repos/{DEST}", "PATCH", {"has_issues": True})])
        with patch.object(subject, "api") as api:
            with self.assertRaisesRegex(subject.BootstrapError, "admin access"):
                subject.ensure_issues("token", DEST, {**row, "permissions": {"admin": False}}, 42, 7)
            api.assert_not_called()

    def test_notice_creator_target_open_and_unlock_are_required(self):
        notice = {"id": 99, "state": "open", "locked": False, "user": VIEWER,
                  "repository_url": f"https://api.github.com/repos/{DEST}"}
        subject.verify_notice(notice, notice, DEST, 7)
        for bad in ({"user": {"id": 8}}, {"repository_url": "https://api.github.com/repos/other/repo"},
                    {"locked": True}, {"state": "closed"}, {"id": 100}):
            with self.subTest(bad=bad), self.assertRaisesRegex(subject.BootstrapError, "notice"):
                subject.verify_notice({**notice, **bad}, notice, DEST, 7)

    def test_private_git_uses_env_askpass_not_token_in_argv_or_url(self):
        seen = []
        def fake_run(args, **kwargs):
            seen.append((args, kwargs))
            return subprocess.CompletedProcess(args, 0, stdout="", stderr="")
        with patch("subprocess.run", side_effect=fake_run):
            subject.process(["git", "fetch", "https://github.com/example-user/Private-Factory.git", HEAD],
                            cwd=ROOT, token="TOP_SECRET_CANARY")
        args, kwargs = seen[0]
        self.assertNotIn("TOP_SECRET_CANARY", " ".join(args))
        self.assertEqual(kwargs["env"]["GITHUB_TOKEN"], "TOP_SECRET_CANARY")
        self.assertTrue(kwargs["env"]["GIT_ASKPASS"].endswith("documentation_journal_askpass.sh"))
        self.assertEqual(kwargs["env"]["GIT_CONFIG_GLOBAL"], os.devnull)

    def test_apply_creates_private_nonfork_only_and_never_enables_writer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            writes = []
            state = {"repo": None, "notice": None, "tip": None}
            original_staging = subject.tempfile.TemporaryDirectory
            class Staging:
                def __init__(self, **_):
                    pass
                def __enter__(self):
                    return str(root)
                def __exit__(self, *_):
                    return False
            def fake_git(_root, *args, token=None):
                writes.append(("git", args, token is not None))
                if args == ("rev-parse", "HEAD"):
                    return HEAD if state["tip"] is None else "b" * 40
                if args[0] == "push":
                    state["tip"] = HEAD if state["tip"] is None else "b" * 40
                return ""
            def fake_api(_token, path, method="GET", payload=None, **_):
                if path == "/user/repos" and method == "POST":
                    writes.append(("create", payload))
                    state["repo"] = {"id": 42, "full_name": DEST, "owner": VIEWER,
                                     "private": True, "fork": False, "has_issues": True,
                                     "default_branch": "main"}
                    return state["repo"]
                if path == f"/repos/{DEST}":
                    return state["repo"]
                if path == f"/repos/{DEST}/issues" and method == "POST":
                    writes.append(("notice", payload))
                    state["notice"] = {"id": 99, "number": 17, "state": "open", "locked": False,
                                       "user": VIEWER,
                                       "repository_url": f"https://api.github.com/repos/{DEST}"}
                    return state["notice"]
                if path == f"/repos/{DEST}/issues/17":
                    return state["notice"]
                if path == f"/repos/{DEST}/git/ref/heads/main":
                    return {"object": {"sha": state["tip"]}}
                raise AssertionError((path, method))
            try:
                with patch.object(subject.tempfile, "TemporaryDirectory", Staging), \
                     patch.object(subject, "git", side_effect=fake_git), \
                     patch.object(subject, "api", side_effect=fake_api), \
                     patch("builtins.print"):
                    subject.apply("SECRET", VIEWER, HEAD, DEST)
            finally:
                subject.tempfile.TemporaryDirectory = original_staging
            create = next(item for item in writes if item[0] == "create")[1]
            self.assertEqual(create["private"], True)
            self.assertEqual(create["auto_init"], False)
            self.assertFalse(any(item[0] == "fork" for item in writes))
            self.assertTrue(all(item[0] != "variable" for item in writes))
            self.assertEqual(json.loads((root / "authority.json").read_text())["status"], "UNKNOWN")
            self.assertEqual(json.loads((root / subject.CONFIG).read_text())["visibility"], "private")


if __name__ == "__main__":
    unittest.main()
