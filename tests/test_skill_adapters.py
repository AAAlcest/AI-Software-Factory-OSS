"""Executable skill adapter and context measurement tests."""
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
from generate_cockpit import generate
from measure_context import measure
from run_skill import Invalid, run_skill


class SkillAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.instance = Path(self.tmp.name) / "factory"
        shutil.copytree(ROOT / "examples" / "factory-instance", self.instance)
        self.bundle = Path(self.tmp.name) / "bundle"
        generate(self.instance, self.bundle, "workstream:atlas-release-readiness")

    def test_factory_and_project_overview(self):
        factory = run_skill(self.instance, self.bundle, "factory-overview")
        self.assertEqual(factory["status"], "OK")
        self.assertFalse(factory["execution_authorized"])
        self.assertIn("Factory overview", factory["content"])

        project = run_skill(self.instance, self.bundle, "project-overview", project="project:atlas")
        self.assertEqual(project["facts"]["project"]["id"], "project:atlas")
        self.assertTrue(project["facts"]["workstreams"])

    def test_role_overview_and_unknown_scope(self):
        role = run_skill(self.instance, self.bundle, "role-overview", role="role:management")
        self.assertEqual(role["status"], "OK")
        self.assertEqual(role["facts"]["role"]["id"], "role:management")
        with self.assertRaises(Invalid):
            run_skill(self.instance, self.bundle, "project-overview", project="project:not-real")

    def test_recovery_and_handoff_classification(self):
        same = run_skill(self.instance, self.bundle, "handoff", workstream="workstream:atlas-release-readiness")
        self.assertEqual(same["classification"], "SAME_INCUMBENT_RECOVERY")
        first = run_skill(self.instance, self.bundle, "handoff", workstream="workstream:beacon-environment")
        self.assertEqual(first["classification"], "FIRST_APPOINTMENT")
        successor = run_skill(self.instance, self.bundle, "handoff", workstream="workstream:atlas-governance-transition")
        self.assertEqual(successor["classification"], "TRUE_SUCCESSION")
        self.assertEqual(successor["facts"]["continuity"]["handoff_ref"], "fixture:governance-handoff-1")

    def test_project_and_role_recovery_match_scope(self):
        project = run_skill(
            self.instance, self.bundle, "project-recovery",
            project="project:atlas", workstream="workstream:atlas-release-readiness"
        )
        self.assertEqual(project["facts"]["continuity"]["mode"], "SAME_INCUMBENT_RECOVERY")
        role = run_skill(
            self.instance, self.bundle, "role-recovery",
            role="role:runtime", workstream="workstream:beacon-environment"
        )
        self.assertEqual(role["facts"]["continuity"]["mode"], "FIRST_APPOINTMENT")
        with self.assertRaises(Invalid):
            run_skill(
                self.instance, self.bundle, "project-recovery",
                project="project:beacon", workstream="workstream:atlas-release-readiness"
            )

    def test_task_packaging_requires_matching_generated_lane(self):
        current = run_skill(
            self.instance, self.bundle, "task-packaging",
            workstream="workstream:atlas-release-readiness"
        )
        self.assertEqual(current["status"], "OK")
        self.assertIn("Bounded Codex task package", current["content"])
        other = run_skill(
            self.instance, self.bundle, "task-packaging",
            workstream="workstream:beacon-environment"
        )
        self.assertEqual(other["status"], "REGENERATE_REQUIRED")
        self.assertFalse(other["execution_authorized"])

    def test_stale_bundle_blocks_skills_and_measurement(self):
        state = self.instance / "projects" / "atlas" / "STATE.md"
        state.write_text(state.read_text(encoding="utf-8") + "\ndrift\n", encoding="utf-8")
        skill = run_skill(self.instance, self.bundle, "factory-overview")
        self.assertEqual(skill["status"], "BLOCKED_STALE_BUNDLE")
        measured = measure(self.instance, self.bundle)
        self.assertEqual(measured["status"], "BLOCKED_STALE_BUNDLE")

    def test_measurement_is_observable_not_token_claim(self):
        result = measure(self.instance, self.bundle)
        self.assertEqual(result["status"], "MEASURED")
        self.assertGreater(result["broad_context"]["files"], result["bounded_context"]["files"])
        self.assertGreater(result["broad_context"]["bytes"], result["bounded_context"]["bytes"])
        self.assertEqual(result["token_counts"], "NOT_EXPOSED")
        self.assertIn("not a token-saving guarantee", result["interpretation"])
        self.assertFalse(result["execution_authorized"])

    def test_cli_adapter_and_measurement(self):
        adapter = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / "run_skill.py"),
             "--root", str(self.instance), "--bundle", str(self.bundle),
             "--skill", "handoff", "--workstream", "workstream:atlas-release-readiness"],
            capture_output=True, text=True
        )
        self.assertEqual(adapter.returncode, 0, adapter.stderr)
        self.assertEqual(json.loads(adapter.stdout)["classification"], "SAME_INCUMBENT_RECOVERY")

        measured = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / "measure_context.py"),
             "--root", str(self.instance), "--bundle", str(self.bundle)],
            capture_output=True, text=True
        )
        self.assertEqual(measured.returncode, 0, measured.stderr)
        self.assertEqual(json.loads(measured.stdout)["token_counts"], "NOT_EXPOSED")


if __name__ == "__main__":
    unittest.main()
