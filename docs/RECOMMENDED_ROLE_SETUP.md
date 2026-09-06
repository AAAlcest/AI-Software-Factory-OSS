# Recommended setup: ChatGPT staff, Codex engineering

This is the recommended small-Factory profile, not a mandatory vendor dependency,
not a real appointment registry and not a permission grant. The machine-readable
companion is [the profile](../profiles/chatgpt-codex.json). Other compatible tools
may replace either surface through an explicit assignment and capability check.

| Responsibility | Recommended surface | Scope |
| --- | --- | --- |
| Human Factory Director / owner | Human | Direction, retained risk decisions, license and publication |
| Deputy / executive + product and development management | ChatGPT | Product direction, scope, prioritization, coordination, acceptance preparation |
| Secretary / records | ChatGPT; may be the deputy | Current records, decisions and unresolved work, not duplicate chat transcripts |
| Governance / consistency maintenance | ChatGPT; may be the deputy | Bounded consistency checks and policy upkeep |
| Infrastructure / runtime planning | ChatGPT; may be the deputy | Architecture, environment boundaries, operational plans; no implied server rights |
| Optional project-level manager | ChatGPT | Project planning and review responses, not automatic local worker creation |
| Per-project development / execution primary | Codex | Implement, test, diagnose and prepare evidence in an explicitly assigned project |
| Development Lead / development-group lead | Codex | Engineering coordination, quality and explicit engineering tasks |
| Development Portfolio Console | Codex; may share Development Lead context | Portfolio visibility and routing, not execution ownership of every project |
| Independent technical reviewer | Separate engineering context, usually Codex | Review the actual candidate, not the author's self-report |
| Final independent privacy/public-safety reviewer | Separate ChatGPT context | Review content/history/disclosure independently of the author |

“Each project in Codex” means its **development execution role**. A Project Room,
repository or display title is not itself a live coding session. A project may
also have a ChatGPT manager. Unknown execution identity, working directory or
thread ID remains NOT_CONFIGURED / NOT_EXPOSED; do not create a worker because a
registry entry is vacant. Console visibility never transfers implementation ownership.

## Minimal arrangement, without one chat per title

Start with a Human, one ChatGPT deputy carrying compatible staff duties, and one
Codex engineering context for an active project. Add separate project execution
contexts as actual work requires. The Development Lead may carry Console duties.
Add a separate reviewer when independence is required, rather than making the
same author change hats and approve their own output. Management role bundles
are configurable; combining staff work does not combine protected approvals.

A deputy can maintain governance and prepare publication material, but that
same author cannot sign the final **independent** privacy review. Separation is
about actor/context/provenance, not whether two comments use the same GitHub
technical account. No tool/provider label grants organizational authority.

## Work is exceptional, not the default management path

Keep ordinary reading, planning, bounded GitHub review, task coordination and
short reports in the management chat. Use direct available repository tools.
Do not launch Work to acknowledge a message, rewrite a short note, or check a
status that a direct read resolves. Do not create a chain of Work sessions to
imitate departments or claim background work that is not actually running.

Move substantial engineering execution to an explicitly assigned Codex role.
Use a separate Work/execution surface only when a concrete capability or workload
requires it and the task permits it. Carry a bounded task, exact repository/ref,
allowed actions, evidence requirements and return route. Record session metadata
only when exposed. A transition never creates a new tenure automatically.

After an initial takeover, refresh new messages and changed relevant sources;
do not repeat a full Factory audit for every small task. Expand inspection only
for actual authority changes, conflicts, risks or a specifically scoped audit.
Preserve meaningful tests and actual defects while avoiding receipt/ACK loops.

## Product features versus staffing

This recommendation does not remove the optional correspondence, Console or
Wardrobe framework features. A Factory may coordinate ordinary product work in
Issue/PR threads without generating duplicate mailbox records. Use one primary
working surface for each decision and keep evidence linked rather than copied.

Terminology reference: OpenAI describes [Codex](https://help.openai.com/en/articles/11369540)
as its coding agent. The allocation above is this framework's recommendation,
not an OpenAI organizational rule or a promise about a plan's tools/limits.
