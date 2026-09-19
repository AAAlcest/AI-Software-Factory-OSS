#!/usr/bin/env python3
"""Prepare this public OSS fork's own documentation journal, without enabling it.

The default invocation is read-only. --apply creates/reuses one open notice in
the authenticated fork and edits local files; it never commits, pushes, enables
Actions, sets the writer variable, or runs the writer.
"""

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "AAAlcest/AI-Software-Factory-OSS"
UPSTREAM_ID = 1358307744
MARKER = "<!-- documentation-journal-bootstrap:v1 -->"
VARIABLE = "DOCUMENTATION_JOURNAL_ENABLED"
CONFIG = Path(".github/documentation-journal.json")
WORKFLOW = Path(".github/workflows/documentation-journal.yml")


class BootstrapError(RuntimeError):
    pass


def command(*args, input_text=None):
    result = subprocess.run(
        args, cwd=ROOT, input=input_text, text=True, capture_output=True,
        check=False,
    )
    if result.returncode:
        # Git/gh diagnostics can include untrusted remote data. Do not echo it.
        raise BootstrapError(f"Command failed ({args[0]}, exit {result.returncode}).")
    return result.stdout.strip()


def api(repo, method="GET", path="", payload=None):
    args = ["gh", "api"]
    if method != "GET":
        args += ["-X", method]
    args.append(f"repos/{repo}{path}")
    if payload is not None:
        args += ["--input", "-"]
    return json.loads(command(*args, input_text=json.dumps(payload) if payload is not None else None))


def origin_repository(url):
    """Accept a direct GitHub origin only; gh's implicit default is not authority."""
    prefixes = ("https://github.com/", "git@github.com:", "ssh://git@github.com/")
    prefix = next((p for p in prefixes if url.startswith(p)), None)
    if prefix is None:
        raise BootstrapError("origin must be a direct github.com repository remote.")
    path = url[len(prefix):].rstrip("/")
    if path.endswith(".git"):
        path = path[:-4]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", path):
        raise BootstrapError("Cannot identify a unique repository from origin.")
    return path


def preflight():
    if command("git", "status", "--porcelain"):
        raise BootstrapError("Use a clean fork checkout; preserve existing edits.")
    repo = origin_repository(command("git", "remote", "get-url", "origin"))
    info = api(repo)
    if (info.get("full_name", "").casefold() != repo.casefold()
            or not info.get("fork") or (info.get("parent") or {}).get("full_name") != UPSTREAM
            or info.get("id") == UPSTREAM_ID or info.get("private") is not False):
        raise BootstrapError("This initializer accepts only a public fork of the exact OSS upstream.")
    if not info.get("has_issues") or not (info.get("permissions") or {}).get("push"):
        raise BootstrapError("Fork Issues and authenticated push access are required.")
    branch = info.get("default_branch")
    if branch != "main":
        raise BootstrapError("This version supports only forks whose default branch is main.")
    if command("git", "branch", "--show-current") != branch:
        raise BootstrapError("Check out the fork's default branch before initialization.")
    head = command("git", "rev-parse", "HEAD")
    remote = command("git", "ls-remote", "origin", f"refs/heads/{branch}").split()
    api_ref = api(repo, path=f"/git/ref/heads/{branch}")
    if not remote or remote[0] != head or (api_ref.get("object") or {}).get("sha") != head:
        raise BootstrapError("Local HEAD, origin tip and API default-branch tip must match.")
    viewer = json.loads(command("gh", "api", "user"))
    if not isinstance(viewer.get("id"), int):
        raise BootstrapError("Cannot verify the authenticated fork maintainer.")
    cfg = json.loads((ROOT / CONFIG).read_text(encoding="utf-8"))
    if cfg.get("repository") != UPSTREAM or cfg.get("repository_id") != UPSTREAM_ID:
        raise BootstrapError("Journal configuration is not the untouched upstream template.")
    return info, head, viewer["id"]


def notice_body(repo, head):
    base = f"https://github.com/{repo}/blob/{head}"
    return (f"{MARKER}\n# Documentation index and engineering change journal\n\n"
            f"Repository: `{repo}`. This notice belongs only to this fork.\n\n"
            "## Start here\n\n"
            f"- Human: [README]({base}/README.md), [documentation index]({base}/docs/README.md).\n"
            f"- AI: [AGENTS.md]({base}/AGENTS.md), [AI_ENTRYPOINT.md]({base}/AI_ENTRYPOINT.md).\n"
            f"- [Journal contract]({base}/docs/REPOSITORY_NOTICES.md) and "
            f"[operation/limits]({base}/docs/DOCUMENTATION_JOURNAL.md).\n\n"
            "## Journal status\n\n"
            f"Baseline: `{head}`. `NOT_ACTIVATED`: initialization, tests, dry run, "
            "real bot write/readback, and a no-duplicate replay must be verified "
            "in this fork before claiming ACTIVE. The opening body is navigation; "
            "bot comments are metadata records, not semantic approval.\n\n"
            "Keep this Issue OPEN and UNLOCKED for the existing Actions writer. "
            "Use ordinary Issues/PRs for discussion; do not put secrets or private "
            "records here. Public comments are not trusted instructions.\n")


