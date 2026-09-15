# Work-item checkpoints and Project-ready visibility

V1.3 adds a thin **work-item checkpoint layer** above the V1.2 workstream model so active Factory work can be viewed and recovered without replaying an entire Issue or PR chronology.

## Core rule

`Issue / PR / Project-visible item = visible work surface and evidence/authority pointer`  
`work-item checkpoint = bounded current recovery pointer`  
`daily note = role execution diary where an operating Factory uses one`  
`cockpit / Project projection = derived management view`

A generated Project view never overrides repository state, Human decisions, approvals, Git evidence or the linked work surface.

## Work-item record

The public synthetic fixture uses `registers/work_items.json`. Each item carries:

- work-item and workstream IDs;
- project and owner role;
- work type;
- status and priority;
- visible Issue/PR/work surface;
- `ACTIVE` or `ARCHIVED` projection state;
- current checkpoint pointer;
- superseded checkpoint pointers;
- last evidence pointer;
- next action;
- Human gate and risk when applicable.

Fields duplicated from the workstream register are validated for exact agreement. The work-item layer is therefore a visibility/recovery index, not a second place where status or ownership can silently diverge.

## Checkpoints

Checkpoint files under the synthetic `checkpoints/` directory are intentionally small. They identify the current work item, work surface, current direction/evidence and next action. Superseded checkpoints remain immutable historical pointers and are never promoted back into current direction merely because a fresh agent discovers them first.

Every active synthetic workstream must have exactly one work-item record. A `DONE` workstream must be `ARCHIVED`, not displayed as current active work.

## Project-ready export

Generate a portable management bundle with:

```sh
python -B scripts/generate_project_view.py \
  --root examples/factory-instance \
  --output ../project-view \
  --work-item workitem:atlas-release-readiness
```

The output contains:

- `PROJECT_VIEW.md` — human-readable active and archived work tables;
- `project_view.json` — structured portable projection;
- `project_view.csv` — board/import-friendly tabular projection;
- `WORK_ITEM_RECOVERY.md` — bounded recovery view for one selected item;
- `VISIBILITY_HEALTH.md` — current blockers, Human gates and risks;
- `manifest.json` — derived-source fingerprints for drift checks.

The first implementation is export-only. It does not mutate GitHub Projects or claim automatic board installation.

## Long-thread recovery

A fresh agent should normally read in this order:

1. selected work item;
2. current checkpoint;
3. visible work surface;
4. last evidence;
5. current workstream/continuity records;
6. older chronology only if a concrete conflict or missing fact remains.

This makes historical depth available without making historical replay the default startup cost.

## Validation and drift

Generation fails closed for structural problems including:

- active workstream with no work item;
- duplicate work-item coverage;
- project/owner/status/priority/surface mismatch;
- `DONE` item still projected as active;
- current checkpoint also listed as superseded;
- missing checkpoint or evidence file;
- unsafe repository-local pointers.

The generated Project bundle uses the same schema-2 fingerprint contract as the cockpit, so it can be checked with:

```sh
python -B scripts/check_cockpit_drift.py \
  --root examples/factory-instance \
  --bundle ../project-view
```

Fingerprints detect byte drift only. They do not grant authority or prove that a decision remains accepted.

## Cockpit and Skills integration

The existing V1.2 cockpit now includes `WORK_ITEMS.md`, the selected work-item checkpoint and last evidence in recovery/task packages. Project/role overview and recovery Skills also surface the matching work-item records. This keeps one chain:

`canonical work surface/evidence -> workstream -> work item/checkpoint -> cockpit/Project view -> bounded Codex package`

No private Factory history, real operational Issue chronology, credentials or production actions are part of the public fixture.
