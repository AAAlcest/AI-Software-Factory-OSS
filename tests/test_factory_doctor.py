"""Portable Factory Doctor tests. No network or repository mutation."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "factory_doctor.py"
SPEC = importlib.util.spec_from_file_location("factory_doctor", SCRIPT)
doctor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(doctor)

A = "a" * 40


def command(root, *args):
    return subprocess.run(
        list(args), cwd=root, text=True, capture_output=True, check=True)


def init_repo(root, remote="https://github.com/example/factory.git"):
    command(root, "git", "init", "-b", "main")
    command(root, "git", "config", "user.name", "Doctor Test")
    command(root, "git", "config", "user.email", "doctor@example.invalid")
    command(root, "git", "remote", "add", "origin", remote)


def commit_all(root):
    command(root, "git", "add", ".")
    command(root, "git", "commit", "-m", "fixture")


def write(root, path, content):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def common_surfaces(root, rationale="docs/DESIGN_RATIONALE_INDEX.md"):
    write(root, "AGENTS.md", "# Agents\n")
    write(root, "AI_ENTRYPOINT.md", "# Entrypoint\n")
    write(root, "docs/EXECUTION_FIRST.md", "# Execution First\n")
    write(root, rationale, "# Rationale\n")


class FactoryDoctorTests(unittest.TestCase):
    def test_framework_distribution_passes_and_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            common_surfaces(root)
            init_repo(root)
            commit_all(root)
            before = command(root, "git", "rev-parse", "HEAD").stdout.strip()
            result = doctor.inspect(root)
            after = command(root, "git", "rev-parse", "HEAD").stdout.strip()
            status = command(root, "git", "status", "--porcelain").stdout
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["surface"], "FRAMEWORK_DISTRIBUTION")
            self.assertIs(result["execution_authorized"], False)
            self.assertIs(result["read_only"], True)
            self.assertEqual(before, after)
            self.assertEqual(status, "")

    def test_blocked_operating_instance_is_healthy_not_authorized(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            common_surfaces(root, "RATIONALE_INDEX.md")
            for name in ("instance.json", "authority.json", "state.json", "CURRENT.md"):
                shutil.copyfile(ROOT / "templates" / "instance" / name, root / name)
            write(root, "SOURCE_PROVENANCE.json", json.dumps({
                "upstream": "AAAlcest/AI-Software-Factory-OSS",
                "upstream_repository_id": 1358307744,
                "source_ref": "refs/tags/v1.6.0",
                "source_sha": A,
                "license": "MIT",
                "status": "COPIED_FRAMEWORK_NOT_OPERATING_AUTHORITY",
            }))
            write(root, ".github/documentation-journal.json", json.dumps({
                "repository": "example/private-factory",
                "repository_id": 42,
                "default_branch": "main",
                "visibility": "private",
                "notice_issue": 1,
                "baseline_sha": A,
                "paths": ["*.md"],
            }))
            init_repo(root, "https://github.com/example/private-factory.git")
            commit_all(root)
            result = doctor.inspect(root)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["surface"], "OPERATING_INSTANCE")
            self.assertEqual(result["instance_status"], "BLOCKED")
            self.assertIs(result["execution_authorized"], False)
            instance = next(
                item for item in result["checks"]
                if item["name"] == "instance-validator")
            self.assertIn("BLOCKED", instance["detail"])

    def test_tracked_secret_like_filename_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            common_surfaces(root)
            write(root, ".env", "SECRET=synthetic-not-a-real-secret\n")
            init_repo(root)
            commit_all(root)
            result = doctor.inspect(root)
            self.assertEqual(result["status"], "FAIL")
            secret = next(
                item for item in result["checks"]
                if item["name"] == "tracked-secret-like-files")
            self.assertEqual(secret["status"], "FAIL")

    def test_json_cli_reports_diagnostic_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            common_surfaces(root)
            init_repo(root)
            commit_all(root)
            result = subprocess.run(
                [str(Path(__import__("sys").executable)), "-B", str(SCRIPT),
                 "--root", str(root), "--json"],
                text=True, capture_output=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "PASS")
            self.assertIs(payload["read_only"], True)
            self.assertIs(payload["execution_authorized"], False)


if __name__ == "__main__":
    unittest.main()
