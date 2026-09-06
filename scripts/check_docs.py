#!/usr/bin/env python3
"""Offline Markdown file-target and JSON syntax checks, not semantic approval."""
from __future__ import annotations
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


def check_docs(root: Path) -> dict:
    root = Path(root).resolve()
    errors = []
    links = json_count = 0
    files = [p for p in root.rglob("*") if p.is_file() and
             not any(part in {".git", "__pycache__", ".venv"} for part in p.relative_to(root).parts)]
    for path in files:
        name = path.relative_to(root).as_posix()
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            errors.append(name + ": unsafe file reference")
            continue
        if path.suffix == ".json":
            json_count += 1
            try:
                from validate_instance import pairs, bad_constant
                json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs, parse_constant=bad_constant)
            except (OSError, UnicodeError, ValueError, RecursionError):
                errors.append(name + ": invalid JSON")
        if path.suffix != ".md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(name + ": unreadable Markdown")
            continue
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for target in re.findall(r"\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)", text):
            try:
                parsed = urlsplit(target.strip("<>"))
            except ValueError:
                errors.append(name + ": malformed link")
                continue
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            links += 1
            resolved = (path.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                errors.append(name + ": missing or outside-root file target " + parsed.path)
    return {"status": "PASS" if not errors else "FAIL", "relative_file_links_checked": links,
            "json_files_checked": json_count, "errors": errors,
            "external_links_checked": False, "all_anchors_checked": False,
            "semantic_privacy_approved": False}


if __name__ == "__main__":
    result = check_docs(Path(__file__).resolve().parents[1])
    print(json.dumps(result, sort_keys=True, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
