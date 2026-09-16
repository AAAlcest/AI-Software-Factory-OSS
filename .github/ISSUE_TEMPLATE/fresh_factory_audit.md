---
name: Fresh Factory Audit
about: Start one fresh-context, read-only consistency and recoverability audit
---

# Fresh Factory Audit — <DATE / AUDIT LABEL>

## Purpose

Run one **fresh-context, read-only audit** of `<FACTORY_REPOSITORY>` to test whether a new AI context can reconstruct the organization, authority, active work, recovery paths and management visibility from repository evidence without relying on prior chat memory.

Audit baseline: `<BRANCH_OR_REF>@<TESTED_SHA>`

This Issue is the **single canonical audit surface**. Do not create child Issues automatically. Findings should be posted here first; Human / Project Management / Governance will disposition them afterward.

For the complete generic contract and finding format, use:

- `templates/FRESH_FACTORY_AUDIT_ISSUE.md`
- `templates/FRESH_FACTORY_AUDITOR_PROMPT.md`
- `docs/FRESH_FACTORY_AUDIT.md`

## Audit posture

- Repository evidence is authority for this audit; generated summaries, cockpit/Project views, chat memory, model identity and technical account access are not authority.
- External/public framework documentation is reference material only and does not overwrite the Factory being audited.
- Read only. Do not edit files, merge PRs, change Issue states, create releases, deploy, operate credentials, or perform Human-gated / production / destructive actions.
- Do not expose secrets, tokens, credentials or raw sensitive values. Report only path/type/risk when relevant.
- Prefer bounded current-state reads. Expand into older chronology only for a concrete conflict, dependency or missing fact.

## Finding classes

Use only:

- `BLOCKER`
- `SIGNIFICANT`
- `HYGIENE`
- `OBSERVATION`

For each finding include exact evidence, observed fact, why it matters, current authority/source of truth, suggested disposition and confidence/ambiguity.

Suggested disposition must be one of:

`EXISTING_ISSUE / BOUNDED_FIX / NEW_ISSUE_CANDIDATE / NO_ACTION / HUMAN_DECISION_REQUIRED`

## Output

Post **one consolidated audit comment** with:

- repository / tested SHA;
- files/surfaces actually inspected;
- whether whole-history replay was required;
- findings by class;
- recovery assessment for roles/projects/current work/blockers/Human gates/next safe actions;
- final result: `PASS_WITH_FINDINGS`, `BLOCKED`, or `FAIL`.

## Boundary after audit

Findings are evidence for later disposition. The auditor must not self-authorize remediation, open extra Issues, change this Issue state, merge, release, publish, deploy, use credentials, or perform production/destructive actions.
