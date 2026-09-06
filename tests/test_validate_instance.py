"""Offline tests; all mutated inputs are disposable synthetic fixtures."""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_instance.py"
SPEC = importlib.util.spec_from_file_location("preflight", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preflight)


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "instance"
        shutil.copytree(ROOT / "examples" / "demo-factory" / "boot", self.root)

    def edit(self, name, mutate):
        path = self.root / name
        value = json.loads(path.read_text(encoding="utf-8"))
        mutate(value)
        path.write_text(json.dumps(value), encoding="utf-8")

    def expect(self, status, fragment=None):
        result = preflight.inspect(self.root)
        self.assertEqual(result["status"], status, result)
        self.assertIs(result["execution_authorized"], False)
        if fragment:
            self.assertIn(fragment, " ".join(result["diagnostics"]))
        return result

    def test_synthetic_boot_is_structurally_valid_not_authorized(self):
        self.assertEqual(self.expect("VALID")["mode"], "SYNTHETIC")

    def test_template_deliberately_blocked(self):
        result = preflight.inspect(ROOT / "templates" / "instance")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIs(result["execution_authorized"], False)
        self.assertIn("template", " ".join(result["diagnostics"]))

    def test_title_change_does_not_change_scope(self):
        self.edit("instance.json", lambda x: x["role"].update(display_title="General Manager"))
        self.expect("VALID")
        self.edit("state.json", lambda x: x["next_action"].update(action="PUBLICATION"))
        self.expect("BLOCKED", "Human gate")

    def test_missing_owner_blocked(self):
        self.edit("instance.json", lambda x: x.update(human_owner="UNCONFIGURED"))
        self.expect("BLOCKED", "human_owner")

    def test_instance_mode_is_not_authority_verification(self):
        self.edit("instance.json", lambda x: x.update(mode="INSTANCE"))
        self.expect("VALID")

    def test_revoked_authority_blocked(self):
        self.edit("authority.json", lambda x: x.update(status="REVOKED"))
        self.expect("BLOCKED", "not active")

    def test_unknown_decision_blocked(self):
        self.edit("authority.json", lambda x: x.update(decision_record="UNKNOWN"))
        self.expect("BLOCKED", "decision record")

    def test_missing_decision_invalid(self):
        (self.root / "ASSIGNMENT.md").unlink()
        self.expect("INVALID", "missing")

    def test_empty_decision_invalid(self):
        (self.root / "ASSIGNMENT.md").write_text("")
        self.expect("INVALID", "empty")

    def test_state_identity_mismatch(self):
        for field in ("role_id", "incumbent_id", "project_id"):
            with self.subTest(field=field):
                original = (self.root / "state.json").read_bytes()
                self.edit("state.json", lambda x: x.update({field: "other"}))
                self.expect("INVALID", "identity mismatch")
                (self.root / "state.json").write_bytes(original)

    def test_authority_identity_mismatch(self):
        self.edit("authority.json", lambda x: x.update(incumbent_id="other"))
        self.expect("INVALID", "identity mismatch")

    def test_no_grant_blocked(self):
        self.edit("authority.json", lambda x: x.update(grants=[]))
        self.expect("BLOCKED", "no exact")

    def test_cross_project_grant_invalid(self):
        self.edit("authority.json", lambda x: x["grants"][0].update(scope="project:beacon"))
        self.expect("INVALID", "out-of-project")

    def test_cross_project_next_action_blocked(self):
        self.edit("state.json", lambda x: x["next_action"].update(scope="project:beacon"))
        self.expect("BLOCKED", "no exact")

    def test_reserved_actions_blocked_even_with_active_role(self):
        for action in sorted(preflight.GATES):
            with self.subTest(action=action):
                self.edit("state.json", lambda x: x["next_action"].update(action=action))
                self.expect("BLOCKED", "Human gate")

    def test_reserved_grant_invalid(self):
        self.edit("authority.json", lambda x: x["grants"][0].update(action="PUBLICATION"))
        self.expect("INVALID", "reserved action")

    def test_gate_cannot_be_self_approved(self):
        self.edit("authority.json", lambda x: x["gates"].update(PUBLICATION="APPROVED"))
        self.expect("INVALID", "reserved actions")

    def test_blocker_stops_readiness(self):
        self.edit("state.json", lambda x: x.update(blockers=["Review unresolved"]))
        self.expect("BLOCKED", "blockers")

    def test_unknown_phase_blocked(self):
        self.edit("state.json", lambda x: x.update(phase="UNKNOWN"))
        self.expect("BLOCKED", "phase")

    def test_first_appointment_cannot_invent_handoff(self):
        self.edit("state.json", lambda x: x["continuity"].update(handoff="CURRENT.md"))
        self.expect("INVALID", "first appointment")

    def test_recovery_preserves_incumbent(self):
        self.edit("state.json", lambda x: x["continuity"].update(
            kind="RECOVERY", previous_incumbent_id="demo-primary-1"))
        self.expect("VALID")

    def test_recovery_cannot_change_incumbent(self):
        self.edit("state.json", lambda x: x["continuity"].update(
            kind="RECOVERY", previous_incumbent_id="other"))
        self.expect("INVALID", "recovery")

    def test_recovery_cannot_create_succession_handoff(self):
        self.edit("state.json", lambda x: x["continuity"].update(
            kind="RECOVERY", previous_incumbent_id="demo-primary-1", handoff="CURRENT.md"))
        self.expect("INVALID", "recovery")

    def test_succession_requires_existing_distinct_predecessor_record(self):
        (self.root / "HANDOFF.md").write_text("Synthetic finalized historical fixture.\n")
        self.edit("state.json", lambda x: x["continuity"].update(
            kind="SUCCESSION", previous_incumbent_id="demo-earlier", handoff="HANDOFF.md"))
        self.expect("VALID")
        (self.root / "HANDOFF.md").unlink()
        self.expect("INVALID", "missing")

    def test_succession_cannot_use_same_incumbent(self):
        self.edit("state.json", lambda x: x["continuity"].update(
            kind="SUCCESSION", previous_incumbent_id="demo-primary-1", handoff="CURRENT.md"))
        self.expect("INVALID", "different known")

    def test_path_traversal_absolute_url_and_windows_paths_invalid(self):
        for path in ("../outside.md", "/etc/passwd", "C:\\demo\\state.json", "C:state.json",
                     "https://example.invalid/authority", "./CURRENT.md", "a//b", "a/../b"):
            with self.subTest(path=path):
                self.edit("instance.json", lambda x: x.update(current=path))
                self.expect("INVALID", "unsafe relative")

    def test_symlink_invalid(self):
        target = self.root / "CURRENT.md"
        alias = self.root / "alias.md"
        try:
            alias.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink creation unavailable; this case is not verified here")
        self.edit("instance.json", lambda x: x.update(current="alias.md"))
        self.expect("INVALID", "symlinks")

    def test_duplicate_json_key_invalid(self):
        path = self.root / "instance.json"
        path.write_text(path.read_text().replace('"schema_version": 1',
                                               '"schema_version": 1, "schema_version": 1'))
        self.expect("INVALID", "duplicate key")

    def test_unknown_field_invalid(self):
        self.edit("instance.json", lambda x: x.update(admin=True))
        self.expect("INVALID", "unknown fields")

    def test_boolean_is_not_schema_version(self):
        self.edit("instance.json", lambda x: x.update(schema_version=True))
        self.expect("INVALID", "schema version")

    def test_non_finite_number_invalid(self):
        (self.root / "instance.json").write_text('{"schema_version": NaN}')
        self.expect("INVALID", "non-finite")

    def test_wrong_types_do_not_crash(self):
        for value in (None, [], {}, True, 42):
            with self.subTest(value=value):
                self.edit("instance.json", lambda x: x.update(human_owner=value))
                self.expect("INVALID", "string")

    def test_invalid_utf8_and_json_do_not_echo_input(self):
        path = self.root / "instance.json"
        for raw in (b'\xff', b'{private-marker', b'[]'):
            path.write_bytes(raw)
            result = self.expect("INVALID")
            self.assertNotIn("private-marker", str(result))

    def test_oversized_input_invalid(self):
        (self.root / "instance.json").write_bytes(b" " * (preflight.MAX_BYTES + 1))
        self.expect("INVALID", "oversized")

    def test_missing_evidence_invalid(self):
        self.edit("state.json", lambda x: x.update(evidence=["not-present.md"]))
        self.expect("INVALID", "missing")

    def test_duplicate_grant_invalid(self):
        self.edit("authority.json", lambda x: x["grants"].append(x["grants"][0].copy()))
        self.expect("INVALID", "duplicate")

    def test_inspection_does_not_mutate_instance(self):
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.expect("VALID")
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_cli_exit_codes(self):
        for root, code, status in [(self.root, 0, "VALID"),
                                   (ROOT / "templates" / "instance", 3, "BLOCKED"),
                                   (self.root / "missing", 2, "INVALID")]:
            with self.subTest(code=code):
                process = subprocess.run([sys.executable, str(SCRIPT), "--root", str(root)],
                                         capture_output=True, text=True, timeout=10)
                self.assertEqual(process.returncode, code, process.stderr)
                self.assertEqual(json.loads(process.stdout)["status"], status)
                self.assertEqual(process.stderr, "")


if __name__ == "__main__":
    unittest.main()
