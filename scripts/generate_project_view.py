#!/usr/bin/env python3
"""Generate a portable Project-ready projection and bounded work-item recovery view."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from generate_cockpit import Invalid, digest, parse_instance, require

DERIVED = "> DERIVED PROJECT VIEW — generated management context only; repository records remain canonical.\n\n"


def item_row(item: dict) -> dict:
    return {
        "work_item": item["id"],
        "project": item["project_id"],
        "owner_role": item["owner_role"],
        "work_type": item["work_type"],
        "status": item["status"],
        "priority": item["priority"],
        "projection_state": item["projection_state"],
        "surface": item["surface"],
        "checkpoint": item["checkpoint_ref"],
        "last_evidence": item["last_evidence_ref"],
        "next_action": item["next_action"],
        "human_gate": item["human_gate"],
        "risk": item["risk"],
    }


def markdown_table(items: list[dict]) -> str:
    if not items:
        return "none\n"
    lines = [
        "| Work item | Project | Owner | Type | Status | Priority | Surface | Checkpoint | Last evidence | Next action | Human gate / risk |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        gate_risk = "; ".join(value for value in (item.get("human_gate"), item.get("risk")) if value) or "none"
        values = [
            item["id"], item["project_id"], item["owner_role"], item["work_type"], item["status"], item["priority"],
            item["surface"], item["checkpoint_ref"], item["last_evidence_ref"], item["next_action"], gate_risk,
        ]
        safe = [str(value).replace("|", "\\|").replace("\n", " ") for value in values]
        lines.append("| " + " | ".join(safe) + " |")
    return "\n".join(lines) + "\n"


def generate_project_view(root: Path, output: Path, selected_work_item: str | None = None) -> dict:
    instance = parse_instance(Path(root))
    output = Path(output)
    require(not output.exists(), "output already exists")
    output.parent.mkdir(parents=True, exist_ok=True)

    items = instance["work_items"]
    by_id = {item["id"]: item for item in items}
    active = [item for item in items if item["projection_state"] == "ACTIVE"]
    archived = [item for item in items if item["projection_state"] == "ARCHIVED"]
    if selected_work_item is None:
        require(active, "no active work item")
        selected = active[0]
    else:
        require(selected_work_item in by_id, "unknown work item")
        selected = by_id[selected_work_item]

    source_refs = {"registers/work_items.json", "registers/workstreams.json", "registers/continuity.json"}
    for item in items:
        source_refs.add(item["checkpoint_ref"])
        source_refs.add(item["last_evidence_ref"])
        source_refs.update(item["superseded_checkpoint_refs"])
    source_paths = {ref: instance["source_paths"][ref] for ref in sorted(source_refs)}
    fingerprints = {ref: digest(path) for ref, path in source_paths.items()}

    project_md = "# Project-ready management view\n\n" + DERIVED
    project_md += "This projection manages work items, not raw daily notes or copied Issue bodies. Refresh the linked surface/checkpoint/evidence before acting.\n\n"
    project_md += "## Active work\n\n" + markdown_table(active) + "\n"
    project_md += "## Archived work\n\n" + markdown_table(archived) + "\n"

    rows = [item_row(item) for item in items]
    project_json = {
        "schema_version": 1,
        "derived": True,
        "canonical_truth": "repository",
        "execution_authorized": False,
        "active_work_items": [item_row(item) for item in active],
        "archived_work_items": [item_row(item) for item in archived],
        "selected_work_item": selected["id"],
    }

    recovery = "# Work-item recovery\n\n" + DERIVED
    recovery += (
        f"Work item: `{selected['id']}`  \nProject: `{selected['project_id']}`  \nOwner role: `{selected['owner_role']}`  \n"
        f"Type: `{selected['work_type']}`  \nStatus / priority: `{selected['status']}` / `{selected['priority']}`  \n"
        f"Projection: `{selected['projection_state']}`  \nVisible work surface: `{selected['surface']}`  \n"
        f"Current checkpoint: `{selected['checkpoint_ref']}`  \nLast evidence: `{selected['last_evidence_ref']}`  \n"
        f"Superseded checkpoints: {', '.join(f'`{ref}`' for ref in selected['superseded_checkpoint_refs']) if selected['superseded_checkpoint_refs'] else 'none'}  \n"
        f"Human gate: `{selected['human_gate'] or 'none'}`  \nRisk: {selected['risk'] or 'none'}  \n"
        f"Next safe action: {selected['next_action']}\n\n"
        "Start from the current checkpoint, then refresh the visible work surface and last evidence. Do not replay superseded checkpoints as current direction. Expand into older chronology only when a concrete conflict or missing fact requires it.\n"
    )

    health = "# Project visibility health\n\n" + DERIVED
    findings = []
    for item in active:
        if item["status"] == "BLOCKED":
            findings.append(f"- `{item['id']}` is BLOCKED; current checkpoint `{item['checkpoint_ref']}` remains the recovery pointer.")
        if item.get("human_gate"):
            findings.append(f"- `{item['id']}` waits on Human gate `{item['human_gate']}`.")
        if item.get("risk"):
            findings.append(f"- `{item['id']}` risk: {item['risk']}")
    if archived:
        findings.append(f"- {len(archived)} archived item(s) are excluded from the active management set.")
    health += "\n".join(findings) if findings else "No visibility-health findings in the selected synthetic inputs."
    health += "\n\nStructural inconsistencies such as missing coverage, owner/project mismatch, invalid status, current/superseded checkpoint collision or missing evidence cause generation to fail closed.\n"

    output.mkdir()
    (output / "PROJECT_VIEW.md").write_text(project_md, encoding="utf-8")
    (output / "project_view.json").write_text(json.dumps(project_json, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (output / "project_view.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output / "WORK_ITEM_RECOVERY.md").write_text(recovery, encoding="utf-8")
    (output / "VISIBILITY_HEALTH.md").write_text(health, encoding="utf-8")
    manifest = {
        "schema_version": 2,
        "derived": True,
        "canonical_truth": "repository",
        "execution_authorized": False,
        "selected_work_item": selected["id"],
        "source_fingerprints": fingerprints,
        "outputs": ["PROJECT_VIEW.md", "project_view.json", "project_view.csv", "WORK_ITEM_RECOVERY.md", "VISIBILITY_HEALTH.md"],
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return {
        "status": "GENERATED",
        "derived": True,
        "execution_authorized": False,
        "active_work_items": len(active),
        "archived_work_items": len(archived),
        "selected_work_item": selected["id"],
        "output": str(output),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--work-item")
    args = parser.parse_args()
    try:
        result = generate_project_view(Path(args.root), Path(args.output), args.work_item)
    except (Invalid, OSError, UnicodeError, ValueError, json.JSONDecodeError, RecursionError):
        result = {"status": "INVALID", "derived": True, "execution_authorized": False}
        print(json.dumps(result, sort_keys=True, indent=2))
        return 2
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
