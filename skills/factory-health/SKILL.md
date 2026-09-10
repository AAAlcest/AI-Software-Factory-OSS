# Skill: factory-health

Purpose: surface operational problems without taking ownership of them automatically.

Inputs: Factory state, role/project registries, Office CURRENT/pending pointers, Project state/evidence pointers and freshness policy.

Detect: stale CURRENT/state, unowned pending work, blocked projects, missing evidence, current-vs-reviewed candidate mismatch, unresolved Human gates and long-idle open loops.

Output: finding, affected role/project, source refs, severity/rationale, owner if explicitly known and next safe routing action.

A health finding grants no execution authority and must not auto-dispatch workers.
