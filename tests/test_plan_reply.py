"""Offline tests of routing plans, not delivery, permission or agent acceptance."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("plan_reply", ROOT / "scripts/plan_reply.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.request = json.loads((ROOT / "examples/correspondence/reply-request.json").read_text())

    def plan(self):
        return module.plan_reply(self.request)

    def invalid(self):
        with self.assertRaises(module.InvalidInput):
            self.plan()

    def test_reply_all(self):
        result = self.plan()
        self.assertEqual(result["to_role"], "role:management")
        self.assertEqual(result["cc_roles"], ["role:governance", "role:portfolio-console"])

    def test_reply_only_keeps_console(self):
        self.request["reply_mode"] = "REPLY_ONLY"
        self.assertEqual(self.plan()["cc_roles"], ["role:portfolio-console"])

    def test_reply_only_keeps_mandatory_cc(self):
        self.request.update(reply_mode="REPLY_ONLY", mandatory_cc=["role:governance"])
        self.assertEqual(self.plan()["cc_roles"], ["role:governance", "role:portfolio-console"])

    def test_no_self_or_duplicate_cc(self):
        self.request["parent"]["cc_roles"] += ["role:governance", "project:atlas", "role:management"]
        self.assertEqual(self.plan()["cc_roles"], ["role:governance", "role:portfolio-console"])

    def test_cc_actor_not_action_owner(self):
        self.request["actor"] = "role:governance"
        self.invalid()

    def test_reference_is_not_canonical_parent(self):
        for kind in ["CC_REFERENCE", "SENT_REFERENCE"]:
            with self.subTest(kind=kind):
                self.request["parent"]["record_type"] = kind
                self.invalid()

    def test_one_body_and_reference_routes(self):
        result = self.plan()
        body, sent, *copies = result["records"]
        self.assertEqual(body["path"], "offices/management/inbox/synthetic-reply-002.md")
        self.assertEqual(sent["path"], "projects/atlas/outbox/synthetic-reply-002.md")
        for record in [sent, *copies]:
            self.assertEqual(record["canonical_body"], body["path"])
        for record in copies:
            self.assertFalse(record["ack_required"])
            self.assertFalse(record["cc_action_expected"])
        self.assertEqual(sum(r["record_type"] == "MESSAGE" for r in result["records"]), 1)

    def test_console_as_reply_recipient_not_copied(self):
        self.request["parent"]["from_role"] = "role:portfolio-console"
        self.assertEqual(self.plan()["cc_roles"], ["role:governance"])

    def test_console_as_reply_sender_not_copied(self):
        self.request["actor"] = self.request["parent"]["to_role"] = "role:portfolio-console"
        self.assertEqual(self.plan()["cc_roles"], ["role:governance"])

    def test_project_roles_trigger_console_without_metadata(self):
        self.request["parent"].pop("project_id")
        self.request["parent"]["cc_roles"] = []
        self.assertEqual(self.plan()["cc_roles"], ["role:portfolio-console"])

    def test_non_project_reply_no_automatic_console(self):
        self.request["actor"] = self.request["parent"]["to_role"] = "role:governance"
        self.request["parent"].update(cc_roles=[], project_id=None)
        self.assertEqual(self.plan()["cc_roles"], [])

    def test_missing_console_blocked(self):
        self.request["endpoints"].pop("role:portfolio-console")
        self.invalid()

    def test_unknown_cc_not_silently_dropped_by_reply_only(self):
        self.request["reply_mode"] = "REPLY_ONLY"
        self.request["endpoints"].pop("role:governance")
        self.invalid()

    def test_one_generation_only(self):
        first = self.plan()
        self.request.update(actor=first["to_role"], reply_id="synthetic-reply-003", reply_mode="REPLY_ONLY")
        self.request["parent"] = {"record_type": "MESSAGE", "message_id": first["reply_id"],
                                  "from_role": first["from_role"], "to_role": first["to_role"],
                                  "cc_roles": first["cc_roles"], "project_id": "atlas"}
        second = self.plan()
        self.request.update(actor=second["to_role"], reply_id="synthetic-reply-004", reply_mode="REPLY_ALL")
        self.request["parent"].update(message_id=second["reply_id"], from_role=second["from_role"],
                                      to_role=second["to_role"], cc_roles=second["cc_roles"])
        self.assertNotIn("role:governance", self.plan()["cc_roles"])

    def test_deterministic_and_no_input_mutation(self):
        before = copy.deepcopy(self.request)
        self.assertEqual(self.plan(), self.plan())
        self.assertEqual(self.request, before)
        self.assertFalse(self.plan()["execution_authorized"])
        self.assertFalse(self.plan()["delivery_performed"])

    def test_reject_unsafe_or_mismatched_endpoints(self):
        for path in ["../outside", "/tmp/inbox", "C:\\mail", "https://example.invalid/inbox",
                     "offices/../other", "offices/a/inbox", "offices/a\n", "projects/beacon", "offices/atlas"]:
            with self.subTest(path=path):
                self.request["endpoints"]["project:atlas"] = path
                self.invalid()

    def test_reject_alias_collision(self):
        self.request["endpoints"]["role:governance"] = "offices/management"
        self.invalid()

    def test_reject_new_unknown_fields_and_bad_types(self):
        for field, value in [("schema_version", True), ("schema_version", 2), ("reply_mode", "SEND"),
                             ("actor", []), ("mandatory_cc", None), ("reply_id", "../x"),
                             ("endpoints", []), ("parent", None), ("authority_override", True)]:
            with self.subTest(field=field):
                original = copy.deepcopy(self.request)
                self.request[field] = value
                self.invalid()
                self.request = original

    def test_no_overwrite_parent_id(self):
        self.request["reply_id"] = self.request["parent"]["message_id"]
        self.invalid()

    def test_self_reply_rejected(self):
        self.request["parent"]["from_role"] = "project:atlas"
        self.invalid()

    def cli(self, raw):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "request.json"
            path.write_bytes(raw)
            result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/plan_reply.py"), str(path)],
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(path.read_bytes(), raw)
            self.assertEqual(sorted(p.name for p in Path(folder).iterdir()), ["request.json"])
            return result, json.loads(result.stdout)

    def test_cli_success_no_writes(self):
        result, output = self.cli(json.dumps(self.request).encode())
        self.assertEqual(result.returncode, 0)
        self.assertEqual(output, self.plan())

    def test_cli_invalid_is_sanitized(self):
        for raw in [b"not-json-private-value", b'{"schema_version":1,"schema_version":1}',
                    b"[]", b"null", b"\xff", b" " * 65537, b"[" * 2000]:
            with self.subTest(length=len(raw)):
                result, output = self.cli(raw)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stderr, "")
                self.assertEqual(output["status"], "INVALID")
                self.assertNotIn("private-value", result.stdout)
                self.assertFalse(output["execution_authorized"])

    def test_cli_missing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "absent.json"
            result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/plan_reply.py"), str(path)],
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn(folder, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
