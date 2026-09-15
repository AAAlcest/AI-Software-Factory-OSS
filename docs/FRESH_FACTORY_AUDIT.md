# Fresh Factory Audit

A running AI Software Factory can remain locally correct while its **management and recovery surfaces drift**. A project may be healthy in its own room while a central portfolio omits it; frozen work may remain visible in an older cursor; a HOLD may be superseded by a later decision while a roll-up still repeats it.

A **Fresh Factory Audit** tests whether a new AI context can recover the Factory safely from repository evidence, detect those inconsistencies, and report them without relying on prior chat memory or automatically changing the system.

## What this audit is for

The audit answers four practical questions:

1. Can a fresh context reconstruct the Factory's identity, roles, projects, authority boundaries, blockers and next safe actions?
2. Do current management/recovery surfaces agree with stronger project/Human/Git evidence?
3. Can current direction be recovered with bounded reads, expanding into old chronology only when a concrete conflict requires it?
4. Can defects be reported in a way that supports Human/management disposition without turning the auditor into an unauthorized remediator?

This is **not** a substitute for security testing, code review, secret scanning, release review, privacy review or production validation.

## Authority rule

The operating repository being audited is the authority for that audit. Generated cockpit files, Project views, summaries, model memory, connected accounts and technical access do not become authority merely because the auditor can see them.

A public AI Software Factory OSS repository can provide reference mechanisms, but it must not silently override the audited Factory's own governance/state model.

When evidence conflicts, the auditor should:

1. identify the conflict;
2. prefer the stronger canonical source defined by the Factory;
3. leave unresolved facts `UNKNOWN` when the hierarchy does not resolve them;
4. fail closed on authority-sensitive actions;
5. expand read scope only enough to resolve the concrete conflict.

## Recommended reading strategy

Do **not** begin by replaying every Issue, mailbox or historical chat-derived record.

Start with bounded current-state surfaces:

```text
entrypoint / Factory config
        ↓
Factory state + organization standards
        ↓
project / role registers and central visibility
        ↓
Project Room / Staff Office current state
        ↓
current Issue / PR / work item / checkpoint
        ↓
current evidence + next safe action
```

Only expand into older chronology when the bounded path exposes a concrete contradiction, missing fact or unresolved authority question.

This makes the audit itself a test of recoverability cost: if discovering current direction routinely requires archaeology, that is a finding.

## What to inspect

A comprehensive fresh audit should cover at least:

- **Boot / takeover path** — can a new context determine what the Factory is and where current truth lives?
- **Authority integrity** — Human authority, role authority, project authority, technical identity and tool/account access remain distinct.
- **Factory / Office / Project consistency** — central state, Project Rooms, Staff Offices, Issues/PRs and evidence do not materially contradict one another.
- **CURRENT / notes / pending / handoff hygiene** — recovery aids stay bounded and non-authoritative.
- **Project-management boundaries** — project-level management does not invent Staff Office authority or borrow another role's records.
- **Work visibility** — meaningful active work has a visible work surface and a recoverable owner/status/evidence/next action.
- **Long-thread recovery** — current direction and superseded direction can be distinguished without routine whole-history replay.
- **Cross-project ownership** — visibility does not silently become implementation, approval or production authority.
- **Continuity semantics** — first appointment, same-incumbent recovery and true succession stay distinguishable.
- **Stale / orphan records** — frozen work shown active, completed work shown current, stale Project State, unresolved ownership, obsolete draft PRs or duplicate truth surfaces.
- **Trust boundaries** — private/public or external-company boundaries remain explicit and fail closed.

## Finding classes

Use a small qualitative vocabulary rather than pseudo-precise scores:

- `BLOCKER` — prevents safe recovery/operation or creates a material authority/security/trust-boundary failure.
- `SIGNIFICANT` — meaningful consistency/recoverability/ownership defect that should be corrected but does not by itself require an immediate Factory stop.
- `HYGIENE` — stale, redundant, poorly indexed or unnecessarily expensive context with a bounded remedy.
- `OBSERVATION` — notable condition with no demonstrated defect yet.

## Suggested dispositions

An auditor may suggest a disposition, but must not self-authorize the fix:

- `EXISTING_ISSUE`
- `BOUNDED_FIX`
- `NEW_ISSUE_CANDIDATE`
- `NO_ACTION`
- `HUMAN_DECISION_REQUIRED`

Avoid automatically opening one Issue per finding. A consolidated audit surface followed by management disposition usually produces a cleaner system.

## Required finding shape

Each finding should include:

```text
Finding ID / class / short title
Evidence
Observed fact
Why it matters
Current authority / source of truth
Suggested disposition
Confidence / ambiguity
```

Use exact paths, Issue/PR references and commit/evidence pointers. Do not paste whole private threads, secrets or credentials into the report.

## Final audit result

Use one of:

- `PASS_WITH_FINDINGS` — the Factory remained safely recoverable, but defects require disposition.
- `BLOCKED` — required evidence/access was unavailable or ambiguity prevented a safe conclusion.
- `FAIL` — the Factory could not be recovered safely, or a material authority/trust-boundary failure was demonstrated.

`PASS_WITH_FINDINGS` does **not** mean no defects exist.

## Typical drift patterns

The synthetic example in [`examples/factory-instance/audit/`](../examples/factory-instance/audit/README.md) demonstrates fictional variants of common failures:

- active project missing from a central portfolio;
- frozen work resurfacing as active in a role cursor;
- a superseded HOLD still shown as current direction;
- an authorized repository/release/visibility transition not propagated into an older Project State;
- stale `CURRENT` / `pending` recovery queues retaining resolved work;
- an obsolete draft PR remaining highly visible after its governing decision is complete.

These examples are newly authored fictional stress cases. They are not copies or redactions of a private Factory audit.

## After the audit

The recommended flow is:

```text
Fresh auditor
    ↓
One consolidated audit Issue / work surface
    ↓
Findings + evidence
    ↓
Human / PM / Governance disposition
    ↓
existing Issue | bounded fix | new Issue if genuinely needed | no action
```

The auditor should not edit files, merge PRs, change Issue states, release, publish, deploy, operate credentials, or perform destructive/production actions unless a separate explicit authority path grants those actions.

Use [`templates/FRESH_FACTORY_AUDIT_ISSUE.md`](../templates/FRESH_FACTORY_AUDIT_ISSUE.md) to open an audit surface and [`templates/FRESH_FACTORY_AUDITOR_PROMPT.md`](../templates/FRESH_FACTORY_AUDITOR_PROMPT.md) to brief a fresh evaluator.
