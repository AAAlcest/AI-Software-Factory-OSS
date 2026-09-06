"""Static checks of synthetic records, NOT a fresh-agent acceptance test."""
import copy
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = ROOT / "examples" / "demo-factory" / "scenario"


def read(name):
    return json.loads((SCENARIO / name).read_text(encoding="utf-8"))


def pointer(ref, current="records.json"):
    name, _, fragment = ref.partition("#")
    value = read(name or current)
    for component in fragment.strip("/").split("/") if fragment else []:
        value = value[component.replace("~1", "/").replace("~0", "~")]
    return value


def target_chain_matches(change):
    """Pedagogical comparison, not authorization or evidence authentication."""
    target = change["candidate"]
    return (all(value == target for value in change["reviews"].values())
            and pointer(change["evidence_ref"])["target"] == target
            and change["integration_decision_target"] == target
            and change["integrated_target"] == target
            and change["post_integration_readback"] == target)


class ScenarioTests(unittest.TestCase):
    def setUp(self):
        self.factory = read("factory.json")
        self.records = read("records.json")
        self.atlas = read("projects/atlas.json")
        self.beacon = read("projects/beacon.json")
        self.console = read("console.json")

    def test_every_record_file_is_explicitly_synthetic(self):
        for path in SCENARIO.rglob("*.json"):
            self.assertEqual(json.loads(path.read_text())["classification"], "SYNTHETIC_ONLY")

    def test_first_assignment_matches_project_and_decision(self):
        assignment = self.factory["assignments"]["project:atlas"]
        decision = pointer(assignment["authority_ref"])
        self.assertEqual(assignment["incumbent"], self.atlas["incumbent"])
        self.assertEqual(assignment["incumbent"], decision["incumbent"])
        self.assertEqual(assignment["allowed_project"], decision["project"])
        self.assertEqual(assignment["allowed_hypothetical_actions"], decision["allowed_hypothetical_actions"])
        self.assertIsNone(assignment["predecessor"])
        self.assertEqual(self.atlas["handoffs"], [])
        self.assertFalse(self.factory["real_execution_authorized"])

    def test_beacon_missing_assignment_stays_blocked(self):
        self.assertNotIn(self.beacon["owner_role"], self.factory["assignments"])
        self.assertEqual(self.beacon["incumbent"], "UNKNOWN")
        self.assertEqual(self.beacon["phase"], "BLOCKED")

    def test_console_resolves_state_and_message_references(self):
        for ref in self.console["project_state_refs"] + self.console["visible_message_refs"]:
            self.assertIsInstance(pointer(ref), dict)
        for loop in self.console["open_loops"]:
            self.assertTrue(pointer(loop["source"]))
        self.assertFalse(self.console["execution_owner"])

    def test_project_change_and_task_references_resolve(self):
        for key in ("task_ref", "completed_change_ref", "current_change_ref", "work_ref"):
            self.assertIsInstance(pointer(self.atlas[key]), dict)
        self.assertEqual(pointer(self.atlas["current_change_ref"])["candidate"], self.atlas["current_candidate"])

    def test_completed_chain_and_current_state_readback_match(self):
        change = self.records["changes"]["completed"]
        self.assertTrue(target_chain_matches(change))
        self.assertEqual(self.atlas["canonical_baseline"], change["post_integration_readback"])

    def test_active_candidate_cannot_reuse_stale_review(self):
        self.assertFalse(target_chain_matches(self.records["changes"]["active"]))
        self.assertEqual(self.atlas["next_action"], "request-review")

    def test_candidate_movement_invalidates_matching_fixture_chain(self):
        change = copy.deepcopy(self.records["changes"]["completed"])
        change["candidate"] = "fixture:different-candidate"
        self.assertFalse(target_chain_matches(change))

    def test_each_body_has_one_sent_and_correct_cc_reference(self):
        for ident, body in self.records["messages"].items():
            refs = [r for r in self.records["references"].values()
                    if r["canonical_body"] == "#/messages/" + ident]
            sent = [r for r in refs if r["record_type"] == "SENT_REFERENCE"]
            copied = [r for r in refs if r["record_type"] == "CC_REFERENCE"]
            self.assertEqual(len(sent), 1)
            self.assertEqual(sent[0]["holder_role"], body["from_role"])
            self.assertEqual([r["holder_role"] for r in copied], body["cc_roles"])
            for ref in refs:
                self.assertNotIn("body", ref)
                self.assertIs(pointer(ref["canonical_body"]).__class__, dict)
            self.assertTrue(all(r["action_expected"] is False for r in copied))

    def test_reply_uses_immediate_parent_and_retains_console(self):
        reply = self.records["messages"]["result-atlas"]
        parent = pointer(reply["in_reply_to"])
        self.assertEqual(reply["from_role"], parent["to_role"])
        self.assertEqual(reply["to_role"], parent["from_role"])
        self.assertEqual(reply["cc_roles"], parent["cc_roles"])

    def test_work_receipt_does_not_mean_success_or_live_session(self):
        work = self.records["work"]["atlas-session"]
        self.assertEqual([e["state"] for e in work["events"]],
                         ["ACTIVE", "DONE_UNACKED", "COMPLETED_ACKED"])
        self.assertEqual(work["events"][-1]["actor"], work["origin_role"])
        self.assertEqual(work["result"], "BLOCKED")
        self.assertEqual(work["session_id"], "NOT_EXPOSED")
        for field in ("receipt_means_success", "liveness_verified", "evidence_verified"):
            self.assertFalse(work[field])

    def test_fictional_evidence_is_not_actual_execution(self):
        for evidence in self.records["evidence"].values():
            self.assertEqual(evidence["kind"], "FICTIONAL_RESULT")
            self.assertFalse(evidence["actual_execution"])
        self.assertEqual(self.factory["reserved_gates"]["publication"], "HUMAN_REQUIRED")

    def test_result_template_cannot_claim_acceptance(self):
        result = json.loads((ROOT / "templates/cold-takeover/result.json").read_text())
        self.assertEqual(result["status"], "NOT_RUN")
        self.assertIsNone(result["observed_behavior"])
        self.assertFalse(result["actual_fresh_agent_run"])
        self.assertFalse(result["independent_review_granted"])
        self.assertFalse(result["publication_authorized"])


if __name__ == "__main__":
    unittest.main()
