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
9. Human-approved real roles/projects/authority are configured only inside the
   private Factory. Project source may remain in separate private repositories and
   be referenced from the Factory.
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
   [roles](docs/ROLES_AND_AUTHORITY.md) and [role setup](docs/RECOMMENDED_ROLE_SETUP.md).
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
6. Identify current role, known scope, unresolved facts, retained gates, evidence
   and next safe action. A helper's VALID output does not complete this process.

For a real successor, read the finalized predecessor record unchanged, then
reconcile newer state. For same-incumbent recovery do not fabricate a new tenure.
For a first incumbent do not fabricate a predecessor handoff.

## 4. Default operational picture

Human owner -> ChatGPT management/staff -> Codex engineering/project execution.
The deputy may combine compatible staff duties, while the Development Lead may
also carry Console visibility. The [recommended profile](profiles/chatgpt-codex.json)
is replaceable and grants no execution rights. An independent reviewer must be
separate from the author, even when staff titles are combined. Keep Work exceptional.

The optional [Skills layer](docs/SKILLS_LAYER.md) can compress Factory/project/role
context and build bounded Codex task packages. Skills reduce repeated context; they
do not grant authority or replace freshness checks.

## 5. Continue without re-onboarding every turn

After initial boot, refresh new/unprocessed messages and changed relevant files.
Do not repeat a full Factory audit, old handoffs or unrelated office records for
a small task. Expand the bounded inspection when authority/environment changes,
a concrete conflict or defect appears, or an actual audit is assigned. Current
repository facts still override a remembered summary or rolling cursor.

Finish authorized work and post the result in its original Issue/PR; avoid
kickoff/received/ACK-to-ACK cycles and duplicate mail records. A short Human-facing
wake-up may identify the next action role, repository and Issue/PR. A posted
comment does not prove another chat or worker was dispatched.

## 6. Boundaries and final acceptance

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
