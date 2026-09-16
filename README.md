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

**Version 1.4.0 is the current published release line of AI Software Factory OSS.**
It consolidates the Project cockpit and skills, executable derived views and drift
checks, work-item checkpoints and bounded long-thread recovery, and the Fresh
Factory Audit pattern. The immutable `v1.4.0` tag points to the exact published
release commit recorded in Issue #19; do not move it. Historical `v1.0.0` evidence
remains pinned to its original reviewed targets and is not presented as having
rerun on later bytes.
See [1.4.0 release notes](docs/releases/1.4.0.md),
[1.0.0 historical release notes](docs/releases/1.0.0.md) and
[security reporting](SECURITY.md).

## Start here

**New Human user:** open the [Quickstart](docs/QUICKSTART.md), then the
[recommended ChatGPT + Codex role setup](docs/RECOMMENDED_ROLE_SETUP.md). If you
want to understand the shape before running anything, browse the
[synthetic Factory instance](examples/factory-instance/README.md).

**AI Agent:** read [AGENTS.md](AGENTS.md), then [AI_ENTRYPOINT.md](AI_ENTRYPOINT.md).
For an already-selected, low-risk bounded task, use the minimal safe boot described
there instead of rereading the entire mechanism set.

**Want to audit an operating Factory:** use [Fresh Factory Audit](docs/FRESH_FACTORY_AUDIT.md)
or choose the Fresh Factory Audit template from GitHub **New issue**.

Recommended setup: **ChatGPT for Factory staff and management; Codex for project
development, Development Lead and Console.** The deputy may combine records,
governance maintenance and infrastructure planning. Keep independent acceptance
separate from its author; use Work sparingly, not for routine status/ACK cycles.
This is a configurable operating recommendation, not a vendor permission rule.

## Project cockpit, recovery and bounded work

The operating layers include an optional [ChatGPT Project cockpit](docs/CHATGPT_PROJECT_COCKPIT.md)
for Factory/project/role overview, [workstream recovery](docs/WORKSTREAM_RECOVERY.md),
[work-item checkpoints and Project-ready visibility](docs/WORK_ITEMS_AND_PROJECT_VIEW.md),
and bounded Codex task packages while the repository remains canonical truth.
The [skill contracts](skills/README.md) standardize overview, recovery, handoff,
health and task packaging; the [token-efficiency design](docs/TOKEN_EFFICIENCY.md)
explains how to measure the benefit without promising a fixed saving percentage.

The checked-in fictional cockpit is a **static teaching snapshot**. Its own
[Project instructions](examples/factory-instance/project-cockpit/PROJECT_INSTRUCTIONS.md)
explain that current schema-2 output should be generated when you want the latest
work-item/checkpoint package shape.

## Fresh Factory Audit

Use the [Fresh Factory Audit](docs/FRESH_FACTORY_AUDIT.md) pattern when you want a
new AI context to test whether an operating Factory can still be reconstructed
safely from current repository evidence. The audit prefers bounded current-state
reads, expands into chronology only for concrete conflicts, classifies governance
and recovery drift, and reports findings for later Human/management disposition
without self-authorizing fixes.

Copy-ready starters are available as a
[consolidated audit Issue template](templates/FRESH_FACTORY_AUDIT_ISSUE.md) and a
[fresh auditor prompt](templates/FRESH_FACTORY_AUDITOR_PROMPT.md). The
[synthetic audit example](examples/factory-instance/audit/README.md) demonstrates
fictional drift patterns such as missing project visibility, frozen-work
resurrection, superseded direction and stale recovery queues. It contains no
private Factory audit history.

## Browse a Factory before generating one

Open the checked-in [synthetic Factory instance](examples/factory-instance/README.md)
to browse Staff Offices, Project Rooms, Factory state, registers, a Meeting Hall,
mailbox/reference examples, a Work receipt and a handoff archive shape directly in
GitHub. It is public-safe fictional material, not a copy or redaction of any private
Factory. Use it to understand the layout; use `scripts/create_demo.py` when you want
deterministic disposable fixtures for validation.

## Try the integrated fictional Factory

Python 3.10+; no third-party Python dependencies, model API key or cloud deployment
is required for these local exercises. The [Quickstart](docs/QUICKSTART.md) shows
how to get an exact release locally with or without Git, including Windows-friendly
commands. From a checkout of this repository:

```sh
python -B scripts/create_demo.py --destination ../example-factory --case first
python -B scripts/validate_demo.py ../example-factory
python -B scripts/validate_cockpit.py --root examples/factory-instance
python -B scripts/check_all.py
```

The destination must not exist. The builder creates synthetic files only; it does
not create repositories, agents or credentials. The validator connects instance,
reply-routing and Work History contracts over a real generated Office/Project
Room/mailbox/Console layout. Cockpit validation checks only derived bundle structure.
`VALID` still grants no authority, sends no mail and is not an actual fresh-agent result.

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
repeatable software checks; a nine-variant cold-start package; Project cockpit and
skills; executable cockpit/Project-view generation and drift checks; work-item
checkpoints for bounded long-thread recovery; and a reusable Fresh Factory Audit
pattern with synthetic governance-drift examples.

This is not an autonomous scheduler, authorization service, production deployment
system or authenticated mail transport. Its helpers check declared consistency;
read [the limits and readiness status](docs/V1_BASELINE_STATUS.md).

## Publication and security

Use the [publication checklist](docs/PUBLICATION_CHECKLIST.md),
[public privacy standard](docs/PUBLIC_PRIVACY_STANDARD.md) and
[cold-start evaluator procedure](docs/COLD_TAKEOVER_EXERCISE.md) in proportion to
change risk. Do not import private histories, rename real messages into examples,
commit credentials, or silently change license/authority boundaries.

The MIT license covers this distribution. The unconfigured publication defaults
in `factory.yaml` and synthetic Human gates concern separately operated instances;
they do not add restrictions to the MIT license or approve other projects' releases.

[Documentation index](docs/README.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md)
