# Browseable synthetic Factory instance

This directory is a checked-in, public-safe example of what a running AI Software Factory can look like on disk.

It is intentionally synthetic. It does **not** contain private Factory history, real appointments, real correspondence, customer/company data, credentials, production topology, or any hidden source repository content.

The goal is simple: let a reader browse the Factory shape without first running a generator.

## Structure

```text
factory-instance/
├── factory/
│   ├── FACTORY_STATE.md
│   └── OPEN_LOOPS.md
├── registers/
│   ├── roles.json
│   ├── projects.json
│   ├── workstreams.json
│   ├── continuity.json
│   └── work_items.json
├── checkpoints/
│   ├── atlas-release-readiness-current.md
│   ├── atlas-release-readiness-obsolete.md
│   ├── beacon-environment-current.md
│   ├── beacon-environment-legacy.md
│   └── atlas-governance-transition-current.md
├── audit/
│   ├── README.md
│   └── SAMPLE_AUDIT_REPORT.md
├── project-cockpit/
│   ├── PROJECT_INSTRUCTIONS.md
│   ├── FACTORY_OVERVIEW.md
│   ├── PROJECTS.md
│   ├── ROLES.md
│   ├── RECOVERY_BRIEF.md
│   ├── HEALTH.md
│   ├── CODEX_TASK_PACKAGE.md
│   ├── END_TO_END.md
│   └── manifest.json
├── offices/
│   ├── management/
│   │   ├── README.md
│   │   ├── inbox/example-request.md
│   │   ├── outbox/example-result-reference.md
│   │   ├── desk/CURRENT.md
│   │   ├── pending/atlas-review.md
│   │   ├── wardrobe/atlas-work.json
│   │   └── handoffs/README.md
│   ├── governance/
│   │   ├── README.md
│   │   └── desk/CURRENT.md
│   ├── runtime/
│   │   ├── README.md
│   │   └── desk/CURRENT.md
│   └── portfolio-console/
│       ├── README.md
│       └── desk/CURRENT.md
├── projects/
│   ├── atlas/
│   │   ├── README.md
│   │   ├── STATE.md
│   │   ├── inbox/example-task.md
│   │   └── outbox/example-result-reference.md
│   └── beacon/
│       ├── README.md
│       └── STATE.md
└── meeting-hall/
    └── README.md
```

The `project-cockpit/` directory demonstrates how a ChatGPT Project can present Factory/project/role overviews, recovery context, health findings and a bounded Codex task package while keeping the surrounding repository records canonical. [END_TO_END.md](project-cockpit/END_TO_END.md) walks through the complete Human → ChatGPT management → bounded refresh → Codex package → result reconciliation path.

The V1.3 `work_items.json` plus `checkpoints/` fixtures demonstrate a separate idea: one bounded Project-visible work item can point to the current Issue/PR surface, current checkpoint, last evidence, superseded checkpoints, Human gate and next action without copying a long discussion thread.

The [`audit/`](audit/README.md) directory adds a V1.4-style **Fresh Factory Audit** example. It uses a deliberately fictional counterfactual drift scenario to show how a fresh evaluator can report missing project visibility, frozen-work resurrection, superseded direction, stale state propagation, stale recovery queues and orphaned draft work surfaces without copying any private Factory incident.

Generate an executable cockpit or Project-ready management export with:

```sh
python -B scripts/generate_cockpit.py --root examples/factory-instance --output ../generated-cockpit
python -B scripts/generate_project_view.py --root examples/factory-instance --output ../project-view
```

Check either generated bundle for source drift with `scripts/check_cockpit_drift.py`. The checked-in V1.1 cockpit structure can still be validated with:

```sh
python -B scripts/validate_cockpit.py --root examples/factory-instance
```

This browseable instance complements, rather than replaces, `scripts/create_demo.py`:

- this directory is for **reading and understanding**;
- the cockpit is for **derived overview/recovery/task context**;
- the work-item Project view is for **bounded active-work visibility and recovery**;
- the audit example is for **fresh-context semantic consistency/recoverability review**, not automatic remediation;
- the demo generator is for **creating deterministic disposable fixtures and running validation**.

Nothing in this example grants real authority. Treat all identities, decisions, evidence labels and correspondence as fictional.
