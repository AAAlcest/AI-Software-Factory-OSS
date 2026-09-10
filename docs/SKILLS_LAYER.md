# Skills layer

The V1.1 Skills layer standardizes how a management model reads, compresses and hands off Factory context. These are portable **skill contracts**, not claims that a particular ChatGPT installation has already installed them.

Each contract lives under `skills/<name>/SKILL.md` and follows four rules:

1. repository facts outrank memory and generated summaries;
2. read the smallest canonical source set that can answer the task;
3. preserve explicit UNKNOWN/BLOCKED states instead of inventing missing facts;
4. every output is context or analysis unless separate authority grants an action.

## Contracts

- `factory-overview` — Factory-wide project/role/status/open-loop view.
- `project-overview` — one project's current operating picture.
- `role-overview` — one Staff Office/role operating picture.
- `project-recovery` — compact recovery package for a project context.
- `role-recovery` — compact recovery package for a role context.
- `handoff` — classify first appointment, same-incumbent recovery or true succession and prepare the correct continuity package.
- `factory-health` — detect stale CURRENT records, unowned pending work, blockers and missing evidence.
- `task-packaging` — create a bounded implementation package for Codex.

## Common output discipline

A useful skill output should state:

- selected scope;
- canonical source pointers actually used;
- observed current facts;
- unresolved/conflicting facts;
- authority/Human gates;
- next safe action;
- whether the output is derived and whether execution was performed.

Do not duplicate entire Office histories or large Issue threads when a current pointer plus a narrow excerpt is enough.

## Composition

Typical management flow:

`factory-overview -> project-overview -> factory-health -> task-packaging -> Codex`

Typical continuity flow:

`role-overview/project-overview -> handoff classification -> role-recovery/project-recovery`

The Project cockpit described in [CHATGPT_PROJECT_COCKPIT.md](CHATGPT_PROJECT_COCKPIT.md) is the human-facing surface where these outputs can be organized. The repository remains canonical.
