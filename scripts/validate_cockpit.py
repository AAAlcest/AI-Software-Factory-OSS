#!/usr/bin/env python3
"""Validate a derived ChatGPT Project cockpit bundle without granting authority."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

MAX_MANIFEST_BYTES = 256_000
RECOVERY_MODES = {"FIRST_APPOINTMENT", "SAME_INCUMBENT_RECOVERY", "TRUE_SUCCESSION"}
REQUIRED_OUTPUTS = {
    "project-cockpit/FACTORY_OVERVIEW.md",
    "project-cockpit/PROJECTS.md",
    "project-cockpit/ROLES.md",
    "project-cockpit/RECOVERY_BRIEF.md",
    "project-cockpit/HEALTH.md",
    "project-cockpit/CODEX_TASK_PACKAGE.md",
}
ID_RE = re.compile(r"^(?:project|role):[a-z0-9][a-z0-9-]{0,79}$")


class Invalid(ValueError):
    pass


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise Invalid("duplicate JSON key")
        result[key] = value
    return result


def bad_constant(value):
    raise Invalid("non-finite JSON constant")


def require(condition, message):
    if not condition:
        raise Invalid(message)


def safe_file(root: Path, value: object) -> Path:
    require(isinstance(value, str) and value and len(value) <= 240, "invalid file reference")
    require("\\" not in value and "://" not in value, "invalid file reference")
    path = Path(value)
    require(not path.is_absolute() and ".." not in path.parts and "." not in path.parts, "unsafe file reference")
    candidate = root / path
    require(not candidate.is_symlink(), "unsafe file reference")
    target = candidate.resolve()
    require(target.is_relative_to(root), "outside-root file reference")
    require(target.exists() and target.is_file(), "missing or unsafe file reference")
    return target


def load_manifest(root: Path) -> dict:
    path = root / "project-cockpit" / "manifest.json"
    require(path.exists() and path.is_file() and not path.is_symlink(), "missing manifest")
    require(path.stat().st_size <= MAX_MANIFEST_BYTES, "manifest too large")
    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs, parse_constant=bad_constant)
    except (OSError, UnicodeError, json.JSONDecodeError, Invalid, RecursionError) as exc:
        raise Invalid("invalid manifest") from exc
    require(isinstance(data, dict), "manifest must be an object")
    return data


def validate_bundle(root: Path) -> dict:
    try:
        root = Path(root).resolve()
        require(root.exists() and root.is_dir(), "invalid root")
        data = load_manifest(root)
        require(data.get("schema_version") == 1, "unsupported schema version")
        require(data.get("derived") is True, "cockpit must be marked derived")
        require(data.get("canonical_truth") == "repository", "repository must remain canonical truth")
        require(data.get("execution_authorized") is False, "cockpit cannot authorize execution")
        require(data.get("recovery_mode") in RECOVERY_MODES, "invalid recovery mode")

        sources = data.get("source_refs")
        require(isinstance(sources, list) and sources, "source_refs required")
        for ref in sources:
            safe_file(root, ref)

        seen = set()
        projects = data.get("projects")
        require(isinstance(projects, list) and projects, "projects required")
        for item in projects:
            require(isinstance(item, dict), "invalid project entry")
            ident = item.get("id")
            require(isinstance(ident, str) and ident.startswith("project:") and ID_RE.fullmatch(ident), "invalid project id")
            require(ident not in seen, "duplicate id")
            seen.add(ident)
            safe_file(root, item.get("room_ref"))
            safe_file(root, item.get("state_ref"))

        roles = data.get("roles")
        require(isinstance(roles, list) and roles, "roles required")
        for item in roles:
            require(isinstance(item, dict), "invalid role entry")
            ident = item.get("id")
            require(isinstance(ident, str) and ident.startswith("role:") and ID_RE.fullmatch(ident), "invalid role id")
            require(ident not in seen, "duplicate id")
            seen.add(ident)
            safe_file(root, item.get("office_ref"))
            safe_file(root, item.get("current_ref"))

        outputs = data.get("outputs")
        require(isinstance(outputs, list), "outputs required")
        require(REQUIRED_OUTPUTS.issubset(set(outputs)), "required cockpit output missing")
        for ref in outputs:
            path = safe_file(root, ref)
            text = path.read_text(encoding="utf-8")
            require("DERIVED COCKPIT SNAPSHOT" in text[:600], "output missing derived marker")

        return {
            "status": "VALID",
            "scope": "DERIVED_COCKPIT_STRUCTURE_ONLY",
            "projects": len(projects),
            "roles": len(roles),
            "outputs": len(outputs),
            "recovery_mode": data["recovery_mode"],
            "execution_authorized": False,
            "repository_truth_overridden": False,
            "fresh_agent_validated": False,
            "independent_privacy_approved": False,
        }
    except (OSError, UnicodeError, Invalid, ValueError, RecursionError):
        return {
            "status": "INVALID",
            "scope": "DERIVED_COCKPIT_STRUCTURE_ONLY",
            "execution_authorized": False,
            "repository_truth_overridden": False,
            "fresh_agent_validated": False,
            "independent_privacy_approved": False,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    result = validate_bundle(Path(args.root))
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["status"] == "VALID" else 2


if __name__ == "__main__":
    raise SystemExit(main())
