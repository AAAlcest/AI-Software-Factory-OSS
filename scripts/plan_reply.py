#!/usr/bin/env python3
"""Plan one reply's routing; never deliver mail or grant execution authority."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SLUG = re.compile(r"[a-z0-9][a-z0-9-]{0,79}\Z")
ROLE = re.compile(r"(?:role|project):[a-z0-9][a-z0-9-]{0,79}\Z")
ROOT = re.compile(r"(?:offices|projects)/[a-z0-9][a-z0-9-]{0,79}\Z")
MAX_BYTES = 65536


class InvalidInput(ValueError):
    """Invalid or unsupported routing declaration; message contains no input values."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise InvalidInput(message)


def identifier(value: object, pattern: re.Pattern[str]) -> bool:
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def object_keys(value: object, required: set[str], optional: set[str]) -> dict:
    require(isinstance(value, dict), "expected an object")
    require(required <= value.keys() <= required | optional, "missing or unsupported fields")
    return value


def role_list(value: object) -> list[str]:
    require(isinstance(value, list) and len(value) <= 64, "expected a bounded role list")
    require(all(identifier(role, ROLE) for role in value), "invalid role identifier")
    return value


def plan_reply(request: dict) -> dict:
    """Pure, deterministic plan from caller-verified parent/registry/policy inputs.

    References are constructed, not read or written. Declarations are not proof
    of authority, privacy permission, delivery, uniqueness or current Git state.
    """
    object_keys(request, {"schema_version", "actor", "reply_id", "parent", "endpoints"},
                {"reply_mode", "mandatory_cc", "console_role"})
    require(type(request["schema_version"]) is int and request["schema_version"] == 1,
            "unsupported schema version")
    actor, reply_id = request["actor"], request["reply_id"]
    require(identifier(actor, ROLE), "invalid actor")
    require(identifier(reply_id, SLUG), "invalid reply identifier")
    mode = request.get("reply_mode", "REPLY_ALL")
    require(mode in ("REPLY_ALL", "REPLY_ONLY"), "unsupported reply mode")
    parent = object_keys(request["parent"],
                         {"record_type", "message_id", "from_role", "to_role", "cc_roles"},
                         {"project_id"})
    require(parent["record_type"] == "MESSAGE", "parent must be the canonical message")
    require(identifier(parent["message_id"], SLUG), "invalid parent identifier")
    require(reply_id != parent["message_id"], "reply must use a new identifier")
    sender, recipient = parent["from_role"], parent["to_role"]
    require(identifier(sender, ROLE) and identifier(recipient, ROLE), "invalid parent roles")
    require(actor == recipient, "actor must be the primary recipient; CC is not ownership")
    require(sender != actor, "self-reply is unsupported")
    inherited = role_list(parent["cc_roles"])
    mandatory = role_list(request.get("mandatory_cc", []))
    project = parent.get("project_id")
    require(project is None or identifier(project, SLUG), "invalid project identifier")
    console = request.get("console_role", "role:portfolio-console")
    require(identifier(console, ROLE) and console.startswith("role:"), "invalid console role")
    endpoints = request["endpoints"]
    require(isinstance(endpoints, dict) and 1 <= len(endpoints) <= 128,
            "expected a bounded endpoint registry")
    for role, root in endpoints.items():
        require(identifier(role, ROLE) and identifier(root, ROOT), "invalid endpoint")
        expected = "projects/" + role.split(":", 1)[1] if role.startswith("project:") else "offices/"
        require(root == expected if role.startswith("project:") else root.startswith(expected),
                "endpoint kind or project mismatch")
    require(len(set(endpoints.values())) == len(endpoints), "endpoint aliases are unsupported")
    # Validate the complete immediate parent even if REPLY_ONLY drops a CC.
    involved = {actor, sender, recipient, *inherited, *mandatory}
    require(involved <= endpoints.keys(), "unresolved role in endpoint registry")
    copied = set(inherited if mode == "REPLY_ALL" else []) | set(mandatory)
    project_scoped = project is not None or any(role.startswith("project:") for role in involved)
    if project_scoped:
        require(console in endpoints, "project routing requires a configured console endpoint")
        copied.add(console)
    copied -= {actor, sender}  # Console direct sender/recipient needs no self-CC.
    cc_roles = sorted(copied)
    canonical = f"{endpoints[sender]}/inbox/{reply_id}.md"
    records = [
        {"record_type": "MESSAGE", "path": canonical, "to_role": sender},
        {"record_type": "SENT_REFERENCE", "path": f"{endpoints[actor]}/outbox/{reply_id}.md",
         "canonical_body": canonical},
    ]
    for role in cc_roles:
        records.append({"record_type": "CC_REFERENCE",
                        "path": f"{endpoints[role]}/inbox/{reply_id}-CC_REFERENCE.md",
                        "canonical_body": canonical, "cc_role": role,
                        "cc_action_expected": False, "ack_required": False})
    return {"status": "PLANNED", "execution_authorized": False, "delivery_performed": False,
            "schema_version": 1, "from_role": actor, "to_role": sender, "cc_roles": cc_roles,
            "reply_id": reply_id, "in_reply_to": parent["message_id"], "project_id": project,
            "reply_mode": mode, "records": records}


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path, help="local JSON routing request; no mail body needed")
    args = parser.parse_args()
    try:
        require(args.request.is_file(), "request must be a regular file")
        with args.request.open("rb") as stream:
            raw = stream.read(MAX_BYTES + 1)
        require(len(raw) <= MAX_BYTES, "request exceeds size limit")
        request = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object)
        result = plan_reply(request)
    except (OSError, UnicodeError, ValueError, RecursionError):
        # Do not echo input bodies, filesystem paths or parser excerpts.
        print(json.dumps({"status": "INVALID", "execution_authorized": False,
                          "delivery_performed": False, "error": "INVALID_ROUTING_REQUEST"}))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
