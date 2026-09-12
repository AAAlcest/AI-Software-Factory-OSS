#!/usr/bin/env python3
"""Measure observable context size for whole-cockpit vs bounded task inputs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from check_cockpit_drift import check_drift
from generate_cockpit import Invalid, parse_instance


def require(condition, message):
    if not condition:
        raise Invalid(message)


def measure(root: Path, bundle: Path) -> dict:
    root = Path(root).resolve()
    bundle = Path(bundle).resolve()
    drift = check_drift(root, bundle)
    if drift["status"] != "FRESH":
        return {
            "status": "BLOCKED_STALE_BUNDLE" if drift["status"] == "DRIFTED" else "INVALID",
            "execution_authorized": False,
            "drift": drift,
            "token_counts": "NOT_EXPOSED",
        }

    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    fingerprints = manifest.get("source_fingerprints")
    require(isinstance(fingerprints, dict) and fingerprints, "missing fingerprints")
    selected_id = manifest.get("selected_workstream")
    instance = parse_instance(root)
    workstreams = {item["id"]: item for item in instance["workstreams"]}
    require(selected_id in workstreams, "unknown selected workstream")
    selected = workstreams[selected_id]
    pslug = selected["project_id"].split(":", 1)[1]
    rslug = selected["owner_role"].split(":", 1)[1]
    bounded_refs = [
        f"projects/{pslug}/README.md",
        f"projects/{pslug}/STATE.md",
        f"offices/{rslug}/desk/CURRENT.md",
        "registers/workstreams.json",
        "registers/continuity.json",
    ]
    require(all(ref in fingerprints for ref in bounded_refs), "bounded source missing from manifest")

    broad_files = len(fingerprints)
    broad_bytes = sum(item["bytes"] for item in fingerprints.values())
    bounded_bytes = sum(fingerprints[ref]["bytes"] for ref in bounded_refs)
    package = bundle / "CODEX_TASK_PACKAGE.md"
    require(package.exists() and package.is_file() and not package.is_symlink(), "missing task package")
    package_bytes = package.stat().st_size

    return {
        "status": "MEASURED",
        "derived": True,
        "execution_authorized": False,
        "selected_workstream": selected_id,
        "broad_context": {"files": broad_files, "bytes": broad_bytes},
        "bounded_context": {"files": len(bounded_refs), "bytes": bounded_bytes, "refs": bounded_refs},
        "difference": {"files": broad_files - len(bounded_refs), "bytes": broad_bytes - bounded_bytes},
        "bounded_fraction_by_bytes": round(bounded_bytes / broad_bytes, 6) if broad_bytes else None,
        "generated_task_package_bytes": package_bytes,
        "token_counts": "NOT_EXPOSED",
        "interpretation": "Observable file/byte comparison only; not a token-saving guarantee.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--bundle", required=True)
    args = parser.parse_args()
    try:
        result = measure(Path(args.root), Path(args.bundle))
    except (Invalid, OSError, UnicodeError, ValueError, json.JSONDecodeError, RecursionError):
        result = {"status": "INVALID", "execution_authorized": False, "token_counts": "NOT_EXPOSED"}
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["status"] == "MEASURED" else (3 if result["status"] == "BLOCKED_STALE_BUNDLE" else 2)


if __name__ == "__main__":
    raise SystemExit(main())
