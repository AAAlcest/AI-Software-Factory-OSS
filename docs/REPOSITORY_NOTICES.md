# Repository notices and documentation-change journals

Status: CURRENT design contract. See the [recorder guide](DOCUMENTATION_JOURNAL.md)
for implemented behavior, limits and the separate live-activation evidence requirement.
Owner: OSS Project Primary for this contract and its journal implementation;
each document's logical owner for its content and declared change rationale.
Automatic journal work: [Issue #28](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/28).
Product-documentation maintenance: [Issue #25](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/25).
Live OSS notice: [Issue #26](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/26).

## One repository, one notice

Each newly created Factory repository and each governed software-product repository
must have one persistent documentation/engineering notice Issue. Its opening body
is an index; its comments are a documentation-maintenance journal. Existing
repositories backfill this once. Do not repurpose a historical delivery Issue or
create a second notice for each version. A [copy-ready starter](../templates/REPOSITORY_NOTICE.md)
is provided; copying it does not create an Issue or grant authority.

Bootstrap readiness requires canonical entrypoints, a real notice Issue, and a
README or AI-entrypoint link to both. Missing manuals may be explicitly tracked,
but an index of planned paths is not evidence that those manuals are complete.
Keep the notice OPEN while the repository is maintained. A successor notice must
be explicitly linked before retiring the old one. Pinning is optional navigation
convenience, not an authority or readiness prerequisite.

The repository's explicit decisions, current documents, source and evidence control
their respective scopes. The notice only links and describes them. Technical
access, a bot comment or a logical role label does not grant organizational scope.

## Opening body: useful navigation, not a second backlog

Include a short product/Factory purpose, Human and AI reading order, current merged
documentation links, exact candidate links when relevant, release/security routes,
manual owners and known gaps. Distinguish merged documents from an unmerged PR.
Use current-branch links for navigation and immutable refs for historical claims.
Do not silently turn a candidate link into evidence that the candidate is deployed.

Reference product/requirements, architecture, development, data/schema, contracts,
operations/recovery, decisions/history, migrations and validation where applicable.
Reuse existing detailed pages instead of writing parallel manuals. Every applicable
manual must answer a concrete reader question, not merely provide a directory or
TODO list. Record purpose, logical owner, status, applicable source/ref, evidence
and known limitations. A short page can satisfy this; a large empty skeleton cannot.

Keep these dimensions separate:

| Dimension | Examples | What it does not prove |
| --- | --- | --- |
| Lifecycle | CURRENT, SUPERSEDED, HISTORICAL, NOT_APPLICABLE | Completeness or approval |
| Maturity | SKELETON, PARTIAL, COMPLETE_IN_DECLARED_SCOPE | Merge or deployment |
| Delivery | LOCAL_DRAFT, CANDIDATE_UNMERGED, MERGED, WITHDRAWN | Release or successful operation |
| Validation | NOT_RUN, PASS, FAIL, BLOCKED with scope/ref | Blanket privacy or production acceptance |

Current design expresses intended behavior; source/tests describe observed
implementation; release/deployment readbacks describe published/running behavior.
Record conflicts instead of letting one dimension silently overwrite another.
An incident hypothesis is not a proven technical root cause without diagnostics.

Database-server documentation can be NOT_APPLICABLE with a reason and activation
trigger. That does not make existing JSON schemas, files, checkpoints, manifests or
browser storage cease to be data contracts. Source-generated references must name
the source ref, extractor/version, coverage and gaps. Static extraction is not an
inspection of a live database. Historical records retain target scope and point to
current replacements; do not manufacture missing history.

## Shared maintenance and public access

All authorized document owners participate. The PM maintains scope/navigation and
acceptance; technical execution follows the owner of the actual Issue, not an
implicit delegation. Console tracks visibility and routes explicitly assigned work.
Engineering, data and infrastructure roles update the manuals coupled to their changes.
Reviewers add scoped findings without becoming the content owner. Large inventory/
backfill work should be delegated where appropriate, not repeatedly reconstructed in
one management chat. No attendance, ACK or no-change replies.

For public repositories, a locked notice can keep ordinary discussion elsewhere.
GitHub allows owners/collaborators and people with write access to comment on a
locked conversation; body editing still depends on actual permissions. See
[GitHub's locking rules](https://docs.github.com/en/communities/moderating-comments-and-conversations/locking-conversations).
Test the actual automation writer on the locked Issue; a successful human or
connector comment is not proof that the bot has access. Do not request broad
credentials merely to edit an index. General feedback stays in normal Issues/PRs;
vulnerabilities use the repository's private security-reporting route.

## Automatic recording contract

Human reminders are a fallback, not the durable event detector. Implement this as
repository-owned GitHub Actions, not a chat that must remain online. This document
specifies the required behavior; a real activation still needs the evidence below.

### Observation boundary and triggers

- On default-branch push, discover documentation-changing revisions from actual Git
  history/API evidence, including direct commits, merges and bot commits. Record
  additions, edits, deletions and renames. Do not depend on a label, commit subject
  or a manually ticked PR checkbox. A typo is still a documentation change.
- On PR submission/update/closure, inspect metadata and file lists and record the
  exact observed candidate head as CANDIDATE_UNMERGED or WITHDRAWN as appropriate.
  Merged history produces the separate MERGED record. Never execute PR/fork code in
  the privileged recorder. Multiple files may share one event record.
- Add periodic reconciliation and manual workflow_dispatch recovery. Replay from a
  durable recorded baseline/cursor and compare recorded event keys with actual
  integrated history and currently visible PR heads, rather than checking only a
  recent time window. The operator declares activation baseline and excluded past
  history so initial installation does not flood the notice with every old commit.

Local unsaved/unpushed edits and unsubmitted branches are outside this observation
boundary. Events cannot reconstruct unavailable intermediate heads after history
was rewritten. Report a coverage gap rather than promise every transient save was
observed. Add branch-specific coverage only with an explicit safe design.

### Event records

Each entry includes technical actor, explicitly declared logical role or UNKNOWN,
actual commit/merge time with timezone, journal registration time, changed paths
and operations, exact commit/parent or candidate head, PR/Issue links and delivery
status. Link why/impact from the maintainer's declaration; do not invent intent.
Unknown test or review state stays UNKNOWN/NOT_RUN; a commit event is not a PASS.
Escape untrusted titles/paths and avoid unwanted mentions. Log links/metadata, not
document bodies, diffs, emails, secrets or private cross-repository content.

Use repository + integrated commit SHA for integrated revisions. Candidate keys
include the normalized snapshot and previous confirmed event, not head SHA alone:
observed A-to-B-to-A, same-head declaration/target corrections and cleared document
diffs must remain distinguishable. Base-tip motion alone is not a posting reason.
Repeated runs must not duplicate entries. Confirm the origin of bot-owned markers;
an arbitrary comment must not forge the cursor. Batch long file lists with exact
evidence links and explicit coverage counts, not silent truncation. Humans may
append rationale/corrections without duplicating the bot's mechanical inventory.

### Reliability and security

Serialize writes and paginate API reads. Advance covered progress only after
required records have been posted and read back. Keep exact pending observations
for replay. A failure in one lane must remain visible without blocking independent
new records; observed/scanned progress is not the same as complete coverage.
Reconciliation must survive coalesced events, retries, partial batches and a docs
change followed by a revert. Compare individual revisions, not only the final net
diff. An absent/rewritten baseline fails closed with a coverage warning.

Avoid trigger-level path filters as the sole source of truth: classify watched
paths in the recorder from complete change evidence. Configure documentation paths
explicitly, including root Markdown/entrypoints, docs, templates and doc assets;
retain both old and new paths when a rename crosses the watched boundary.

Use repository-scoped GITHUB_TOKEN with contents/pull-requests read and issues write
only as needed; actions read is used for workflow provenance. No PAT, production
secret or cross-repository token. The privileged writer runs trusted default-branch
code only. The selected implementation separates an unprivileged PR signal from
that writer; it does not use pull_request_target. Do not execute PR text or consume
fork artifacts/caches as instructions. Use no issue-comment trigger for the writer
itself. Keep third-party actions pinned; the journal cannot approve, merge, release
or deploy.

GitHub event delivery/scheduling is not an infallible queue: schedules can be delayed
or dropped and public-repository schedules can be disabled after inactivity.
GITHUB_TOKEN-originated pushes do not normally trigger another push workflow.
See [workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows),
[token event behavior](https://docs.github.com/en/actions/concepts/security/github_token)
and [privileged PR security](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target).
Expose last successful reconciliation, pending gaps and failed runs; manual replay
is the recovery path when Actions is unavailable. Do not describe this as
instantaneous or guaranteed exactly-once delivery under every outage.

## Acceptance and activation

Require positive and negative tests for merge/direct/bot changes, no-doc no-op,
rename/delete, multiple commits including a revert, rerun deduplication, failed
post and retry, missed-event backfill, pagination/large lists, rewritten history,
unknown role, failed/unknown validation and an untrusted fork PR. Template presence
or CI green alone does not prove automated journaling.

Activation requires a merged/enabled workflow, configured repository/notice and
baseline, a real authorized bot entry on the actual locked notice, and replay
showing no duplicate. Record exact workflow/ref/run/comment evidence in the
implementation Issue. Only then change the notice status to ACTIVE. Until then use
manual entries and state NOT_ACTIVATED honestly. Do not close the umbrella work
Issue because only the notice or design document exists.

## 中文要点

每仓一面公告墙：正文放导航，评论记变更。目录不等于手册，已提交不等于已合并，
已合并不等于已部署，自动记录不等于验收通过。自动化采用“事件触发 + 定期补漏 +
可手动重放 + 去重”，不依赖维护者记得回复。程序未真实跑通前，必须标明
NOT_ACTIVATED；本地未提交的编辑不能算已记录。自动记录由 OSS 在 #28 负责，
#25 只保留产品文档整理与维护规范，不再向 Console 并行派发自动化任务。
