# Synthetic ChatGPT Project instructions

> **Static teaching snapshot:** this checked-in `project-cockpit/` directory is a
> browseable legacy/static example retained for teaching and validation. It is not
> the full current schema-2 output of `scripts/generate_cockpit.py`. To inspect the
> current generated shape, run the generator into a new destination and compare the
> derived bundle there.

This is a fictional Project cockpit for the checked-in example Factory.

Repository files are canonical truth. Files in this directory are derived navigation/context snapshots. Before material action, refresh the smallest relevant source refs from `manifest.json` and the active Issue/PR/evidence if applicable.

Current schema-2 generation consumes workstreams, continuity, work items, current checkpoints and last-evidence pointers. Generate it with:

```sh
python -B scripts/generate_cockpit.py --root examples/factory-instance --output ../generated-cockpit
```

Do not infer authority from this Project, a model name, a chat title or connected tooling. Preserve UNKNOWN/BLOCKED states and Human gates. Prefer a bounded project/role refresh over rereading the whole Factory.

For engineering work, create a bounded `CODEX_TASK_PACKAGE.md`; Codex expands beyond it only when implementation discovers a concrete dependency, conflict or missing fact.
