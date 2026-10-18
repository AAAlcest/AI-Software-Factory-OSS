# Event-driven Staff Office Notes

Notes are non-authoritative recovery/execution deltas for a role. They are not a
daily reporting obligation and must not become a second work-management system.

## Surface model

```text
Issue / PR / Project-visible item = visible work surface
desk/CURRENT.md                  = concise mutable recovery cursor
desk/pending/                    = unresolved queue
desk/notes/                      = event-driven delta history
handoff                          = true-succession historical record
```

Current authority/state, Human decisions, Git/evidence and the active work surface
remain stronger than Notes.

## When to write

Write a note only when actual work produces a meaningful recovery delta, for example:

- a work surface changes;
- implementation/review evidence appears;
- a decision/disposition changes;
- a blocker/wait changes;
- the next action changes;
- a cross-role dependency/handoff appears;
- a propagation/announcement is actually needed.

A date filename such as `YYYY-MM-DD.md` is only a grouping convenience. Do not
create empty files, daily heartbeats, "still working" notes or no-change entries.

Before adding a note, compare the last applicable note with current canonical
Issue/PR/Project/Git/correspondence/evidence and record only what changed.

## Suggested compact shape

```text
# YYYY-MM-DD

Work surfaces:
- <Issue / PR / work item>

Delta / evidence:
- <what changed + exact pointer>

Decision / disposition observed:
- <pointer, not copied authority>

Blockers / waits:
- <changed blocker or none>

Next action:
- <current next action>

Cross-role dependency / propagation:
- <only if changed/applicable>
```

Do not paste whole Issue/PR/mail threads, secrets, credentials or large reports.
Use exact references instead.

## CURRENT and pending

`desk/CURRENT.md` stays short. It points to current focus, relevant active surface,
last reliable checkpoint/recent note, blocker and next action. It is not chronology.

`desk/pending/` contains unresolved queue items only. Resolved work leaves the
active queue with durable provenance.

A stale Note/CURRENT/pending entry must not resurrect superseded or completed work.

## Continuity

Same-incumbent chat/session recovery is not succession. Notes may help recovery,
but a real succession uses the governed handoff process. Historical Notes and
handoffs never override fresher verified current state.

## Audit interpretation

Fresh Factory Audit should treat empty heartbeat files, duplicated chronology,
stale blockers, resolved pending entries and CURRENT files that become long work
logs as recoverability/record-hygiene findings.
