# Fresh Factory Audit — <DATE / AUDIT LABEL>

## Purpose

Run one **fresh-context, read-only comprehensive audit** of `<FACTORY_REPOSITORY>` to test whether a new AI context can reconstruct the organization, authority, active work, recovery paths and management visibility from repository evidence without relying on prior chat memory.

Audit baseline: `<BRANCH_OR_REF>@<TESTED_SHA>`

This Issue is the **single canonical audit surface**. Do not create child Issues automatically. Findings should be posted here first; Human / Project Management / Governance will disposition them afterward.

## Audit posture

- Auditor starts without prior private-chat context.
- Repository evidence is authoritative for this audit; generated summaries, cockpit/Project views, chat memory, model identity and technical account access are not authority.
- External/public framework documentation may be used as a reference only; differences are not automatically defects.
- Read only. Do not edit files, merge PRs, change Issue states, create releases, deploy, operate credentials, or perform Human-gated / production / destructive actions.
- Do not expose secrets, tokens, credentials or raw sensitive values in the report. If encountered, report only path/type/risk.
- Do not paste large private histories or whole Issue threads. Use exact paths / Issue / PR / commit references and bounded quotations only when necessary.

## Audit questions

Evaluate at minimum:

1. **Boot / takeover path** — can a fresh AI determine what the Factory is, what roles/projects exist, current state, blockers and next safe actions?
2. **Authority integrity** — Human authority, organizational role authority, project authority, technical identity and tool/account access remain separated and fail closed when unknown.
3. **Factory / Office / Project consistency** — Factory state, role/project registers, Staff Offices, Project Rooms, Issues/PRs and evidence do not materially contradict one another.
4. **CURRENT / Notes / pending / handoff hygiene** — recovery cursors are bounded, notes are non-authoritative, and stale/superseded guidance is detectable.
5. **Project-level manager vs Staff Office boundary** — project roles do not invent Office surfaces or borrow supervising-office authority.
6. **Work visibility** — meaningful active work has a visible work surface with recoverable owner, status, last evidence/update and next action.
7. **Long-thread recoverability** — current direction, superseded direction, blockers, gates and next action can be recovered without routinely replaying whole histories.
8. **Cross-project authority / ownership** — visibility does not silently become implementation, approval or production authority.
9. **Continuity semantics** — first appointment, same-incumbent recovery and true succession remain distinguishable.
10. **Stale / orphan / contradictory records** — frozen work shown active, completed work shown current, stale Project State/README/registers, unresolved ownership, missing evidence, duplicate truth surfaces or orphaned PRs/work items.
11. **Trust boundaries** — public/private/external-system boundaries remain explicit; no other repository or generated view silently overwrites this Factory's truth.
12. **Operational recoverability cost** — identify places where a fresh context must read disproportionate history because current-state surfaces are insufficient.

## Finding classes

Use only:

- `BLOCKER`
- `SIGNIFICANT`
- `HYGIENE`
- `OBSERVATION`

Do not invent numeric severity scores.

## Required finding format

For every finding provide:

- **Finding ID / class / short title**
- **Evidence** — exact repository path(s), Issue/PR/comment/commit refs, or bounded source references
- **Observed fact**
- **Why it matters**
- **Current authority / source of truth** — use `UNKNOWN` if unresolved
- **Suggested disposition** — one of `EXISTING_ISSUE`, `BOUNDED_FIX`, `NEW_ISSUE_CANDIDATE`, `NO_ACTION`, `HUMAN_DECISION_REQUIRED`
- **Confidence / ambiguity**

## Output

Post **one consolidated audit comment** in this Issue containing:

### Fresh Factory Audit Summary
- Repository / tested SHA
- Files / surfaces actually inspected
- Whether whole-Factory chronology replay was required
- Count of findings by class
- Highest-impact findings
- Areas that recovered cleanly
- Areas requiring Human or governance disposition

### Findings
All findings in the required format.

### Recovery assessment
State whether a fresh AI can reconstruct, with bounded reads:
- Factory identity and current operating model
- roles and authority boundaries
- active / frozen / completed projects
- meaningful active work surfaces
- blockers / Human gates
- next safe actions

### Final result
Use one of:
- `PASS_WITH_FINDINGS`
- `BLOCKED`
- `FAIL`

`PASS_WITH_FINDINGS` means the Factory remained safely recoverable while defects were identified for disposition. It does not mean no defects exist.

## Boundaries after audit

The auditor must not fix findings, open additional Issues, change this Issue state, merge, release, publish, deploy, or perform governance/production actions. This Issue remains open until the applicable Human / Project Management / Governance role records disposition of the findings.
