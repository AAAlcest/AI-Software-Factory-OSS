# Skill: factory-overview

Purpose: produce a compact Factory-wide project/role/status view without rereading unrelated history.

Inputs: Factory state pointer, project registry, role registry, open-loop source and optional freshness checkpoint.

Read: canonical current records only; expand into a project/Office only when the registry/status indicates a material blocker, stale pointer or requested detail.

Output: projects, roles, blockers, open loops, Human gates, changed-since-checkpoint notes, source refs and next safe action.

Fail closed: preserve UNKNOWN/conflicts; never infer authority from visibility. Output is derived context and performs no execution.
