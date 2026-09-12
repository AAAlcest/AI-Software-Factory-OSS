# Workstream recovery and supersession-aware cockpit

Long-lived Issues can accumulate hundreds of comments, multiple implementation lanes, superseded decisions, external gates and partial results. A fresh agent should not have to replay the entire chronology merely to discover the current safe action.

The V1.2 workstream model adds a **derived recovery index**, not a replacement authority layer.

## Three layers

- **Issue / PR / Project-visible item** — visible work surface and authority/evidence pointer.
- **Workstream register** — thin repository-local management index that points at the current lane, controlling references, superseded references, blockers, Human gates and next action.
- **Generated cockpit** — disposable context package for overview, recovery and bounded Codex execution.

The generated cockpit must never turn a summary or fingerprint into authority. If its text conflicts with the referenced work surface or canonical state, refresh the source and treat the bundle as stale.

## Why supersession matters

A long-running work surface may contain an old decision that was correct at the time and later replaced. Recovery therefore needs two explicit sets:

- `controlling_refs` — the references that currently define accepted direction;
- `superseded_refs` — historical references that remain evidence but must not be replayed as current direction.

The cockpit may say “do not reopen as current” for superseded references, but it does not decide that supersession itself. The register must point to the canonical work evidence that established it.

## Workstream lanes

A single project may carry independent lanes such as identity, export, deployment, documentation, privacy review or external provider setup. Each lane should expose:

- project;
- owner role;
- Project-visible work surface;
- status and priority;
- controlling and superseded references;
- blockers;
- Human/external gate when applicable;
- next safe action.

This prevents a blocked external-provider lane from hiding progress in an unrelated implementation lane and prevents one giant Issue from becoming the only usable recovery interface.

## Drift

`generate_cockpit.py` fingerprints the repository-local sources used to generate a bundle. `check_cockpit_drift.py` can later report changed or missing inputs.

A fingerprint answers only **“did these bytes change?”** It does not answer **“is this authorized?”** or **“is this decision still valid?”**. Authority and current direction still come from the referenced canonical sources.

## Bounded Codex packaging

The selected workstream determines the smallest default read set for Codex: the project room/state, owner-role current cursor and workstream register. Codex expands scope only when a concrete dependency, conflict or missing fact appears.

This is the intended context-efficiency mechanism: preserve correctness by keeping exact pointers, while avoiding routine replay of unrelated Factory history.
