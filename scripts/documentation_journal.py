#!/usr/bin/env python3
"""Issue #28: metadata-only, same-repository documentation journal. Stdlib only.

Never imports candidate code, executes hooks/diffs, or accepts a write destination
from an event. Git objects are data. Issue comments are recoverable bookkeeping,
not a tamper-proof audit store or organizational authority.
"""
from __future__ import annotations

import argparse
import base64
import copy
import datetime as dt
import fnmatch
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

SHA = re.compile(r"[0-9a-f]{40}\Z")
MARKER = re.compile(r"\A<!-- documentation-journal:v1 ([A-Za-z0-9_-]+) -->\n")
WRITER = ".github/workflows/documentation-journal.yml"
SIGNAL = ".github/workflows/documentation-journal-signal.yml"


class Gap(RuntimeError):
    """A recoverable coverage/delivery failure; never silently skip it."""


class DeliveryGap(Gap):
    def __init__(self, key, reason):
        super().__init__(reason)
        self.key = key


def canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sha(value):
    if not isinstance(value, str) or not SHA.fullmatch(value):
        raise Gap("invalid Git object id")
    return value


def safe(value):
    # Do not permit markdown links, mentions, controls, or HTML injection.
    value = re.sub(r"[\x00-\x1f\x7f]", " ", str(value))
    return html.escape(value, quote=True).replace("@", "&#64;").replace("`", "&#96;").replace("[", "&#91;").replace("]", "&#93;").replace("*", "&#42;").replace("_", "&#95;").replace("|", "&#124;")


def pack(data):
    text = base64.urlsafe_b64encode(canonical(data).encode()).decode().rstrip("=")
    return f"<!-- documentation-journal:v1 {text} -->\n"


def unpack(body):
    match = MARKER.match(body or "")
    if not match:
        return None
    try:
        text = match.group(1)
        return json.loads(base64.urlsafe_b64decode(text + "=" * (-len(text) % 4)))
    except (ValueError, UnicodeError):
        return None


class API:
    """Fixed-host REST client. No redirects; never print a response or a token."""
    def __init__(self, repo, token):
        self.root = f"https://api.github.com/repos/{repo}"
        self.token = token
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs):
                return None
        self.opener = urllib.request.build_opener(NoRedirect())

    def call(self, path, method="GET", data=None):
        if (path and not path.startswith("/")) or ".." in path or "://" in path:
            raise Gap("invalid API path")
        request = urllib.request.Request(self.root + path,
            data=None if data is None else canonical(data).encode(), method=method,
            headers={"Accept": "application/vnd.github+json", "Content-Type": "application/json",
                     "Authorization": f"Bearer {self.token}", "X-GitHub-Api-Version": "2022-11-28"})
        try:
            with self.opener.open(request, timeout=30) as response:
                raw = response.read(20_000_001)
                if len(raw) > 20_000_000:
                    raise Gap("API response exceeds safe read budget")
                return json.loads(raw)
        except urllib.error.HTTPError as exc:
            raise Gap(f"API {method} HTTP {exc.code}") from None
        except (OSError, ValueError) as exc:
            raise Gap(f"API {method} transport/decoding failure") from None

    def pages(self, path):
        rows = []
        for page in range(1, 201):
            value = self.call(path + ("&" if "?" in path else "?") + f"per_page=100&page={page}")
            if not isinstance(value, list):
                raise Gap("expected paginated list")
            rows.extend(value)
            if len(value) < 100:
                return rows
        raise Gap("pagination budget exceeded; coverage incomplete")


