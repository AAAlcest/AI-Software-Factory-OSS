#!/usr/bin/env python3
"""Read-only, declaration-only Work Invocation History consistency checks."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Any

MAX_BYTES = 65536
UNKNOWN = {"UNKNOWN", "NOT_EXPOSED", "UNCONFIGURED"}
STATES = ["ACTIVE", "DONE_UNACKED", "COMPLETED_ACKED"]
CORE = {"schema_version", "record_kind", "work_id", "project_id", "origin_role",
        "incumbent_id", "task_ref", "authority_ref", "session"}
SESSION = {"entry", "session_id", "title", "cwd"}
EVENT = {"state", "at", "by_role", "evidence_ref"}
STAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)")


class Invalid(ValueError):
    """A stable diagnostic code, never untrusted input or a filesystem path."""


def require(condition: bool, code: str) -> None:
    if not condition:
        raise Invalid(code)


def text(value: Any) -> str:
    require(isinstance(value, str) and 0 < len(value) <= 512, "TEXT_INVALID")
    require(value == value.strip() and all(ord(c) >= 32 and ord(c) != 127 for c in value),
            "TEXT_INVALID")
    return value


def keys(value: Any, expected: set[str]) -> None:
    require(isinstance(value, dict) and set(value) == expected, "FIELDS_INVALID")


def inspect_record(record: Any) -> list[str]:
    keys(record, CORE | {"events"})
    require(type(record["schema_version"]) is int and record["schema_version"] == 1,
            "VERSION_INVALID")
    kind = text(record["record_kind"])
    require(kind in {"TEMPLATE", "SYNTHETIC", "OPERATIONAL"}, "KIND_INVALID")
    blocked = ["TEMPLATE_NOT_CONFIGURED"] if kind == "TEMPLATE" else []
    for field in sorted(CORE - {"schema_version", "record_kind", "session"}):
        if text(record[field]) in UNKNOWN:
            blocked.append("CORE_UNRESOLVED")
    session = record["session"]
    keys(session, SESSION)
    for value in session.values():
        text(value)
    require(session["entry"] in {"CREATED", "REUSED", "RESUMED", "REQUESTED_NOT_ENTERED", "UNKNOWN"},
            "ENTRY_INVALID")
    events = record["events"]
    require(isinstance(events, list) and len(events) <= len(STATES), "EVENTS_INVALID")
    if session["entry"] in {"REQUESTED_NOT_ENTERED", "UNKNOWN"}:
        require(not events, "UNENTERED_HAS_EVENTS")
        blocked.append("SESSION_NOT_ENTERED")
    elif not events:
        blocked.append("START_NOT_RECORDED")
    previous_time = None
    for index, event in enumerate(events):
        keys(event, EVENT)
        for value in event.values():
            text(value)
        require(event["state"] == STATES[index], "TRANSITION_INVALID")
        if event["by_role"] in UNKNOWN:
            blocked.append("ACTOR_UNRESOLVED")
        if event["evidence_ref"] in UNKNOWN:
            blocked.append("EVIDENCE_UNRESOLVED")
        if event["at"] in UNKNOWN:
            blocked.append("TIME_UNRESOLVED")
        else:
            require(STAMP.fullmatch(event["at"]) is not None, "TIME_INVALID")
            try:
                current_time = datetime.fromisoformat(event["at"].replace("Z", "+00:00"))
            except ValueError as exc:
                raise Invalid("TIME_INVALID") from exc
            require(previous_time is None or current_time >= previous_time, "TIME_REVERSED")
            previous_time = current_time
        if event["state"] == "COMPLETED_ACKED":
            require(event["by_role"] == record["origin_role"], "ACK_ROLE_MISMATCH")
    return sorted(set(blocked))


def validate_record(record: Any, previous: Any = None) -> dict[str, Any]:
    """Validate declared history; optionally compare a caller-supplied prior snapshot."""
    result: dict[str, Any] = {"status": "INVALID", "codes": [],
        "execution_authorized": False, "liveness_verified": False,
        "evidence_verified": False, "independent_review_granted": False}
    try:
        blocked = inspect_record(record)
        if previous is not None:
            require(not inspect_record(previous), "PREVIOUS_NOT_VALID")
            require(all(record[k] == previous[k] for k in CORE), "IDENTITY_OR_CONTEXT_CHANGED")
            count = len(previous["events"])
            require(record["events"][:count] == previous["events"], "HISTORY_REWRITTEN")
        result.update(status="BLOCKED" if blocked else "VALID", codes=blocked,
                      recorded_state=record["events"][-1]["state"] if record["events"] else "NOT_STARTED")
    except Invalid as exc:
        result["codes"] = [str(exc)]
    return result


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "JSON_DUPLICATE_KEY")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise Invalid("JSON_NONFINITE")


def load_record(path: Path) -> Any:
    require(path.is_file() and not path.is_symlink(), "INPUT_NOT_REGULAR_FILE")
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    require(len(raw) <= MAX_BYTES, "INPUT_TOO_LARGE")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--previous", type=Path, help="optional previously verified snapshot")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
        previous = load_record(args.previous) if args.previous is not None else None
        if args.previous is not None:
            require(isinstance(previous, dict), "PREVIOUS_INVALID")
        result = validate_record(record, previous)
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        result = validate_record(None)
        result["codes"] = [str(exc) if isinstance(exc, Invalid) else "INPUT_UNREADABLE_OR_INVALID_JSON"]
    print(json.dumps(result, sort_keys=True))
    return {"VALID": 0, "INVALID": 2, "BLOCKED": 3}[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
