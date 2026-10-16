#!/usr/bin/env python3
"""Read-only cross-platform health check for an AI Software Factory repository."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

SECRET_GLOBS = (".env", ".env.*", "*.pem", "*.key", "id_rsa", "id_ed25519")
SHA = re.compile(r"[0-9a-f]{40}\Z")


def run(args, cwd, timeout=20):
    try:
        result = subprocess.run(args, cwd=cwd, text=True, capture_output=True,
                                check=False, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return 127, ""
    return result.returncode, result.stdout.strip()


def add(checks, name, status, detail):
    checks.append({"name": name, "status": status, "detail": detail})


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def git_check(root, checks):
    if shutil.which("git") is None:
        add(checks, "git", "FAIL", "git not available")
        return {"head": None, "origin": None}

    code, version = run(["git", "--version"], root)
    add(checks, "git", "PASS" if code == 0 else "FAIL",
        version or "git invocation failed")

    code, top = run(["git", "rev-parse", "--show-toplevel"], root)
    if code != 0:
        add(checks, "git-root", "FAIL", "not a Git work tree")
        return {"head": None, "origin": None}
    same = Path(top).resolve() == root.resolve()
    add(checks, "git-root", "PASS" if same else "FAIL",
        "selected root matches Git root" if same
        else "selected root differs from Git root")

    code, head = run(["git", "rev-parse", "HEAD"], root)
    if code == 0 and SHA.fullmatch(head):
        add(checks, "git-head", "PASS", head)
    else:
        add(checks, "git-head", "FAIL", "HEAD unavailable or invalid")
        head = None

    code, branch = run(["git", "branch", "--show-current"], root)
    if code == 0:
        add(checks, "git-branch", "PASS", branch or "DETACHED")
    else:
        add(checks, "git-branch", "WARN", "branch unavailable")

    code, status = run(["git", "status", "--porcelain"], root)
    if code != 0:
        add(checks, "git-working-tree", "FAIL", "git status failed")
    elif status:
        count = len([line for line in status.splitlines() if line.strip()])
        add(checks, "git-working-tree", "WARN", f"{count} uncommitted path(s)")
    else:
        add(checks, "git-working-tree", "PASS", "clean")

    code, origin = run(["git", "remote", "get-url", "origin"], root)
    if code == 0 and origin:
        add(checks, "git-origin", "PASS", origin)
    else:
        origin = None
        add(checks, "git-origin", "WARN", "origin not configured")

    code, tracked = run(["git", "ls-files", "--", *SECRET_GLOBS], root)
    if code != 0:
        add(checks, "tracked-secret-like-files", "WARN", "git ls-files failed")
    elif tracked:
        add(checks, "tracked-secret-like-files", "FAIL",
            f"{len(tracked.splitlines())} tracked secret-like filename(s)")
    else:
        add(checks, "tracked-secret-like-files", "PASS",
            "none under checked filename patterns")

    return {"head": head, "origin": origin}


def instance_check(root, checks):
    required = ("instance.json", "authority.json", "state.json", "CURRENT.md")
    present = [name for name in required if (root / name).is_file()]
    if not present:
        return None

    missing = [name for name in required if not (root / name).is_file()]
    if missing:
        add(checks, "instance-contract-files", "FAIL",
            "missing: " + ", ".join(missing))
        return "INVALID"

    add(checks, "instance-contract-files", "PASS",
        "root instance contract present")

    validator = Path(__file__).resolve().parent / "validate_instance.py"
    if not validator.is_file():
        add(checks, "instance-validator", "FAIL",
            "scripts/validate_instance.py missing")
        return "INVALID"

    code, output = run(
        [sys.executable, "-B", str(validator), "--root", str(root)], root)
    try:
        result = json.loads(output)
        status = result.get("status")
    except (ValueError, AttributeError):
        status = None

    if status in {"VALID", "BLOCKED"} and code in {0, 3}:
        add(checks, "instance-validator", "PASS",
            f"{status}; structural result only; execution_authorized=false")
        return status

    add(checks, "instance-validator", "FAIL", "instance validation failed")
    return "INVALID"


def provenance_check(root, surface, checks):
    path = root / "SOURCE_PROVENANCE.json"
    if not path.exists():
        if surface == "OPERATING_INSTANCE":
            add(checks, "source-provenance", "WARN",
                "SOURCE_PROVENANCE.json not present")
        return

    value = read_json(path)
    if not isinstance(value, dict):
        add(checks, "source-provenance", "FAIL", "invalid JSON")
        return

    required = ("upstream", "upstream_repository_id", "source_ref",
                "source_sha", "license", "status")
    missing = [key for key in required if key not in value]
    if missing or not SHA.fullmatch(str(value.get("source_sha", ""))):
        add(checks, "source-provenance", "FAIL",
            "missing/invalid required provenance fields")
    else:
        add(checks, "source-provenance", "PASS",
            f"{value['source_ref']} @ {value['source_sha']}")


def journal_check(root, checks, origin):
    path = root / ".github" / "documentation-journal.json"
    if not path.exists():
        return

    value = read_json(path)
    if not isinstance(value, dict):
        add(checks, "documentation-journal-config", "FAIL", "invalid JSON")
        return

    required = ("repository", "repository_id", "default_branch",
                "notice_issue", "baseline_sha", "paths")
    missing = [key for key in required if key not in value]
    visibility = value.get("visibility", "public")
    if (missing or visibility not in {"public", "private"}
            or not SHA.fullmatch(str(value.get("baseline_sha", "")))):
        add(checks, "documentation-journal-config", "FAIL",
            "missing/invalid binding fields")
        return

    detail = (f"{value['repository']} visibility={visibility} "
              f"notice=#{value['notice_issue']}")
    if origin:
        expected = value["repository"] + ".git"
        if expected not in origin:
            add(checks, "documentation-journal-config", "WARN",
                detail + "; origin does not visibly match configured repository")
            return
    add(checks, "documentation-journal-config", "PASS", detail)


def github_check(root, checks):
    if shutil.which("gh") is None:
        add(checks, "github-cli", "WARN", "gh not available")
        return

    code, first = run(["gh", "--version"], root)
    add(checks, "github-cli", "PASS" if code == 0 else "WARN",
        first.splitlines()[0] if first else "gh invocation failed")

    code, _ = run(["gh", "auth", "status"], root)
    add(checks, "github-auth", "PASS" if code == 0 else "WARN",
        "authenticated" if code == 0
        else "gh auth status did not succeed")

    code, name = run(
        ["gh", "repo", "view", "--json", "nameWithOwner",
         "--jq", ".nameWithOwner"], root)
    add(checks, "github-repository-read", "PASS" if code == 0 else "WARN",
        name if code == 0 and name else "repository readback unavailable")


def inspect(root: Path, github=False):
    root = root.resolve()
    checks = []

    for relative in ("AGENTS.md", "AI_ENTRYPOINT.md"):
        present = (root / relative).is_file()
        add(checks, f"file:{relative}",
            "PASS" if present else "FAIL",
            "present" if present else "missing")

    is_instance = ((root / "instance.json").exists()
                   or (root / "SOURCE_PROVENANCE.json").exists())
    surface = ("OPERATING_INSTANCE" if is_instance
               else "FRAMEWORK_DISTRIBUTION")

    execution_path = root / "docs" / "EXECUTION_FIRST.md"
    add(checks, "execution-first-contract",
        "PASS" if execution_path.is_file() else "WARN",
        ("docs/EXECUTION_FIRST.md present"
         if execution_path.is_file() else "not present"))

    rationale_candidates = [
        root / "RATIONALE_INDEX.md",
        root / "docs" / "DESIGN_RATIONALE_INDEX.md",
    ]
    rationale = next((p for p in rationale_candidates if p.is_file()), None)
    add(checks, "rationale-index",
        "PASS" if rationale else "WARN",
        rationale.relative_to(root).as_posix() if rationale else "not present")

    git = git_check(root, checks)
    instance_status = instance_check(root, checks)
    provenance_check(root, surface, checks)
    journal_check(root, checks, git["origin"])

    if github:
        github_check(root, checks)

    failures = sum(1 for item in checks if item["status"] == "FAIL")
    warnings = sum(1 for item in checks if item["status"] == "WARN")
    overall = "FAIL" if failures else ("WARN" if warnings else "PASS")

    return {
        "status": overall,
        "surface": surface,
        "root": root.name,
        "git_head": git["head"],
        "instance_status": instance_status,
        "execution_authorized": False,
        "read_only": True,
        "github_checks_requested": bool(github),
        "checks": checks,
        "summary": {
            "failures": failures,
            "warnings": warnings,
            "total": len(checks),
        },
        "limitations": [
            "Doctor checks local declarations and optional read-only GitHub "
            "reachability; it does not grant authority.",
            "PASS does not prove organizational truth, evidence authenticity, "
            "privacy, deployment, production permission or fresh-agent acceptance.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", default=None,
        help="Factory/repository root; defaults to the parent of this script")
    parser.add_argument(
        "--json", action="store_true",
        help="Print machine-readable JSON")
    parser.add_argument(
        "--github", action="store_true",
        help="Add read-only GitHub CLI/auth/repository checks")
    args = parser.parse_args()

    root = (Path(args.root).resolve() if args.root
            else Path(__file__).resolve().parents[1])
    result = inspect(root, args.github)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            f"Factory Doctor: {result['status']}  "
            f"surface={result['surface']}  read_only=true")
        for item in result["checks"]:
            print(f"[{item['status']}] {item['name']}: {item['detail']}")
        print("Execution authorized: false")
        print(
            "Doctor is diagnostic only; PASS is not organizational "
            "or production authority.")

    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