class Git:
    def __init__(self, root, repo, patterns):
        self.root, self.repo, self.patterns = root, repo, patterns

    def run(self, *args):
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "GITHUB_TOKEN"}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
        try:
            result = subprocess.run(["git", "-c", f"core.hooksPath={os.devnull}",
                "-c", "protocol.allow=never", "-c", "protocol.https.allow=always",
                "-c", "diff.external=", *args], cwd=self.root, env=env,
                capture_output=True, check=True, timeout=90)
            if len(result.stdout) > 16_000_000:
                raise Gap("Git output exceeds read budget")
            return result.stdout
        except (OSError, subprocess.SubprocessError):
            raise Gap("Git object unavailable, comparison failed, or read timed out") from None

    def exists(self, ref):
        self.run("cat-file", "-e", sha(ref) + "^{commit}")

    def ensure(self, ref):
        try:
            self.exists(ref)
        except Gap:
            self.run("fetch", "--no-tags", "--no-write-fetch-head",
                     f"https://github.com/{self.repo}.git", sha(ref))
            self.exists(ref)

    def fetch_pr(self, number, head):
        try:
            self.exists(head)
        except Gap:
            # Only fetch objects; never checkout or execute a PR tree.
            self.run("fetch", "--no-tags", "--no-write-fetch-head",
                f"https://github.com/{self.repo}.git", f"refs/pull/{int(number)}/head")
            self.exists(head)

    def watched(self, path):
        return any(fnmatch.fnmatchcase(path, p) for p in self.patterns)

    def changes(self, base, head):
        tokens = self.run("diff", "--raw", "--no-abbrev", "-z", "-M", "--no-ext-diff",
            "--no-textconv", sha(base), sha(head), "--").decode("utf-8").split("\0")
        changes, i = [], 0
        while i < len(tokens) and tokens[i]:
            fields = tokens[i].split()
            if len(fields) != 5 or not fields[0].startswith(":"):
                raise Gap("invalid raw Git diff")
            old_blob, new_blob, status = fields[2:]
            old_path = tokens[i + 1]
            new_path = tokens[i + 2] if status[0] in "RC" else old_path
            i += 3 if status[0] in "RC" else 2
            if self.watched(old_path) or self.watched(new_path):
                changes.append({"status": status, "old": old_path, "new": new_path,
                                "old_blob": old_blob, "new_blob": new_blob})
        return sorted(changes, key=canonical)

    def commits(self, base, tip):
        self.run("merge-base", "--is-ancestor", sha(base), sha(tip))
        # Include newly reachable side-branch commits, not just final net differences.
        rows = self.run("rev-list", "--reverse", "--topo-order", f"{base}..{tip}").decode().splitlines()
        if len(rows) > 2000:
            raise Gap("revision budget exceeded; explicit baseline/replay decision required")
        return rows

    def parents(self, ref):
        return self.run("show", "-s", "--format=%P", sha(ref)).decode().strip().split()

    def timestamp(self, ref):
        return self.run("show", "-s", "--format=%cI", sha(ref)).decode().strip()

    def merge_base(self, base, head):
        return sha(self.run("merge-base", sha(base), sha(head)).decode().strip())


def declared(body):
    """Only hash selected declarations; link to the PR rather than echo its prose."""
    values = {}
    for name in ("logical role", "reason", "impact"):
        matches = re.findall(r"^" + name + r":\s*([^\r\n]{1,500})$", body or "", re.I | re.M)
        values[name] = matches[-1].strip() if matches else "UNKNOWN"
    return digest(values), values["logical role"] != "UNKNOWN"


def context(pr):
    return (pr["base"]["repo"]["id"], pr["base"]["ref"], pr["base"]["sha"],
            (pr["head"].get("repo") or {}).get("id"), pr["head"]["sha"],
            pr["state"], pr.get("draft", False), pr.get("merged", False), declared(pr.get("body"))[0])


def candidate(pr, changes, merge_base):
    declaration, has_role = declared(pr.get("body"))
    snap = {"head_repo_id": (pr["head"].get("repo") or {}).get("id"),
            "head": sha(pr["head"]["sha"]), "base_repo_id": pr["base"]["repo"]["id"],
            "base_ref": pr["base"]["ref"], "diff": digest(changes),
            "declaration": declaration, "state": pr["state"], "draft": pr.get("draft", False)}
    return {"snapshot": snap, "digest": digest(snap), "base": sha(pr["base"]["sha"]),
            "merge_base": sha(merge_base), "ever_had_docs": bool(changes), "ever_had_docs_now": bool(changes),
            "actor": (pr.get("user") or {}).get("login", "UNKNOWN"),
            "role": "DECLARED (see PR)" if has_role else "UNKNOWN"}


