"""Offline tests: no network, runtime dispatcher or private fixtures."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_work_history.py"
SPEC = importlib.util.spec_from_file_location("work_history", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
FIXTURE = ROOT / "examples/work-history/completed-session.json"


class WorkHistoryTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def check(self, value, status="INVALID", code=None, previous=None):
        result = MODULE.validate_record(value, previous)
        self.assertEqual(result["status"], status, result)
        for key in ("execution_authorized", "liveness_verified", "evidence_verified",
                    "independent_review_granted"):
            self.assertIs(result[key], False)
        if code:
            self.assertIn(code, result["codes"])
        return result

    def test_valid_prefixes_and_unknown_session_metadata(self):
        for count, state in enumerate(MODULE.STATES, 1):
            with self.subTest(state=state):
                record = deepcopy(self.record)
                record["events"] = record["events"][:count]
                result = self.check(record, "VALID")
                self.assertEqual(result["recorded_state"], state)

    def test_unconfigured_template_is_blocked(self):
        self.check(json.loads((ROOT / "templates/work-history/session.json").read_text()), "BLOCKED")

    def test_requested_but_not_entered_cannot_claim_active(self):
        self.record["session"]["entry"] = "REQUESTED_NOT_ENTERED"
        self.check(self.record, code="UNENTERED_HAS_EVENTS")
        self.record["events"] = []
        self.check(self.record, "BLOCKED", "SESSION_NOT_ENTERED")

    def test_unknown_entry_cannot_claim_active(self):
        self.record["session"]["entry"] = "UNKNOWN"
        self.check(self.record, code="UNENTERED_HAS_EVENTS")

    def test_entered_without_start_is_blocked(self):
        self.record["events"] = []
        self.check(self.record, "BLOCKED", "START_NOT_RECORDED")

    def test_skipped_or_duplicate_transition(self):
        for states in (["DONE_UNACKED"], ["ACTIVE", "COMPLETED_ACKED"], ["ACTIVE", "ACTIVE"]):
            with self.subTest(states=states):
                record = deepcopy(self.record)
                record["events"] = record["events"][:len(states)]
                for event, state in zip(record["events"], states):
                    event["state"] = state
                self.check(record, code="TRANSITION_INVALID")

    def test_worker_cannot_declare_management_ack(self):
        self.record["events"][-1]["by_role"] = "fictional-worker"
        self.check(self.record, code="ACK_ROLE_MISMATCH")

    def test_unresolved_actor_evidence_or_time(self):
        for field, code in (("by_role", "ACTOR_UNRESOLVED"), ("evidence_ref", "EVIDENCE_UNRESOLVED"),
                            ("at", "TIME_UNRESOLVED")):
            with self.subTest(field=field):
                record = deepcopy(self.record)
                record["events"][1][field] = "UNKNOWN"
                self.check(record, "BLOCKED", code)

    def test_unresolved_core(self):
        self.record["authority_ref"] = "UNKNOWN"
        self.check(self.record, "BLOCKED", "CORE_UNRESOLVED")

    def test_reversed_time(self):
        self.record["events"][1]["at"] = "1999-12-31T23:59:59Z"
        self.check(self.record, code="TIME_REVERSED")

    def test_timezone_aware_comparison(self):
        self.record["events"][1]["at"] = "2000-01-01T17:05:00+08:00"
        self.check(self.record, "VALID")

    def test_invalid_timestamps(self):
        for stamp in ("2000-01-01T09:05:00", "2000-02-30T09:05:00Z", "2000-01-01T09:05:00+25:00", "2000-01-01T09:05:00+00:60", "today"):
            with self.subTest(stamp=stamp):
                record = deepcopy(self.record)
                record["events"][1]["at"] = stamp
                self.check(record, code="TIME_INVALID")

    def test_schema_and_types(self):
        for value in (None, [], True, "record", {}, {"schema_version": 1}):
            with self.subTest(value=value):
                self.check(value, code="FIELDS_INVALID")
        for field, value in (("schema_version", True), ("schema_version", 2), ("record_kind", "UNKNOWN"),
                             ("session", []), ("events", {}), ("project_id", 1), ("work_id", " ")):
            with self.subTest(field=field, value=value):
                record = deepcopy(self.record)
                record[field] = value
                self.check(record)

    def test_unknown_fields_are_rejected(self):
        for target in (self.record, self.record["session"], self.record["events"][0]):
            target["execution_authorized"] = True
            self.check(self.record, code="FIELDS_INVALID")
            del target["execution_authorized"]

    def test_control_characters_and_long_values(self):
        for value in ("a\nb", "x\x00y", "x\x7fy", "x" * 513):
            self.record["task_ref"] = value
            self.check(self.record, code="TEXT_INVALID")

    def test_extra_events(self):
        self.record["events"].append(deepcopy(self.record["events"][-1]))
        self.check(self.record, code="EVENTS_INVALID")

    def test_previous_unchanged_and_append(self):
        self.check(self.record, "VALID", previous=deepcopy(self.record))
        previous = deepcopy(self.record)
        previous["events"] = previous["events"][:1]
        self.check(self.record, "VALID", previous=previous)

    def test_previous_event_rewrite_or_truncation(self):
        previous = deepcopy(self.record)
        self.record["events"][0]["evidence_ref"] = "fixture:replacement"
        self.check(self.record, code="HISTORY_REWRITTEN", previous=previous)
        self.record = deepcopy(previous)
        self.record["events"].pop()
        self.check(self.record, code="HISTORY_REWRITTEN", previous=previous)

    def test_previous_identity_and_context_change(self):
        previous = deepcopy(self.record)
        for field in ("incumbent_id", "origin_role", "task_ref", "project_id", "authority_ref"):
            with self.subTest(field=field):
                record = deepcopy(previous)
                record[field] += "-changed"
                if field == "origin_role":
                    record["events"][-1]["by_role"] = record[field]
                self.check(record, code="IDENTITY_OR_CONTEXT_CHANGED", previous=previous)

    def test_previous_must_be_structurally_valid(self):
        previous = deepcopy(self.record)
        previous["authority_ref"] = "UNKNOWN"
        self.check(self.record, code="PREVIOUS_NOT_VALID", previous=previous)

    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), *map(str, args)],
                              capture_output=True, text=True, timeout=10)

    def test_cli_success_and_no_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            original = FIXTURE.read_bytes()
            path.write_bytes(original)
            run = self.run_cli(path)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)["status"], "VALID")
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(list(Path(directory).iterdir()), [path])
            self.assertEqual(run.stderr, "")

    def test_cli_blocked(self):
        run = self.run_cli(ROOT / "templates/work-history/session.json")
        self.assertEqual(run.returncode, 3)
        self.assertEqual(json.loads(run.stdout)["status"], "BLOCKED")

    def test_cli_malformed_duplicate_nonfinite_and_oversized(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            for raw in (b"{", b"\xff", b'{"x":1,"x":2}', b'{"x":NaN}', b"[" * 2000,
                        b" " * (MODULE.MAX_BYTES + 1)):
                with self.subTest(size=len(raw)):
                    path.write_bytes(raw)
                    run = self.run_cli(path)
                    self.assertEqual(run.returncode, 2, run.stderr)
                    self.assertEqual(json.loads(run.stdout)["status"], "INVALID")
                    self.assertNotIn(directory, run.stdout + run.stderr)

    def test_cli_missing_directory_and_null_previous(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.json"
            for path in (missing, Path(directory)):
                run = self.run_cli(path)
                self.assertEqual(run.returncode, 2)
                self.assertNotIn(directory, run.stdout + run.stderr)
            prior = Path(directory) / "previous.json"
            prior.write_text("null")
            run = self.run_cli(FIXTURE, "--previous", prior)
            self.assertEqual(run.returncode, 2)
            self.assertIn("PREVIOUS_INVALID", run.stdout)

    def test_cli_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "link.json"
            try:
                path.symlink_to(FIXTURE)
            except (OSError, NotImplementedError):
                self.skipTest("Environment cannot create symlinks")
            run = self.run_cli(path)
            self.assertEqual(run.returncode, 2)
            self.assertIn("INPUT_NOT_REGULAR_FILE", run.stdout)


if __name__ == "__main__":
    unittest.main()
