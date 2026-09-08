# V1 public baseline

Version: see [VERSION](../VERSION). The current delivery line is **1.0.0**.
The repository is public, distributed under MIT, and uses GitHub Private
Vulnerability Reporting. Exact Git targets, executed checks, review evidence and
final release readback are recorded in repository Issue #1.

This page is a product-status summary, not an appointment record or an independent
acceptance result.

## Implemented scope

AI-first entry and bounded refresh; configurable role/staffing profile; instance,
Office and Project Room starters; exact-candidate PR and Issue templates; one-body
reply routing; visibility-only Console; declaration-only Work History; static
Atlas/Beacon scenario; deterministic generation of a full fictional office/project/
mailbox layout; combined validation through all three helper contracts; and nine
fixture variants covering the eight cold-start cases, including positive authorized
true succession and same-incumbent recovery.

A checked-in [browseable synthetic Factory instance](../examples/factory-instance/README.md)
shows Staff Offices, Project Rooms, Factory state, registers, a Meeting Hall,
mailbox/reference examples, Work history and handoff shapes without exposing any
private Factory. The generated demo remains the deterministic validation path.

The integrated generator materializes the educational layout rather than copying
an organization's operational files. It has no automatic worker, transport,
credential, server or publication operation. Existing compact examples remain
available as focused teaching material, not competing real project truth.

## Verification and limits

Run `python -B scripts/check_all.py`. Its output records actually observed software
tests, skips, docs/JSON checks and synthetic integration checks. CI is ordinary
engineering evidence, not an independent privacy reviewer or a fresh AI session.
`VALID`, `PLANNED`, `COMPLETED_ACKED` and historical fixture integration each retain
their narrower meanings; none grants real authority or publication approval.

Only platform/interpreter combinations with returned execution evidence are
verified. A configured CI matrix is not evidence it ran. A symlink skip on a
platform must remain visible. Relative file links, not external link availability
or all Markdown anchors, are mechanically checked. Filesystem guards are not
sandboxes against concurrent mutation by a hostile local actor.

The preflight's large-integer JSON exception has an explicit regression test:
malformed/unsupported input returns INVALID rather than an uncaught traceback.

## Accepted baseline and release packaging

The behavioral baseline is `41a1b127daa69308839490eecf06fbb82ee2cb8c`
(`1.0.0-rc.2`). Its [fresh-Agent result](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/1#issuecomment-5561859245)
and [privacy closeout](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/1#issuecomment-5561877291)
are PASS in their recorded scopes. CT-05 was actually rerun; the other eight
observations were retained after input-equivalence verification. The earlier
failure and shared-host isolation limitation remain in the evidence history.
Existing exact-head CI results are retained, not claimed as a run on later
publication-only changes.

Changes after rc.2 are publication packaging and public-facing documentation/example
surfaces: MIT licensing, PVR instructions/status, version metadata, Quirmn branding,
bilingual README content, the FlowThread product example and the browseable
synthetic Factory instance. Core validators, generator behavior, tests, profiles,
root Agent entrypoints and workflow definitions remain unchanged. These additions
receive proportionate delta checks instead of a full behavioral/fresh-Agent rerun.

Current release decisions:

- License: **MIT**, included as [LICENSE](../LICENSE).
- Security channel: **GitHub Private Vulnerability Reporting**, enabled; no personal
  email is published. See [SECURITY.md](../SECURITY.md).
- Repository visibility: **Public**.
- Release tag: `v1.0.0`, fixed to the exact final release commit when created.
- GitHub Release: use [the 1.0.0 release notes](releases/1.0.0.md) and record the
  final tag/Release readback in Issue #1.

Earlier slice-specific reviews remain historical scoped evidence, not blanket
approval of later bytes. The consolidated release workflow reuses accepted evidence
for unchanged behavior while requiring proportionate inspection of new public
surfaces. Issue #1 is the durable release closeout surface.