def next_candidate(repo_id, number, current, previous):
    """Same snapshot is a no-op; predecessor preserves observed A -> B -> A."""
    if previous and previous.get("digest") == current["digest"]:
        return None
    ever = bool(current["ever_had_docs"] or (previous or {}).get("ever_had_docs"))
    if not ever:
        return None
    current = copy.deepcopy(current)
    current["ever_had_docs"] = ever
    current["previous"] = (previous or {}).get("key")
    current["kind"] = ("WITHDRAWN" if current["snapshot"]["state"] == "closed" else
                       "DOC_DELTA_CLEARED" if not current["ever_had_docs_now"] else "CANDIDATE")
    current["key"] = digest([repo_id, number, current["previous"], current["kind"], current["digest"]])
    return current


class Journal:
    def __init__(self, api, config, run_id, apply=False, source_sha="UNKNOWN"):
        self.api, self.cfg, self.run_id, self.apply = api, config, int(run_id), apply
        self.source_sha = source_sha
        self.endpoint = f"/issues/{int(config['notice_issue'])}/comments"
        self.run_cache = {}
        self.events, self.state_comment = {}, None
        self.reload()

    def trusted(self, row, marker):
        user = row.get("user") or {}
        if (user.get("login") != self.cfg["writer_login"] or user.get("type") != "Bot"
            or marker.get("repository_id") != self.cfg["repository_id"]):
            return False
        try:
            run_id = int(marker["run_id"])
            if run_id not in self.run_cache:
                run = self.api.call(f"/actions/runs/{run_id}")
                self.run_cache[run_id] = (run.get("path") == WRITER and
                    (run.get("repository") or {}).get("id") == self.cfg["repository_id"] and
                    run.get("head_branch") == self.cfg["default_branch"] and
                    run.get("event") in {"push", "workflow_run", "schedule", "workflow_dispatch"})
            return self.run_cache[run_id]
        except (Gap, ValueError, KeyError):
            # Cannot verify existing receipts: fail rather than blindly duplicate them.
            raise Gap("cannot verify journal marker provenance") from None

    def reload(self):
        events, states, parts = {}, [], {}
        for row in self.api.pages(self.endpoint):
            marker = unpack(row.get("body"))
            if not isinstance(marker, dict) or not self.trusted(row, marker):
                continue
            if marker.get("kind") == "state":
                states.append((row["id"], marker["state"]))
            elif marker.get("kind") == "event":
                event = marker["event"]
                key, part, total = event["key"], marker["part"], marker["total"]
                parts.setdefault(key, {})[part] = (total, event)
        for key, found in parts.items():
            total, event = next(iter(found.values()))
            if set(found) == set(range(total)) and all(x == (total, event) for x in found.values()):
                events[key] = event
        self.events, self.parts = events, parts
        self.state_comment = max(states, default=None, key=lambda item: item[0])

    def marker(self, kind, **fields):
        return {"kind": kind, "repository_id": self.cfg["repository_id"],
                "run_id": self.run_id, "source_sha": self.source_sha, **fields}

    def write(self, event, changes):
        if event["key"] in self.events:
            return
        if event["key"] in self.parts:
            saved = next(iter(self.parts[event["key"]].values()))[1]
            if saved.get("docs_digest") != event.get("docs_digest") or saved.get("digest") != event.get("digest"):
                raise Gap("conflicting partial receipt; no overwrite")
            event = saved
        groups = [changes[i:i + 40] for i in range(0, len(changes), 40)] or [[]]
        bodies = []
        url = f"https://github.com/{self.cfg['repository']}"
        for index, group in enumerate(groups):
            marker = self.marker("event", event=event, part=index, total=len(groups))
            text = pack(marker) + "## Documentation journal / 文档自动记录\n\n"
            text += f"Event: `{event['key']}` · part {index + 1}/{len(groups)}\n\n"
            for field in ("lane", "kind", "delivery", "actor", "role", "changed_at", "observed_at", "validation"):
                text += f"- {field}: {safe(event.get(field, 'UNKNOWN'))}\n"
            ref = event.get("commit") or event.get("snapshot", {}).get("head")
            if ref:
                text += f"- Evidence: [commit]({url}/commit/{sha(ref)})\n"
            if event.get("pr"):
                text += f"- Declaration / review / rationale: [PR #{event['pr']}]({url}/pull/{event['pr']})\n"
            text += f"- Recorder: [run]({url}/actions/runs/{self.run_id}); independent acceptance: NOT_CLAIMED\n"
            text += f"- Complete observed documentation diff: {len(changes)} paths; this part: {len(group)}.\n\n"
            for change in group:
                text += f"- {safe(change['status'])}: {safe(change['old'])} → {safe(change['new'])}\n"
            text += "\nMetadata only. A journal entry is not approval, deployment, or a semantic PASS.\n"
            if len(text.encode()) > 55_000:
                raise Gap("comment capacity exceeded; record remains pending")
            bodies.append(text)
        for index, body in enumerate(bodies):
            if index in self.parts.get(event["key"], {}):
                continue
            if not self.apply:
                continue
            try:
                response = self.api.call(self.endpoint, "POST", {"body": body})
                row = self.api.call(f"/issues/comments/{int(response['id'])}")
                if row.get("body") != body or not self.trusted(row, unpack(body)):
                    raise Gap("posted receipt readback mismatch")
            except Gap:
                self.reload()  # Includes POST-success/response-loss recovery before retry.
                if index not in self.parts.get(event["key"], {}):
                    raise
        if self.apply:
            self.reload()
            if event["key"] not in self.events:
                raise Gap("event parts not fully confirmed")
        else:
            self.events[event["key"]] = event  # In-memory simulation only.

    def save(self, state):
        body = pack(self.marker("state", state=state)) + "## Documentation journal status / 核对状态\n\n"
        body += f"Result: **{state['last_run']['result']}**; last observation: {state['last_run']['observed_at']}\n\n"
        body += f"Pending gaps: {len(state['gaps'])}. This is operational state, not acceptance.\n"
        body += f"\nRun: https://github.com/{self.cfg['repository']}/actions/runs/{self.run_id}\n"
        if len(body.encode()) > 55_000:
            raise Gap("state capacity exceeded; no coverage checkpoint saved")
        if not self.apply:
            return
        if self.state_comment:
            path = f"/issues/comments/{self.state_comment[0]}"
            self.api.call(path, "PATCH", {"body": body})
            row = self.api.call(path)
        else:
            response = self.api.call(self.endpoint, "POST", {"body": body})
            row = self.api.call(f"/issues/comments/{int(response['id'])}")
        if row.get("body") != body or not self.trusted(row, unpack(body)):
            raise Gap("state readback mismatch")
        self.state_comment = (row["id"], copy.deepcopy(state))


