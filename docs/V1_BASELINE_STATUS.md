# V1 public baseline

Version: see [VERSION](../VERSION). The current published release line is **1.4.0**.
The repository is public, distributed under MIT, and uses GitHub Private
Vulnerability Reporting. Exact Git targets, executed checks, review evidence and
release readbacks remain on the corresponding repository Issues/PRs rather than
being flattened into this summary.

This page is a product-status summary, not an appointment record, an independent
acceptance result, or release authorization.

## Implemented scope

The V1 line now includes the original repository-first role/authority/state model,
Staff Offices, Project Rooms, Issue/PR coordination, correspondence/CC, Console,
Work History, continuity exercises, deterministic synthetic Factory generation and
cold-start fixtures, plus the later bounded-management layers:

- ChatGPT Project cockpit for Factory/project/role overview and bounded recovery;
- reusable overview/recovery/handoff/health/task-packaging skill contracts;
- executable cockpit generation, source fingerprints and stale-bundle drift checks;
- Project-ready Markdown/JSON/CSV management export without GitHub Project mutation;
- work-item checkpoints with controlling/superseded refs, last evidence, Human gates
  and next safe actions;
- bounded long-thread recovery and Codex task packaging;
- Fresh Factory Audit documentation, copy-ready templates and synthetic governance-
  drift stress cases.

A checked-in [browseable synthetic Factory instance](../examples/factory-instance/README.md)
shows Staff Offices, Project Rooms, Factory state, registers, checkpoints, derived
cockpit views, audit examples, mailbox/reference examples, Work history and handoff
shapes without exposing any private Factory. The generated demo remains the
deterministic validation path.

Generated cockpit, Project view, manifests and audit reports are derived context.
They do not replace canonical repository evidence and do not authorize execution,
remediation, release, publication, deployment or credential/production actions.

## Verification and limits

Run `python -B scripts/check_all.py`. Its output records actually observed software
tests, skips, docs/JSON checks and synthetic integration checks. CI is ordinary
engineering evidence, not an independent privacy reviewer or a fresh AI session.
`VALID`, `FRESH`, `PASS_WITH_FINDINGS`, `PLANNED`, `COMPLETED_ACKED` and fixture
states retain their narrower meanings; none grants real authority or publication
approval.

Only platform/interpreter combinations with returned execution evidence are
verified. A configured CI matrix is not evidence it ran. Relative file links, not
external link availability or all Markdown anchors, are mechanically checked.
Filesystem guards are not sandboxes against concurrent mutation by a hostile local
actor.

The public helpers check declarations and repository relationships. They do not
prove organizational authority, evidence authenticity, provider isolation, live
security boundaries, external-system access, or production permission.

## Evidence carried forward

The original behavioral baseline remains
`41a1b127daa69308839490eecf06fbb82ee2cb8c` (`1.0.0-rc.2`). The historical
`v1.0.0` tag is fixed at `e9b9a61648746ffa64c32043a076af28d445bd30`.
Its [fresh-Agent result](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/1#issuecomment-5561859245)
and [privacy closeout](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/1#issuecomment-5561877291)
remain PASS in their recorded scopes. They are retained as historical evidence for
those exact targets, not claimed as runs on later bytes.

Later feature evidence remains scoped to the corresponding work surfaces:

- V1.1: Issue #6 and PRs #8/#9;
- V1.2: Issue #10 and PRs #12/#14;
- V1.3: Issue #15 and PR #16; CI run `35021376274`; fresh-context recovery
  acceptance comment `5687990205`;
- V1.4: Issue #17 and PR #18; CI run `35026380398` on Ubuntu/Windows ×
  Python 3.10/3.13;
- v1.4.0 release consolidation/publication: Issue #19 and PR #20; RC CI run
  `35058489632`; final tag/release readback on the exact published target.

The V1.3 fresh-context result demonstrates bounded recovery for that accepted
synthetic work-item/checkpoint path. The post-release v1.4.0 Fresh product
acceptance recorded `PASS_WITH_FINDINGS`: cold recovery, bounded Codex handoff and
Fresh Factory Audit usability passed without whole-history replay or authority
confusion, while discoverability/onboarding findings were retained for later
productization. Neither result is described as a blanket privacy certification of
all future `main` bytes.

## Current release line

Current release decisions and boundaries:

- Version line: **1.4.0**.
- License: **MIT**, included as [LICENSE](../LICENSE).
- Security channel: **GitHub Private Vulnerability Reporting**, enabled; no personal
  email is published. See [SECURITY.md](../SECURITY.md).
- Repository visibility: **Public**.
- Historical release tag: `v1.0.0`, immutable and never to be moved.
- Current published tag: `v1.4.0` ->
  `15f5c4c6b4a8b325385c3b7a0d4c10ccd790858f`; it must not be moved after
  publication.
- GitHub Release: `AI Software Factory OSS 1.4.0`, published as the latest release.
- Release notes: [1.4.0](releases/1.4.0.md) and historical
  [1.0.0](releases/1.0.0.md).

Issue #19 is the canonical release-consolidation/publication evidence surface for
1.4.0. Its RC SHA, automated CI, explicit Human publication authorization, exact
tag target and final readback are historical release evidence.

Earlier slice-specific reviews remain historical scoped evidence, not blanket
approval of later bytes. Later `main` documentation/productization changes must use
current proportionate validation and must not move the immutable published tag or
pretend historical fresh-Agent/privacy evidence reran.
