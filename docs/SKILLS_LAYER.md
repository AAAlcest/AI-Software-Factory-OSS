# Skills layer

The Skills layer standardizes how a management model reads, compresses and hands off Factory context. Each portable contract lives under `skills/<name>/SKILL.md`; V1.2 also provides one composable executable adapter rather than eight duplicated implementations.

Every skill follows four rules:

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
- `handoff` — classify first appointment, same-incumbent recovery or true succession from repository continuity evidence.
- `factory-health` — surface blockers, Human gates and missing structural evidence.
- `task-packaging` — return the bounded implementation package generated for one selected workstream.

## Executable adapter

Generate a fresh cockpit first, then call the shared adapter:

```sh
python -B scripts/generate_cockpit.py \
  --root examples/factory-instance \
  --output ../factory-cockpit \
  --workstream workstream:atlas-release-readiness

python -B scripts/run_skill.py \
  --root examples/factory-instance \
  --bundle ../factory-cockpit \
  --skill handoff \
  --workstream workstream:atlas-release-readiness
```

`run_skill.py` performs a drift check before using the bundle. If a referenced canonical source changed or disappeared, the skill blocks with `BLOCKED_STALE_BUNDLE` rather than treating an old summary as current. `task-packaging` requires the requested workstream to match the bundle's selected workstream; otherwise regenerate the bundle for that lane.

The adapter performs no canonical-state mutation and every successful result still reports `execution_authorized: false`.

## Common output discipline

A useful skill output should state the selected scope, canonical pointers actually used, observed facts, unresolved/conflicting facts, Human gates, next safe action, and that the output is derived. Do not duplicate entire Office histories or large Issue threads when a current pointer plus a bounded source set is sufficient.

Typical management flow:

`factory-overview -> project-overview -> factory-health -> task-packaging -> Codex`

Typical continuity flow:

`role-overview/project-overview -> handoff classification -> role-recovery/project-recovery`

The Project cockpit described in [CHATGPT_PROJECT_COCKPIT.md](CHATGPT_PROJECT_COCKPIT.md) is the human-facing surface where these outputs can be organized. The repository remains canonical.
