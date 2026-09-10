# ChatGPT Project cockpit

The Project cockpit is an optional Human-facing operating layer for an AI Software Factory. It can live in a ChatGPT Project or an equivalent persistent workspace, but it is **not** a new source of authority or current truth.

## Canonical-truth rule

**Repository records remain canonical.** The cockpit is a derived index and context-compression surface over Factory state, Staff Offices, Project Rooms, Issues/PRs and evidence.

If a cockpit summary conflicts with a repository source, refresh the source and report the conflict. Do not repair the conflict by trusting memory, a chat title, a model identity, a connected account or an older summary.

## What the cockpit should answer

A useful Factory-level cockpit should make these questions cheap to answer:

- What projects exist and what state is each project in?
- Who is the current Project Primary or owner for each project?
- Which Factory roles are involved in each project?
- Which projects are currently attached to a role?
- What is blocked, stale, waiting for evidence or waiting for a Human gate?
- What changed since the last reliable checkpoint?
- What is the next safe action?
- What bounded context should be sent to Codex?

## Recommended Project files

A Project-facing bundle normally contains:

- `PROJECT_INSTRUCTIONS.md` — stable operating rules for the Project workspace;
- `FACTORY_OVERVIEW.md` — top-level state, blockers, open loops and Human gates;
- `PROJECTS.md` — compact project-by-project view;
- `ROLES.md` — compact role-by-role view;
- `RECOVERY_BRIEF.md` — first-appointment, recovery or true-succession context;
- `HEALTH.md` — stale/unowned/blocked/missing-evidence findings;
- `CODEX_TASK_PACKAGE.md` — bounded engineering context for one implementation task.

The reusable starter is [PROJECT_COCKPIT_TEMPLATE.md](../templates/PROJECT_COCKPIT_TEMPLATE.md). A fully fictional example is under [examples/factory-instance/project-cockpit](../examples/factory-instance/project-cockpit/PROJECT_INSTRUCTIONS.md).

## Refresh protocol

Use the cockpit to **narrow** repository reads, not replace them.

1. Identify the requested project/role and the cockpit sources it references.
2. Refresh the smallest relevant canonical set: current Factory state, the selected Office `CURRENT`, the selected Project Room/state, active Issue/PR and evidence needed for the action.
3. Compare those facts with the cockpit snapshot.
4. Update or regenerate the derived snapshot if it is stale.
5. Act only within currently verified authority. Unknown or conflicting authority stops the affected action.

A full-Factory reread is unnecessary for a small, well-scoped project task unless the relevant pointers are missing, stale, conflicting or the task is an audit.

## Recovery and handoff

The cockpit must distinguish three continuity events:

- **FIRST_APPOINTMENT** — no predecessor handoff is invented.
- **SAME_INCUMBENT_RECOVERY** — a chat/model/device change keeps the same tenure; refresh current facts and do not create a succession record.
- **TRUE_SUCCESSION** — only an explicitly authorized incumbent change creates a finalized predecessor handoff. Historical handoffs remain immutable; fresher current state is reconciled separately.

A recovery brief should contain role, project, canonical repository, current state, active Issue, last verified ref/SHA, pending work, blockers, decisions already made, do-not-reopen items, authority boundaries, next safe action and evidence pointers.

## Project-to-role and role-to-project navigation

The cockpit should expose both directions:

`project -> Project Primary -> related Factory roles -> Office CURRENT`

and

`role -> Office CURRENT -> active projects -> project state / Issue / evidence`.

Cross-project visibility is not cross-project execution authority. A portfolio or governance role can see several projects without becoming their Project Primary.

## Codex handoff

ChatGPT management should package a bounded implementation request for Codex instead of asking Codex to re-read the whole Factory by default. The package should include only:

- exact task and expected output;
- target repository/project and relevant paths;
- current branch/ref/SHA when material;
- accepted decisions and constraints;
- applicable tests/evidence expectations;
- explicit exclusions and Human gates;
- source pointers for anything Codex may need to refresh.

Codex should expand beyond the package only when implementation discovers a concrete dependency, conflict or missing fact.

## Derived-bundle validation

`scripts/validate_cockpit.py` checks the checked-in cockpit manifest and its source/output references. `VALID` means only that the derived bundle is structurally coherent and still marked non-authoritative. It does not grant execution authority, prove freshness, validate a real ChatGPT Project session or replace privacy review.

## Privacy boundary

Never populate a public cockpit by copying private Factory history and then redacting names. Public examples must be newly authored synthetic material. Real cockpits may contain operational data only in the already-authorized private environment that owns those records.
