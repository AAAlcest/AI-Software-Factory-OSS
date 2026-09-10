# Project cockpit template

Template only. Every mutable fact below is derived from canonical repository sources and must carry a source pointer or remain `UNKNOWN`.

## PROJECT_INSTRUCTIONS

- Repository records are canonical truth.
- Cockpit summaries are derived caches/indexes only.
- Refresh the smallest relevant canonical source set before material action.
- Do not infer authority from model/account/tool access.
- Preserve Human gates and fail closed on missing/conflicting authority.
- Prefer bounded project/role reads over whole-Factory rereads.

## FACTORY_OVERVIEW

> DERIVED COCKPIT SNAPSHOT

Factory: `UNKNOWN`
Source refs: `UNKNOWN`
Projects: `UNKNOWN`
Roles: `UNKNOWN`
Open loops: `UNKNOWN`
Blockers: `UNKNOWN`
Human gates: `UNKNOWN`
Next safe action: `UNKNOWN`

## PROJECTS

> DERIVED COCKPIT SNAPSHOT

For each project record: project ID/display name, repository, Project Primary, status, current ref/SHA, active Issue/milestone, pending, blockers, current/reviewed candidate, evidence refs, related roles, Human gates and next safe action.

## ROLES

> DERIVED COCKPIT SNAPSHOT

For each role record: role ID/title, incumbent/lifecycle, responsibility bundle, Office/CURRENT ref, active projects, pending, reporting/escalation, authority boundaries and next action.

## RECOVERY_BRIEF

> DERIVED COCKPIT SNAPSHOT

Continuity mode: `FIRST_APPOINTMENT | SAME_INCUMBENT_RECOVERY | TRUE_SUCCESSION`
Role: `UNKNOWN`
Project: `UNKNOWN`
Canonical repository: `UNKNOWN`
Current state: `UNKNOWN`
Current active Issue: `UNKNOWN`
Last verified ref/SHA: `UNKNOWN`
Pending work: `UNKNOWN`
Blockers: `UNKNOWN`
Decisions already made: `UNKNOWN`
Do not reopen: `UNKNOWN`
Authority boundaries: `UNKNOWN`
Next safe action: `UNKNOWN`
Evidence pointers: `UNKNOWN`

## HEALTH

> DERIVED COCKPIT SNAPSHOT

Report stale CURRENT/state, unowned pending work, blockers, missing evidence, current-vs-reviewed candidate mismatch and idle open loops. Visibility alone never grants authority to fix a finding.

## CODEX_TASK_PACKAGE

> DERIVED COCKPIT SNAPSHOT

Task: `UNKNOWN`
Target project/repository: `UNKNOWN`
Relevant paths: `UNKNOWN`
Current ref/SHA: `UNKNOWN`
Accepted decisions: `UNKNOWN`
Constraints/Human gates: `UNKNOWN`
Expected outputs: `UNKNOWN`
Required checks: `UNKNOWN`
Source pointers: `UNKNOWN`
Expansion rule: read outside this package only for a concrete implementation dependency/conflict/missing fact.
