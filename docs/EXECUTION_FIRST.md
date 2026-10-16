# Execution-First operating contract

Status: public framework contract. This document defines behavior after authority
has already been established; it does not create authority.

## Core loop

When an action is inside the current role/task authority, executable with the
available trusted surface, and not blocked by a retained gate, perform the action
and verify its evidence before reporting completion.

Reading, acknowledging, planning, apologizing, promising, describing a future
action, or saying that work is "in progress" is not the action itself.

Use this loop:

```text
READ / REFRESH
→ DECIDE WITHIN AUTHORITY
→ EXECUTE
→ VERIFY EVIDENCE
→ REPORT OR CONTINUE
```

Do not stop at an acknowledgement while authorized, executable and unblocked work
remains.

## Evidence-backed status

Execution claims must have observable evidence appropriate to the task: for example
a file/commit/ref change, submitted review, created artifact, returned command/test
result, verified remote readback, or concrete blocker evidence.

Without such evidence, do not claim `STARTED`, `EXECUTING`, `IN_PROGRESS`,
`DONE`, `VERIFIED` or an equivalent state. Use a narrower factual statement such
as `NOT_EXECUTED` or `NO_EVIDENCE` when the distinction matters.

Do not imply unsupported background work. Work continues after the current turn only
when a real queue, automation, scheduled task, independently running executor or
other supported mechanism has actually been created/started and can be evidenced.

## Valid bounded closure states

A bounded execution loop ends only in one of these states:

- `DONE` — the authorized bounded work is complete and the required evidence exists;
- `BLOCKED` — a concrete condition prevents further authorized execution;
- `HUMAN_ACTION_REQUIRED` — a genuine Human-only/manual gate remains; identify the
  minimum exact Human action;
- `AUTHORIZED_BOUNDARY_REACHED` — continuing would exceed scope, authority or a
  required review/acceptance gate.

`NO_HUMAN_ACTION_REQUIRED` means only that the Human has no current action. It does
not mean the Factory, project, release, publication, UAT or commercial outcome is
complete.

## Inbox/check semantics

A request such as "check inbox", "receive", "read new messages" or equivalent means
a bounded sweep of every unprocessed canonical recipient message since the last
reliable acknowledged checkpoint, not a search for one matching message.

Classify the whole new-message set, then execute every authorized, executable and
unblocked action discovered by the sweep. If the checkpoint is uncertain, widen the
bounded inspection and record the uncertainty instead of silently omitting mail.

## Authority is unchanged

Execution-First changes when already-authorized work should be performed. It never
changes who is authorized.

It does not bypass or weaken Human-only, Security, Release, Independent Review,
TEST/PROD, destructive, credential, publication, external-company, separation-of-
duties or other explicit gates.

Technical identity and organizational authority remain separate. A GitHub account,
App/token, branch, Issue/PR, runner, model, chat, agent or tool does not acquire a
Factory role or broader authority merely because it can perform a mutation.

If the authorized execution surface is unavailable and substituting another actor,
credential, repository/ref, environment, network/data boundary, routing path or
side-effect model would materially change the trust/approval semantics, stop at
`BLOCKED` or `HUMAN_ACTION_REQUIRED`. Do not silently substitute a convenient
surface.

## Relationship to validation

A validator, Doctor, green CI run or generated view is evidence about its stated
scope only. It does not appoint a role or authorize the next action.

Policy text, implementation and observed verification remain distinct claims.