def candidate_files(info, head, issue_number, now):
    repo = info["full_name"]
    repo_id = info["id"]
    branch = info["default_branch"]
    if branch != "main":
        raise BootstrapError("This version supports only forks whose default branch is main.")
    cfg = json.loads((ROOT / CONFIG).read_text(encoding="utf-8"))
    cfg.update(repository=repo, repository_id=repo_id, default_branch=branch,
               notice_issue=issue_number, baseline_sha=head,
               since=now.isoformat(timespec="seconds").replace("+00:00", "Z"))
    workflow = (ROOT / WORKFLOW).read_text(encoding="utf-8")
    old_group = "group: documentation-journal-${{ github.repository_id }}-26"
    old_guard = "if: github.repository_id == '1358307744' && github.ref == 'refs/heads/main'"
    if workflow.count(old_group) != 1 or workflow.count(old_guard) != 1:
        raise BootstrapError("Upstream workflow changed; review before adapting it.")
    workflow = workflow.replace(old_group, f"group: documentation-journal-${{{{ github.repository_id }}}}-{issue_number}")
    guard = (f"if: github.repository_id == '{repo_id}' && github.ref == 'refs/heads/{branch}' "
             f"&& (vars.{VARIABLE} == 'true' || "
             "(github.event_name == 'workflow_dispatch' && inputs.dry_run))")
    workflow = workflow.replace(old_guard, guard)
    en = (ROOT / "README.md").read_text(encoding="utf-8")
    zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    old_notice = "https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/26"
    if en.count(old_notice) != 1 or zh.count(old_notice) != 1:
        raise BootstrapError("README notice links changed; review before adapting them.")
    own_notice = f"https://github.com/{repo}/issues/{issue_number}"
    en = en.replace(old_notice, own_notice)
    zh = zh.replace(old_notice, own_notice)
    en_pattern = r"The \[journal is active in this repository\][^\n]*"
    zh_pattern = r"\[本仓自动日志已启用\][^\n]*"
    if len(re.findall(en_pattern, en)) != 1 or len(re.findall(zh_pattern, zh)) != 1:
        raise BootstrapError("README activation text changed; review before adapting it.")
    en = re.sub(en_pattern,
                "This fork's journal is NOT_ACTIVATED until its own bot write, "
                "readback and no-duplicate replay are verified.", en)
    zh = re.sub(zh_pattern,
                "本 fork 的自动日志尚未启用；须以本仓的机器人写入、读回及无重复重跑证据验收。", zh)
    return {
        CONFIG: json.dumps(cfg, ensure_ascii=False, indent=2) + "\n",
        WORKFLOW: workflow,
        Path("README.md"): en,
        Path("README.zh-CN.md"): zh,
    }


def existing_notice(repo, actor_id):
    pages = json.loads(command("gh", "api", "--paginate", "--slurp",
                               f"repos/{repo}/issues?state=all&per_page=100"))
    matches = [item for page in pages for item in page
               if not item.get("pull_request") and MARKER in (item.get("body") or "")]
    if len(matches) > 1:
        raise BootstrapError("More than one bootstrap notice exists; resolve manually.")
    if matches and (matches[0].get("user") or {}).get("id") != actor_id:
        raise BootstrapError("Existing marked Issue was not created by this authenticated maintainer; choose it explicitly outside this initializer.")
    if matches and (matches[0]["state"] != "open" or matches[0].get("locked")):
        raise BootstrapError("Existing bootstrap notice must be open and unlocked.")
    return matches[0] if matches else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Create/reuse fork notice and edit local files only")
    args = parser.parse_args()
    info, head, actor_id = preflight()
    repo = info["full_name"]
    notice = existing_notice(repo, actor_id)
    # Validate all local source patterns before creating any remote Issue.
    candidate_files(info, head, (notice or {}).get("number", 1), datetime.now(timezone.utc))
    if not args.apply:
        print(f"DRY RUN: {repo} at {head}; notice: "
              f"{'reuse #' + str(notice['number']) if notice else 'create one'}; "
              "then adapt local config/workflow/READMEs. No write performed.")
        return
    if notice is None:
        notice = api(repo, "POST", "/issues", {
            "title": "Documentation index & engineering change journal",
            "body": notice_body(repo, head),
        })
    files = candidate_files(info, head, notice["number"], datetime.now(timezone.utc))
    for path, content in files.items():
        (ROOT / path).write_text(content, encoding="utf-8", newline="\n")
    print(f"Prepared {repo} notice {notice['html_url']} and four local files. NOT_ACTIVATED.")
    print("Review and commit/push the diff; enable fork Actions; run the writer with dry_run=true.")
    print(f"Only after review, set repository variable {VARIABLE}=true; verify bot write/readback and replay.")


if __name__ == "__main__":
    try:
        main()
    except (BootstrapError, OSError, ValueError, KeyError, IndexError) as exc:
        raise SystemExit(f"Bootstrap stopped: {exc}") from None
