# Quickstart

## 1. Get the public OSS source

Create Private Factory is currently on post-v1.5 `main`, not the immutable
`v1.5.0` release. Install Git, Python 3.10+ and GitHub CLI (`gh`), authenticate
with `gh auth login`, then clone the public source without forking:

```sh
git clone https://github.com/AAAlcest/AI-Software-Factory-OSS.git
cd AI-Software-Factory-OSS
```

Keep this checkout clean and on the exact current `main`; the command checks
the local HEAD against the upstream Git remote and GitHub API before any write.

## 2. Create your private Factory

Preview first (read-only); use a new name under your authenticated GitHub user:

```powershell
py -3 -B scripts/create_private_factory.py --repository My-AI-Factory
py -3 -B scripts/create_private_factory.py --repository My-AI-Factory --apply
```

On macOS/Linux, substitute `python3` for `py -3`. The first invocation reads
GitHub identity/source/destination and prints the plan; it creates nothing.
`--apply` creates an independent **private, non-fork** repository with a fresh
Git history, an unconfigured/BLOCKED Factory starter, exact OSS source provenance
and MIT license, and an OPEN/UNLOCKED private documentation notice. It configures
the existing journal for that private repository, with writer disabled. No real
role/project appointment, existing private project import, or production authority
is inferred. V1 supports the authenticated user's own account and upstream `main`
only; a pre-existing destination fails closed. A partially failed apply is not
auto-deleted or automatically resumed; inspect it privately before retrying.

The source checkout remains a distribution/update surface; the **new private
repository** is the operating instance. Project code may remain in separate
private repositories, referenced only from the private Factory. Normal private
use does **not** require a GitHub Fork. A public fork is for OSS contribution,
public-safe evaluation or intentionally public work.

After creation, inspect the private repository and its notice, run the journal
manually with `dry_run=true`, then explicitly opt in with repository variable
`DOCUMENTATION_JOURNAL_ENABLED=true`. Only real bot write/readback and a repeat
without duplicate receipts can establish ACTIVE. Do not expose the private
repository identity or evidence in public OSS Issues.

## 3. Understand the split

Read [the recommended role setup](RECOMMENDED_ROLE_SETUP.md). Use ChatGPT for
Factory staff/management and Codex for engineering roles. A Human owns decisions;
no example appoints its reader. Unconfigured values remain unknown.

## 4. Get an exact release locally for the fictional exercise

For the `1.5.0` release line, use the exact `v1.5.0` tag rather than an arbitrary
future `main` when you want reproducible results.

### No Git: GitHub Source ZIP

Open the [v1.5.0 Release](https://github.com/AAAlcest/AI-Software-Factory-OSS/releases/tag/v1.5.0),
download **Source code (zip)**, extract it, and open a terminal in the extracted
repository directory.

### Git

```sh
git clone https://github.com/AAAlcest/AI-Software-Factory-OSS.git
cd AI-Software-Factory-OSS
git checkout v1.5.0
```

Confirm the version before continuing:

```sh
cat VERSION
```

On Windows PowerShell:

```powershell
Get-Content VERSION
```

It should print `1.5.0` for this release.

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
