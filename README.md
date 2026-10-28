# AI Software Factory OSS

**A Quirmn product.**

[简体中文](README.zh-CN.md)

A **provider-neutral** framework for Human-led software work. Humans set
direction; **user-chosen AI management roles** plan and coordinate; capable
**engineering Agents** implement and test. You choose the models and tools.
Repository-backed roles, authority, state and evidence survive conversations,
but a model identity or credential never grants organizational authority.

## 5-minute Quick Demo

**What:** See a fictional Factory's role/project/authority records checked locally, rather than watching a conceptual slideshow.  
**Try:** [**Run the 5-minute Quick Demo →**](docs/QUICK_DEMO.md) — Python 3.10+, no AI account, API key or private Factory needed.  
**Failure behavior:** The synthetic Atlas records can be structurally `VALID`, while an unconfigured starter deliberately returns `BLOCKED` (exit `3`). Both keep `execution_authorized: false`; neither appoints an Agent or authorizes execution.  
**Architecture:** [Repository-first roles and projects](docs/AI_FACTORY_IN_30_SECONDS.md) → [explicit instance authority](docs/INSTANCE_BOOT_PROTOCOL.md) → read-only validation. No automatic agent dispatch, cloud deployment or production action.

By keeping planning, governance, task routing and review coordination in
chosen management AI roles, and using capable engineering Agents primarily for
coding and tests, the Factory aims to avoid unnecessary coding-agent quota or
token consumption. **ChatGPT + Codex is one optional pairing**, not a
requirement; Claude, Gemini, Claude Code and other suitable tools can fill
appropriate roles. Actual savings depend on workload and tools; no fixed
token, cost or subscription saving is guaranteed.

**Source version line: 1.7.1.** This patch clarifies chat-based management
and hands-on engineering during private-Factory creation. The bootstrap preview
points to role guidance, and new private starters include that guide. It retains
the v1.7.0 diagnostics, Quick Demo, journal defaults and minimal private upgrade;
see the release notes for the complete delta from v1.7.0.

`VERSION` identifies these source bytes; **it does not mean a GitHub Release
has already been published**. Consult [GitHub Releases](https://github.com/AAAlcest/AI-Software-Factory-OSS/releases)
and [v1.7.1 packaging coordination](https://github.com/AAAlcest/AI-Software-Factory-OSS/pull/59)
for the actual published tag and approval. Historical tags remain unchanged.
See [1.7.1 release notes](docs/releases/1.7.1.md),
[1.7.0 historical release notes](docs/releases/1.7.0.md),
[1.6.0 historical release notes](docs/releases/1.6.0.md),
[1.5.0 historical release notes](docs/releases/1.5.0.md),
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
This source version's bootstrap verifies either exact official current `main`
or its matching **official `v1.7.1` release tag once published**. Until the
v1.7.1 tag exists, follow the most recent **published** release for normal
stable use; a proposed tag is not a valid checkout.

**Already have a private Factory?** Use the [provenance-checked minimal upgrade](docs/PRIVATE_FACTORY_UPGRADE.md): default read-only preview, conflict refusal, and (only after explicit authorization) a private draft PR. No upstream fork-sync, operating-state overwrite or automatic merge.

**New Human user and your assisting AI Agent:** while creating your own
Factory, first review the [provider-neutral role recommendations](docs/RECOMMENDED_ROLE_SETUP.md)
and decide who should manage, develop and review. The [Quickstart](docs/QUICKSTART.md)
and [AI entrypoint](AI_ENTRYPOINT.md) bring these suggestions directly into
the **creation flow**. ChatGPT + Codex is just one optional example. Explore
the [synthetic Factory instance](examples/factory-instance/README.md)
without making any real appointments.

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

**Operational discipline and health:** once work is actually authorized, use the
[Execution-First contract](docs/EXECUTION_FIRST.md) so evidence-backed action replaces
ACK-only narration. [`python -B scripts/factory_doctor.py --json`](docs/FACTORY_DOCTOR.md) provides a portable
read-only Factory/repository health snapshot; Doctor PASS never grants authority.
The [Design Rationale Index](docs/DESIGN_RATIONALE_INDEX.md) explains selected public
rules and provenance without becoming a second authority source.

**Want to audit an operating Factory:** use [Fresh Factory Audit](docs/FRESH_FACTORY_AUDIT.md)
or choose the Fresh Factory Audit template from GitHub **New issue**.

Recommended staffing: **Human director + chosen AI management roles +
capable engineering Agents + independent review as needed**. A Deputy can
combine compatible record/governance/planning duties; Development Lead and
Console can be combined. ChatGPT + Codex is one optional example; no vendor
combination is required. Independent acceptance remains separate from its
author, and Work/execution sessions should be used proportionately.

## Project cockpit, recovery and bounded work

**Management chat approaching its limit?** [FlowThread](https://flowthread.quirmn.com/)
can help you search and export an available ChatGPT conversation as Markdown,
PDF or other supported formats before moving to a new chat. Keep that archive
as background for recovery or a real tenure handoff, alongside—not instead of—the
current repository records. See [conversation backup and handoff](docs/HANDOFF_AND_SUCCESSION.md#conversation-backup).

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

**Chats have limits. Your work history should not end there.**

**[FlowThread](https://flowthread.quirmn.com/)** is an independent **Quirmn
product**, incubated through this Factory and used in its author's daily work.
Its current public product is a browser extension for long ChatGPT conversations:
keep long chats easier to use, search earlier messages in context, and export
the available active conversation branch as **PDF, Markdown, TXT, HTML or JSON**.
Visit the product site for current platform support and installation.

For a Factory's chat-based manager, this is a practical recovery and tenure-handoff
tool. Before moving away from a long conversation or one nearing its limit, save
an available conversation export as a private work archive. It can preserve
requirements, design choices, rejected alternatives and unresolved questions
that a short handoff summary cannot fully explain. Use Markdown to provide
relevant background to a new AI chat, or PDF for a readable human archive.

**Factory keeps roles, current state and handoffs continuous; FlowThread helps
you keep the conversations in which that work happened.** Export → check the
archive → update the recovery/handoff summary → give the new chat only the
background it needs and verify current repository evidence. See the
[English / 中文 backup guidance](docs/HANDOFF_AND_SUCCESSION.md#conversation-backup).

Changing chats alone is recovery, not automatically a new tenure. An export is
supporting history—not automatic AI-memory transfer, a substitute for current
repository authority, or a guarantee of recovering unavailable messages.
Keep private transcripts out of public forks and Issues.

**Using AI Software Factory does not require installing or purchasing FlowThread.**
Use another appropriate export tool when preferred or when your chat platform
is not supported. FlowThread is both a real product example and an optional
workflow aid, not a framework dependency.

[Explore FlowThread and installation →](https://flowthread.quirmn.com/)

## What V1 includes

Configurable Human/executive/role bundles; offices and project rooms; current and
pending records; Issue meetings and exact-candidate PRs; optional one-body mail,
Reply-All and visibility-only CC; Console/open-loop records; Work result receipts;
first appointment, same-incumbent recovery and authorized true-succession examples;
repeatable software checks; a nine-variant cold-start package; Project cockpit and
skills; executable cockpit/Project-view generation and drift checks; work-item
checkpoints for bounded long-thread recovery; a reusable Fresh Factory Audit
pattern with synthetic governance-drift examples; the V1.5 first-use routing,
release-acquisition, minimal-safe-boot and native-audit-entry improvements; and the
V1.6 repository documentation notice, active documentation journal, opt-in
public-fork bootstrap, independent private-Factory bootstrap, release-tag source
provenance and fresh-Agent private-Factory routing.

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
