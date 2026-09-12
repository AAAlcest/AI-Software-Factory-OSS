#!/usr/bin/env python3
"""Execute bounded Factory skill adapters over a fresh generated cockpit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from check_cockpit_drift import check_drift
from generate_cockpit import Invalid, parse_instance

SKILLS = {
    "factory-overview",
    "project-overview",
    "role-overview",
    "project-recovery",
    "role-recovery",
    "handoff",
    "factory-health",
    "task-packaging",
}


def require(condition, message):
    if not condition:
        raise Invalid(message)


def read_bundle_file(bundle: Path, name: str) -> str:
    path = (bundle / name).resolve()
    require(path.is_relative_to(bundle.resolve()), "unsafe bundle path")
    require(path.exists() and path.is_file() and not path.is_symlink(), "missing bundle output")
    return path.read_text(encoding="utf-8")


def base_result(skill: str, scope: str, sources: list[str]) -> dict:
    return {
        "status": "OK",
        "skill": skill,
        "scope": scope,
        "derived": True,
        "canonical_truth": "repository",
        "execution_authorized": False,
        "sources": sources,
    }


def run_skill(root: Path, bundle: Path, skill: str, project: str | None = None,
              role: str | None = None, workstream: str | None = None) -> dict:
    require(skill in SKILLS, "unknown skill")
    root = Path(root).resolve()
    bundle = Path(bundle).resolve()
    drift = check_drift(root, bundle)
    if drift["status"] != "FRESH":
        return {
            "status": "BLOCKED_STALE_BUNDLE" if drift["status"] == "DRIFTED" else "INVALID",
            "skill": skill,
            "derived": True,
            "execution_authorized": False,
            "drift": drift,
        }

    instance = parse_instance(root)
    projects = {item["id"]: item for item in instance["projects"]}
    roles = {item["id"]: item for item in instance["roles"]}
    workstreams = {item["id"]: item for item in instance["workstreams"]}
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))

    if skill == "factory-overview":
        result = base_result(skill, "factory", ["factory/FACTORY_STATE.md", "factory/OPEN_LOOPS.md", "registers/projects.json", "registers/roles.json", "registers/workstreams.json"])
        result["content"] = read_bundle_file(bundle, "FACTORY_OVERVIEW.md")
        return result

    if skill == "factory-health":
        result = base_result(skill, "factory", ["registers/projects.json", "registers/roles.json", "registers/workstreams.json", "registers/continuity.json"])
        result["content"] = read_bundle_file(bundle, "HEALTH.md")
        return result

    if skill == "project-overview":
        require(project in projects, "unknown project")
        item = projects[project]
        related = [w for w in instance["workstreams"] if w["project_id"] == project]
        slug = project.split(":", 1)[1]
        result = base_result(skill, project, [f"projects/{slug}/README.md", f"projects/{slug}/STATE.md", "registers/workstreams.json"])
        result["facts"] = {"project": item, "workstreams": related}
        return result

    if skill == "role-overview":
        require(role in roles, "unknown role")
        item = roles[role]
        related = [w for w in instance["workstreams"] if w["owner_role"] == role]
        slug = role.split(":", 1)[1]
        result = base_result(skill, role, [f"offices/{slug}/README.md", f"offices/{slug}/desk/CURRENT.md", "registers/workstreams.json"])
        result["facts"] = {"role": item, "workstreams": related}
        return result

    require(workstream in workstreams, "unknown workstream")
    lane = workstreams[workstream]
    continuity = instance["continuity_by_pair"][(lane["project_id"], lane["owner_role"])]

    if skill == "project-recovery":
        if project is not None:
            require(project == lane["project_id"], "workstream/project mismatch")
        pslug = lane["project_id"].split(":", 1)[1]
        result = base_result(skill, lane["project_id"], [f"projects/{pslug}/README.md", f"projects/{pslug}/STATE.md", "registers/workstreams.json", "registers/continuity.json"])
        result["facts"] = {"workstream": lane, "continuity": continuity}
        return result

    if skill == "role-recovery":
        if role is not None:
            require(role == lane["owner_role"], "workstream/role mismatch")
        rslug = lane["owner_role"].split(":", 1)[1]
        result = base_result(skill, lane["owner_role"], [f"offices/{rslug}/README.md", f"offices/{rslug}/desk/CURRENT.md", "registers/workstreams.json", "registers/continuity.json"])
        result["facts"] = {"workstream": lane, "continuity": continuity}
        return result

    if skill == "handoff":
        result = base_result(skill, workstream, ["registers/workstreams.json", "registers/continuity.json"])
        result["classification"] = continuity["mode"]
        result["facts"] = {"workstream": lane, "continuity": continuity}
        return result

    if skill == "task-packaging":
        if manifest.get("selected_workstream") != workstream:
            return {
                "status": "REGENERATE_REQUIRED",
                "skill": skill,
                "requested_workstream": workstream,
                "bundle_workstream": manifest.get("selected_workstream"),
                "derived": True,
                "execution_authorized": False,
            }
        result = base_result(skill, workstream, ["registers/workstreams.json", "registers/continuity.json"])
        result["content"] = read_bundle_file(bundle, "CODEX_TASK_PACKAGE.md")
        return result

    raise Invalid("unsupported skill")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--bundle", required=True)
    parser.add_argument("--skill", required=True, choices=sorted(SKILLS))
    parser.add_argument("--project")
    parser.add_argument("--role")
    parser.add_argument("--workstream")
    args = parser.parse_args()
    try:
        result = run_skill(Path(args.root), Path(args.bundle), args.skill, args.project, args.role, args.workstream)
    except (Invalid, OSError, UnicodeError, ValueError, json.JSONDecodeError, RecursionError):
        result = {"status": "INVALID", "skill": args.skill, "derived": True, "execution_authorized": False}
    print(json.dumps(result, sort_keys=True, indent=2))
    if result["status"] == "OK":
        return 0
    if result["status"] in {"BLOCKED_STALE_BUNDLE", "REGENERATE_REQUIRED"}:
        return 3
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