def validate_environment(api, cfg):
    repo = api.call("")
    if (repo["id"] != cfg["repository_id"] or repo["full_name"] != cfg["repository"]
        or repo["default_branch"] != cfg["default_branch"] or repo.get("private") is not False):
        raise Gap("repository identity/default branch/public boundary mismatch")
    if os.environ.get("GITHUB_REPOSITORY") != cfg["repository"]:
        raise Gap("wrong workflow repository")
    expected = f"{cfg['repository']}/{WRITER}@refs/heads/{cfg['default_branch']}"
    if os.environ.get("GITHUB_WORKFLOW_REF") != expected:
        raise Gap("writer must run from configured default branch")
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    event_name = os.environ.get("GITHUB_EVENT_NAME")
    if event_name not in {"push", "workflow_run", "schedule", "workflow_dispatch"}:
        raise Gap("unsupported privileged trigger")
    if event_name == "workflow_run":
        run = api.call(f"/actions/runs/{int(event['workflow_run']['id'])}")
        workflow = api.call("/actions/workflows/documentation-journal-signal.yml")
        if (run.get("workflow_id") != workflow["id"] or run.get("path") != SIGNAL or
            run.get("event") != "pull_request" or (run.get("repository") or {}).get("id") != cfg["repository_id"]):
            raise Gap("untrusted signal origin")
        # Association is a hint only: all actual PRs are fetched from this repository.
    notice = api.call(f"/issues/{int(cfg['notice_issue'])}")
    if notice.get("state") != "open" or notice.get("locked") is not True:
        raise Gap("notice must remain open and locked; never auto-unlock")


