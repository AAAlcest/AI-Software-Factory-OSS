#!/usr/bin/env python3
"""Check generated cockpit source drift without treating fingerprints as authority."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def safe_source(root: Path, ref: object) -> Path:
    require(isinstance(ref, str) and ref and len(ref) <= 240, "invalid source ref")
    require("\\" not in ref and "://" not in ref, "invalid source ref")
    path = Path(ref)
    require(not path.is_absolute() and ".." not in path.parts and "." not in path.parts, "unsafe source ref")
    candidate = root / path
    require(not candidate.is_symlink(), "unsafe source ref")
    target = candidate.resolve()
    require(target.is_relative_to(root), "outside-root source")
    return target


def fingerprint(path: Path) -> dict:
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def check_drift(root: Path, bundle: Path) -> dict:
    try:
        root = Path(root).resolve()
        bundle = Path(bundle).resolve()
        require(root.exists() and root.is_dir(), "invalid root")
        manifest_path = bundle / "manifest.json"
        require(manifest_path.exists() and manifest_path.is_file() and not manifest_path.is_symlink(), "missing manifest")
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        require(isinstance(data, dict) and data.get("schema_version") == 2, "unsupported manifest")
        require(data.get("derived") is True and data.get("canonical_truth") == "repository", "invalid derived bundle")
        require(data.get("execution_authorized") is False, "derived bundle cannot authorize")
        expected = data.get("source_fingerprints")
        require(isinstance(expected, dict) and expected, "source fingerprints required")
        changed = []
        missing = []
        for ref, prior in sorted(expected.items()):
            path = safe_source(root, ref)
            if not path.exists() or not path.is_file():
                missing.append(ref)
                continue
            now = fingerprint(path)
            if now != prior:
                changed.append(ref)
        status = "FRESH" if not changed and not missing else "DRIFTED"
        return {
            "status": status,
            "changed_sources": changed,
            "missing_sources": missing,
            "fingerprints_are_authority": False,
            "execution_authorized": False,
        }
    except (Invalid, OSError, UnicodeError, json.JSONDecodeError, ValueError, RecursionError):
        return {
            "status": "INVALID",
            "changed_sources": [],
            "missing_sources": [],
            "fingerprints_are_authority": False,
            "execution_authorized": False,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--bundle", required=True)
    args = parser.parse_args()
    result = check_drift(Path(args.root), Path(args.bundle))
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["status"] == "FRESH" else (3 if result["status"] == "DRIFTED" else 2)


if __name__ == "__main__":
    raise SystemExit(main())
