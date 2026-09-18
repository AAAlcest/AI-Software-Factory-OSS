# <Repository> — Documentation & Engineering Notice

Template only. Replace placeholders using authorized repository evidence before
creating an Issue. Do not paste private operating history into a public repository.
See [the notice/journal contract](../docs/REPOSITORY_NOTICES.md).

> Opening body = current navigation. Comments = documentation-change journal.
> This is not a backlog, approval source, release gate or attendance channel.

## Start here

Repository/purpose: <repository and short purpose>
Human reading order: <README, quickstart, documentation index>
AI reading order: <AGENTS, actual AI entrypoint, scoped current work>
Operating assignment/authority: <appropriate authorized source, or UNKNOWN>
Release/status evidence: <canonical release/work surface>
Last index reconciliation: <time with timezone and inspected ref>

## Documentation map

List existing canonical paths with their purpose and logical content owner. Cover
product/requirements, architecture, development, data/schema, contracts, operations,
decisions, history, migrations and validation as applicable. Existing detailed
pages may be linked without moving or duplicating them.

For every entry distinguish lifecycle, maturity, delivery and validation. Put
candidate PR paths in a clearly separate pending section. For absent families,
record the reason, applicability trigger and existing work item; do not invent a
file link or represent a skeleton as a complete manual. Source-derived dictionaries
must disclose the applicable source ref and extraction gaps.

## Journal operation

Automatic recording: NOT_ACTIVATED until real workflow and bot-comment evidence.
Workflow/config: <path or NOT_IMPLEMENTED>
Activation baseline: <exact ref or UNCONFIGURED>
Last successful reconciliation / gaps: <evidence or NOT_RUN>
Implementation work surface: <existing Issue; do not use this notice as a backlog>

Coverage after activation: every integrated documentation revision on the configured
default branch, and observed documentation PR candidates separately marked pending.
Local uncommitted saves and unsubmitted branches are not covered. Event recording,
periodic backfill, manual replay and idempotency must be tested before activation.

## Change entry

```text
Logical role: <explicitly declared responsibility or UNKNOWN>
Technical actor: <GitHub login, not authority>
Changed at: <commit/merge timestamp with timezone>
Documents: <paths, exact-ref links, added/edited/moved/deleted>
What / why / reader impact: <concise summary or declaration link>
Evidence: <PR / commit / related Issue>
Delivery: <CANDIDATE_UNMERGED | MERGED | WITHDRAWN>
Validation: <actual scoped result or NOT_RUN; retain failures/gaps>
Supersession: <old record and controlling replacement if applicable>
```

Authorized maintainers share content maintenance; no one needs to say received or
no change. Once automated recording is active, humans add rationale or corrections,
not a duplicate file inventory. Read the latest body before updating navigation.
An automated record must not claim acceptance or invent an undeclared logical role.

## Access and routing

Keep the notice OPEN. For public repositories, an authorized maintainer may lock
general conversation and optionally pin the notice; verify actual bot write access
on the locked thread. Lack of body-edit access does not justify broader credentials.
Normal defects/discussion/review: <normal Issues or PRs>
Private security reporting: <authorized private channel; no personal email required>
Never post document bodies, credentials, private history or sensitive external data.
Keep historical references, and explicitly link a successor before retiring this
notice. README/AI entrypoints must link here and to the canonical documents.
