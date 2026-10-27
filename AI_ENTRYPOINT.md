# AI ENTRYPOINT

## 1. Context before action

This is a reusable AI Software Factory framework, not an already-appointed
organization. A chat, tool, GitHub account or model is an execution surface, not
a durable role or authority source. Read AGENTS.md first.

Distinguish framework maintenance, an explicitly selected operating instance,
and a synthetic exercise. A real task chooses the context. Missing authority
never causes fallback to a convenient demo identity. `factory.yaml` and role
profiles are unconfigured defaults, not real assignments.

### Recommended first-contact Factory creation workflow

**Teach the chat-management / hands-on-development split during creation.**
As the Human's assisting AI, before offering `--apply`, explain:

- **Human + chat manager:** use ordinary conversation for careful reasoning,
  requirements, product direction, design, trade-offs and acceptance decisions.
  Routine discussion should not launch a coding/execution run or spend its
  execution allocation merely to talk through the work.
- **Chat manager -> developer:** write a precise task with context, work surface,
  scope, non-goals, acceptance criteria and required evidence. Management may
  read/write authorized GitHub records; this is not the same as entering a
  project development environment for routine planning.
- **Developer with hands:** use an authorized engineering environment to edit
  files, run commands, build, test and debug. A chat that prints code is not
  itself this execution capability.
- **Developer -> chat manager/Human:** return real artifacts and evidence.
  Management checks alignment with Human intent and decides the next scoped
  action, with independent review and Human-only approvals where required.

Recommend **one Human director, one chat-based manager and one hands-on project
engineering Agent** to start. Offer compatible management duties such as
Deputy/PDM, project management, records, governance and infrastructure planning;
add Development Lead/Console and appropriate reviewers as needed. First ask
which chat and engineering execution surfaces the Human actually has. Then
choose tools for each side. Vendors may differ, but **do not collapse routine
management into the coding executor and call that the same split**.

The purpose is to let the chat manager focus on thinking and management while
reserving development execution usage for actual implementation. This does
not promise that chat is free/unlimited, that every provider separates usage
pools, or that a fixed amount will be saved. Keep the operational distinction
clear rather than replacing it with an unrestricted vendor/role menu.

Present the proposal and seek Human confirmation **during this same creation
conversation**. Read [recommended setup](docs/RECOMMENDED_ROLE_SETUP.md) for
role responsibilities, provider examples and the actual handoff contract.
The preview still creates nothing; `--apply` creates a BLOCKED/UNCONFIGURED
private starter, not sessions or appointments. After verifying that private
repo, help record only Human-approved roles and scope **inside it**; leave
unknowns BLOCKED and never write private assignments into the public OSS.

When a fresh Agent enters this public OSS repository, **do not assume the OSS
distribution is the Human's operating Factory**. Determine the Human's intent
before creating operating state.

Use this routing:

1. **If the Human is maintaining/contributing to the OSS framework or doing a
   public-safe exercise:** remain in this repository (or an appropriate public
   fork) and follow the framework/evaluation workflow.
2. **If the Human already has a private operating Factory:** do not create another
   one. Enter the explicitly selected private repository and perform the normal
   full/minimal boot there.
3. **If the Human wants to start real private Factory operation and no private
   Factory exists yet:** treat this public repository only as the distribution
   source. Do not put real appointments, project state, company/customer data,
   credentials, correspondence, or private history into this public repository.
