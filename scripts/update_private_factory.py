#!/usr/bin/env python3
"""Preview a small provenance-checked OSS framework upgrade for one private Factory.

Preview performs read-only Git/GitHub checks. --apply writes ONLY a new private
upgrade branch and draft PR. It never updates target main or operating state.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import create_private_factory as bootstrap

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = bootstrap.UPSTREAM
UPSTREAM_ID = bootstrap.UPSTREAM_ID
LOCK = "FRAMEWORK_MANAGED_LOCK.json"
PROVENANCE = "SOURCE_PROVENANCE.json"
JOURNAL = ".github/documentation-journal.json"
# Intentionally tiny, exact-copy set; generated/private-bound files are excluded.
MANAGED = (
    "scripts/validate_instance.py",
    "templates/STAFF_OFFICE_TEMPLATE.md",
    "templates/PROJECT_ROOM_TEMPLATE.md",
)
SHA = re.compile(r"[0-9a-f]{40}\Z")
NAME = re.compile(r"[A-Za-z0-9_.-]{1,100}\Z")
MAX_BYTES = 262144


class UpgradeError(RuntimeError):
    """A sanitized fail-closed diagnostic."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(row: dict) -> bytes:
    return (json.dumps(row, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")


def source_identity(token: str) -> tuple[dict, str]:
    """Verify exact, clean official main using local, remote and API identities."""
    if bootstrap.process(["git", "status", "--porcelain"]):
        raise UpgradeError("Use a clean official OSS checkout.")
    if Path(bootstrap.process(["git", "rev-parse", "--show-toplevel"])).resolve() != ROOT.resolve():
        raise UpgradeError("OSS checkout root mismatch.")
    origin = bootstrap.process(["git", "remote", "get-url", "origin"])
    if origin not in (f"https://github.com/{UPSTREAM}.git", f"git@github.com:{UPSTREAM}.git"):
        raise UpgradeError("Unexpected official OSS origin.")
    if bootstrap.process(["git", "branch", "--show-current"]) != "main":
        raise UpgradeError("Use official OSS main, not a branch or release tag.")
    head = bootstrap.process(["git", "rev-parse", "HEAD"])
    if not SHA.fullmatch(head):
        raise UpgradeError("Invalid OSS source HEAD.")
    row = bootstrap.api(token, f"/repos/{UPSTREAM}")
    if (row.get("id") != UPSTREAM_ID or row.get("full_name") != UPSTREAM
            or row.get("private") is not False or row.get("default_branch") != "main"):
        raise UpgradeError("Official OSS repository identity mismatch.")
    ref = bootstrap.api(token, f"/repos/{UPSTREAM}/git/ref/heads/main")
    remote = bootstrap.process(["git", "ls-remote", "origin", "refs/heads/main"]).split()
    if ((ref.get("object") or {}).get("sha") != head
            or not remote or remote[0] != head):
        raise UpgradeError("Local/origin/API main disagreement.")
    viewer = bootstrap.api(token, "/user")
    if (not isinstance(viewer.get("id"), int)
            or not isinstance(viewer.get("login"), str)
            or not NAME.fullmatch(viewer["login"])):
        raise UpgradeError("Authenticated owner cannot be verified.")
    return viewer, head


def target_identity(token: str, dest: str, viewer: dict) -> dict:
    """Own-account private/non-fork repositories only; no org impersonation."""
    parts = dest.split("/")
    if (len(parts) != 2 or parts[0] != viewer["login"]
            or not NAME.fullmatch(parts[1]) or parts[1] in {".", ".."}
            or parts[1].endswith(".git")):
        raise UpgradeError("Target must be one explicit repository owned by the authenticated user.")
    row = bootstrap.api(token, f"/repos/{dest}")
    if (row.get("full_name") != dest or not isinstance(row.get("id"), int)
            or (row.get("owner") or {}).get("id") != viewer["id"]
            or row.get("private") is not True or row.get("fork") is not False
            or row.get("parent") is not None or row.get("default_branch") != "main"
            or (row.get("permissions") or {}).get("push") is not True):
        raise UpgradeError("Target is not the verified, writable, independent private Factory.")
    return row


def get_bytes(token: str, dest: str, path: str, *, optional: bool = False, ref: str = "main") -> bytes | None:
    # Only fixed paths from this module are accepted; never interpolate input paths.
    if path not in (*MANAGED, PROVENANCE, JOURNAL, LOCK, "instance.json"):
        raise UpgradeError("Unmanaged read path rejected.")
    if ref != "main" and not SHA.fullmatch(ref):
        raise UpgradeError("Unverified private read ref.")
    item = bootstrap.api(token, f"/repos/{dest}/contents/{path}?ref={ref}", missing_ok=optional)
    if item is None:
        if optional:
            return None
        raise UpgradeError("A required managed/identity file is missing.")
    if (item.get("type") != "file" or item.get("encoding") != "base64"
            or not isinstance(item.get("content"), str)
            or not isinstance(item.get("size"), int)
            or not 0 <= item["size"] <= MAX_BYTES):
        raise UpgradeError("Invalid or oversized managed/identity file.")
    try:
        value = base64.b64decode(item["content"], validate=False)
    except (ValueError, binascii.Error):
        raise UpgradeError("Invalid encoded managed/identity file.") from None
    if len(value) != item["size"] or len(value) > MAX_BYTES:
        raise UpgradeError("Managed/identity file size mismatch.")
    return value


def object_json(data: bytes | None, name: str) -> dict:
    if data is None:
        raise UpgradeError(f"Missing {name}.")
    try:
        row = json.loads(data.decode("utf-8"))
    except (UnicodeError, ValueError):
        raise UpgradeError(f"Invalid {name}.") from None
    if not isinstance(row, dict):
        raise UpgradeError(f"Invalid {name} structure.")
    return row


def historical_bytes(sha: str, path: str) -> bytes:
    """Require an actual reachable historical OSS blob; no heuristic reconstruction."""
    if not SHA.fullmatch(sha) or path not in MANAGED:
        raise UpgradeError("Invalid historical source reference.")
    try:
        run = subprocess.run(
            ["git", "show", f"{sha}:{path}"], cwd=ROOT,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False, timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired):
        raise UpgradeError("Historical source blob unavailable.") from None
    if run.returncode or len(run.stdout) > MAX_BYTES:
        raise UpgradeError("Historical managed file cannot be reconstructed.")
    return run.stdout


def is_ancestor(old: str, new: str) -> bool:
    if not SHA.fullmatch(old) or not SHA.fullmatch(new):
        return False
    try:
        run = subprocess.run(
            ["git", "merge-base", "--is-ancestor", old, new],
            cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            check=False, timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return run.returncode == 0


def verify_journal(token: str, dest: str, repo_id: int, ref: str = "main") -> None:
    raw = get_bytes(token, dest, JOURNAL, optional=True, ref=ref)
    if raw is None:
        return
    row = object_json(raw, "private journal configuration")
    if (row.get("repository") != dest or row.get("repository_id") != repo_id
            or row.get("visibility") != "private" or row.get("default_branch") != "main"
            or not isinstance(row.get("notice_issue"), int) or row["notice_issue"] < 1
            or not SHA.fullmatch(str(row.get("baseline_sha", "")))
            or row.get("cadence_mode") not in (None, *bootstrap.JOURNAL_MODES)):
        raise UpgradeError("Private journal identity/binding conflicts with the target.")
    # Preserve notice and all writer settings; this script never writes this config.


def target_tip(token: str, dest: str) -> str:
    ref = bootstrap.api(token, f"/repos/{dest}/git/ref/heads/main")
    sha = (ref.get("object") or {}).get("sha")
    if not isinstance(sha, str) or not SHA.fullmatch(sha):
        raise UpgradeError("Target main ref is unavailable.")
    return sha


def no_conflicting_upgrade(token: str, dest: str, branch: str) -> None:
    if bootstrap.api(token, f"/repos/{dest}/git/ref/heads/{branch}", missing_ok=True) is not None:
        raise UpgradeError("An upgrade branch already exists; manual inspection required.")
    prs = bootstrap.api(token, f"/repos/{dest}/pulls?state=open&per_page=100")
    if not isinstance(prs, list) or len(prs) >= 100:
        raise UpgradeError("Private open-PR inventory is incomplete.")
    if any(str((p.get("head") or {}).get("ref", "")).startswith("factory-upgrade/")
           for p in prs):
        raise UpgradeError("An existing private upgrade PR requires disposition first.")


def build_plan(token: str, dest: str) -> dict:
    viewer, newsha = source_identity(token)
    row = target_identity(token, dest, viewer)
    repo_id = row["id"]
    mainsha = target_tip(token, dest)

    # Confirm a real instance without inspecting or publishing its operating records.
    if get_bytes(token, dest, "instance.json", optional=True, ref=mainsha) is None:
        raise UpgradeError("Target is missing its private instance anchor.")
    old = object_json(get_bytes(token, dest, PROVENANCE, ref=mainsha), "source provenance")
    oldsha = old.get("source_sha")
    if (old.get("upstream") != UPSTREAM or old.get("upstream_repository_id") != UPSTREAM_ID
            or not isinstance(oldsha, str) or not SHA.fullmatch(oldsha)
            or not is_ancestor(oldsha, newsha)):
        raise UpgradeError("Foreign, invalid or unverified prior OSS provenance.")
    verify_journal(token, dest, repo_id, ref=mainsha)

    name = f"factory-upgrade/{oldsha[:12]}-to-{newsha[:12]}"
    no_conflicting_upgrade(token, dest, name)

    current_lock = get_bytes(token, dest, LOCK, optional=True, ref=mainsha)
    if current_lock is not None:
        recorded = object_json(current_lock, "managed lock")
        if (recorded.get("schema_version") != 1
                or recorded.get("upstream") != UPSTREAM
                or recorded.get("repository_id") != UPSTREAM_ID
                or recorded.get("source_sha") != oldsha
                or not isinstance(recorded.get("files"), dict)
                or set(recorded["files"]) != set(MANAGED)):
            raise UpgradeError("Managed lock conflicts with source provenance.")

    changes = {}
    file_hashes = {}
    for path in MANAGED:
        expected = historical_bytes(oldsha, path)
        actual = get_bytes(token, dest, path, ref=mainsha)
        if actual != expected:
            # Includes missing, edited and unreconstructable managed files.
            raise UpgradeError("Locally changed managed file: conflict, no overwrite.")
        if current_lock is not None and recorded["files"].get(path) != digest(expected):
            raise UpgradeError("Managed lock hash mismatch.")
        desired = (ROOT / path).read_bytes()
        if len(desired) > MAX_BYTES:
            raise UpgradeError("New framework managed file is oversized.")
        file_hashes[path] = digest(desired)
        if desired != expected:
            changes[path] = desired

    if target_tip(token, dest) != mainsha:
        raise UpgradeError("Private main changed during preview; retry.")
    if oldsha == newsha and not changes:
        raise UpgradeError("Target managed framework is already at current source.")
    provenance = dict(old)
    provenance.update(source_ref="refs/heads/main", source_sha=newsha,
                      managed_scope="EXPLICIT_PARTIAL_FRAMEWORK_UPGRADE",
                      managed_lock=LOCK)
    locked = {
        "schema_version": 1,
        "upstream": UPSTREAM,
        "repository_id": UPSTREAM_ID,
        "source_sha": newsha,
        "files": file_hashes,
    }
    # This fixed candidate set expressly excludes README, AGENTS, state, Offices,
    # Projects, journal config/workflows and any private operating or user files.
    changes[PROVENANCE] = json_bytes(provenance)
    changes[LOCK] = json_bytes(locked)
    return {
        "dest": dest, "source_sha": newsha, "prior_sha": oldsha,
        "target_id": repo_id, "viewer_id": viewer["id"],
        "base_sha": mainsha, "branch": name, "changes": changes,
        "changed_managed": [p for p in MANAGED if p in changes],
        "legacy_without_lock": current_lock is None,
    }


def commit_private_candidate(token: str, plan: dict) -> int:
    dest = plan["dest"]
    # All checks and conflicts were resolved before the first remote mutation.
    if target_tip(token, dest) != plan["base_sha"]:
        raise UpgradeError("Private target main moved; re-run preview.")
    if bootstrap.api(token, f"/repos/{dest}/git/ref/heads/{plan['branch']}",
                     missing_ok=True) is not None:
        raise UpgradeError("Private upgrade branch appeared; no overwrite.")

    commit = bootstrap.api(token, f"/repos/{dest}/git/commits/{plan['base_sha']}")
    tree_sha = (commit.get("tree") or {}).get("sha")
    if not isinstance(tree_sha, str) or not SHA.fullmatch(tree_sha):
        raise UpgradeError("Private base tree unavailable.")

    elements = []
    for path, data in sorted(plan["changes"].items()):
        obj = bootstrap.api(token, f"/repos/{dest}/git/blobs", "POST", {
            "content": base64.b64encode(data).decode("ascii"),
            "encoding": "base64",
        })
        sha = obj.get("sha")
        if not isinstance(sha, str) or not SHA.fullmatch(sha):
            raise UpgradeError("Private candidate blob write failed.")
        elements.append({"path": path, "mode": "100644", "type": "blob", "sha": sha})
    new_tree = bootstrap.api(token, f"/repos/{dest}/git/trees", "POST", {
        "base_tree": tree_sha, "tree": elements,
    }).get("sha")
    if not isinstance(new_tree, str) or not SHA.fullmatch(new_tree):
        raise UpgradeError("Private candidate tree failed.")
    commit_sha = bootstrap.api(token, f"/repos/{dest}/git/commits", "POST", {
        "message": "chore: upgrade explicitly managed OSS framework files",
        "tree": new_tree, "parents": [plan["base_sha"]],
    }).get("sha")
    if not isinstance(commit_sha, str) or not SHA.fullmatch(commit_sha):
        raise UpgradeError("Private candidate commit failed.")
    bootstrap.api(token, f"/repos/{dest}/git/refs", "POST", {
        "ref": "refs/heads/" + plan["branch"], "sha": commit_sha,
    })
    pr = bootstrap.api(token, f"/repos/{dest}/pulls", "POST", {
        "title": "Upgrade explicit OSS framework-managed files (review required)",
        "head": plan["branch"], "base": "main", "draft": True,
        "body": (
            "Framework-only candidate: " + plan["prior_sha"] + " -> " + plan["source_sha"]
            + "\nManaged files changed: " + ", ".join(plan["changed_managed"])
            + "\nPrivate operating state, journal configuration and writer variable unchanged."
            + "\nNo automatic merge, public export or release. Human review required."
        ),
    })
    number = pr.get("number")
    if not isinstance(number, int):
        raise UpgradeError("Private PR could not be verified; inspect the branch manually.")
    readback = bootstrap.api(token, f"/repos/{dest}/pulls/{number}")
    if ((readback.get("head") or {}).get("sha") != commit_sha
            or (readback.get("base") or {}).get("ref") != "main"
            or readback.get("draft") is not True):
        raise UpgradeError("Private draft PR readback mismatch.")
    return number


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, help="OWN_LOGIN/private-repository-name")
    parser.add_argument("--apply", action="store_true",
                        help="Create a private candidate branch and draft PR, never merge")
    args = parser.parse_args()
    token = bootstrap.process(["gh", "auth", "token"])
    if not token:
        raise UpgradeError("Authenticated GitHub token unavailable.")
    plan = build_plan(token, args.repository)
    print(json.dumps({
        "status": "READY_FOR_PRIVATE_REVIEW" if args.apply else "PREVIEW_ONLY",
        "source_sha": plan["source_sha"],
        "prior_source_sha": plan["prior_sha"],
        "changed_managed_paths": plan["changed_managed"],
        "legacy_lock_reconstruction": plan["legacy_without_lock"],
        "target_main_write": False,
        "instance_state_write": False,
        "journal_configuration_write": False,
        "writer_variable_write": False,
        "execution_authorized": False,
    }, sort_keys=True))
    if args.apply:
        number = commit_private_candidate(token, plan)
        print(json.dumps({"status": "PRIVATE_DRAFT_PR_CREATED",
                          "pr_number": number, "main_pushed": False,
                          "auto_merge": False, "execution_authorized": False}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (UpgradeError, bootstrap.BootstrapError, OSError, ValueError, KeyError) as error:
        msg = str(error) if isinstance(error, (UpgradeError, bootstrap.BootstrapError)) else "invalid input"
        print("Private upgrade stopped: " + msg, file=sys.stderr)
        raise SystemExit(2) from None
