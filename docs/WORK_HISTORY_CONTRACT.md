# Work Invocation History: declaration-only lifecycle checks

This optional contract makes the [Office Wardrobe](WORK_INVOCATION_WARDROBE.md)
usable without a particular model, chat provider, workstation or dispatcher.
It records one bounded invocation, not an appointment and not a tenure.
It does not replace current project state, actual evidence or independent review.

## Quick exercise

Python 3.10+ and the standard library are the implementation target. Run from
this repository's root:

```sh
python -B scripts/validate_work_history.py examples/work-history/completed-session.json
python -B scripts/validate_work_history.py templates/work-history/session.json
python -B -m unittest discover -s tests -p 'test_work_history.py' -v
```

The authored [example](../examples/work-history/README.md) should return `VALID`
and exit 0. The [unconfigured starter](../templates/work-history/session.json)
should return `BLOCKED` and exit 3. Invalid structures return `INVALID` and exit 2.
All results retain false `execution_authorized`, `liveness_verified`,
`evidence_verified` and `independent_review_granted` flags.
**VALID means consistency of declarations, not that their claims are true.**

## Version 1 record

The JSON object has exactly these fields; unknown fields are errors rather than
silently accepted policy extensions. Duplicate JSON keys and non-finite numbers
are rejected. Input is UTF-8, at most 65,536 bytes.

| Field | Meaning |
| --- | --- |
| `schema_version` | Integer 1, not a boolean. |
| `record_kind` | `TEMPLATE`, `SYNTHETIC` or `OPERATIONAL`; classification is declared, not verified. |
| `work_id`, `project_id` | Stable identifiers for one invocation and its project. |
| `origin_role`, `incumbent_id` | Originating management role and continuing incumbent; neither grants authority. |
| `task_ref`, `authority_ref` | Opaque pointers to the bounded task and its authority; not dereferenced. |
| `session` | Exactly `entry`, `session_id`, `title`, `cwd`; unavailable provider metadata stays `UNKNOWN` or `NOT_EXPOSED`. |
| `events` | Ordered snapshots of observed entry, result return and management receipt. |

All text is nonempty, trimmed, no more than 512 characters, without ASCII control
characters. Core identity/task/authority placeholders yield `BLOCKED`. Missing
or extra fields, malformed values and contradictory transitions yield `INVALID`.
An unconfigured `TEMPLATE` always remains blocked.

`session.entry` is `CREATED`, `REUSED`, `RESUMED`, `REQUESTED_NOT_ENTERED` or
`UNKNOWN`. The first three are declarations of actual entry: do not set them
because an entry was merely requested. The last two must have no events and
remain blocked. Entered sessions with no start event are also blocked. An absent
provider session ID does not justify inventing one or claiming resumability.
The validator does not contact the provider to prove entry or resumption.

## Lifecycle and receipt

Each event has exactly `state`, `at`, `by_role` and `evidence_ref`. Valid histories
are nonempty prefixes of this sequence:

```text
ACTIVE -> DONE_UNACKED -> COMPLETED_ACKED
```

`ACTIVE` records observed entry; it does not prove that a process is still alive.
`DONE_UNACKED` records a returned result, including a failed, blocked or cancelled
result; it does not mean successful product delivery. `COMPLETED_ACKED` requires
`by_role` to match `origin_role` and a receipt evidence reference. This closes the
work-result receipt only. It is **not** merge approval, independent acceptance,
Human UAT, publication approval or proof that the project is complete.

`evidence_ref` should identify an entry observation, a returned result and a
management receipt respectively. The checker tests presence, not existence or
truth; a forged reference or actor declaration can still pass structural checks.
Role equality is not authentication. Real reviewers must inspect authoritative
records and retain their own separation of duties.

Event times must include seconds and an explicit UTC offset, for example
`2000-01-01T09:00:00Z` or `2000-01-01T17:00:00+08:00`. Known times are compared as
instants and must not decrease; equal seconds are allowed. `UNKNOWN`, `NOT_EXPOSED`
or `UNCONFIGURED` time/actor/evidence placeholders keep the result blocked. The
helper does not obtain time, read the local clock or authenticate timestamp
provenance. A real record must use its operator's governed trusted time source.
The example's dates are fictional fixtures, not observed events.

## Optional prior-snapshot comparison

```sh
python -B scripts/validate_work_history.py current.json --previous previous.json
```

The supplied previous record must be structurally `VALID`. All core and session
fields must remain equal, and the complete previous event list must be an exact
prefix of the new list. An identical snapshot is accepted; appending the next
valid event is accepted; event editing, truncation, identity changes and changed
context are rejected. Resolving a blocked starter is setup, not an append to an
already-valid history; do not pass the blocked starter as `--previous`.

The caller selects both snapshots. Without a trusted previous snapshot this
cannot detect rewritten history, and it provides no storage-level immutability.
Use a separate invocation record for changed session/context and governed current
state for corrections. A chat/device change does not create a new tenure;
this helper neither creates nor verifies a succession handoff. See
[Handoff and Succession](HANDOFF_AND_SUCCESSION.md).

## Trust boundary and scope

The CLI reads only the explicitly supplied regular, non-symlink JSON files and
prints a result; it never follows task/evidence/cwd pointers, writes records,
dispatches workers, sends messages, fetches credentials or changes Git. Basic input
checks are not a sandbox against concurrent filesystem mutation or a security
boundary for hostile local users. Do not supply files concurrently modified by
untrusted actors. Diagnostics for handled input errors do not echo record data or
filesystem paths; command-line usage errors are handled by argparse.

Operational records can contain private identifiers and paths: keep those in the
appropriate private instance, not this framework's future-public history. Public
examples must be independently authored fiction. A successful check is not a
privacy clearance, liveness check, authorization decision or independent review.

This slice is a standalone optional helper. Full multi-project demo integration,
Console/register wiring and real fresh-agent acceptance remain separate work.