4. Verify the public source is the official OSS checkout and route to
   [Create your private Factory](docs/QUICKSTART.md#2-create-your-private-factory).
   The recommended first command is the read-only preview:

   ```powershell
   py -3 -B scripts/create_private_factory.py --repository <NEW_REPOSITORY_NAME>
   ```

   On macOS/Linux use `python3` instead of `py -3`.
5. Explain the preview result and privacy boundary to the Human. The preview must
   not create a repository, Issue, commit, variable, or other remote state.
6. Creating the private repository is a real external mutation. Run the
   `--apply` form only after explicit Human authorization:

   ```powershell
   py -3 -B scripts/create_private_factory.py --repository <NEW_REPOSITORY_NAME> --apply
   ```

7. After creation, verify the new repository is **private, independent/non-fork,
   and correctly owned/bound**, then move the operating context into that private
   repository. From that point, the private repository—not this OSS checkout—is
   the Factory operating instance.
8. Read the private repository's own `AGENTS.md`, `AI_ENTRYPOINT.md`,
   `SOURCE_PROVENANCE.json`, instance/authority/state records and current cursor.
   The generated starter is intentionally **BLOCKED / UNCONFIGURED**; repository
   access does not appoint a role or create project authority.
9. Continue the role plan discussed and approved with the Human as part
   of creation: read the new private instance's role recommendations and help
   record real appointments/authority only there. Leave any unapproved role
   BLOCKED/UNCONFIGURED. Project source may remain in separate private
   repositories and be referenced from the Factory.
10. Treat documentation-journal activation as a separate acceptance step: first
    manual dry run, then explicit repository-local opt-in, then real bot
    write/readback and no-duplicate replay. Do not infer ACTIVE from creation alone.

This is the recommended normal-use path. **Forking the public OSS repository is
not required to create a private Factory**; Fork is primarily for OSS contribution,
public-safe evaluation, or an intentionally public Factory.

## 2. Choose the boot depth

Use the **full initial boot** when the Factory/instance is new to you, the role or
project is unclear, authority/environment may have changed, the task crosses
projects or retained gates, or an audit/recovery exercise explicitly requires the
broader model.

Use the **minimal safe boot** only when all of these are already explicit and
current: selected operating instance, selected project/role, bounded work surface,
and no known authority/environment conflict. Minimal boot is a progressive-
disclosure path, not permission to skip authority checks.

### Minimal safe boot for a bounded scoped task

1. Read the selected instance's current authority/state pointer and the specific
   project/role state needed for the task.
2. Read the active Issue/PR/work item, current checkpoint/CURRENT pointer and last
   relevant evidence. If a cockpit/Project view exists, use it only as a derived
   index to those canonical sources.
3. Verify exact Git/ref and environment facts that materially affect the task.
4. Identify retained Human gates, blockers, unresolved facts and next safe action.
5. Expand into mechanism docs, older history or additional projects only when a
   concrete dependency, conflict, missing fact, authority change or audit need is
   discovered.

If any prerequisite is unknown, fall back to the full initial boot or stop the
affected action fail-closed.

## 3. Full initial boot order

1. Read [the short model](docs/AI_FACTORY_IN_30_SECONDS.md),
   [roles](docs/ROLES_AND_AUTHORITY.md), [role setup](docs/RECOMMENDED_ROLE_SETUP.md)
   and the [Execution-First contract](docs/EXECUTION_FIRST.md).
2. Read [the instance boot protocol](docs/INSTANCE_BOOT_PROTOCOL.md), then resolve
   the original assignment and current authority/state for the selected instance.
3. Read [facilities](docs/FACILITIES_AND_SURFACES.md),
   [GitHub workflow](docs/GITHUB_NATIVE_WORKFLOW.md),
   [correspondence](docs/CORRESPONDENCE_AND_CC.md),
   [mailbox/Console](docs/PROJECT_MAILBOX_AND_CONSOLE.md),
   [Work History](docs/WORK_INVOCATION_WARDROBE.md),
   [continuity](docs/HANDOFF_AND_SUCCESSION.md) and [privacy](docs/PUBLIC_PRIVACY_STANDARD.md).
4. If the instance exposes a [Project cockpit](docs/CHATGPT_PROJECT_COCKPIT.md), use
   it as a **derived index** to select the smallest relevant Office/Project/Issue
   source set. Never treat cockpit text or a skill output as newer authority than
   the repository records it references.
5. Follow the selected role/project task and unprocessed primary working surface
   (Issue/PR or inbox according to the actual workflow), verify relevant Git/ref
   and environment facts, then current cursor and pending work. Report conflicts.
6. Identify current role, known scope, unresolved facts, gates, evidence
   and next safe action. A helper's VALID output does not complete this process.

When explanation or provenance for a durable framework rule is needed, consult the
[Design Rationale Index](docs/DESIGN_RATIONALE_INDEX.md) only after this
current-authority skeleton. Rationale/history never overrides current authority.

For a real successor, read the finalized predecessor record unchanged, then
reconcile newer state. For same-incumbent recovery do not fabricate a new tenure.
For a first incumbent do not fabricate a predecessor handoff.

## 4. Default operational picture

Human + ordinary chat manager reason and decide -> manager issues a bounded
task and acceptance criteria -> hands-on engineering Agent implements/tests ->
chat manager inspects evidence and gives a scoped disposition -> independent
review and Human-retained decisions where applicable.

**Management is real thinking, design and oversight, not only message routing.**
Keep ordinary management work in chat rather than opening coding sessions for
it. A manager may use authorized repository connectors; a developer needs the
actual engineering environment. Execution Agents still make implementation
judgments and escalate material product decisions rather than guessing.

Providers can change on either side, but provider choice does not erase this
working split. The [ChatGPT + Codex example profile](profiles/chatgpt-codex.json)
is one optional illustration; Claude or other suitable chat/development tools
may fill equivalent surfaces when capabilities and authority are verified.
Compatible chat-side staff duties may be combined, as may Development Lead
and Console engineering duties; this is not advice to make the coding executor
do all the planning under a different title. Independent review stays separate
from the author where required. No fixed quota savings are promised.

The optional [Skills layer](docs/SKILLS_LAYER.md) can compress Factory/project/role
context and build bounded engineering task packages. Skills reduce repeated context;
they do not grant authority or replace freshness checks.

## 5. Execute authorized work and inspect health

After authority is established, follow
[Execution-First](docs/EXECUTION_FIRST.md): authorized, executable and unblocked
work should be performed and verified rather than acknowledged only. Status claims
need observable evidence. Stop at `DONE`, `BLOCKED`, `HUMAN_ACTION_REQUIRED`
or `AUTHORIZED_BOUNDARY_REACHED`; none of these rules expands authority or
bypasses retained gates.

For a read-only local health snapshot, use:

```sh
python -B scripts/factory_doctor.py --json
```

Add `--github` only when read-only GitHub CLI/auth/repository checks are useful.
Doctor PASS is diagnostic evidence only: `execution_authorized` remains false.

## 6. Continue without re-onboarding every turn

After initial boot, refresh new/unprocessed messages and changed relevant files.
Do not repeat a full Factory audit, old handoffs or unrelated office records for
a small task. Expand the bounded inspection when authority/environment changes,
a concrete conflict or defect appears, or an actual audit is assigned. Current
repository facts still override a remembered summary or rolling cursor.

Finish authorized work and post the result in its original Issue/PR; avoid
kickoff/received/ACK-to-ACK cycles and duplicate mail records. A short Human-facing
wake-up may identify the next action role, repository and Issue/PR. A posted
comment does not prove another chat or worker was dispatched.

## 7. Boundaries and final acceptance

Issues coordinate decisions; PRs hold exact candidate changes and evidence.
Review intensity is proportional to risk and explicit authority. A Human may
permit continuous private-staging integration with concentrated final acceptance;
that does not erase defects, independent review or retained Human gates.

Use only synthetic, newly authored examples. Never import private history or
rename real correspondence/handoffs into distributable fixtures. No implicit
credentials, production/destructive, external-company, license or publication
authority exists. Unknown facts remain UNKNOWN and the affected action stops.

For current product scope see [V1 status](docs/V1_BASELINE_STATUS.md).
Use [the generated demo](docs/QUICKSTART.md) for an offline exercise,
[the evaluator runbook](docs/COLD_TAKEOVER_EXERCISE.md) for actual fresh-Agent
validation, and [Fresh Factory Audit](docs/FRESH_FACTORY_AUDIT.md) for a read-only
consistency/recoverability audit. Final privacy/public-safety review and Human
release decisions remain separate from tests and staging commits.
