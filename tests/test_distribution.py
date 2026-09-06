"""Integrated synthetic demonstration; these are NOT fresh-agent acceptance tests."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from create_demo import CASES, build_files, create_demo
from plan_reply import plan_reply
from validate_demo import check_demo
from validate_instance import inspect
from validate_work_history import validate_record


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "factory"

    def make(self, case="first"):
        create_demo(self.root, case)
        return self.root

    def load(self, name):
        return json.loads((self.root / name).read_text(encoding="utf-8"))

    def test_all_nine_generated_variants(self):
        for case in CASES:
            with self.subTest(case=case):
                target = Path(self.tmp.name) / case
                create_demo(target, case)
                self.assertEqual(check_demo(target)["status"], "VALID")

    def test_first_incumbent_has_no_handoff(self):
        self.make()
        self.assertEqual(self.load("projects/atlas/state.json")["continuity"],
          {"kind": "FIRST_APPOINTMENT", "previous_incumbent_id": None, "handoff": None})
        self.assertFalse((self.root / "projects/atlas/handoff").exists())

    def test_authorized_succession_positive(self):
        self.make("succession")
        state = self.load("projects/atlas/state.json")
        self.assertNotEqual(state["incumbent_id"], state["continuity"]["previous_incumbent_id"])
        self.assertEqual(inspect(self.root / "projects/atlas")["status"], "VALID")
        handoff = self.root / "projects/atlas" / state["continuity"]["handoff"]
        before = handoff.read_bytes()
        self.assertEqual(check_demo(self.root)["status"], "VALID")
        self.assertEqual(handoff.read_bytes(), before)

    def test_recovery_keeps_identity(self):
        self.make("recovery")
        state = self.load("projects/atlas/state.json")
        self.assertEqual(state["incumbent_id"], state["continuity"]["previous_incumbent_id"])
        self.assertIsNone(state["continuity"]["handoff"])

    def test_missing_assignment_is_blocked(self):
        self.make("missing")
        self.assertEqual(inspect(self.root / "projects/beacon")["status"], "BLOCKED")
        self.assertEqual(self.load("factory.json")["selected_project"], "beacon")

    def test_publication_remains_blocked(self):
        self.make("human-gate")
        self.assertEqual(inspect(self.root / "projects/atlas")["status"], "BLOCKED")

    def test_reply_only_retains_mandatory_roles(self):
        self.make("routing")
        request = self.load("reply-request.json")
        request["reply_mode"] = "REPLY_ONLY"
        result = plan_reply(request)
        self.assertEqual(result["cc_roles"], ["role:governance", "role:portfolio-console"])
        self.assertFalse(result["delivery_performed"])

    def test_reviewed_head_is_not_current_head(self):
        self.make("changed-head")
        data = self.load("projects/atlas/evidence/candidate.json")
        self.assertNotEqual(data["current_head"], data["reviewed_head"])
        self.assertFalse(data["integration_authorized"])

    def test_tamper_detected(self):
        self.make()
        (self.root / "TASK.md").write_text("tampered", encoding="utf-8")
        self.assertEqual(check_demo(self.root)["status"], "INVALID")

    def test_added_file_detected(self):
        self.make()
        (self.root / "extra.txt").write_text("unexpected", encoding="utf-8")
        self.assertEqual(check_demo(self.root)["status"], "INVALID")

    def test_no_overwrite(self):
        self.make()
        before = (self.root / "TASK.md").read_bytes()
        with self.assertRaises(ValueError):
            create_demo(self.root)
        self.assertEqual(before, (self.root / "TASK.md").read_bytes())

    def test_unknown_case_has_no_side_effect(self):
        with self.assertRaises(ValueError):
            create_demo(self.root, "not-a-case")
        self.assertFalse(self.root.exists())

    def test_bytes_are_deterministic(self):
        self.assertEqual(build_files("succession"), build_files("succession"))
        self.make()
        for name, digest in self.load("fixture-manifest.json")["files"].items():
            self.assertEqual(hashlib.sha256((self.root / name).read_bytes()).hexdigest(), digest)

    def test_prior_history_rewrite_is_rejected(self):
        self.make()
        work = self.load("offices/management/wardrobe/atlas.json")
        prior = deepcopy(work)
        prior["events"] = prior["events"][:1]
        self.assertEqual(validate_record(work, prior)["status"], "VALID")
        work["events"][0]["evidence_ref"] = "fixture:rewritten"
        self.assertEqual(validate_record(work, prior)["status"], "INVALID")

    def test_cli_actual_generation_and_check(self):
        generated = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/create_demo.py"),
          "--destination", str(self.root), "--case", "succession"], capture_output=True, text=True)
        self.assertEqual(generated.returncode, 0, generated.stderr)
        checked = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/validate_demo.py"), str(self.root)],
          capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertFalse(json.loads(checked.stdout)["fresh_agent_validated"])

    def test_oversized_integer_is_invalid_not_traceback(self):
        # Regression: Python's integer conversion limit previously escaped inspect().
        self.root.mkdir()
        (self.root / "instance.json").write_text('{"schema_version":' + "9" * 5000 + '}', encoding="utf-8")
        self.assertEqual(inspect(self.root)["status"], "INVALID")
        result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/validate_instance.py"),
          "--root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_result_never_claims_independent_acceptance(self):
        self.make()
        result = check_demo(self.root)
        for key in ("execution_authorized", "fresh_agent_validated", "independent_privacy_approved"):
            self.assertIs(result[key], False)

    def test_console_does_not_spawn_workers(self):
        self.make()
        self.assertFalse(self.load("console/portfolio.json")["auto_dispatch"])
        self.assertFalse(self.load("registers/roles.json")["roles"]["project:beacon"]["auto_dispatch"])


if __name__ == "__main__":
    unittest.main()
