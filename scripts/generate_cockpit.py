#!/usr/bin/env python3
"""Generate a disposable Project cockpit from explicit repository-local Factory state."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ID_RE = re.compile(r"^(?:project|role|workstream):[a-z0-9][a-z0-9-]{0,79}$")
STATUSES = {"INBOX", "READY", "IN_PROGRESS", "WAITING", "REVIEW", "BLOCKED", "DONE"}
PRIORITIES = {"P0", "P1", "P2", "P3"}
RECOVERY_MODES = {"FIRST_APPOINTMENT", "SAME_INCUMBENT_RECOVERY", "TRUE_SUCCESSION"}
DERIVED = "> DERIVED COCKPIT SNAPSHOT — generated context only; repository records remain canonical.\n\n"


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
    require(target.exists() and target.is_file(), "missing file reference")
    return target


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs, parse_constant=bad_constant)
    except (OSError, UnicodeError, json.JSONDecodeError, Invalid, RecursionError) as exc:
        raise Invalid("invalid JSON") from exc


def digest(path: Path) -> dict:
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def unique_strings(value, name):
    require(isinstance(value, list), f"{name} must be a list")
    require(all(isinstance(item, str) and item for item in value), f"invalid {name}")
    require(len(value) == len(set(value)), f"duplicate {name}")
    return value


def parse_instance(root: Path) -> dict:
    root = root.resolve()
    require(root.exists() and root.is_dir(), "invalid root")
    project_reg = load_json(safe_file(root, "registers/projects.json"))
    role_reg = load_json(safe_file(root, "registers/roles.json"))
    workstream_reg = load_json(safe_file(root, "registers/workstreams.json"))

    projects = project_reg.get("projects")
    roles = role_reg.get("roles")
    workstreams = workstream_reg.get("workstreams")
    require(project_reg.get("synthetic_only") is True, "public fixture project register must be synthetic")
    require(role_reg.get("synthetic_only") is True, "public fixture role register must be synthetic")
    require(workstream_reg.get("synthetic_only") is True, "public fixture workstream register must be synthetic")
    require(isinstance(projects, list) and projects, "projects required")
    require(isinstance(roles, list) and roles, "roles required")
    require(isinstance(workstreams, list) and workstreams, "workstreams required")

    project_ids = set()
    for item in projects:
        require(isinstance(item, dict), "invalid project")
        ident = item.get("id")
        require(isinstance(ident, str) and ident.startswith("project:") and ID_RE.fullmatch(ident), "invalid project id")
        require(ident not in project_ids, "duplicate project id")
        project_ids.add(ident)

    role_ids = set()
    for item in roles:
        require(isinstance(item, dict), "invalid role")
        ident = item.get("id")
        require(isinstance(ident, str) and ident.startswith("role:") and ID_RE.fullmatch(ident), "invalid role id")
        require(ident not in role_ids, "duplicate role id")
        role_ids.add(ident)

    ws_ids = set()
    for item in workstreams:
        require(isinstance(item, dict), "invalid workstream")
        ident = item.get("id")
        require(isinstance(ident, str) and ident.startswith("workstream:") and ID_RE.fullmatch(ident), "invalid workstream id")
        require(ident not in ws_ids, "duplicate workstream id")
        ws_ids.add(ident)
        require(item.get("project_id") in project_ids, "unknown workstream project")
        require(item.get("owner_role") in role_ids, "unknown workstream owner")
        require(item.get("status") in STATUSES, "invalid workstream status")
        require(item.get("priority") in PRIORITIES, "invalid workstream priority")
        require(isinstance(item.get("surface"), str) and item["surface"], "workstream surface required")
        unique_strings(item.get("controlling_refs"), "controlling refs")
        unique_strings(item.get("superseded_refs"), "superseded refs")
        unique_strings(item.get("blockers"), "blockers")
        gate = item.get("human_gate")
        require(gate is None or (isinstance(gate, str) and gate), "invalid human gate")
        require(isinstance(item.get("next_action"), str) and item["next_action"], "next action required")
        require(not set(item["controlling_refs"]) & set(item["superseded_refs"]), "controlling ref cannot be superseded")

    sources = {
        "factory/FACTORY_STATE.md",
        "factory/OPEN_LOOPS.md",
        "registers/projects.json",
        "registers/roles.json",
        "registers/workstreams.json",
    }
    for item in projects:
        slug = item["id"].split(":", 1)[1]
        sources.update({f"projects/{slug}/README.md", f"projects/{slug}/STATE.md"})
    for item in roles:
        slug = item["id"].split(":", 1)[1]
        sources.update({f"offices/{slug}/README.md", f"offices/{slug}/desk/CURRENT.md"})
    source_paths = {ref: safe_file(root, ref) for ref in sorted(sources)}

    return {
        "root": root,
        "projects": projects,
        "roles": roles,
        "workstreams": workstreams,
        "source_paths": source_paths,
    }


def lines(values):
    return ", ".join(f"`{item}`" for item in values) if values else "none"


def generate(root: Path, output: Path, recovery_mode: str, selected_workstream: str | None = None) -> dict:
    require(recovery_mode in RECOVERY_MODES, "invalid recovery mode")
    instance = parse_instance(root)
    output = Path(output)
    require(not output.exists(), "output already exists")
    output.parent.mkdir(parents=True, exist_ok=True)

    projects = instance["projects"]
    roles = instance["roles"]
    workstreams = instance["workstreams"]
    by_ws = {item["id"]: item for item in workstreams}
    if selected_workstream is None:
        selected = next((item for item in workstreams if item["status"] != "DONE"), workstreams[0])
    else:
        require(selected_workstream in by_ws, "unknown selected workstream")
        selected = by_ws[selected_workstream]

    fingerprints = {ref: digest(path) for ref, path in instance["source_paths"].items()}
    source_bytes = sum(item["bytes"] for item in fingerprints.values())

    overview = "# Factory overview\n\n" + DERIVED
    overview += f"Projects: {len(projects)}  \nRoles: {len(roles)}  \nWorkstreams: {len(workstreams)}\n\n"
    gates = [item for item in workstreams if item.get("human_gate")]
    blocked = [item for item in workstreams if item["status"] == "BLOCKED" or item["blockers"]]
    overview += f"Human-gated lanes: {len(gates)}  \nBlocked/waiting lanes with blockers: {len(blocked)}\n\n"
    overview += "Use `WORKSTREAMS.md` as the current management index; refresh every controlling source before acting.\n"

    projects_md = "# Projects\n\n" + DERIVED
    for item in projects:
        owned = [w["id"] for w in workstreams if w["project_id"] == item["id"]]
        projects_md += f"## {item['id']}\n\nStatus: `{item.get('state', 'UNKNOWN')}`  \nPrimary: `{item.get('primary', 'UNKNOWN')}`  \nWorkstreams: {lines(owned)}\n\n"

    roles_md = "# Roles\n\n" + DERIVED
    for item in roles:
        owned = [w["id"] for w in workstreams if w["owner_role"] == item["id"]]
        roles_md += f"## {item['id']} — {item.get('title', 'Untitled role')}\n\nSurface: `{item.get('recommended_surface', 'UNKNOWN')}`  \nOwned workstreams: {lines(owned)}\n\n"

    workstreams_md = "# Workstreams\n\n" + DERIVED
    workstreams_md += "Controlling references are pointers to current accepted direction; superseded references remain history and must not be replayed as current authority.\n\n"
    for item in workstreams:
        workstreams_md += (
            f"## {item['id']}\n\n"
            f"Project: `{item['project_id']}`  \nOwner role: `{item['owner_role']}`  \n"
            f"Status / priority: `{item['status']}` / `{item['priority']}`  \n"
            f"Visible work surface: `{item['surface']}`  \n"
            f"Controlling refs: {lines(item['controlling_refs'])}  \n"
            f"Superseded refs: {lines(item['superseded_refs'])}  \n"
            f"Blockers: {lines(item['blockers'])}  \n"
            f"Human gate: `{item['human_gate'] or 'none'}`  \n"
            f"Next action: {item['next_action']}\n\n"
        )

    recovery_md = "# Recovery brief\n\n" + DERIVED
    recovery_md += (
        f"Recovery mode: `{recovery_mode}`\n\n"
        f"Selected workstream: `{selected['id']}`  \n"
        f"Project: `{selected['project_id']}`  \nOwner role: `{selected['owner_role']}`  \n"
        f"Visible work surface: `{selected['surface']}`  \n"
        f"Current controlling refs: {lines(selected['controlling_refs'])}  \n"
        f"Do not reopen as current: {lines(selected['superseded_refs'])}  \n"
        f"Blockers: {lines(selected['blockers'])}  \nHuman gate: `{selected['human_gate'] or 'none'}`  \n"
        f"Next safe action: {selected['next_action']}\n\n"
        "Before action, refresh the visible work surface and controlling references. This brief does not appoint an incumbent, approve a gate or prove receipt by another role.\n"
    )

    health_md = "# Factory health\n\n" + DERIVED
    findings = []
    for item in projects:
        if item.get("primary") in {None, "", "UNKNOWN"}:
            findings.append(f"- `{item['id']}` has no resolved primary.")
    for item in workstreams:
        if item["status"] == "BLOCKED" or item["blockers"]:
            findings.append(f"- `{item['id']}` blocked/waiting: {lines(item['blockers'])}.")
        if item.get("human_gate"):
            findings.append(f"- `{item['id']}` waits on Human gate `{item['human_gate']}`.")
        if not item["controlling_refs"]:
            findings.append(f"- `{item['id']}` has no controlling reference.")
    health_md += "\n".join(findings) if findings else "No structural health findings in the selected synthetic inputs."
    health_md += "\n"

    pslug = selected["project_id"].split(":", 1)[1]
    rslug = selected["owner_role"].split(":", 1)[1]
    bounded_sources = [
        f"projects/{pslug}/README.md",
        f"projects/{pslug}/STATE.md",
        f"offices/{rslug}/desk/CURRENT.md",
        "registers/workstreams.json",
    ]
    task_md = "# Bounded Codex task package\n\n" + DERIVED
    task_md += (
        f"Workstream: `{selected['id']}`  \nProject: `{selected['project_id']}`  \n"
        f"Work surface: `{selected['surface']}`\n\n"
        "## Start with\n\n" + "\n".join(f"- `{ref}`" for ref in bounded_sources) + "\n\n"
        "## Current direction\n\n"
        f"- controlling refs: {lines(selected['controlling_refs'])}\n"
        f"- superseded refs: {lines(selected['superseded_refs'])}\n"
        f"- blockers: {lines(selected['blockers'])}\n"
        f"- Human gate: `{selected['human_gate'] or 'none'}`\n"
        f"- expected next action: {selected['next_action']}\n\n"
        "Expand read scope only for a concrete dependency, conflict or missing fact discovered during implementation. Do not infer authority from this package.\n"
    )

    instructions = "# ChatGPT Project bootstrap\n\n" + DERIVED
    instructions += (
        "This directory is a portable bootstrap package, not an automatically installed ChatGPT Project.\n\n"
        "Read `RECOVERY_BRIEF.md`, then `WORKSTREAMS.md`, then refresh only the canonical sources needed for the selected action. "
        "If generated text conflicts with repository evidence, repository evidence wins and the bundle is stale.\n"
    )

    outputs = {
        "PROJECT_INSTRUCTIONS.md": instructions,
        "FACTORY_OVERVIEW.md": overview,
        "PROJECTS.md": projects_md,
        "ROLES.md": roles_md,
        "WORKSTREAMS.md": workstreams_md,
        "RECOVERY_BRIEF.md": recovery_md,
        "HEALTH.md": health_md,
        "CODEX_TASK_PACKAGE.md": task_md,
    }

    manifest = {
        "schema_version": 2,
        "derived": True,
        "canonical_truth": "repository",
        "execution_authorized": False,
        "recovery_mode": recovery_mode,
        "selected_workstream": selected["id"],
        "source_fingerprints": fingerprints,
        "outputs": sorted(outputs),
        "metrics": {
            "source_files_fingerprinted": len(fingerprints),
            "source_bytes_fingerprinted": source_bytes,
            "bounded_task_source_files": len(bounded_sources),
        },
    }

    output.mkdir()
    for name, text in outputs.items():
        (output / name).write_text(text, encoding="utf-8")
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_bytes = sum(path.stat().st_size for path in output.iterdir() if path.is_file())
    return {
        "status": "GENERATED",
        "output": str(output),
        "selected_workstream": selected["id"],
        "source_files_fingerprinted": len(fingerprints),
        "source_bytes_fingerprinted": source_bytes,
        "output_bytes": output_bytes,
        "execution_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--recovery-mode", default="SAME_INCUMBENT_RECOVERY", choices=sorted(RECOVERY_MODES))
    parser.add_argument("--workstream")
    args = parser.parse_args()
    try:
        result = generate(Path(args.root), Path(args.output), args.recovery_mode, args.workstream)
    except (Invalid, OSError, UnicodeError, ValueError, RecursionError):
        result = {"status": "INVALID", "execution_authorized": False}
        print(json.dumps(result, sort_keys=True, indent=2))
        return 2
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
