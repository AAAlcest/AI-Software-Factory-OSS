# AI Software Factory OSS

A repository-first operating framework for Human-led software work with AI
management and coding agents. Roles, authority, project state and evidence
survive a conversation; a model name or account credential never grants authority.

**1.0.0 publication preparation, private staging; not yet released.**
The Human owner selected the [MIT License](LICENSE) and GitHub Private
Vulnerability Reporting, without publishing a personal email address.
Completed engineering, fresh-Agent and privacy results remain pinned to their
reviewed targets in Issue #1. This license/security/documentation-only preparation
preserves that evidence; it is not a new execution or independent certification.
Public visibility and Release publication still require explicit Human approval.
See [prepared release notes](docs/releases/1.0.0.md) and [reporting availability](SECURITY.md).

## Start with the useful path

Humans: [quickstart](docs/QUICKSTART.md), [中文上手说明](docs/QUICKSTART_ZH.md),
and [recommended ChatGPT + Codex roles](docs/RECOMMENDED_ROLE_SETUP.md).
AI agents: [AGENTS.md](AGENTS.md), then [AI_ENTRYPOINT.md](AI_ENTRYPOINT.md).

Recommended setup: **ChatGPT for Factory staff and management; Codex for project
development, Development Lead and Console.** The deputy may combine records,
governance maintenance and infrastructure planning. Keep independent acceptance
separate from its author; use Work sparingly, not for routine status/ACK cycles.
This is a configurable operating recommendation, not a vendor permission rule.

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

## Product example: FlowThread

**FlowThread** is a real product incubated through this AI Software Factory and
used by its author in day-to-day AI development and collaboration. Problems found
in actual use can feed back into the Factory workflow, while the Factory provides
a durable way to keep improving the product.

This repository demonstrates the **working method**. FlowThread demonstrates the
kind of **real product** that can be built with that method.

**Using AI Software Factory does not require installing or purchasing FlowThread.**
FlowThread is a product example and author workflow tool, not a framework
dependency, required companion app or condition of using this repository.

## What V1 includes

Configurable Human/executive/role bundles; offices and project rooms; current and
pending records; Issue meetings and exact-candidate PRs; optional one-body mail,
Reply-All and visibility-only CC; Console/open-loop records; Work result receipts;
first appointment, same-incumbent recovery and authorized true-succession examples;
repeatable software checks; and a nine-variant package for eight cold-start cases.

This is not an autonomous scheduler, authorization service, production deployment
system or authenticated mail transport. Its helpers check declared consistency;
read [the limits and readiness status](docs/V1_BASELINE_STATUS.md).

## Before publication

Follow the [publication checklist](docs/PUBLICATION_CHECKLIST.md),
[public privacy standard](docs/PUBLIC_PRIVACY_STANDARD.md) and
[cold-start evaluator procedure](docs/COLD_TAKEOVER_EXERCISE.md).
Do not import private histories, rename real messages into examples, commit
credentials, change license terms or change repository visibility implicitly.

The MIT license covers this distribution. The unconfigured publication defaults
in `factory.yaml` and synthetic Human gates concern separately operated instances;
they do not add restrictions to the MIT license or approve other projects' releases.

[Documentation index](docs/README.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md)
