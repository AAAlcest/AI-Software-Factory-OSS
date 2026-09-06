"""Regression checks for the participant-visible CT-05 routing policy.

These are author/CI checks, not observations from a fresh Agent session.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from create_demo import build_files, create_demo
from plan_reply import plan_reply


# Actual fixture-manifest SHA-256 values generated from d9970658 before this
# revision. Unaffected participant inputs must not drift merely to fix CT-05.
UNCHANGED_MANIFESTS = {
    "first": "aae8ef27e2f915f9c7ec15326271089ed86f423576bf168426661b5911d3cc33",
    "missing": "fcc93254c37a3d56293743d298f0ce8815a238fbc44971a3d32adce7c15d08ac",
    "stale": "a48ec0786cd7c9259498f4bbee67d173c2b1779331f8cd37e3f1091c324a18f4",
    "recovery": "807e1a48a4e2565f3fe38454df66af57bbc6ac2458a9bcb2ea5c3f770f861592",
    "succession": "56a5e82aeece09aca51df18dfad6e3b8a3b723f2e47db7845461fc61ad1941e9",
    "changed-head": "7e3219f375e7ae13f89c249ed860031ab86b8e494dfc01f3ac0af1a8ff80b108",
    "human-gate": "f60c3c610ba7f975457df8a8c61584a396fe649f050c18aa3652203cbd712bab",
    "isolation": "09ab2e657c95a3254933766cda176a0bfb70b86e6aa8af7aa3413c4fbefc6591",
}
MANDATORY = ["role:governance", "role:portfolio-console"]


class RoutingDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.files = build_files("routing")
        self.request = json.loads(self.files["reply-request.json"])

    def test_both_mandatory_recipients_are_explicit_in_participant_input(self):
        self.assertCountEqual(self.request["mandatory_cc"], MANDATORY)
        self.assertEqual(self.request["console_role"], "role:portfolio-console")

    def test_task_and_entrypoint_link_a_package_local_policy(self):
        for source in ("TASK.md", "AI_ENTRYPOINT.md"):
            with self.subTest(source=source):
                self.assertIn("[routing policy](CORRESPONDENCE.md)", self.files[source])
                self.assertIn("reply-request.json", self.files[source])
        policy = self.files["CORRESPONDENCE.md"]
        for role in MANDATORY:
            self.assertIn(role, policy)
        self.assertIn("REPLY_ONLY", policy)
        self.assertIn("not inherited-only", policy)
        self.assertIn("No helper execution", policy)

    def test_both_modes_keep_one_body_and_visibility_only_references(self):
        for mode in ("REPLY_ALL", "REPLY_ONLY"):
            with self.subTest(mode=mode):
                request = deepcopy(self.request)
                request["reply_mode"] = mode
                plan = plan_reply(request)
                self.assertEqual(plan["to_role"], "role:management")
                self.assertEqual(plan["from_role"], "project:atlas")
                self.assertEqual(plan["cc_roles"], MANDATORY)
                self.assertFalse(plan["execution_authorized"])
                self.assertFalse(plan["delivery_performed"])
                records = plan["records"]
                self.assertEqual([r["record_type"] for r in records],
                                 ["MESSAGE", "SENT_REFERENCE", "CC_REFERENCE", "CC_REFERENCE"])
                body_path = records[0]["path"]
                for record in records[1:]:
                    self.assertEqual(record["canonical_body"], body_path)
                for record in records[2:]:
                    self.assertFalse(record["cc_action_expected"])
                    self.assertFalse(record["ack_required"])

    def test_reply_only_drops_optional_inheritance_not_mandatory_policy(self):
        request = deepcopy(self.request)
        request["parent"]["cc_roles"].append("role:observer")
        request["endpoints"]["role:observer"] = "offices/observer"
        self.assertIn("role:observer", plan_reply(request)["cc_roles"])
        request["reply_mode"] = "REPLY_ONLY"
        self.assertEqual(plan_reply(request)["cc_roles"], MANDATORY)

    def test_policy_is_hashed_in_the_actual_participant_package(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "routing"
            create_demo(root, "routing")
            manifest = json.loads((root / "fixture-manifest.json").read_text(encoding="utf-8"))
            self.assertIn("CORRESPONDENCE.md", manifest["files"])
            for name, digest in manifest["files"].items():
                self.assertEqual(hashlib.sha256((root / name).read_bytes()).hexdigest(), digest)
            self.assertFalse(manifest["execution_authorized"])
            self.assertEqual(manifest["fresh_agent_result"], "NOT_RUN")

    def test_other_eight_participant_packages_are_byte_identical(self):
        with tempfile.TemporaryDirectory() as temp:
            for case, expected in UNCHANGED_MANIFESTS.items():
                with self.subTest(case=case):
                    root = Path(temp) / case
                    create_demo(root, case)
                    actual = hashlib.sha256((root / "fixture-manifest.json").read_bytes()).hexdigest()
                    self.assertEqual(actual, expected)
                    self.assertFalse((root / "CORRESPONDENCE.md").exists())

    def test_routing_package_is_deterministic_without_input_side_effects(self):
        original = deepcopy(self.request)
        self.assertEqual(build_files("routing"), self.files)
        plan_reply(self.request)
        self.assertEqual(self.request, original)


if __name__ == "__main__":
    unittest.main()
