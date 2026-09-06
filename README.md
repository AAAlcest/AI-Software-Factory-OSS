# AI Software Factory OSS

An AI-native software factory framework for coordinating roles, projects, governance, evidence, and GitHub-native workflows.

## Start here

For humans: read this README, then `docs/AI_FACTORY_IN_30_SECONDS.md`.

For AI agents: read `AGENTS.md` first, then follow `AI_ENTRYPOINT.md`.

## What this repository is

This repository is a reusable operating framework for running software work with Human leadership and multiple AI/agent execution surfaces. It separates organizational authority from technical credentials, keeps project state durable outside chat history, and specializes GitHub Issues and Pull Requests as first-class Factory coordination surfaces.

Core ideas include:

- configurable executive/deputy management roles rather than one mandatory title;
- Staff Offices, Project Rooms, Project Mailboxes and portfolio visibility;
- GitHub Issues as meeting / coordination surfaces;
- Pull Requests as Candidate Change Envelopes;
- one-canonical-body correspondence with `SENT_REFERENCE` and `CC_REFERENCE`;
- Work Invocation History / Office Wardrobe for execution-session continuity;
- immutable append-only tenure handoffs with same-incumbent recovery kept separate from succession;
- deny-by-default privacy and trust boundaries.

## Current maturity

This repository is an early private staging build. Documentation and synthetic examples are being assembled before any public release decision.

No license is selected yet. Public visibility and publication are separate Human decisions.

## V1 candidate baseline

The first bounded implementation connects a deterministic instance boot protocol,
reusable templates, a synthetic boot fixture and a read-only preflight. See
[the candidate scope and remaining work](docs/V1_BASELINE_STATUS.md),
[the boot protocol](docs/INSTANCE_BOOT_PROTOCOL.md) and
[the template guide](templates/README.md).

With Python 3.10 or later and no third-party dependencies:

```sh
python scripts/validate_instance.py --root examples/demo-factory/boot
python -m unittest discover -s tests -v
```

The synthetic fixture expects `VALID` (exit 0), which is structural consistency,
not actual authority. The unconfigured `templates/instance` starter intentionally
returns `BLOCKED` (exit 3). Every result keeps `execution_authorized: false`.
Fresh-agent acceptance, full demo completion and independent review are separate
work; successful unit tests do not prove them or authorize publication.
