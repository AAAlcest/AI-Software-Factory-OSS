# Demo Factory

All examples here are fictional. They do not encode real organization facts,
private conversations, actual appointments or real operating evidence.

## Implemented candidate: compact Atlas boot fixture

The [boot/instance.json](boot/instance.json) manifest selects a fictional Human,
role and project with separate [authority](boot/authority.json),
[assignment](boot/ASSIGNMENT.md), [state](boot/state.json) and
[current cursor](boot/CURRENT.md). This deliberately flat fixture exercises the
boot contract; it is not yet a complete multi-project Factory layout.

From the repository root:

```sh
python scripts/validate_instance.py --root examples/demo-factory/boot
```

Expected: `VALID`, exit 0, and `execution_authorized: false`. The result proves
only structural consistency of declarations. It neither appoints the reader
nor authorizes real work. Tests mutate copies in temporary directories, never
these checked-in records. No fictional timestamp, commit or PR is represented
as actual runtime evidence.

## Fresh-agent exercise — not executed by this fixture

Give a genuinely fresh session only this repository at the exact candidate HEAD
and a read-only exercise task: start at root AGENTS, follow the entrypoint, use
this synthetic instance, report its declared role/scope and identify why no real
authority follows. Do not provide earlier conversations or private repositories.
Record supplied inputs, observed references/actions, expected versus observed
behavior and PASS / FAIL / BLOCKED / NOT_RUN. A scripted validator invocation is
not that agent run. The remaining CT-01 through CT-08 matrix lives in Issue #1.

## Remaining fictional scenario

The full demo will use Example Corp, Project Atlas and Project Beacon, a Human
Factory Director, a configurable primary management AI, separate Governance and
Runtime roles, and Project Primaries. It will connect Offices, Project Rooms,
mailboxes, Issue deliberation, PR candidates/review/readback, Console visibility,
Wardrobe records and true succession. Those end-to-end fixtures are not yet
implemented by this first boot slice.
