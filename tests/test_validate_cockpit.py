"""Project cockpit bundle validation tests; not fresh-agent acceptance."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_cockpit import validate_bundle


class CockpitValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "factory"
        shutil.copytree(ROOT / "examples" / "factory-instance", self.root)

    def load(self):
        return json.loads((self.root / "project-cockpit" / "manifest.json").read_text(encoding="utf-8"))

    def save(self, data):
        (self.root / "project-cockpit" / "manifest.json").write_text(
            json.dumps(data, indent=2) + "\n", encoding="utf-8"
        )

    def test_checked_in_cockpit_is_valid(self):
        result = validate_bundle(self.root)
        self.assertEqual(result["status"], "VALID")
        self.assertFalse(result["execution_authorized"])
        self.assertFalse(result["repository_truth_overridden"])

    def test_duplicate_role_or_project_id_is_invalid(self):
        data = self.load()
        data["roles"].append(deepcopy(data["roles"][0]))
        self.save(data)
        self.assertEqual(validate_bundle(self.root)["status"], "INVALID")

    def test_outside_root_reference_is_invalid(self):
        data = self.load()
        data["source_refs"][0] = "../README.md"
        self.save(data)
        self.assertEqual(validate_bundle(self.root)["status"], "INVALID")

    def test_unknown_recovery_mode_is_invalid(self):
        data = self.load()
        data["recovery_mode"] = "NEW_CHAT_MEANS_NEW_TENURE"
        self.save(data)
        self.assertEqual(validate_bundle(self.root)["status"], "INVALID")

    def test_output_must_be_marked_derived(self):
        target = self.root / "project-cockpit" / "HEALTH.md"
        target.write_text("# Health\n\nLooks fine.\n", encoding="utf-8")
        self.assertEqual(validate_bundle(self.root)["status"], "INVALID")

    def test_cockpit_cannot_claim_execution_authority(self):
        data = self.load()
        data["execution_authorized"] = True
        self.save(data)
        self.assertEqual(validate_bundle(self.root)["status"], "INVALID")

    def test_cli(self):
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / "validate_cockpit.py"),
             "--root", str(self.root)], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "VALID")


if __name__ == "__main__":
    unittest.main()
