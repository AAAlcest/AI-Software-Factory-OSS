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

**Version 1.5.0 is the latest published release of AI Software Factory OSS.**
It keeps the v1.4 bounded-recovery/audit model and adds first-use productization:
clearer Human/AI/audit routing, exact-release local acquisition, Windows-friendly
first-run guidance, a minimal safe AI boot, explicit static-cockpit labeling and a
native Fresh Factory Audit Issue entry.

Current `main` also contains **post-v1.5, unreleased maintenance improvements**:
a durable repository documentation notice, an active GitHub-native documentation
change journal, an opt-in self-setup path for public direct forks, and a
**Create Private Factory** path that creates a new independent private operating
repository without requiring Fork. These main-only improvements are not part of
the immutable `v1.5.0` tag unless and until
a later release publishes them. Published-release status is authoritative on
GitHub Releases and the release coordination Issue; historical tags are never
moved to follow later `main` changes.
See [1.5.0 release notes](docs/releases/1.5.0.md),
[1.4.0 historical release notes](docs/releases/1.4.0.md),
[1.0.0 historical release notes](docs/releases/1.0.0.md) and
[security reporting](SECURITY.md).

## Start here

**Documentation notice:** [repository index and change journal](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/26).
The opening body routes readers to canonical docs; comments record changes. See the
[notice/journal contract](docs/REPOSITORY_NOTICES.md). The [journal is active in this repository](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/28#issuecomment-5736870432): configured documentation changes on `main` and observed PR candidates are recorded asynchronously, not on each local save. A fork does **not** inherit the notice or active writer; see [fork setup](docs/DOCUMENTATION_JOURNAL.md#fork-self-setup).

**Create your private Factory (normal use):** clone this public OSS source and
run the [read-only private-bootstrap preview](docs/QUICKSTART.md#2-create-your-private-factory)
before explicitly applying it. This creates a **new independent private repository**;
normal private use does **not** require Fork. The operating starter remains
BLOCKED/unconfigured and its journal writer remains off until separately accepted.
This post-v1.5 `main` feature is not in the immutable `v1.5.0` release.

**New Human user:** open the [Quickstart](docs/QUICKSTART.md), then the
[recommended ChatGPT + Codex role setup](docs/RECOMMENDED_ROLE_SETUP.md). If you
want to understand the shape before running anything, browse the
[synthetic Factory instance](examples/factory-instance/README.md).

**Fork this repository (contributors/public-safe evaluation):** a GitHub fork is **public OSS/distribution space, not
the default home for a private operating Factory**. A fork receives the files, but
not this repository's notice Issue or active journal state. Use the public-fork
[journal self-setup](docs/DOCUMENTATION_JOURNAL.md#fork-self-setup) only for
public-safe evaluation, framework maintenance/contribution, or an intentionally
public Factory. **Do not put private projects, assignments, customer/company data,
or private Factory history into a public fork.**

For real private work, use the private-bootstrap command above to create a
**separate private operating repository** from the framework/starters. Project source
repositories may remain separate private repositories referenced by that Factory.
The public fork can remain only as an upstream/update/contribution copy. See
[private instance guidance](docs/QUICKSTART.md#8-instance-and-source-remain-separate).

For a public direct GitHub.com fork whose default branch is `main`, the journal
self-setup can create that fork's own notice and prepare its writer configuration.
If Issues are disabled, `--apply` enables them there after repository/admin
verification; the default check remains read-only. Activation remains explicit:
the fork owner reviews the generated changes, enables Actions, opts in, and verifies
a real bot write/readback plus a no-duplicate replay.

**AI Agent:** read [AGENTS.md](AGENTS.md), then [AI_ENTRYPOINT.md](AI_ENTRYPOINT.md).
A fresh Agent must first decide whether it is doing OSS/framework work, public-safe
evaluation, or real private Factory operation. If the Human wants real private work
and no private Factory exists yet, the recommended path is:

```text
public OSS distribution
→ read-only Create Private Factory preview
→ explain the plan/privacy boundary
→ explicit Human authorization
→ create NEW independent private repository
→ verify private/non-fork binding
→ continue real operating work inside that private Factory
```

Do not put real private assignments, project state, customer/company records or
private history into this public OSS repository. If a private Factory already
exists, enter that instance instead of creating another one. The Agent may route to
and perform the read-only preview, but `--apply` creates remote GitHub state and
requires explicit Human authorization. Detailed first-contact routing lives in
[AI_ENTRYPOINT.md](AI_ENTRYPOINT.md). For an already-selected, low-risk bounded
task, use the minimal safe boot described there instead of rereading the entire
mechanism set.

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
checkpoints for bounded long-thread recovery; a reusable Fresh Factory Audit
pattern with synthetic governance-drift examples; the V1.5 first-use routing,
release-acquisition, minimal-safe-boot and native-audit-entry improvements; and,
on current post-v1.5 `main`, the repository documentation notice, active
documentation journal, opt-in public-fork journal bootstrap, and independent
private-Factory bootstrap for normal private use.

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
