# AI ENTRYPOINT

## 1. What you are entering

This repository defines an AI-native software Factory: a durable organizational control plane around software projects, Human decisions, AI/agent roles, evidence, and GitHub-native workflows.

The Factory is not one chat. Chats, coding agents, Work sessions and tools are interaction/execution surfaces. Durable identity and authority live in repository-defined roles, projects, state and evidence.

## 2. First mental model

```text
Human Factory Director / Owner
        |
        v
Primary Management AI
Executive / Deputy responsibility bundle
        |
        +-- Governance / Consistency AI
        +-- Runtime / Infrastructure AI
        +-- Engineering / Project Primary agents
```

Small Factories may combine functions. Large Factories may split them. Logical roles do not require one permanent chat each.

## 2.1 Select the operating context

Before applying a role, read [the instance boot protocol](docs/INSTANCE_BOOT_PROTOCOL.md).
Distinguish framework maintenance, an explicitly selected operating instance,
and a synthetic exercise. Framework defaults and demo assignments cannot appoint
the reader. Unknown context or authority means no execution.

After reading the required mechanism documents below, follow that protocol's
ordered authority/state/inbox/Git/current-cursor checks. The read-only preflight
is optional assistance, not proof of authority or completion of takeover.

## 3. Authority model

Keep these distinctions explicit:

```text
Human / technical credential
    -> AI or agent instance
    -> Factory role
    -> authority scope
    -> action
    -> evidence
    -> policy / review gate
    -> canonical integration
```

`display title != authority scope`

`GitHub identity != Factory organizational identity`

## 4. Main facilities

Read:

- `docs/AI_FACTORY_IN_30_SECONDS.md`
- `docs/ROLES_AND_AUTHORITY.md`
- `docs/FACILITIES_AND_SURFACES.md`
- `docs/GITHUB_NATIVE_WORKFLOW.md`
- `docs/CORRESPONDENCE_AND_CC.md`
- `docs/PROJECT_MAILBOX_AND_CONSOLE.md`
- `docs/WORK_INVOCATION_WARDROBE.md`
- `docs/HANDOFF_AND_SUCCESSION.md`
- `docs/PUBLIC_PRIVACY_STANDARD.md`

## 5. GitHub specialization

GitHub Issue may act as a Factory Meeting / Coordination Surface for product, architecture, cross-role deliberation, evidence collection and Human decision points.

GitHub PR acts as a Candidate Change Envelope: an exact candidate state plus evidence and review, not merely a developer asking a maintainer to merge code.

## 6. Recovery and succession

Changing chat, model, computer or execution surface does not automatically mean succession. Same-incumbent recovery should restore the same role from current state and evidence.

Only a real incumbent change creates a succession handoff. Finalized tenure handoffs are immutable append-only historical records and never override fresher current state.

## 7. Privacy and trust

Examples must be synthetic. Do not publish private correspondence, real customer/company material, credentials, server topology, private runtime evidence, real tenure history or other identifying operational records merely after renaming them.

Re-author reusable mechanisms; do not sanitize-copy private history.

## 8. Safe first action

If this is a fresh Factory bootstrap, inspect `factory.yaml` as framework defaults, then resolve the explicitly selected instance and original authority under `docs/INSTANCE_BOOT_PROTOCOL.md`. Unconfigured values stay unresolved. State:

- who you are acting as;
- what authority is known;
- what remains unknown;
- which project or Factory surface owns the next action.

Do not invent missing authority.
