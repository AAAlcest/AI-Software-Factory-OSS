#!/usr/bin/env python3
"""Read-only instance preflight. Structural validity NEVER grants authority."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

MAX_BYTES = 262144
ACTIONS = {"DOCS_CHANGE", "TEMPLATE_CHANGE", "TEST", "REVIEW_REQUEST"}
GATES = {"LICENSE", "PUBLICATION", "PRODUCTION", "DESTRUCTIVE", "CREDENTIAL_CHANGE"}
UNKNOWN = {"", "UNKNOWN", "UNCONFIGURED", "NOT_EXPOSED"}


class Invalid(ValueError):
    """An invalid input with a stable, non-content-bearing diagnostic."""


def require(condition: bool, code: str) -> None:
    if not condition:
        raise Invalid(code)


def obj(value: Any, keys: set[str], name: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{name}: expected object")
    require(set(value) == keys, f"{name}: missing or unknown fields")
    return value


def text(value: Any, name: str) -> str:
    require(isinstance(value, str) and value == value.strip(), f"{name}: expected trimmed string")
    require(not any(ord(c) < 32 for c in value), f"{name}: control characters forbidden")
    return value


def strings(value: Any, name: str) -> list[str]:
    require(isinstance(value, list), f"{name}: expected array")
    for item in value:
        text(item, name)
        require(bool(item), f"{name}: empty item")
    require(len(value) == len(set(value)), f"{name}: duplicate item")
    return value


def local_file(root: Path, value: Any) -> Path:
    name = text(value, "path")
    parts = name.split("/")
    require(bool(name) and all(p not in {"", ".", ".."} and
            re.fullmatch(r"[A-Za-z0-9_.-]+", p) for p in parts), "path: unsafe relative path")
    path = root
    for part in parts:
        path = path / part
        require(not path.is_symlink(), "path: symlinks forbidden")
    require(path.is_file(), "path: missing regular file")
    require(path.resolve().is_relative_to(root), "path: outside instance root")
    require(0 < path.stat().st_size <= MAX_BYTES, "path: empty or oversized file")
    return path


def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        require(key not in result, "json: duplicate key")
        result[key] = value
    return result


def bad_constant(_: str) -> None:
    raise Invalid("json: non-finite number")


def load(root: Path, name: str) -> dict[str, Any]:
    path = local_file(root, name)
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    require(len(raw) <= MAX_BYTES, "path: empty or oversized file")
    data = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=bad_constant)
    require(isinstance(data, dict), "json: top level must be object")
    return data


def inspect(root: Path) -> dict[str, Any]:
    """Inspect explicitly selected local files without executing their contents.

    Inputs are declarations, not proof of appointment, freshness or permission.
    The caller must independently resolve actual authority and exact Git state.
    """
    result: dict[str, Any] = {
        "status": "INVALID", "execution_authorized": False,
        "checks": "STRUCTURE_AND_DECLARED_CONSISTENCY_ONLY",
        "diagnostics": [], "mode": "UNKNOWN",
    }
    try:
        root = root.resolve(strict=True)
        require(root.is_dir(), "root: expected directory")
        m = obj(load(root, "instance.json"), {
            "schema_version", "mode", "human_owner", "role", "project_id",
            "authority", "state", "current",
        }, "instance")
        require(type(m["schema_version"]) is int and m["schema_version"] == 1,
                "instance: unsupported schema version")
        mode = text(m["mode"], "mode")
        require(mode in {"TEMPLATE", "SYNTHETIC", "INSTANCE"}, "instance: unsupported mode")
        result["mode"] = mode
        owner = text(m["human_owner"], "human_owner")
        role = obj(m["role"], {"id", "incumbent_id", "display_title"}, "role")
        for field, value in role.items():
            text(value, f"role.{field}")
        project = text(m["project_id"], "project_id")
        local_file(root, m["current"])
        a = obj(load(root, m["authority"]), {
            "status", "role_id", "incumbent_id", "project_id", "decision_record", "grants", "gates",
        }, "authority")
        s = obj(load(root, m["state"]), {
            "role_id", "incumbent_id", "project_id", "phase", "blockers", "next_action",
            "continuity", "evidence",
        }, "state")
        blocked = []
        if mode == "TEMPLATE":
            blocked.append("template is not an appointed instance")
        for name, value in [("human_owner", owner), ("project_id", project),
                            ("role_id", role["id"]), ("incumbent_id", role["incumbent_id"])]:
            if value.upper() in UNKNOWN:
                blocked.append(f"{name} is unresolved")
        require(role["display_title"].upper() not in UNKNOWN, "role: missing display title")
        for record, label in [(a, "authority"), (s, "state")]:
            for field, expected in [("role_id", role["id"]),
                                    ("incumbent_id", role["incumbent_id"]), ("project_id", project)]:
                require(text(record[field], f"{label}.{field}") == expected,
                        f"{label}: identity mismatch")
        require(text(a["status"], "authority.status") in {"UNKNOWN", "ACTIVE", "REVOKED"},
                "authority: invalid status")
        if a["status"] != "ACTIVE":
            blocked.append("authority is not active")
        if text(a["decision_record"], "decision_record").upper() in UNKNOWN:
            blocked.append("decision record is unresolved")
        else:
            local_file(root, a["decision_record"])
        gates = obj(a["gates"], GATES, "gates")
        require(all(value == "HUMAN_REQUIRED" for value in gates.values()),
                "gates: this preflight cannot admit reserved actions")
        require(isinstance(a["grants"], list), "grants: expected array")
        grants = set()
        for grant in a["grants"]:
            grant = obj(grant, {"action", "scope"}, "grant")
            action, scope = text(grant["action"], "action"), text(grant["scope"], "scope")
            require(action in ACTIONS, "grant: unsupported or reserved action")
            require(scope == f"project:{project}", "grant: out-of-project scope")
            require((action, scope) not in grants, "grant: duplicate")
            grants.add((action, scope))
        phase = text(s["phase"], "phase")
        if phase.upper() in UNKNOWN:
            blocked.append("phase is unresolved")
        if strings(s["blockers"], "blockers"):
            blocked.append("state has unresolved blockers")
        nxt = obj(s["next_action"], {"action", "scope"}, "next_action")
        action, scope = text(nxt["action"], "action"), text(nxt["scope"], "scope")
        require(action in ACTIONS | GATES | {"UNKNOWN"}, "next_action: unsupported action")
        if action in GATES:
            blocked.append("next action requires a reserved Human gate")
        elif (action, scope) not in grants:
            blocked.append("next action has no exact declared grant")
        c = obj(s["continuity"], {"kind", "previous_incumbent_id", "handoff"}, "continuity")
        kind = text(c["kind"], "continuity.kind")
        require(kind in {"FIRST_APPOINTMENT", "RECOVERY", "SUCCESSION"}, "continuity: unsupported kind")
        if kind == "FIRST_APPOINTMENT":
            require(c["previous_incumbent_id"] is None and c["handoff"] is None,
                    "continuity: first appointment cannot have a predecessor")
        elif kind == "RECOVERY":
            require(c["previous_incumbent_id"] == role["incumbent_id"] and c["handoff"] is None,
                    "continuity: recovery must preserve incumbent without a succession handoff")
        else:
            previous = text(c["previous_incumbent_id"], "previous_incumbent_id")
            require(previous.upper() not in UNKNOWN and previous != role["incumbent_id"],
                    "continuity: succession requires a different known predecessor")
            local_file(root, c["handoff"])
        for evidence in strings(s["evidence"], "evidence"):
            local_file(root, evidence)
        result["status"] = "BLOCKED" if blocked else "VALID"
        result["diagnostics"] = blocked
        result["declared_role"] = role["id"]
        result["declared_project"] = project
    except (ValueError, UnicodeError, OSError, RuntimeError) as error:
        # Do not echo supplied file contents, host paths or OS error details.
        result["diagnostics"] = [str(error) if isinstance(error, Invalid) else
                                 "input: unreadable, malformed or inaccessible"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="explicit instance directory")
    args = parser.parse_args()
    result = inspect(args.root)
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2))
    return {"VALID": 0, "BLOCKED": 3, "INVALID": 2}[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
