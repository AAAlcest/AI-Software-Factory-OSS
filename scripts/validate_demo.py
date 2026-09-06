#!/usr/bin/env python3
"""Check a generated synthetic Factory across the three V1 helper contracts."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

from create_demo import CASES
from plan_reply import plan_reply
from validate_instance import inspect as inspect_instance, local_file, pairs, bad_constant
from validate_work_history import validate_record


def check_demo(root: Path) -> dict:
    result = {"status": "INVALID", "execution_authorized": False,
              "fresh_agent_validated": False, "independent_privacy_approved": False}
    try:
        root = Path(root).resolve(strict=True)
        def require(condition: bool) -> None:
            if not condition:
                raise ValueError("INCONSISTENT_SYNTHETIC_BUNDLE")
        def read(name: str) -> str:
            return local_file(root, name).read_text(encoding="utf-8")
        def load(name: str) -> dict:
            data = json.loads(read(name), object_pairs_hook=pairs, parse_constant=bad_constant)
            require(isinstance(data, dict))
            return data
        def meta(name: str) -> dict:
            match = re.search(r"```json\n(.*?)\n```", read(name), flags=re.S)
            require(match is not None)
            data = json.loads(match.group(1), object_pairs_hook=pairs, parse_constant=bad_constant)
            require(isinstance(data, dict))
            return data
        manifest = load("fixture-manifest.json")
        require(manifest["classification"] == "SYNTHETIC_ONLY")
        case = manifest["case"]
        require(case in CASES and manifest["fresh_agent_result"] == "NOT_RUN")
        require(manifest["execution_authorized"] is False)
        require(isinstance(manifest["files"], dict) and 1 <= len(manifest["files"]) <= 128)
        for name, digest in manifest["files"].items():
            require(hashlib.sha256(local_file(root, name).read_bytes()).hexdigest() == digest)
        actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
        require(actual == set(manifest["files"]) | {"fixture-manifest.json"})
        factory = load("factory.json")
        require(factory["classification"] == "SYNTHETIC_ONLY")
        require(factory["mode"] == "READ_ONLY_EXERCISE" and factory["real_execution_authorized"] is False)
        expected_selected = "beacon" if case == "missing" else "atlas"
        require(factory["selected_project"] == expected_selected)
        require(factory["selected_root"] == "projects/" + expected_selected)
        observed = {name: inspect_instance(root / "projects" / name) for name in ("atlas", "beacon")}
        require(observed["beacon"]["status"] == "BLOCKED")
        require(observed["atlas"]["status"] == ("BLOCKED" if case == "human-gate" else "VALID"))
        require(all(item["execution_authorized"] is False for item in observed.values()))
        state = load("projects/atlas/state.json")
        continuity = state["continuity"]
        expected_kind = {"recovery": "RECOVERY", "succession": "SUCCESSION"}.get(case, "FIRST_APPOINTMENT")
        require(continuity["kind"] == expected_kind)
        candidate = load("projects/atlas/evidence/candidate.json")
        require(candidate["current_head"] != candidate["reviewed_head"])
        require(candidate["integration_authorized"] is False and candidate["real_evidence"] is False)
        require(set(candidate["completed_history"].values()) == {candidate["reviewed_head"]})
        request = load("reply-request.json")
        require(request["parent"] == meta("projects/atlas/inbox/task-atlas-v1.md"))
        plan = plan_reply(request)
        require(not plan["execution_authorized"] and not plan["delivery_performed"])
        for expected in plan["records"]:
            found = meta(expected["path"])
            require(all(found.get(key) == value for key, value in expected.items() if key != "path"))
            if expected["record_type"] == "MESSAGE":
                require(found["from_role"] == plan["from_role"] and found["cc_roles"] == plan["cc_roles"])
                require(found["in_reply_to"] == request["parent"]["message_id"])
        bodies = {}
        for name in manifest["files"]:
            if name.endswith(".md") and "```json\n" in read(name):
                record = meta(name)
                if record["record_type"] == "MESSAGE":
                    require(record["message_id"] not in bodies)
                    bodies[record["message_id"]] = name
                else:
                    target = meta(record["canonical_body"])
                    require(target["record_type"] == "MESSAGE")
                    if record["record_type"] == "CC_REFERENCE":
                        require(record["cc_action_expected"] is False and record["ack_required"] is False)
        require(set(bodies) == {"task-atlas-v1", "result-atlas-v1"})
        console = load("console/portfolio.json")
        require(console["auto_dispatch"] is False)
        require({item["id"] for item in console["projects"]} == {"atlas", "beacon"})
        for item in console["projects"]:
            require(load(item["state_ref"])["project_id"] == item["id"])
        work = load("offices/management/wardrobe/atlas.json")
        checked = validate_record(work)
        require(checked["status"] == "VALID" and checked["recorded_state"] == "COMPLETED_ACKED")
        require(work["incumbent_id"] == state["incumbent_id"])
        require(all(checked[key] is False for key in ("execution_authorized", "liveness_verified", "evidence_verified", "independent_review_granted")))
        result.update(status="VALID", case=case, checks="STATIC_AND_HELPER_INTEGRATION_ONLY",
                      atlas=observed["atlas"]["status"], beacon=observed["beacon"]["status"],
                      correspondence_records=len(plan["records"]), work_state=checked["recorded_state"])
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, RuntimeError, AttributeError):
        result["error"] = "INVALID_OR_INCONSISTENT_SYNTHETIC_BUNDLE"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    result = check_demo(parser.parse_args().root)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "VALID" else 2


if __name__ == "__main__":
    raise SystemExit(main())