def reconcile(api, git, journal, cfg):
    state = copy.deepcopy(journal.state_comment[1]) if journal.state_comment else {
        "schema_version": 1, "baseline": cfg["baseline_sha"], "main_covered": cfg["baseline_sha"], "gaps": {}}
    if state.get("schema_version") != 1 or state.get("baseline") != cfg["baseline_sha"]:
        raise Gap("state/baseline mismatch")
    if state.get("config_digest", digest(cfg)) != digest(cfg):
        raise Gap("configuration changed; explicit state/baseline migration required")
    state["config_digest"] = digest(cfg)
    state["config_ref"] = journal.source_sha
    state.setdefault("pending", {})
    state["last_run"] = {"run_id": journal.run_id, "observed_at": now(), "result": "PARTIAL"}
    gaps = state["gaps"]
    observed = now()
    current_keys = set()

    def attempt(key, lane, evidence, action):
        current_keys.add(key)
        try:
            action()
            gaps.pop(key, None)
            return True
        except (Gap, UnicodeError, ValueError, KeyError) as exc:
            if isinstance(exc, DeliveryGap):
                key = "pending:" + exc.key
            gaps[key] = {"lane": lane, "evidence": evidence,
                         "reason": str(exc) if isinstance(exc, Gap) else "malformed/incomplete source evidence",
                         "last_attempt": observed}
            return False

    def post(event, changes):
        if event["key"] in journal.events:
            state["pending"].pop(event["key"], None)
            gaps.pop("pending:" + event["key"], None)
            return
        saved = state["pending"].get(event["key"])
        if saved:
            event, changes = saved["event"], saved["changes"]
        event.setdefault("observed_at", observed)
        event.setdefault("validation", "UNKNOWN; see linked exact evidence")
        state["pending"][event["key"]] = {"event": event, "changes": changes}
        # Persist the exact observation before posting. A hard kill can then replay it.
        try:
            journal.save(state)
            journal.write(event, changes)
        except Gap as exc:
            raise DeliveryGap(event["key"], str(exc)) from None
        state["pending"].pop(event["key"], None)
        gaps.pop("pending:" + event["key"], None)

    for key, pending in list(state["pending"].items()):
        event = pending["event"]
        attempt("pending:" + key, event["lane"], {"key": key, "refs": event.get("snapshot")},
                lambda pending=pending: post(pending["event"], pending["changes"]))

    tip = sha(api.call(f"/git/ref/heads/{cfg['default_branch']}")["object"]["sha"])
    state["observed_tip"] = tip
    main_ok = True
    try:
        git.ensure(tip)
        revisions = git.commits(state["main_covered"], tip)
        state["scanned_through"] = tip
    except Gap as exc:
        gaps["main-scan"] = {"lane": "main", "evidence": tip, "reason": str(exc), "last_attempt": observed}
        revisions, main_ok = [], False
    else:
        gaps.pop("main-scan", None)
    for revision in revisions:
        def commit_action(revision=revision):
            key = digest([cfg["repository_id"], "MERGED", revision])
            if key in journal.events:
                return
            parents = git.parents(revision)
            if not parents:
                raise Gap("unexpected root commit after baseline")
            changes = git.changes(parents[0], revision)
            if not changes:
                return
            prs = api.pages(f"/commits/{revision}/pulls")
            matches = [p for p in prs if p.get("merged_at") and p["base"]["ref"] == cfg["default_branch"]]
            pr = matches[0] if len(matches) == 1 else None
            metadata = api.call(f"/commits/{revision}")
            event = {"key": key, "lane": "main", "kind": "INTEGRATED_COMMIT", "delivery": "MERGED",
                     "commit": revision, "parents": parents, "pr": pr["number"] if pr else None,
                     "integration_method": "PR" if pr else "DIRECT_COMMIT" if not matches else "UNKNOWN",
                     "actor": (metadata.get("author") or {}).get("login", "UNKNOWN"), "role": "UNKNOWN",
                     "changed_at": git.timestamp(revision), "docs_digest": digest(changes)}
            post(event, changes)
        main_ok = attempt("main:" + revision, "main", revision, commit_action) and main_ok
    if main_ok:
        state["main_covered"] = tip

    def record_lifecycle(pr, n):
        for item in api.pages(f"/issues/{n}/timeline"):
            if item.get("event") not in {"closed", "reopened"} or item.get("created_at", "") < cfg["since"]:
                continue
            if pr.get("merged") and item.get("event") == "closed" and (
                item.get("created_at") == pr.get("merged_at") or
                item.get("commit_id") == pr.get("merge_commit_sha")):
                continue  # Merge is already represented by its integrated Git revision.
            kind = item["event"].upper()
            post({"key": digest([cfg["repository_id"], n, "timeline", item["id"]]),
                  "lane": f"pr:{n}:lifecycle", "kind": kind, "pr": n,
                  "delivery": "WITHDRAWN" if kind == "CLOSED" else "CANDIDATE_UNMERGED",
                  "actor": (item.get("actor") or {}).get("login", "UNKNOWN"), "role": "UNKNOWN",
                  "changed_at": item["created_at"], "historical_head": "UNKNOWN"}, [])

    try:
        prs = api.pages("/pulls?state=all&sort=updated&direction=desc")
        gaps.pop("pr-scan", None)
    except Gap as exc:
        gaps["pr-scan"] = {"lane": "prs", "reason": str(exc), "last_attempt": observed}
        prs = []
    for row in prs:
        n = int(row["number"])
        if row["state"] != "open" and row["updated_at"] < cfg["since"]:
            continue
        hint = row["head"]["sha"]
        observation = {"head": hint, "base": row["base"]["sha"], "base_ref": row["base"]["ref"],
                       "declaration_digest": declared(row.get("body"))[0], "state": row["state"],
                       "draft": row.get("draft", False)}
        def pr_action(n=n):
            before = api.call(f"/pulls/{n}")
            if before["base"]["repo"]["id"] != cfg["repository_id"]:
                raise Gap("PR repository mismatch")
            if before.get("merged"):
                # Do not fabricate an unobserved candidate after merge. Historical
                # close/reopen events remain enumerable independently of current state.
                relevant = any(e.get("pr") == n for e in journal.events.values())
                if relevant:
                    record_lifecycle(before, n)
                return
            git.fetch_pr(n, before["head"]["sha"])
            git.ensure(before["base"]["sha"])
            mb = git.merge_base(before["base"]["sha"], before["head"]["sha"])
            changes = git.changes(mb, before["head"]["sha"])
            after = api.call(f"/pulls/{n}")
            if context(before) != context(after):
                raise Gap("PR snapshot changed during comparison; retry without mixing versions")
            previous = None
            for event in journal.events.values():
                if event.get("lane") == f"pr:{n}" and event.get("digest"):
                    if previous is None or event.get("sequence", 0) > previous.get("sequence", 0):
                        previous = event
            snap = candidate(before, changes, mb)
            snap["ever_had_docs_now"] = bool(changes)
            event = next_candidate(cfg["repository_id"], n, snap, previous)
            if event:
                event.update(lane=f"pr:{n}", pr=n, sequence=(previous or {}).get("sequence", 0) + 1,
                    delivery="WITHDRAWN" if before["state"] == "closed" else "CANDIDATE_UNMERGED",
                    changed_at=git.timestamp(before["head"]["sha"]), pr_updated_at=before["updated_at"])
                post(event, changes)
            if changes or (previous or {}).get("ever_had_docs"):
                record_lifecycle(before, n)
        attempt(f"pr:{n}:{hint}", f"pr:{n}", observation, pr_action)
    # Old head gaps remain visible even if a newer snapshot succeeds. Never drop them.
    state["last_run"] = {"run_id": journal.run_id, "observed_at": observed,
                         "result": "PARTIAL" if gaps else "COMPLETE"}
    journal.save(state)
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write only from the trusted default-branch Actions run")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    cfg = json.loads((root / ".github/documentation-journal.json").read_text())
    api = API(cfg["repository"], os.environ.get("GITHUB_TOKEN", ""))
    try:
        validate_environment(api, cfg)
        git = Git(root, cfg["repository"], cfg["paths"])
        source_sha = sha(git.run("rev-parse", "HEAD").decode().strip())
        journal = Journal(api, cfg, int(os.environ["GITHUB_RUN_ID"]), args.apply, source_sha)
        state = reconcile(api, git, journal, cfg)
        print(canonical({"mode": "WRITE" if args.apply else "DRY_RUN", "result": state["last_run"]["result"],
                         "pending_gaps": len(state["gaps"]), "activation": "REQUIRES_PM_READBACK"}))
        return 1 if state["gaps"] else 0
    except (Gap, KeyError, ValueError) as exc:
        print("Journal FAILED: " + (str(exc) if isinstance(exc, Gap) else "invalid configuration/event"), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
