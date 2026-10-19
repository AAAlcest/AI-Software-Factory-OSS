"""CLI evidence for the public, synthetic five-minute demo (not live Agent acceptance)."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


class QuickDemoCLITests(unittest.TestCase):
    def run_cli(self, name: str, *args: object):
        process = subprocess.run(
            [sys.executable, "-B", str(SCRIPTS / name), *map(str, args)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        try:
            output = json.loads(process.stdout)
        except (ValueError, TypeError):
            self.fail(f"{name}: expected JSON stdout; exit={process.returncode}")
        self.assertIsInstance(output, dict)
        if "execution_authorized" in output:
            self.assertIs(output["execution_authorized"], False)
        return process, output

    def test_real_cli_normal_and_fail_closed_exits(self):
        with tempfile.TemporaryDirectory(prefix="oss-quick-demo-") as directory:
            destination = Path(directory) / "factory-quick-demo"

            created, create_json = self.run_cli(
                "create_demo.py", "--destination", destination, "--case", "first"
            )
            self.assertEqual(created.returncode, 0, created.stderr)
            self.assertEqual(create_json["status"], "SYNTHETIC_PACKAGE_CREATED")
            self.assertEqual(create_json["case"], "first")
            self.assertEqual(create_json["fresh_agent_result"], "NOT_RUN")

            generated, generated_json = self.run_cli("validate_demo.py", destination)
            self.assertEqual(generated.returncode, 0, generated.stderr)
            self.assertEqual(generated_json["status"], "VALID")
            self.assertEqual(generated_json["atlas"], "VALID")
            self.assertEqual(generated_json["beacon"], "BLOCKED")
            self.assertFalse(generated_json["fresh_agent_validated"])
            self.assertFalse(generated_json["independent_privacy_approved"])

            atlas, atlas_json = self.run_cli(
                "validate_instance.py", "--root", destination / "projects" / "atlas"
            )
            self.assertEqual(atlas.returncode, 0, atlas.stderr)
            self.assertEqual(atlas_json["status"], "VALID")

            starter, starter_json = self.run_cli(
                "validate_instance.py", "--root", ROOT / "templates" / "instance"
            )
            self.assertEqual(starter.returncode, 3, starter.stderr)
            self.assertEqual(starter_json["status"], "BLOCKED")
            self.assertEqual(starter_json["mode"], "TEMPLATE")
            self.assertTrue(starter_json["diagnostics"])

            before = (destination / "fixture-manifest.json").read_bytes()
            repeated, repeated_json = self.run_cli(
                "create_demo.py", "--destination", destination, "--case", "first"
            )
            self.assertEqual(repeated.returncode, 2, repeated.stderr)
            self.assertEqual(repeated_json["status"], "INVALID")
            self.assertEqual((destination / "fixture-manifest.json").read_bytes(), before)

            print("QUICK_DEMO_CLI_EVIDENCE=" + json.dumps({
                "created": [created.returncode, create_json["status"]],
                "synthetic_validation": [generated.returncode, generated_json["status"]],
                "atlas": [atlas.returncode, atlas_json["status"]],
                "template_refusal": [starter.returncode, starter_json["status"]],
                "existing_destination_refusal": [repeated.returncode, repeated_json["status"]],
                "execution_authorized": False,
                "fresh_agent_validated": False,
            }, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
