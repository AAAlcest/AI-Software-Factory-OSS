# Synthetic Fresh Factory Audit example

This directory demonstrates how a **Fresh Factory Audit** can report governance/recovery drift without copying any real private Factory incident.

Everything here is fictional. The names `Atlas`, `Beacon`, `role:management`, `role:runtime` and the `fixture:*` references belong to the public synthetic Factory example.

## What this example demonstrates

The sample report intentionally models a **counterfactual drifted variant** of the fictional Factory. It is not a claim that the checked-in `examples/factory-instance/` currently contains all of these defects.

The variant demonstrates six common failure patterns:

1. **Missing project visibility** — an active fictional project is recoverable from its Project Room but omitted from a central roll-up.
2. **Frozen-work resurrection** — a project is frozen locally while an older role cursor still lists reconciliation as active.
3. **Superseded HOLD** — a later fictional authorization exists but an older management summary still presents the HOLD as current.
4. **Stale publication/state propagation** — a fictional visibility/release transition is recorded on the canonical work surface but not propagated to an older Project State.
5. **Stale recovery queue** — `CURRENT` or `pending` retains already resolved work.
6. **Orphaned draft PR** — a visible draft candidate describes a meeting state that has already been finalized elsewhere.

These patterns are useful because each can mislead a fresh AI **without necessarily breaking the underlying project-local authority model**.

## Audit principle

The auditor should first attempt bounded recovery:

```text
Factory entrypoint
  -> central visibility
  -> selected Project Room / Staff Office
  -> current work item / checkpoint / evidence
  -> next safe action
```

If a contradiction appears, expand only to the evidence needed to resolve that contradiction.

## Files

- [`SAMPLE_AUDIT_REPORT.md`](SAMPLE_AUDIT_REPORT.md) — a fictional consolidated audit result using the standard finding classes and dispositions.

The sample is documentation, not actual independent audit evidence. It grants no authority and performs no remediation.
