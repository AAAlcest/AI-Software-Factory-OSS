# SAMPLE — Fresh Factory Audit Summary

> SYNTHETIC / ILLUSTRATIVE ONLY. This is not an executed audit result and does not describe any real private Factory.

Repository / tested SHA: `example/factory@fixture-audit-sha`

Files / surfaces actually inspected: Factory entrypoint/config; fictional project/role registers; Atlas and Beacon Project State; management/runtime CURRENT; synthetic work items/checkpoints; one fictional completed meeting Issue and one fictional draft PR.

Whole-Factory chronology replay required: **NO**. Historical expansion was limited to two concrete contradictions discovered during bounded recovery.

Finding count:

- `BLOCKER`: 0
- `SIGNIFICANT`: 4
- `HYGIENE`: 2
- `OBSERVATION`: 1

Highest-impact findings: Beacon omitted from central visibility; frozen Atlas governance work resurfaced in an older role cursor; a superseded HOLD remained in a roll-up; a fictional repository-visibility transition was not propagated into an older Project State.

Areas that recovered cleanly: authority hierarchy, role/project separation, current work-item/checkpoint semantics and fail-closed Human gates.

Final result: `PASS_WITH_FINDINGS`

---

## Findings

### A-01 — `SIGNIFICANT` — Active Beacon Project is missing from central visibility

**Evidence**

- `projects/beacon/STATE.md` — fictional current state says Beacon is active.
- `registers/projects.json` — fictional drifted variant omits Beacon from a central current-project projection.
- `registers/work_items.json` — `workitem:beacon-environment` remains active.

**Observed fact**

Beacon is recoverable project-locally, but a fresh Factory-wide reader stopping at the central project roll-up would miss it.

**Why it matters**

The auditor can miss the owner, blocker, Human gate and next action for a real active lane.

**Current authority / source of truth**

`projects/beacon/STATE.md` plus the current Beacon work item/checkpoint.

**Suggested disposition**

`BOUNDED_FIX`

**Confidence / ambiguity**

High in this synthetic scenario.

---

### A-02 — `SIGNIFICANT` — Frozen Atlas governance work resurfaces in an older role cursor

**Evidence**

- fictional `projects/atlas/STATE.md` — `FROZEN / NO_NEW_WORK`.
- fictional `offices/governance/desk/CURRENT.md` — still says to continue an old reconciliation task.

**Observed fact**

Project-local state freezes the lane, while a weaker recovery cursor still presents pre-freeze work as current.

**Why it matters**

A fresh role context could revive work that stronger current evidence explicitly stopped.

**Current authority / source of truth**

Atlas Project State and the fictional Human freeze decision it references.

**Suggested disposition**

`BOUNDED_FIX`

**Confidence / ambiguity**

High.

---

### A-03 — `SIGNIFICANT` — Superseded HOLD remains in a management roll-up

**Evidence**

- fictional central summary: `Atlas migration: HOLD / NOT_AUTHORIZED`.
- fictional current checkpoint: `fixture:atlas-migration-authorized`.
- fictional project evidence records a later explicit authorization that supersedes the HOLD.

**Observed fact**

The old HOLD remains highly visible after a later accepted direction replaced it.

**Why it matters**

A fresh manager can incorrectly block already-authorized work or spend unnecessary time excavating old correspondence to discover the supersession.

**Current authority / source of truth**

The later explicit project/Human authorization and current checkpoint.

**Suggested disposition**

`BOUNDED_FIX`

**Confidence / ambiguity**

High for supersession; implementation completion after authorization remains `UNKNOWN` unless separately evidenced.

---

### A-04 — `SIGNIFICANT` — Older Project State did not absorb a fictional visibility transition

**Evidence**

- fictional Project State still says repository visibility `PRIVATE / HUMAN_GATE`.
- current fictional repository metadata says `PUBLIC`.
- targeted current work-surface evidence records the Human visibility authorization.

**Observed fact**

The transition itself was authorized, but the older Project State was never reconciled.

**Why it matters**

A fresh context can misreport current state or restart a gate that has already been validly resolved.

**Current authority / source of truth**

The latest valid Human disposition plus live repository metadata; private/public trust-boundary rules remain separately authoritative.

**Suggested disposition**

`BOUNDED_FIX`

**Confidence / ambiguity**

High. This synthetic finding is state-propagation drift, not evidence of unauthorized publication.

---

### A-05 — `HYGIENE` — Recovery queue retains resolved work

**Evidence**

- fictional `offices/management/desk/CURRENT.md` still names `fixture:issue-atlas-4` as awaiting closeout.
- fictional Issue `fixture:issue-atlas-4` is already completed.
- fictional `desk/pending/` retains a candidate that current project state has superseded.

**Observed fact**

Navigation/recovery surfaces lag stronger current evidence.

**Why it matters**

Fresh-session startup cost increases and closed work can be accidentally resurrected.

**Current authority / source of truth**

Current Issue state, Project State and accepted evidence.

**Suggested disposition**

`BOUNDED_FIX`

**Confidence / ambiguity**

High.

---

### A-06 — `HYGIENE` — Obsolete draft PR remains a high-salience work surface

**Evidence**

- fictional `fixture:pr-atlas-8` remains open/draft and says a design meeting awaits a decision.
- fictional governing Issue records that the meeting was finalized later.

**Observed fact**

The draft candidate describes an intermediate state that is no longer current.

**Why it matters**

Open PRs are high-salience recovery surfaces. A fresh agent may treat the obsolete candidate as pending or attempt to review/merge stale bytes.

**Current authority / source of truth**

The finalized meeting decision and current main evidence.

**Suggested disposition**

`BOUNDED_FIX`

**Confidence / ambiguity**

High that the draft's direction is obsolete; this does not imply it should be merged.

---

### A-07 — `OBSERVATION` — Authority still fails closed despite management-view drift

**Evidence**

- fictional Factory entrypoint keeps Human, role, project and technical-access authority separate.
- work-item/checkpoint outputs remain derived and `execution_authorized: false`.
- frozen/superseded conflicts resolve toward stronger current evidence.

**Observed fact**

The synthetic drift defects degrade recovery quality, but do not demonstrate that account access, model identity or summary visibility grants execution authority.

**Why it matters**

This is why the sample result can remain `PASS_WITH_FINDINGS` rather than `FAIL`.

**Current authority / source of truth**

Repository authority hierarchy and current project/Human evidence.

**Suggested disposition**

`NO_ACTION`

**Confidence / ambiguity**

High within this synthetic scenario.

---

## Recovery assessment

- Factory identity / operating model recoverable with bounded reads: **YES**
- roles / authority boundaries recoverable: **YES**
- active / frozen / completed projects recoverable: **PARTIAL** — central visibility drift requires bounded drill-down
- meaningful active work surfaces recoverable: **YES**
- blockers / Human gates recoverable: **YES**
- next safe actions recoverable: **YES**, except stale roll-ups must be reconciled against stronger current evidence

## Why this is `PASS_WITH_FINDINGS`

The fresh auditor can still follow a bounded evidence hierarchy to recover safe current direction, and stale summaries do not override stronger repository evidence. However, central visibility and recovery hygiene are degraded enough that management should reconcile the findings before treating the roll-up as a reliable one-stop operating view.

No remediation, merge, release, publication, deployment, credential or production action is authorized by this sample report.
