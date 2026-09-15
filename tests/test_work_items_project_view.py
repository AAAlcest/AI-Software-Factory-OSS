"""V1.3 Project-visible work-item and long-thread recovery tests."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_cockpit_drift import check_drift
from generate_cockpit import Invalid, generate, parse_instance
from generate_project_view import generate_project_view


class WorkItemProjectViewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.instance = Path(self.tmp.name) / "factory"
        shutil.copytree(ROOT / "examples" / "factory-instance", self.instance)
        self.output = Path(self.tmp.name) / "project-view"

    def work_items_path(self):
        return self.instance / "registers" / "work_items.json"

    def load_work_items(self):
        return json.loads(self.work_items_path().read_text(encoding="utf-8"))

    def save_work_items(self, data):
        self.work_items_path().write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def test_active_workstreams_have_project_visible_items(self):
        instance = parse_instance(self.instance)
        active_lanes = {item["id"] for item in instance["workstreams"] if item["status"] != "DONE"}
        covered = set(instance["work_item_by_workstream"])
        self.assertTrue(active_lanes.issubset(covered))
        done = next(item for item in instance["work_items"] if item["status"] == "DONE")
        self.assertEqual(done["projection_state"], "ARCHIVED")

    def test_project_projection_outputs_markdown_json_csv_and_recovery(self):
        result = generate_project_view(self.instance, self.output, "workitem:atlas-release-readiness")
        self.assertEqual(result["status"], "GENERATED")
        self.assertFalse(result["execution_authorized"])
        for name in (
            "PROJECT_VIEW.md", "project_view.json", "project_view.csv",
            "WORK_ITEM_RECOVERY.md", "VISIBILITY_HEALTH.md", "manifest.json",
        ):
            self.assertTrue((self.output / name).is_file(), name)

        text = (self.output / "PROJECT_VIEW.md").read_text(encoding="utf-8")
        active_section, archived_section = text.split("## Archived work", 1)
        self.assertIn("workitem:atlas-release-readiness", active_section)
        self.assertIn("workitem:beacon-environment", active_section)
        self.assertNotIn("workitem:atlas-governance-transition", active_section)
        self.assertIn("workitem:atlas-governance-transition", archived_section)

        data = json.loads((self.output / "project_view.json").read_text(encoding="utf-8"))
        self.assertTrue(data["derived"])
        self.assertEqual(data["canonical_truth"], "repository")
        self.assertEqual(data["selected_work_item"], "workitem:atlas-release-readiness")
        with (self.output / "project_view.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 3)

        recovery = (self.output / "WORK_ITEM_RECOVERY.md").read_text(encoding="utf-8")
        self.assertIn("checkpoints/atlas-release-readiness-current.md", recovery)
        self.assertIn("checkpoints/atlas-release-readiness-obsolete.md", recovery)
        self.assertIn("fixture:issue-atlas-42", recovery)
        self.assertNotIn("Historical direction: `fixture:atlas-review-obsolete`", recovery)

    def test_cockpit_consumes_work_item_checkpoint_model(self):
        bundle = Path(self.tmp.name) / "cockpit"
        result = generate(self.instance, bundle, "workstream:atlas-release-readiness")
        self.assertEqual(result["selected_work_item"], "workitem:atlas-release-readiness")
        self.assertTrue((bundle / "WORK_ITEMS.md").is_file())
        package = (bundle / "CODEX_TASK_PACKAGE.md").read_text(encoding="utf-8")
        self.assertIn("registers/work_items.json", package)
        self.assertIn("checkpoints/atlas-release-readiness-current.md", package)
        manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
        self.assertIn("registers/work_items.json", manifest["source_fingerprints"])
        self.assertIn("checkpoints/atlas-release-readiness-current.md", manifest["source_fingerprints"])

    def test_project_view_drift_detects_checkpoint_change(self):
        generate_project_view(self.instance, self.output)
        self.assertEqual(check_drift(self.instance, self.output)["status"], "FRESH")
        checkpoint = self.instance / "checkpoints" / "atlas-release-readiness-current.md"
        checkpoint.write_text(checkpoint.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")
        drift = check_drift(self.instance, self.output)
        self.assertEqual(drift["status"], "DRIFTED")
        self.assertIn("checkpoints/atlas-release-readiness-current.md", drift["changed_sources"])

    def test_missing_active_work_item_is_rejected(self):
        data = self.load_work_items()
        data["work_items"] = [item for item in data["work_items"] if item["workstream_id"] != "workstream:atlas-release-readiness"]
        self.save_work_items(data)
        with self.assertRaises(Invalid):
            parse_instance(self.instance)

    def test_duplicate_work_item_id_is_rejected(self):
        data = self.load_work_items()
        data["work_items"][1]["id"] = data["work_items"][0]["id"]
        self.save_work_items(data)
        with self.assertRaises(Invalid):
            parse_instance(self.instance)

    def test_current_checkpoint_cannot_also_be_superseded(self):
        data = self.load_work_items()
        item = data["work_items"][0]
        item["superseded_checkpoint_refs"].append(item["checkpoint_ref"])
        self.save_work_items(data)
        with self.assertRaises(Invalid):
            parse_instance(self.instance)

    def test_done_item_cannot_remain_active_in_projection(self):
        data = self.load_work_items()
        done = next(item for item in data["work_items"] if item["status"] == "DONE")
        done["projection_state"] = "ACTIVE"
        self.save_work_items(data)
        with self.assertRaises(Invalid):
            parse_instance(self.instance)

    def test_missing_checkpoint_or_mismatched_owner_fails_closed(self):
        checkpoint = self.instance / "checkpoints" / "beacon-environment-current.md"
        checkpoint.unlink()
        with self.assertRaises(Invalid):
            parse_instance(self.instance)

        shutil.copy(
            ROOT / "examples" / "factory-instance" / "checkpoints" / "beacon-environment-current.md",
            checkpoint,
        )
        data = self.load_work_items()
        data["work_items"][1]["owner_role"] = "role:management"
        self.save_work_items(data)
        with self.assertRaises(Invalid):
            parse_instance(self.instance)

    def test_cli_projection(self):
        run = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / "generate_project_view.py"),
             "--root", str(self.instance), "--output", str(self.output),
             "--work-item", "workitem:beacon-environment"],
            capture_output=True, text=True,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        payload = json.loads(run.stdout)
        self.assertEqual(payload["selected_work_item"], "workitem:beacon-environment")
        recovery = (self.output / "WORK_ITEM_RECOVERY.md").read_text(encoding="utf-8")
        self.assertIn("fixture:human-environment-approval", recovery)


if __name__ == "__main__":
    unittest.main()
