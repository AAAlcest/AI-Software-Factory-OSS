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
│   └── projects.json
├── project-cockpit/
│   ├── PROJECT_INSTRUCTIONS.md
│   ├── FACTORY_OVERVIEW.md
│   ├── PROJECTS.md
│   ├── ROLES.md
│   ├── RECOVERY_BRIEF.md
│   ├── HEALTH.md
│   ├── CODEX_TASK_PACKAGE.md
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

The `project-cockpit/` directory demonstrates how a ChatGPT Project can present Factory/project/role overviews, recovery context, health findings and a bounded Codex task package while keeping the surrounding repository records canonical.

Validate that derived bundle with:

```sh
python -B scripts/validate_cockpit.py --root examples/factory-instance
```

This browseable instance complements, rather than replaces, `scripts/create_demo.py`:

- this directory is for **reading and understanding**;
- the cockpit is for **derived overview/recovery/task context**;
- the generator is for **creating deterministic disposable fixtures and running validation**.

Nothing in this example grants real authority. Treat all identities, decisions, evidence labels and correspondence as fictional.
