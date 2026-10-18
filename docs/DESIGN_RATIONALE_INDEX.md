# Design Rationale Index

Status: **HISTORICAL EXPLANATION / NAVIGATION ONLY — NOT CURRENT AUTHORITY**

This index explains why selected framework rules exist and points to the current
authority plus public provenance. It does not copy private operating history, and it
never overrides current Git, instance authority/state, an active Issue/PR, a Human
decision or verified environment facts.

Use it after the current-authority boot path when a rule needs explanation,
modification, audit or conflict resolution. Historical rationale is evidence to
check, not an executable instruction.

## Entry schema

Each entry should contain:

- `rationale_id`
- `title`
- `status`
- `rule_or_surface`
- `current_authority`
- `originating_failure_mode_or_problem`
- `why_the_rule_exists`
- `introduced_by`
- `provenance_links`
- optional `superseded_by` / `supersession_scope`
- `last_verified_against_current_authority`
- `notes`

## Public framework rationales

### `OSS-R001` — Repository evidence outranks derived context

- status: `ACTIVE`
- rule_or_surface: boot, recovery and generated cockpit/project views
- current_authority: `AI_ENTRYPOINT.md`, `docs/INSTANCE_BOOT_PROTOCOL.md`
- originating_failure_mode_or_problem: summaries, generated views and remembered
  chat context can be stale or incomplete.
- why_the_rule_exists: current repository authority/state/ref/evidence is inspectable
  and versioned; derived context remains useful navigation without becoming a second
  truth source.
- introduced_by: public V1 recovery/cockpit model and later bounded-recovery work.
- provenance_links: `docs/AI_FACTORY_IN_30_SECONDS.md`,
  `docs/WORKSTREAM_RECOVERY.md`, `docs/WORK_ITEMS_AND_PROJECT_VIEW.md`.
- last_verified_against_current_authority: current `main` for Issue #45 candidate.
- notes: missing/conflicting facts remain UNKNOWN or block the affected action.

### `OSS-R002` — Recovery is not succession

- status: `ACTIVE`
- rule_or_surface: role continuity and handoffs
- current_authority: `docs/HANDOFF_AND_SUCCESSION.md`,
  `docs/INSTANCE_BOOT_PROTOCOL.md`
- originating_failure_mode_or_problem: a new chat/session can be mistaken for a new
  organizational tenure, creating invented predecessor/successor history.
- why_the_rule_exists: continuity is an organizational fact, not a session boundary;
  only a true authorized incumbent change creates a succession record.
- introduced_by: public continuity model.
- provenance_links: `docs/HANDOFF_AND_SUCCESSION.md`,
  `examples/factory-instance/offices/management/handoffs/README.md`.
- last_verified_against_current_authority: current `main` for Issue #45 candidate.
- notes: finalized historical handoffs do not override fresher verified current state.

### `OSS-R003` — Public distribution and private operating Factory are separate

- status: `ACTIVE`
- rule_or_surface: normal private Factory creation
- current_authority: `README.md`, `AI_ENTRYPOINT.md`, `docs/QUICKSTART.md`
- originating_failure_mode_or_problem: a public fork can be mistaken for the place
  to store real appointments, projects, company/customer facts and private history.
- why_the_rule_exists: public OSS is the distribution/contribution surface; real
  private operation needs an independent private repository and explicit authority.
- introduced_by: Issue #37 / PR #38, with first-contact routing in PRs #40/#41.
- provenance_links: Issue #37, PR #38, PR #40, PR #41, v1.6.0 release notes.
- last_verified_against_current_authority: current `main` for Issue #45 candidate.
- notes: Fork remains useful for contribution/public-safe evaluation but is not
  required for normal private use.

### `OSS-R004` — Documentation journal notice remains OPEN / UNLOCKED

- status: `ACTIVE`
- rule_or_surface: repository documentation notice and journal writer
- current_authority: `docs/DOCUMENTATION_JOURNAL.md`, Issue #26
- originating_failure_mode_or_problem: a locked Issue produced a real
  `LOCKED_CONVERSATION` delivery failure for the repository-owned writer.
- why_the_rule_exists: an OPEN / UNLOCKED notice preserves the tested bot-write path;
  provenance/identity checks, not public-comment trust, establish recorder receipts.
- introduced_by: Issue #28 and PR #31.
- provenance_links: Issue #28, PR #31, Issue #26.
- last_verified_against_current_authority: current `main` for Issue #45 candidate.
- notes: public comments are not recorder commands or trusted receipts.

### `OSS-R005` — Execution status requires observable evidence

- status: `ACTIVE`
- rule_or_surface: authorized Agent execution behavior
- current_authority: `docs/EXECUTION_FIRST.md`
- originating_failure_mode_or_problem: acknowledgement, narration or future-tense
  promises can be mistaken for actual execution and leave authorized work unfinished.
- why_the_rule_exists: execution evidence makes status recoverable and prevents
  "I will do it" from being recorded as work already performed.
- introduced_by: Issue #45 / PR #46 operational-hardening extraction.
- provenance_links: Issue #45 and PR #46.
- last_verified_against_current_authority: Issue #45 candidate.
- notes: this changes execution discipline, never authority or retained gates.

### `OSS-R006` — Staff Office Notes are event-driven deltas, not daily reports

- status: `ACTIVE`
- rule_or_surface: Staff Office recovery/execution notes
- current_authority: `docs/STAFF_OFFICE_NOTES.md`,
  `templates/STAFF_OFFICE_TEMPLATE.md`
- originating_failure_mode_or_problem: chronological work logs can grow into duplicate
  truth surfaces, empty heartbeat files and expensive recovery context.
- why_the_rule_exists: meaningful deltas preserve useful recovery evidence while
  keeping CURRENT concise and canonical work/evidence in the proper Issue/PR/state
  surfaces.
- introduced_by: Issue #47 / PR #48 operating-efficiency extraction.
- provenance_links: Issue #47, PR #48,
  `docs/WORK_ITEMS_AND_PROJECT_VIEW.md`.
- last_verified_against_current_authority: Issue #47 candidate.
- notes: date-based filenames are grouping only; no daily reporting obligation.

### `OSS-R007` — New private Factories default to manual journal cadence

- status: `ACTIVE`
- rule_or_surface: private documentation-journal trigger cadence
- current_authority: `docs/DOCUMENTATION_JOURNAL.md`,
  `scripts/create_private_factory.py`
- originating_failure_mode_or_problem: AI-native repositories can create bursts of
  valid commits/events; automatic push/signal/hourly journal wake-ups multiply
  GitHub Actions runs even when the recorder integrity model itself is sound.
- why_the_rule_exists: manual cadence preserves the same explicit dry-run/opt-in,
  recorder, receipt and replay model while removing automatic journal/signal runner
  wake-ups for newly created private Factories. Users who value continuous freshness
  can explicitly choose automatic cadence.
- introduced_by: public CI-cost field note #44 and Issue #47 / PR #48.
- provenance_links: Issue #44, Issue #47, PR #48,
  `docs/DOCUMENTATION_JOURNAL.md`.
- last_verified_against_current_authority: Issue #47 candidate.
- notes: this is a freshness/cadence decision, not a guarantee of billed-minute or
  monetary savings; public OSS #26 keeps its existing automatic cadence.

## Adding a rationale

Add an entry only when the rule is durable enough to merit explanation. Prefer
links/pointers over copied Issue/PR bodies. If the current rule changes, update the
entry's current-authority/supersession pointers without rewriting historical facts.
