#!/usr/bin/env python3
"""Create a new, independent private Factory; default invocation is read-only.

V1 deliberately supports a clean, exact official upstream main checkout or the
exact official release tag matching VERSION, plus the authenticated user's own
account. A failed --apply leaves a private, BLOCKED
partial repository for manual inspection; it never deletes or silently resumes.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "AAAlcest/AI-Software-Factory-OSS"
UPSTREAM_ID = 1358307744
RELEASE_TAG = "v" + (ROOT / "VERSION").read_text(encoding="utf-8").strip()
NAME = re.compile(r"[A-Za-z0-9_.-]{1,100}\Z")
SHA = re.compile(r"[0-9a-f]{40}\Z")
COPY = (
    "LICENSE", "templates/instance/instance.json", "templates/instance/authority.json",
    "templates/instance/state.json", "templates/instance/CURRENT.md",
    "templates/STAFF_OFFICE_TEMPLATE.md", "templates/PROJECT_ROOM_TEMPLATE.md",
    "templates/CORRESPONDENCE_RECORDS_TEMPLATE.md", "scripts/documentation_journal.py",
    "scripts/documentation_journal_askpass.sh", "tests/test_documentation_journal.py",
)
CONFIG = Path(".github/documentation-journal.json")
WRITER = Path(".github/workflows/documentation-journal.yml")
SIGNAL = Path(".github/workflows/documentation-journal-signal.yml")
VARIABLE = "DOCUMENTATION_JOURNAL_ENABLED"


class BootstrapError(RuntimeError):
    pass


def process(args, cwd=ROOT, token=None):
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    if token is not None:
        env["GITHUB_TOKEN"] = token
        env["GIT_ASKPASS"] = str(Path(cwd) / "scripts/documentation_journal_askpass.sh")
        env["GIT_CONFIG_NOSYSTEM"] = "1"
        env["GIT_CONFIG_GLOBAL"] = os.devnull
    try:
        result = subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True,
                                check=False, timeout=120)
    except (OSError, subprocess.TimeoutExpired):
        raise BootstrapError(f"Local operation unavailable ({args[0]}).") from None
    if result.returncode:
        # Git/GitHub diagnostics can contain credentials or private paths.
        raise BootstrapError(f"Local operation failed ({args[0]}, exit {result.returncode}).")
    return result.stdout.strip()


def api(token, path, method="GET", payload=None, missing_ok=False):
    if not path.startswith("/") or ".." in path or "://" in path:
        raise BootstrapError("Invalid fixed GitHub API path.")
    request = urllib.request.Request(
        "https://api.github.com" + path,
        data=None if payload is None else json.dumps(payload).encode(), method=method,
        headers={"Accept": "application/vnd.github+json", "Content-Type": "application/json",
                 "Authorization": f"Bearer {token}", "X-GitHub-Api-Version": "2022-11-28"},
    )
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            return None
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=30) as response:
            return json.loads(response.read(1_000_001))
    except urllib.error.HTTPError as exc:
        exc.close()
        if missing_ok and exc.code == 404:
            return None
        raise BootstrapError(f"GitHub API {method} failed (HTTP {exc.code}).") from None
    except (OSError, ValueError):
        raise BootstrapError(f"GitHub API {method} unavailable or invalid.") from None


def source_and_target(token, name):
    if not NAME.fullmatch(name) or name in {".", ".."} or name.endswith(".git"):
        raise BootstrapError("Invalid destination repository name.")
    if process(["git", "status", "--porcelain"]):
        raise BootstrapError("Use a clean OSS source checkout.")
    if Path(process(["git", "rev-parse", "--show-toplevel"])).resolve() != ROOT.resolve():
        raise BootstrapError("Run from the exact OSS checkout.")
    origin = process(["git", "remote", "get-url", "origin"])
    if origin not in (f"https://github.com/{UPSTREAM}.git", f"git@github.com:{UPSTREAM}.git"):
        raise BootstrapError("Source origin is not the exact OSS distribution.")
    upstream = api(token, f"/repos/{UPSTREAM}")
    if (upstream.get("id") != UPSTREAM_ID or upstream.get("full_name") != UPSTREAM
            or upstream.get("private") is not False or upstream.get("default_branch") != "main"):
        raise BootstrapError("OSS source identity or visibility mismatch.")
    head = process(["git", "rev-parse", "HEAD"])
    if not SHA.fullmatch(head):
        raise BootstrapError("Invalid OSS source commit.")
    branch = process(["git", "branch", "--show-current"])
    if branch == "main":
        source_ref = "refs/heads/main"
        ref = api(token, f"/repos/{UPSTREAM}/git/ref/heads/main")
        remote = process(["git", "ls-remote", "origin", source_ref]).split()
        if ((ref.get("object") or {}).get("sha") != head or not remote or remote[0] != head):
            raise BootstrapError("Local, remote and API OSS main tips differ.")
    elif branch == "":
        source_ref = f"refs/tags/{RELEASE_TAG}"
        local_tags = process(["git", "tag", "--points-at", "HEAD"]).splitlines()
        if RELEASE_TAG not in local_tags:
            raise BootstrapError("Detached checkout is not the exact current release tag.")
        ref = api(token, f"/repos/{UPSTREAM}/git/ref/tags/{RELEASE_TAG}")
        remote = process(["git", "ls-remote", "origin", source_ref]).split()
        obj = ref.get("object") or {}
        if (obj.get("type") != "commit" or obj.get("sha") != head or not remote or remote[0] != head):
            raise BootstrapError("Local, remote and API OSS release-tag targets differ.")
    else:
        raise BootstrapError("Use a clean exact OSS main or current release-tag checkout.")
    viewer = api(token, "/user")
    owner = viewer.get("login")
    if not isinstance(viewer.get("id"), int) or not isinstance(owner, str) or not NAME.fullmatch(owner):
        raise BootstrapError("Authenticated destination owner is not verified.")
    dest = f"{owner}/{name}"
    if api(token, f"/repos/{dest}", missing_ok=True) is not None:
        raise BootstrapError("Destination already exists; no automatic resume or overwrite.")
    return viewer, head, source_ref, dest


def put(root, name, text):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def staged_source(root, source_sha, source_ref="refs/heads/main"):
    for name in COPY:
        dest = root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, dest)
    # The instance contract lives at the operating root, not under templates.
    for name in ("instance.json", "authority.json", "state.json", "CURRENT.md"):
        source = root / "templates/instance" / name
        shutil.move(source, root / name)
    shutil.rmtree(root / "templates/instance")
    put(root, "SOURCE_PROVENANCE.json", json.dumps({
        "upstream": UPSTREAM, "upstream_repository_id": UPSTREAM_ID,
        "source_ref": source_ref, "source_sha": source_sha,
        "license": "MIT", "status": "COPIED_FRAMEWORK_NOT_OPERATING_AUTHORITY",
    }, indent=2) + "\n")
    put(root, "README.md", "# Private Factory — BLOCKED starter\n\n"
        "This repository is a new independent operating instance, not an OSS fork. "
        "No Human, role, project, environment or production authority has been assigned. "
        "Read `AGENTS.md`, `AI_ENTRYPOINT.md`, the root instance contract and "
        "`SOURCE_PROVENANCE.json`. Do not run work until real authority is recorded.\n\n"
        "The documentation journal is NOT_ACTIVATED. Its repository-local writer gate "
        f"`{VARIABLE}` remains unset.\n")
    put(root, "AGENTS.md", "# Private Factory entry\n\nRead `AI_ENTRYPOINT.md` first. "
        "This is an unconfigured private instance, not an appointment. "
        "Do not infer authority from repository access or technical identity.\n")
    put(root, "AI_ENTRYPOINT.md", "# Private Factory — first entry\n\n"
        "1. Read `AGENTS.md`, `SOURCE_PROVENANCE.json`, `instance.json`, "
        "`authority.json`, `state.json` and `CURRENT.md`.\n"
        "2. Resolve a real Human decision and role/project scope before editing "
        "any operating record. `validate_instance.py` or a green test cannot appoint anyone.\n"
        "3. Current status is BLOCKED/UNCONFIGURED. No predecessor, project, "
        "correspondence or production authority is presumed.\n"
        "4. The documentation notice is navigation, not authority; journal writing "
        "requires separate repository-local opt-in and observed bot evidence.\n")
    put(root, "projects/README.md", "# Private project references — unconfigured\n\n"
        "Projects may keep their source in separate private repositories. Add only "
        "Human-authorized project references and state here; never import project "
        "source or private metadata into the public OSS distribution. No project "
        "is appointed by this starter.\n")
    # Keep the existing instance validator as a concrete operating dependency.
    shutil.copyfile(ROOT / "scripts/validate_instance.py", root / "scripts/validate_instance.py")
    (root / "scripts/documentation_journal_askpass.sh").chmod(0o755)


def verify_destination(token, dest, repo_id, viewer_id, branch=None):
    row = api(token, f"/repos/{dest}")
    if (row.get("id") != repo_id or row.get("full_name") != dest
            or (row.get("owner") or {}).get("id") != viewer_id or row.get("private") is not True
            or row.get("fork") is not False or row.get("parent") is not None
            or (branch is not None and row.get("default_branch") != branch)):
        raise BootstrapError("Created destination identity/private/non-fork readback failed.")
    return row


def ensure_issues(token, dest, row, repo_id, viewer_id):
    if row.get("has_issues") is True:
        return row
    if not (row.get("permissions") or {}).get("admin"):
        raise BootstrapError("Issues disabled and repository admin access unavailable.")
    api(token, f"/repos/{dest}", "PATCH", {"has_issues": True})
    row = verify_destination(token, dest, repo_id, viewer_id)
    if row.get("has_issues") is not True:
        raise BootstrapError("Issues enablement readback failed.")
    return row


def verify_notice(receipt, created, dest, viewer_id):
    if (receipt.get("id") != created.get("id") or receipt.get("state") != "open"
            or receipt.get("locked") is not False
            or (receipt.get("user") or {}).get("id") != viewer_id
            or receipt.get("repository_url") != f"https://api.github.com/repos/{dest}"):
        raise BootstrapError("Private notice creator/target/open readback failed.")


def journal_files(root, dest, repo_id, notice, baseline):
    cfg = json.loads((ROOT / CONFIG).read_text(encoding="utf-8"))
    if cfg.get("repository") != UPSTREAM or cfg.get("repository_id") != UPSTREAM_ID:
        raise BootstrapError("OSS journal source configuration changed.")
    cfg.update(repository=dest, repository_id=repo_id, default_branch="main",
               visibility="private", notice_issue=notice, baseline_sha=baseline,
               since=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"))
    writer = (ROOT / WRITER).read_text(encoding="utf-8")
    old_group = "group: documentation-journal-${{ github.repository_id }}-26"
    old_guard = "if: github.repository_id == '1358307744' && github.ref == 'refs/heads/main'"
    if writer.count(old_group) != 1 or writer.count(old_guard) != 1:
        raise BootstrapError("OSS writer source changed; explicit adaptation review required.")
    writer = writer.replace(old_group, f"group: documentation-journal-${{{{ github.repository_id }}}}-{notice}")
    writer = writer.replace(old_guard,
        f"if: github.repository_id == '{repo_id}' && github.ref == 'refs/heads/main' "
        f"&& (vars.{VARIABLE} == 'true' || (github.event_name == 'workflow_dispatch' && inputs.dry_run))")
    put(root, str(CONFIG), json.dumps(cfg, indent=2) + "\n")
    put(root, str(WRITER), writer)
    shutil.copyfile(ROOT / SIGNAL, root / SIGNAL)
    readme = (root / "README.md").read_text(encoding="utf-8")
    put(root, "README.md", readme + f"\nDocumentation notice: https://github.com/{dest}/issues/{notice}\n")


def git(root, *args, token=None):
    return process(["git", *args], cwd=root, token=token)


def commit(root, viewer, message):
    git(root, "add", ".")
    git(root, "update-index", "--chmod=+x", "scripts/documentation_journal_askpass.sh")
    git(root, "-c", f"user.name={viewer['login']}",
        "-c", f"user.email={viewer['id']}+{viewer['login']}@users.noreply.github.com",
        "commit", "-m", message)
    return git(root, "rev-parse", "HEAD")


def apply(token, viewer, source_sha, source_ref, dest):
    # Build and validate all source-dependent files before first remote mutation.
    with tempfile.TemporaryDirectory(prefix="private-factory-bootstrap-") as directory:
        root = Path(directory)
        staged_source(root, source_sha, source_ref)
        # A placeholder destination/notice checks source workflow shape before POST.
        journal_files(root, dest, 1, 1, "0" * 40)
        (root / CONFIG).unlink()
        (root / WRITER).unlink()
        (root / SIGNAL).unlink()
        put(root, "README.md", (root / "README.md").read_text(encoding="utf-8").split("\nDocumentation notice:")[0])
        git(root, "init", "-b", "main")
        baseline = commit(root, viewer, "Create unconfigured private Factory starter")

        created = api(token, "/user/repos", "POST", {
            "name": dest.split("/", 1)[1], "private": True, "has_issues": True,
            "auto_init": False, "description": "Private AI Software Factory operating instance",
        })
        repo_id = created.get("id")
        if not isinstance(repo_id, int):
            raise BootstrapError("Created repository ID unavailable; inspect account privately.")
        row = verify_destination(token, dest, repo_id, viewer["id"])
        ensure_issues(token, dest, row, repo_id, viewer["id"])
        git(root, "remote", "add", "origin", f"https://github.com/{dest}.git")
        git(root, "push", "-u", "origin", "HEAD:refs/heads/main", token=token)
        verify_destination(token, dest, repo_id, viewer["id"], "main")
        notice = api(token, f"/repos/{dest}/issues", "POST", {
            "title": "Documentation index and engineering change journal",
            "body": ("# Private Factory documentation notice\n\n"
                     "This private repository is BLOCKED/UNCONFIGURED; this OPEN and UNLOCKED "
                     "Issue is navigation, not authority or proof of activation. "
                     "Read README.md, AI_ENTRYPOINT.md, SOURCE_PROVENANCE.json and the instance contract. "
                     "Journal writer is NOT_ACTIVATED until dry run, explicit repository-local opt-in, "
                     "real bot write/readback and no-duplicate replay.\n"),
        })
        number = notice.get("number")
        if not isinstance(number, int):
            raise BootstrapError("Private notice number unavailable.")
        receipt = api(token, f"/repos/{dest}/issues/{number}")
        verify_notice(receipt, notice, dest, viewer["id"])
        journal_files(root, dest, repo_id, number, baseline)
        final_sha = commit(root, viewer, "Configure disabled private documentation journal")
        git(root, "push", "origin", "HEAD:refs/heads/main", token=token)
        verify_destination(token, dest, repo_id, viewer["id"], "main")
        ref = api(token, f"/repos/{dest}/git/ref/heads/main")
        if (ref.get("object") or {}).get("sha") != final_sha:
            raise BootstrapError("Private default-branch push readback failed.")
        print("CREATED private independent Factory; status=BLOCKED journal=NOT_ACTIVATED. "
              "Inspect the new private repository and run a manual journal dry run before opt-in.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, help="New repository name under the authenticated user")
    parser.add_argument("--apply", action="store_true", help="Create new private repository and BLOCKED starter")
    args = parser.parse_args()
    token = process(["gh", "auth", "token"])
    if not token:
        raise BootstrapError("Authenticated GitHub token unavailable.")
    viewer, source_sha, source_ref, dest = source_and_target(token, args.repository)
    if not args.apply:
        print(f"DRY RUN: source={UPSTREAM}@{source_ref}:{source_sha}; destination={dest} "
              "NEW private independent repository; plan=create BLOCKED starter, initial commit, "
              "OPEN/UNLOCKED private notice, disabled same-repository journal. No writes performed.")
        return
    apply(token, viewer, source_sha, source_ref, dest)


if __name__ == "__main__":
    try:
        main()
    except (BootstrapError, KeyError, ValueError, OSError) as exc:
        print("Private Factory bootstrap stopped: " +
              (str(exc) if isinstance(exc, BootstrapError) else "invalid source or response"), file=sys.stderr)
        raise SystemExit(2) from None
