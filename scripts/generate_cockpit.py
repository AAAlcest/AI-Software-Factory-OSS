#!/usr/bin/env python3
"""Generate a disposable Project cockpit from explicit repository-local Factory state."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ID_RE = re.compile(r"^(?:project|role|workstream|workitem):[a-z0-9][a-z0-9-]{0,79}$")
WORK_TYPE_RE = re.compile(r"^[A-Z][A-Z0-9_]{0,63}$")
STATUSES = {"INBOX", "READY", "IN_PROGRESS", "WAITING", "REVIEW", "BLOCKED", "DONE"}
PRIORITIES = {"P0", "P1", "P2", "P3"}
PROJECTION_STATES = {"ACTIVE", "ARCHIVED"}
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


def validate_continuity(item: dict, project_ids: set[str], role_ids: set[str]) -> tuple[str, str]:
    require(isinstance(item, dict), "invalid continuity entry")
    project_id = item.get("project_id")
    role_id = item.get("role_id")
    require(project_id in project_ids, "unknown continuity project")
    require(role_id in role_ids, "unknown continuity role")
    mode = item.get("mode")
    require(mode in RECOVERY_MODES, "invalid continuity mode")
    incumbent = item.get("incumbent")
    previous = item.get("previous_incumbent")
    handoff = item.get("handoff_ref")
    require(isinstance(incumbent, str) and incumbent, "continuity incumbent required")
    if mode == "FIRST_APPOINTMENT":
        require(previous is None and handoff is None, "first appointment cannot invent predecessor handoff")
    elif mode == "SAME_INCUMBENT_RECOVERY":
        require(previous == incumbent and handoff is None, "recovery must preserve incumbent without succession handoff")
    else:
        require(isinstance(previous, str) and previous and previous != incumbent, "succession requires distinct predecessor")
        require(isinstance(handoff, str) and handoff, "succession handoff reference required")
    return project_id, role_id


def parse_instance(root: Path) -> dict:
    root = root.resolve()
    require(root.exists() and root.is_dir(), "invalid root")
    project_reg = load_json(safe_file(root, "registers/projects.json"))
    role_reg = load_json(safe_file(root, "registers/roles.json"))
    workstream_reg = load_json(safe_file(root, "registers/workstreams.json"))
    continuity_reg = load_json(safe_file(root, "registers/continuity.json"))
    work_item_reg = load_json(safe_file(root, "registers/work_items.json"))

    projects = project_reg.get("projects")
    roles = role_reg.get("roles")
    workstreams = workstream_reg.get("workstreams")
    continuity = continuity_reg.get("contexts")
    work_items = work_item_reg.get("work_items")
    for register, label in (
        (project_reg, "project"),
        (role_reg, "role"),
        (workstream_reg, "workstream"),
        (continuity_reg, "continuity"),
        (work_item_reg, "work-item"),
    ):
        require(register.get("synthetic_only") is True, f"public fixture {label} register must be synthetic")
    require(isinstance(projects, list) and projects, "projects required")
    require(isinstance(roles, list) and roles, "roles required")
    require(isinstance(workstreams, list) and workstreams, "workstreams required")
    require(isinstance(continuity, list) and continuity, "continuity contexts required")
    require(isinstance(work_items, list) and work_items, "work items required")

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

    continuity_by_pair = {}
    for item in continuity:
        pair = validate_continuity(item, project_ids, role_ids)
        require(pair not in continuity_by_pair, "duplicate continuity context")
        continuity_by_pair[pair] = item

    ws_ids = set()
    workstream_by_id = {}
    for item in workstreams:
        require(isinstance(item, dict), "invalid workstream")
        ident = item.get("id")
        require(isinstance(ident, str) and ident.startswith("workstream:") and ID_RE.fullmatch(ident), "invalid workstream id")
        require(ident not in ws_ids, "duplicate workstream id")
        ws_ids.add(ident)
        workstream_by_id[ident] = item
        project_id = item.get("project_id")
        owner_role = item.get("owner_role")
        require(project_id in project_ids, "unknown workstream project")
        require(owner_role in role_ids, "unknown workstream owner")
        require((project_id, owner_role) in continuity_by_pair, "workstream continuity context missing")
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

    work_item_ids = set()
    work_item_by_workstream = {}
    work_item_paths = set()
    for item in work_items:
        require(isinstance(item, dict), "invalid work item")
        ident = item.get("id")
        require(isinstance(ident, str) and ident.startswith("workitem:") and ID_RE.fullmatch(ident), "invalid work item id")
        require(ident not in work_item_ids, "duplicate work item id")
        work_item_ids.add(ident)
        workstream_id = item.get("workstream_id")
        require(workstream_id in workstream_by_id, "unknown work item workstream")
        require(workstream_id not in work_item_by_workstream, "duplicate work item coverage")
        lane = workstream_by_id[workstream_id]
        work_item_by_workstream[workstream_id] = item
        require(item.get("project_id") == lane["project_id"], "work item project mismatch")
        require(item.get("owner_role") == lane["owner_role"], "work item owner mismatch")
        require(item.get("status") == lane["status"], "work item status mismatch")
        require(item.get("priority") == lane["priority"], "work item priority mismatch")
        require(item.get("surface") == lane["surface"], "work item surface mismatch")
        work_type = item.get("work_type")
        require(isinstance(work_type, str) and WORK_TYPE_RE.fullmatch(work_type), "invalid work type")
        projection_state = item.get("projection_state")
        require(projection_state in PROJECTION_STATES, "invalid projection state")
        require((lane["status"] == "DONE") == (projection_state == "ARCHIVED"), "work item projection/status mismatch")
        checkpoint_ref = item.get("checkpoint_ref")
        checkpoint_path = safe_file(root, checkpoint_ref)
        superseded = unique_strings(item.get("superseded_checkpoint_refs"), "superseded checkpoint refs")
        require(checkpoint_ref not in superseded, "current checkpoint cannot be superseded")
        for ref in superseded:
            safe_file(root, ref)
        last_evidence_ref = item.get("last_evidence_ref")
        safe_file(root, last_evidence_ref)
        require(item.get("next_action") == lane["next_action"], "work item next action mismatch")
        require(item.get("human_gate") == lane["human_gate"], "work item Human gate mismatch")
        risk = item.get("risk")
        require(risk is None or (isinstance(risk, str) and risk), "invalid work item risk")
        work_item_paths.update([checkpoint_ref, last_evidence_ref, *superseded])
        require(checkpoint_path.stat().st_size > 0, "empty checkpoint")

    active_workstreams = {item["id"] for item in workstreams if item["status"] != "DONE"}
    require(active_workstreams.issubset(set(work_item_by_workstream)), "active workstream missing work item")

    sources = {
        "factory/FACTORY_STATE.md",
        "factory/OPEN_LOOPS.md",
        "registers/projects.json",
        "registers/roles.json",
        "registers/workstreams.json",
        "registers/continuity.json",
        "registers/work_items.json",
    }
    sources.update(work_item_paths)
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
        "continuity_by_pair": continuity_by_pair,
        "work_items": work_items,
        "work_item_by_workstream": work_item_by_workstream,
        "source_paths": source_paths,
    }


def lines(values):
    return ", ".join(f"`{item}`" for item in values) if values else "none"


def generate(root: Path, output: Path, selected_workstream: str | None = None) -> dict:
    instance = parse_instance(root)
    output = Path(output)
    require(not output.exists(), "output already exists")
    output.parent.mkdir(parents=True, exist_ok=True)

    projects = instance["projects"]
    roles = instance["roles"]
    workstreams = instance["workstreams"]
    work_items = instance["work_items"]
    by_ws = {item["id"]: item for item in workstreams}
    if selected_workstream is None:
        selected = next((item for item in workstreams if item["status"] != "DONE"), workstreams[0])
    else:
        require(selected_workstream in by_ws, "unknown selected workstream")
        selected = by_ws[selected_workstream]
    selected_item = instance["work_item_by_workstream"].get(selected["id"])
    require(selected_item is not None, "selected workstream missing work item")
    continuity = instance["continuity_by_pair"][(selected["project_id"], selected["owner_role"])]
    recovery_mode = continuity["mode"]

    fingerprints = {ref: digest(path) for ref, path in instance["source_paths"].items()}
    source_bytes = sum(item["bytes"] for item in fingerprints.values())

    overview = "# Factory overview\n\n" + DERIVED
    overview += f"Projects: {len(projects)}  \nRoles: {len(roles)}  \nWorkstreams: {len(workstreams)}  \nActive work items: {sum(1 for item in work_items if item['projection_state'] == 'ACTIVE')}\n\n"
    gates = [item for item in workstreams if item.get("human_gate")]
    blocked = [item for item in workstreams if item["status"] == "BLOCKED" or item["blockers"]]
    overview += f"Human-gated lanes: {len(gates)}  \nBlocked/waiting lanes with blockers: {len(blocked)}\n\n"
    overview += "Use `WORK_ITEMS.md` as the current management index, then refresh the linked work surface/checkpoint before acting.\n"

    projects_md = "# Projects\n\n" + DERIVED
    for item in projects:
        owned = [w["id"] for w in workstreams if w["project_id"] == item["id"]]
        visible = [w["id"] for w in work_items if w["project_id"] == item["id"] and w["projection_state"] == "ACTIVE"]
        projects_md += f"## {item['id']}\n\nStatus: `{item.get('state', 'UNKNOWN')}`  \nPrimary: `{item.get('primary', 'UNKNOWN')}`  \nWorkstreams: {lines(owned)}  \nActive work items: {lines(visible)}\n\n"

    roles_md = "# Roles\n\n" + DERIVED
    for item in roles:
        owned = [w["id"] for w in workstreams if w["owner_role"] == item["id"]]
        visible = [w["id"] for w in work_items if w["owner_role"] == item["id"] and w["projection_state"] == "ACTIVE"]
        roles_md += f"## {item['id']} — {item.get('title', 'Untitled role')}\n\nSurface: `{item.get('recommended_surface', 'UNKNOWN')}`  \nOwned workstreams: {lines(owned)}  \nActive work items: {lines(visible)}\n\n"

    workstreams_md = "# Workstreams\n\n" + DERIVED
    workstreams_md += "Controlling references are pointers to current accepted direction; superseded references remain history and must not be replayed as current authority.\n\n"
    for item in workstreams:
        mode = instance["continuity_by_pair"][(item["project_id"], item["owner_role"])]["mode"]
        linked_item = instance["work_item_by_workstream"].get(item["id"])
        workstreams_md += (
            f"## {item['id']}\n\nProject: `{item['project_id']}`  \nOwner role: `{item['owner_role']}`  \nContinuity: `{mode}`  \n"
            f"Status / priority: `{item['status']}` / `{item['priority']}`  \nVisible work surface: `{item['surface']}`  \n"
            f"Work item: `{linked_item['id'] if linked_item else 'none'}`  \n"
            f"Controlling refs: {lines(item['controlling_refs'])}  \nSuperseded refs: {lines(item['superseded_refs'])}  \n"
            f"Blockers: {lines(item['blockers'])}  \nHuman gate: `{item['human_gate'] or 'none'}`  \nNext action: {item['next_action']}\n\n"
        )

    work_items_md = "# Project-visible work items\n\n" + DERIVED
    work_items_md += "Work items are bounded recovery/management records. Their Issue/PR/work-surface and evidence pointers remain the place to refresh canonical facts.\n\n"
    for projection in ("ACTIVE", "ARCHIVED"):
        work_items_md += f"## {projection.title()}\n\n"
        selected_items = [item for item in work_items if item["projection_state"] == projection]
        if not selected_items:
            work_items_md += "none\n\n"
            continue
        for item in selected_items:
            work_items_md += (
                f"### {item['id']}\n\nProject: `{item['project_id']}`  \nOwner: `{item['owner_role']}`  \n"
                f"Type: `{item['work_type']}`  \nStatus / priority: `{item['status']}` / `{item['priority']}`  \n"
                f"Surface: `{item['surface']}`  \nCurrent checkpoint: `{item['checkpoint_ref']}`  \n"
                f"Superseded checkpoints: {lines(item['superseded_checkpoint_refs'])}  \nLast evidence: `{item['last_evidence_ref']}`  \n"
                f"Human gate: `{item['human_gate'] or 'none'}`  \nRisk: {item['risk'] or 'none'}  \nNext action: {item['next_action']}\n\n"
            )

    recovery_md = "# Recovery brief\n\n" + DERIVED
    recovery_md += (
        f"Recovery mode: `{recovery_mode}` (derived from `registers/continuity.json`, not chosen by this bundle)\n\n"
        f"Selected workstream: `{selected['id']}`  \nWork item: `{selected_item['id']}`  \nProject: `{selected['project_id']}`  \nOwner role: `{selected['owner_role']}`  \n"
        f"Visible work surface: `{selected['surface']}`  \nCurrent checkpoint: `{selected_item['checkpoint_ref']}`  \nLast evidence: `{selected_item['last_evidence_ref']}`  \n"
        f"Current controlling refs: {lines(selected['controlling_refs'])}  \nDo not reopen as current: {lines(selected['superseded_refs'])}  \n"
        f"Superseded checkpoints: {lines(selected_item['superseded_checkpoint_refs'])}  \nBlockers: {lines(selected['blockers'])}  \n"
        f"Human gate: `{selected['human_gate'] or 'none'}`  \nRisk: {selected_item['risk'] or 'none'}  \nNext safe action: {selected['next_action']}\n\n"
    )
    if recovery_mode == "FIRST_APPOINTMENT":
        recovery_md += "No predecessor or handoff is claimed.\n"
    elif recovery_mode == "SAME_INCUMBENT_RECOVERY":
        recovery_md += f"Incumbent remains `{continuity['incumbent']}`; no succession handoff is created.\n"
    else:
        recovery_md += f"Current incumbent: `{continuity['incumbent']}`  \nPredecessor: `{continuity['previous_incumbent']}`  \nFinalized handoff pointer: `{continuity['handoff_ref']}`\n"
    recovery_md += "\nStart from the current checkpoint and visible work surface. Expand into older chronology only when a concrete conflict or missing fact requires it. This brief does not appoint an incumbent, approve a gate or prove receipt by another role.\n"

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
    for item in work_items:
        if item["projection_state"] == "ACTIVE" and item.get("risk"):
            findings.append(f"- `{item['id']}` risk: {item['risk']}")
    health_md += "\n".join(findings) if findings else "No structural health findings in the selected synthetic inputs."
    health_md += "\n"

    pslug = selected["project_id"].split(":", 1)[1]
    rslug = selected["owner_role"].split(":", 1)[1]
    bounded_sources = [
        f"projects/{pslug}/README.md",
        f"projects/{pslug}/STATE.md",
        f"offices/{rslug}/desk/CURRENT.md",
        "registers/workstreams.json",
        "registers/continuity.json",
        "registers/work_items.json",
        selected_item["checkpoint_ref"],
        selected_item["last_evidence_ref"],
    ]
    bounded_sources = list(dict.fromkeys(bounded_sources))
    task_md = "# Bounded Codex task package\n\n" + DERIVED
    task_md += (
        f"Workstream: `{selected['id']}`  \nWork item: `{selected_item['id']}`  \nProject: `{selected['project_id']}`  \nWork surface: `{selected['surface']}`\n\n"
        "## Start with\n\n" + "\n".join(f"- `{ref}`" for ref in bounded_sources) + "\n\n## Current direction\n\n"
        f"- current checkpoint: `{selected_item['checkpoint_ref']}`\n- last evidence: `{selected_item['last_evidence_ref']}`\n"
        f"- controlling refs: {lines(selected['controlling_refs'])}\n- superseded refs: {lines(selected['superseded_refs'])}\n"
        f"- superseded checkpoints: {lines(selected_item['superseded_checkpoint_refs'])}\n- blockers: {lines(selected['blockers'])}\n"
        f"- Human gate: `{selected['human_gate'] or 'none'}`\n- risk: {selected_item['risk'] or 'none'}\n"
        f"- expected next action: {selected['next_action']}\n\nExpand read scope only for a concrete dependency, conflict or missing fact discovered during implementation. Do not infer authority from this package.\n"
    )

    instructions = "# ChatGPT Project bootstrap\n\n" + DERIVED
    instructions += "This directory is a portable bootstrap package, not an automatically installed ChatGPT Project.\n\nRead `RECOVERY_BRIEF.md`, then `WORK_ITEMS.md`, then refresh only the canonical sources needed for the selected action. If generated text conflicts with repository evidence, repository evidence wins and the bundle is stale.\n"

    outputs = {
        "PROJECT_INSTRUCTIONS.md": instructions,
        "FACTORY_OVERVIEW.md": overview,
        "PROJECTS.md": projects_md,
        "ROLES.md": roles_md,
        "WORKSTREAMS.md": workstreams_md,
        "WORK_ITEMS.md": work_items_md,
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
        "selected_work_item": selected_item["id"],
        "source_fingerprints": fingerprints,
        "outputs": sorted(outputs),
        "metrics": {
            "source_files_fingerprinted": len(fingerprints),
            "source_bytes_fingerprinted": source_bytes,
            "bounded_task_source_files": len(bounded_sources),
            "active_work_items": sum(1 for item in work_items if item["projection_state"] == "ACTIVE"),
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
        "selected_work_item": selected_item["id"],
        "recovery_mode": recovery_mode,
        "source_files_fingerprinted": len(fingerprints),
        "source_bytes_fingerprinted": source_bytes,
        "output_bytes": output_bytes,
        "execution_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--workstream")
    args = parser.parse_args()
    try:
        result = generate(Path(args.root), Path(args.output), args.workstream)
    except (Invalid, OSError, UnicodeError, ValueError, RecursionError):
        result = {"status": "INVALID", "execution_authorized": False}
        print(json.dumps(result, sort_keys=True, indent=2))
        return 2
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
