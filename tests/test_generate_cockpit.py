"""Executable cockpit generation and drift checks."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_cockpit import Invalid, generate
from check_cockpit_drift import check_drift


class CockpitGenerationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.instance = Path(self.tmp.name) / "factory"
        shutil.copytree(ROOT / "examples" / "factory-instance", self.instance)
        self.output = Path(self.tmp.name) / "bundle"

    def test_generate_portable_bundle(self):
        result = generate(self.instance, self.output)
        self.assertEqual(result["status"], "GENERATED")
        self.assertEqual(result["recovery_mode"], "SAME_INCUMBENT_RECOVERY")
        self.assertFalse(result["execution_authorized"])
        for name in (
            "PROJECT_INSTRUCTIONS.md", "FACTORY_OVERVIEW.md", "PROJECTS.md", "ROLES.md",
            "WORKSTREAMS.md", "RECOVERY_BRIEF.md", "HEALTH.md", "CODEX_TASK_PACKAGE.md", "manifest.json"
        ):
            self.assertTrue((self.output / name).is_file(), name)
        manifest = json.loads((self.output / "manifest.json").read_text(encoding="utf-8"))
        self.assertTrue(manifest["derived"])
        self.assertEqual(manifest["canonical_truth"], "repository")
        self.assertFalse(manifest["execution_authorized"])
        self.assertIn("registers/workstreams.json", manifest["source_fingerprints"])
        self.assertIn("registers/continuity.json", manifest["source_fingerprints"])

    def test_existing_destination_is_not_overwritten(self):
        self.output.mkdir()
        marker = self.output / "keep.txt"
        marker.write_text("keep", encoding="utf-8")
        with self.assertRaises(Invalid):
            generate(self.instance, self.output)
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def test_supersession_aware_recovery(self):
        generate(self.instance, self.output, "workstream:atlas-release-readiness")
        text = (self.output / "RECOVERY_BRIEF.md").read_text(encoding="utf-8")
        self.assertIn("fixture:atlas-review-current", text)
        self.assertIn("fixture:atlas-review-obsolete", text)
        self.assertIn("Do not reopen as current", text)

    def test_recovery_mode_is_derived_not_user_selected(self):
        generate(self.instance, self.output, "workstream:beacon-environment")
        first = (self.output / "RECOVERY_BRIEF.md").read_text(encoding="utf-8")
        self.assertIn("FIRST_APPOINTMENT", first)
        self.assertIn("No predecessor or handoff is claimed", first)

        successor_output = Path(self.tmp.name) / "successor"
        generate(self.instance, successor_output, "workstream:atlas-governance-transition")
        successor = (successor_output / "RECOVERY_BRIEF.md").read_text(encoding="utf-8")
        self.assertIn("TRUE_SUCCESSION", successor)
        self.assertIn("fixture:governance-handoff-1", successor)
        self.assertIn("fixture:governance-1", successor)

    def test_invalid_continuity_is_rejected(self):
        path = self.instance / "registers" / "continuity.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["contexts"][0]["mode"] = "TRUE_SUCCESSION"
        data["contexts"][0]["handoff_ref"] = None
        path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(Invalid):
            generate(self.instance, self.output)

    def test_human_gate_and_blocker_surface_in_health(self):
        generate(self.instance, self.output)
        text = (self.output / "HEALTH.md").read_text(encoding="utf-8")
        self.assertIn("workstream:beacon-environment", text)
        self.assertIn("fixture:human-environment-approval", text)

    def test_drift_detects_changed_source(self):
        generate(self.instance, self.output)
        self.assertEqual(check_drift(self.instance, self.output)["status"], "FRESH")
        state = self.instance / "projects" / "atlas" / "STATE.md"
        state.write_text(state.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")
        result = check_drift(self.instance, self.output)
        self.assertEqual(result["status"], "DRIFTED")
        self.assertIn("projects/atlas/STATE.md", result["changed_sources"])
        self.assertFalse(result["fingerprints_are_authority"])

    def test_drift_detects_missing_source(self):
        generate(self.instance, self.output)
        (self.instance / "projects" / "atlas" / "STATE.md").unlink()
        result = check_drift(self.instance, self.output)
        self.assertEqual(result["status"], "DRIFTED")
        self.assertIn("projects/atlas/STATE.md", result["missing_sources"])

    def test_unsafe_manifest_source_is_invalid(self):
        generate(self.instance, self.output)
        path = self.output / "manifest.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["source_fingerprints"]["../outside"] = {"sha256": "0" * 64, "bytes": 1}
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertEqual(check_drift(self.instance, self.output)["status"], "INVALID")

    def test_cli_generation_and_drift(self):
        generated = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / "generate_cockpit.py"),
             "--root", str(self.instance), "--output", str(self.output)],
            capture_output=True, text=True
        )
        self.assertEqual(generated.returncode, 0, generated.stderr)
        self.assertEqual(json.loads(generated.stdout)["recovery_mode"], "SAME_INCUMBENT_RECOVERY")
        checked = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / "check_cockpit_drift.py"),
             "--root", str(self.instance), "--bundle", str(self.output)],
            capture_output=True, text=True
        )
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertEqual(json.loads(checked.stdout)["status"], "FRESH")


if __name__ == "__main__":
    unittest.main()
