# V1 baseline — candidate slice A

Coordination: repository Issue #1. This page describes the bounded deliverable;
review state, exact candidate HEAD and execution evidence belong in its PR.
It is not a second source of appointment, license or publication authority.

## Candidate contents

The first implementation connects a deterministic instance boot protocol,
strict read-only JSON preflight, an intentionally blocked starter, reusable
Office/Project Room templates and a synthetic Atlas boot exercise. It targets
Issue #1's boot/authority/facilities/state foundation rather than the whole V1.

Start with [the boot protocol](INSTANCE_BOOT_PROTOCOL.md), then
[the template guide](../templates/README.md) and
[the demo guide](../examples/demo-factory/README.md).

The current automated tests check declared identity, scope, missing authority,
reserved actions, first appointment/recovery/succession, input errors, references
and read-only behavior. These are software tests, not cold-agent acceptance.
The compact boot fixture is not the promised end-to-end multi-project Factory.

## Explicit remaining work under Issue #1

Correspondence/Reply-All helpers and complete message/reference fixtures;
Portfolio Console/register examples; the full Atlas/Beacon demo including PR
candidate/review/integration readback; Wardrobe transition examples; actual
fresh-agent CT-01 through CT-08 execution; independent governance/privacy review;
and any separately authorized integration remain open.

Human license selection and publication/visibility decisions are separate from
V1 staging completion. No checkbox, tool return or successful test waives them.

## Verification discipline

Use `python -m unittest discover -s tests -v` and the two CLI examples in the boot
protocol. Record tested HEAD, interpreter/platform, commands, observed results
and skips. Preserve `NOT_RUN` for fresh-agent tests until a genuinely separate
agent/session has run them without inherited conversation context. An author
cannot certify their own independent review.

Review an exact candidate. Any later implementation commit changes the review
target and requires appropriate revalidation. Store result reports outside the
candidate or record their precise tested code tree so that adding a report does
not falsely claim its own commit was already tested.
