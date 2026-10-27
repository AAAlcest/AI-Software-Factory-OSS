# Quickstart

## 1. Get the public OSS source

For reproducible private-Factory creation, prefer the latest **published**
[GitHub Release](https://github.com/AAAlcest/AI-Software-Factory-OSS/releases)
and verify its exact tag. This source line is **1.7.1**; its `v1.7.1` tag is
usable **only after publication**. Until then, use the latest actually published release
(currently `v1.7.0` at packaging time). Install Git, Python 3.10+ and GitHub CLI (`gh`), then clone
the official source without forking:

```sh
git clone https://github.com/AAAlcest/AI-Software-Factory-OSS.git
cd AI-Software-Factory-OSS
git checkout --detach v1.7.1  # only after v1.7.1 is published
gh auth login
```

Keep the checkout clean. This source version's private-bootstrap command accepts
either exact official current `main` or the exact official release tag matching
`VERSION` (here `v1.7.1` once published). It verifies local HEAD, origin ref
and GitHub API before any write. Do not treat a proposed tag as already available.
Stable users should prefer a real published release tag over moving `main`.

GitHub Source ZIP is still fine for the fictional/offline exercises below, but the
private-bootstrap command requires Git metadata and therefore uses a Git checkout.

## 2. Create your private Factory

**First: let your AI Agent recommend a team *while you create* the Factory.**
Before using `--apply`, read the
[provider-neutral role recommendations](RECOMMENDED_ROLE_SETUP.md) with
your assisting Agent. Start with a Human director, an AI management role
(planning, task packaging and acceptance) and a tool-capable engineering
Agent (code/tests), plus independent review when needed. The Human may add
Deputy/PDM, project manager, secretary, governance, infrastructure,
Project Primary and Development Lead/Console roles as useful.

Ask your Agent to explain the positions, ask which models and tools you have
(ChatGPT, Claude, Gemini, Codex, Claude Code or any compatible alternatives),
and discuss combined roles and first project ownership. **No provider is
required.** Confirm a proposed role map **during this creation conversation**.
Bootstrap remains noninteractive: `--apply` creates a private, BLOCKED
starter, not live sessions or permissions; once the private repository is
verified, continue setting up only the roles and scope the Human approved.
This is the same guided building process, not a separate wizard.

Preview first (read-only); use a new name under your authenticated GitHub user.
Version 1.7.1 source defaults **new** private Factories to the lower-run
`manual` journal cadence:

```powershell
py -3 -B scripts/create_private_factory.py --repository My-AI-Factory
py -3 -B scripts/create_private_factory.py --repository My-AI-Factory --apply
```

To explicitly keep automatic push/signal/hourly journal reconciliation after later
activation, add `--journal-mode automatic` to both preview and apply.

On macOS/Linux, substitute `python3` for `py -3`. The first invocation reads
GitHub identity/source/destination and prints the plan; it creates nothing.
`--apply` creates an independent **private, non-fork** repository with a fresh
Git history, an unconfigured/BLOCKED Factory starter, exact OSS source provenance
and MIT license, and an OPEN/UNLOCKED private documentation notice. It configures
the existing journal for that private repository, with writer disabled. No real
role/project appointment, existing private project import, or production authority
is inferred. This source line supports the authenticated user's own account,
current exact official `main` or exact official version-matching release tag
(after publication); a pre-existing destination fails closed. A partially failed apply is not
auto-deleted or automatically resumed; inspect it privately before retrying.

The source checkout remains a distribution/update surface; the **new private
repository** is the operating instance. Project code may remain in separate
private repositories, referenced only from the private Factory. Normal private
use does **not** require a GitHub Fork. A public fork is for OSS contribution,
public-safe evaluation or intentionally public work.

After creation, inspect the private repository and its notice. **On the 1.7.1
source line**, newly generated private starters include
`docs/EXECUTION_FIRST.md`, `RATIONALE_INDEX.md` and the portable read-only
Doctor. The immutable older `v1.6.0` tag predates this hardening.
From a starter that contains Doctor:

```sh
python -B scripts/factory_doctor.py --json
```

Doctor PASS remains diagnostic only and never appoints a role or authorizes work.
Staff Office Notes, when adopted, are [event-driven deltas](STAFF_OFFICE_NOTES.md),
not daily reporting.

The generated journal configuration records `cadence_mode`. In default `manual`
mode, there are no automatic push/PR/hourly journal wake-ups; freshness advances
only after an authorized manual reconcile. `automatic` mode retains the previous
trigger cadence. Neither mode is activated by repository creation.

Then run the journal manually with `dry_run=true`, and explicitly opt in with
repository variable
`DOCUMENTATION_JOURNAL_ENABLED=true`. Only real bot write/readback and a repeat
without duplicate receipts can establish ACTIVE. Do not expose the private
repository identity or evidence in public OSS Issues.

## 2a. Upgrade an existing private Factory (separate lifecycle)

If you already have an independent private Factory, **do not recreate it** or
sync it through a public Fork. Read the [minimal, provenance-checked framework
upgrade](PRIVATE_FACTORY_UPGRADE.md) first. Its default command is read-only;
with separate explicit authorization, `--apply` creates a **private draft PR**
only. This first slice replaces three exact-copy framework files, stops on
user edits and does not change private operating state, journal configuration,
credential settings, branch visibility or target `main`.

## 3. Understand the split

Read the [provider-neutral role setup](RECOMMENDED_ROLE_SETUP.md) **with
your assisting AI during Factory creation**. Assign management, engineering
and review responsibilities to whichever models/tools fit your capabilities,
permissions and preferences. ChatGPT + Codex is an optional example only.
A Human owns decisions; no example appoints its reader, and unknown
assignments remain UNCONFIGURED.

## 4. Get an exact release locally for the fictional exercise

For source version `1.7.1`, prefer the exact `v1.7.1` tag **after its
publication** rather than an arbitrary future `main` for reproducibility.
Until that tag is publicly available, the previous stable `v1.7.0` release
remains a usable historical source with its older feature set.

### No Git: GitHub Source ZIP

After `v1.7.1` is published, open the [v1.7.1 Release](https://github.com/AAAlcest/AI-Software-Factory-OSS/releases/tag/v1.7.1),
download **Source code (zip)**, extract it, and open a terminal in the extracted
repository directory. Before publication, use the latest **actually published**
release instead. ZIP mode is for local/synthetic exercises; private bootstrap and
upgrade require a Git checkout.

### Git

```sh
git clone https://github.com/AAAlcest/AI-Software-Factory-OSS.git
cd AI-Software-Factory-OSS
git checkout --detach v1.7.1  # after publication
```

Confirm the version before continuing:

```sh
cat VERSION
```

On Windows PowerShell:

```powershell
Get-Content VERSION
```

It should print `1.7.1` for the published v1.7.1 tag; before publication, use the actual version of the older released checkout.

## 5. Run the fictional exercise locally

Use Python 3.10+. No package installation or AI credential is needed for the
scripts. Choose a new sibling directory:

```sh
python -B scripts/create_demo.py --destination ../factory-first --case first
python -B scripts/validate_demo.py ../factory-first
python -B scripts/validate_instance.py --root ../factory-first/projects/atlas
python -B scripts/plan_reply.py ../factory-first/reply-request.json
python -B scripts/validate_work_history.py ../factory-first/offices/management/wardrobe/atlas.json
```

On Windows where `python` is not the configured launcher, use the same commands
with `py -3` instead, for example:

```powershell
py -3 -B scripts/create_demo.py --destination ../factory-first --case first
py -3 -B scripts/validate_demo.py ../factory-first
py -3 -B scripts/check_all.py
```

The builder is the only command above that creates files, and only in its new
explicit destination. A pre-existing destination is rejected; it is never erased.
The generated entrypoint explains where authority, state, inbox, current/pending,
Console and immutable continuity records live. All records are fictional.

Atlas has a declared assignment and a changed candidate requiring new review.
Beacon has no current assignment. Console sees both; it cannot create a worker.
The reply planner's output matches the generated recipient body and sent/CC
references. Work completion acknowledges a BLOCKED result, not product success.

## 6. Verify the distribution

```sh
python -B scripts/check_all.py
```

Or on Windows:

```powershell
py -3 -B scripts/check_all.py
```

It runs all tests, checks local Markdown file targets/JSON syntax, and exercises
all nine generated variants through the three helper contracts. It reports
actual test counts/skips and interpreter/platform. Nonzero means fix the reported
problem; never call a skipped or blocked check a PASS. No external link uptime,
semantic privacy, real authority, fresh-agent behavior or production is verified.

## 7. Browse current recovery/cockpit behavior

The checked-in [synthetic Factory](../examples/factory-instance/README.md) is useful
for browsing. Its `project-cockpit/` directory is a static teaching snapshot; read
its own instructions before assuming it is the newest generated schema. To produce
current schema-2 derived output, run:

```sh
python -B scripts/generate_cockpit.py --root examples/factory-instance --output ../generated-cockpit
python -B scripts/generate_project_view.py --root examples/factory-instance --output ../project-view
```

Generated output is derived context, not authority. Repository state/evidence stays
canonical.

## 8. Instance and source remain separate

Use the command in [Create your private Factory](#2-create-your-private-factory)
and [the starters](../templates/README.md), not copied private histories. Put
real assignments, state, credentials policy and operational records in your own
authorized operating repository; do not fill them into this distributable repo.
Record the Human, explicit role scope, reporting line, current project repository
and environment. Framework `factory.yaml` is configuration guidance, not that
assignment record. A copied template intentionally remains BLOCKED until those
facts are supplied. This guide does not authorize access to an external company.

## 9. Use normal work surfaces

For a bounded task, discuss scope and decisions in an Issue; put implementation,
exact target, tests and review in a PR. Avoid parallel email/ACK bookkeeping.
Optional Factory mail still supports cross-role routing with one canonical body.
Keep current state and unresolved work durable, not hidden in a chat.

For actual fresh-agent verification use [the evaluator procedure](COLD_TAKEOVER_EXERCISE.md).
For a read-only consistency/recoverability audit use [Fresh Factory Audit](FRESH_FACTORY_AUDIT.md)
or choose its template from GitHub **New issue**. Those are separate observed runs,
not the walkthrough or software test suite.
