# AI Software Factory OSS

**A Quirmn product.**

[简体中文](README.zh-CN.md)

A repository-first operating framework for Human-led software work with AI
management and coding agents. Roles, authority, project state and evidence
survive a conversation; a model name or account credential never grants authority.

By keeping planning, governance, task routing and review coordination in ChatGPT
while reserving Codex for implementation-heavy work, the Factory is designed to
materially reduce unnecessary Codex token consumption. Combined with reusable
skills and role-specific workflows, it can increase utilization across the AI
toolchain and improve the practical return from the same token and subscription
budget. Actual savings depend on workload, model choice and how the Factory is
configured; this is an operating-efficiency goal, not a guaranteed quota result.

**Version 1.0.0 is the first public release line of AI Software Factory OSS.**
The repository is public, distributed under the [MIT License](LICENSE), and uses
GitHub Private Vulnerability Reporting without publishing a personal email address.
Completed engineering, fresh-Agent and privacy results remain pinned to their
reviewed targets in Issue #1; later public-surface documentation changes use
proportionate delta checks rather than pretending those acceptance steps reran.
See [1.0.0 release notes](docs/releases/1.0.0.md) and [security reporting](SECURITY.md).

## Start with the useful path

Humans: [quickstart](docs/QUICKSTART.md), [中文上手说明](docs/QUICKSTART_ZH.md),
and [recommended ChatGPT + Codex roles](docs/RECOMMENDED_ROLE_SETUP.md).
AI agents: [AGENTS.md](AGENTS.md), then [AI_ENTRYPOINT.md](AI_ENTRYPOINT.md).

Recommended setup: **ChatGPT for Factory staff and management; Codex for project
development, Development Lead and Console.** The deputy may combine records,
governance maintenance and infrastructure planning. Keep independent acceptance
separate from its author; use Work sparingly, not for routine status/ACK cycles.
This is a configurable operating recommendation, not a vendor permission rule.

## Browse a Factory before generating one

Open the checked-in [synthetic Factory instance](examples/factory-instance/README.md)
to browse Staff Offices, Project Rooms, Factory state, registers, a Meeting Hall,
mailbox/reference examples, a Work receipt and a handoff archive shape directly in
GitHub. It is public-safe fictional material, not a copy or redaction of any private
Factory. Use it to understand the layout; use `scripts/create_demo.py` when you want
deterministic disposable fixtures for validation.

## Try the integrated fictional Factory

Python 3.10+; no third-party Python dependencies, model API key or cloud deployment
is required for these local exercises. From this repository:

```sh
python -B scripts/create_demo.py --destination ../example-factory --case first
python -B scripts/validate_demo.py ../example-factory
python -B scripts/check_all.py
```

The destination must not exist. The builder creates synthetic files only; it does
not create repositories, agents or credentials. The validator connects instance,
reply-routing and Work History contracts over a real generated Office/Project
Room/mailbox/Console layout. `VALID` still grants no authority, sends no mail and
is not an actual fresh-agent result. Use a new destination for another case.

The distribution also includes the original compact [scenario](examples/demo-factory/scenario/WALKTHROUGH.md),
[reusable starters](templates/README.md), PR/Issue templates and focused examples.
A generated Factory is not a duplicate copy of product source trees.

## Product example: [FlowThread](https://flowthread.quirmn.com/)

**[FlowThread](https://flowthread.quirmn.com/)** is another **Quirmn product**—a
real product incubated through this AI Software Factory and used by its author in
day-to-day AI development and collaboration. Problems found in actual use can
feed back into the Factory workflow, while the Factory provides a durable way to
keep improving the product.

This repository demonstrates the **working method**. FlowThread demonstrates the
kind of **real product** that can be built with that method.

**Using AI Software Factory does not require installing or purchasing FlowThread.**
FlowThread is a product example and author workflow tool, not a framework
dependency, required companion app or condition of using this repository.

Learn more about FlowThread: https://flowthread.quirmn.com/

## What V1 includes

Configurable Human/executive/role bundles; offices and project rooms; current and
pending records; Issue meetings and exact-candidate PRs; optional one-body mail,
Reply-All and visibility-only CC; Console/open-loop records; Work result receipts;
first appointment, same-incumbent recovery and authorized true-succession examples;
repeatable software checks; and a nine-variant package for eight cold-start cases.

This is not an autonomous scheduler, authorization service, production deployment
system or authenticated mail transport. Its helpers check declared consistency;
read [the limits and readiness status](docs/V1_BASELINE_STATUS.md).

## Release and safety

For 1.0.0 and future releases, follow the [publication checklist](docs/PUBLICATION_CHECKLIST.md),
[public privacy standard](docs/PUBLIC_PRIVACY_STANDARD.md) and
[cold-start evaluator procedure](docs/COLD_TAKEOVER_EXERCISE.md) when the changed
surface requires them. Do not import private histories, rename real messages into
examples, commit credentials or silently change license/authority boundaries.

The MIT license covers this distribution. The unconfigured publication defaults
in `factory.yaml` and synthetic Human gates concern separately operated instances;
they do not add restrictions to the MIT license or approve other projects' releases.

[Documentation index](docs/README.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md)
