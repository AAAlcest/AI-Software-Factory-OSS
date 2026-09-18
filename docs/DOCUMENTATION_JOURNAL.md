# GitHub-native documentation journal

Owner: OSS Project Primary. Implementation/acceptance: [Issue #28](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/28).
Notice: [Issue #26](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/26).
Status: implementation candidate; **NOT_ACTIVATED until real writer/replay readback**.
The broader product-documentation work remains under #25, not this implementation.

## What runs

[`documentation-journal-signal.yml`](../.github/workflows/documentation-journal-signal.yml)
is an unprivileged PR-event hint. It performs no checkout, installs no dependencies,
and produces no artifact. [`documentation-journal.yml`](../.github/workflows/documentation-journal.yml)
is the only writer: default-branch push, validated signal completion, hourly at
minute 23, or a manual run. It executes trusted default-branch code only, runs its
unit tests, then reconciles Git/API facts with verified bot receipts. No AI,
external server, database, PAT or production credential is required.

The [configuration](../.github/documentation-journal.json) fixes this repository ID,
main branch, locked notice #26, expected bot, watched paths and baseline. No event
text or manual input can select another destination. To adopt the mechanism in a
**different public repository**, its maintainer must review and change the repository
ID/name, notice, baseline and workflow guard together. This installation deliberately
rejects private repositories; exporting their records is not an implied capability.

Initial history starts **after** `974b17a7a70e75824db033a4ce4d69928fb91b30`.
The existing manual #27 entry is not duplicated as automatic evidence. Initial
PR discovery includes open PRs and PRs updated since the configured timestamp.
No whole-history import is performed. Every run thereafter rechecks all in-scope
PRs and newly reachable default-branch revisions; event notifications are hints,
not a durable event queue. Git blobs, including those fetched for a fork PR, are
read as objects: the recorder never checks out, imports, installs or executes them.

## Detection, data and boundaries

The [recorder](../scripts/documentation_journal.py) uses full local Git differences,
not the capped compare/PR-files REST response, for file completeness. Both old and
new rename paths are matched. Additions, deletions, assets, root Markdown, templates
and individual revisions including change-then-revert are covered by explicit globs.
`fnmatchcase` globs are repository-relative; `*.md` also matches nested Markdown.
Non-Markdown structured files outside configured trees require an explicit rule.

PR snapshots use a fixed merge-base-to-head comparison and before/after API context
checks. A head, target, declared-metadata or lifecycle change produces a new event.
The key chains to the previous confirmed snapshot, preserving observed A → B → A.
Base-tip movement alone does not produce a new announcement. A previously observed
document diff becoming empty produces `DOC_DELTA_CLEARED`, not withdrawal. Close/
reopen timeline IDs are separate; a final merge closure is not an extra MERGED entry.
Actual integration records come from newly reachable Git revisions. `MERGED` with
`DIRECT_COMMIT` means integrated, not reviewed by a PR. Side-branch revisions and
the merge revision have distinct keys; duplicate push/closed notifications do not
create another entry for the same integrated commit.

Candidate metadata is deliberately minimal: logical-role declarations are linked
and marked DECLARED rather than copied from arbitrary PR prose; absent declarations
remain UNKNOWN. Optional PR lines `Logical role:`, `Reason:` and `Impact:` participate
in the normalized correction digest. Commit emails, document bodies, patches and
raw PR descriptions are not journaled. Paths are escaped, and mentions suppressed.
External validation results remain UNKNOWN with evidence links; the recorder does
not infer a PASS, perform semantic acceptance, or block recording because other
checks failed. Commit time, observation time and GitHub registration time differ.

Local edits, unsubmitted branches and unobserved transient heads/metadata changes
are outside the guaranteed observation boundary. An unavailable old head remains
an explicit gap; a newer head does not erase it. The current implementation retries
an unavailable snapshot when it is still the PR's observed head. Historical missing
snapshots after head movement remain visible for bounded operator disposition; they
are **not automatically declared repaired**. No per-save or exactly-once claim is made.

## Receipts, state and recovery

Bot-authored receipts carry a versioned marker, repository ID, workflow-run link,
stable event key and part number. All parts must be read back before an event counts
as delivered. The reader checks API bot identity and the referenced run's repository,
workflow path, default branch and allowed event. Human-copied markers are ignored.
These checks are not cryptographic proof against malicious repository maintainers
or other trusted workflows; an editable Issue is not a tamper-proof ledger.

One bot-owned status comment saves the baseline, main observed/scanned/covered tips,
exact pending payloads, persistent gaps and last-run result. PR latest snapshots are
reconstructed from confirmed receipt chains instead of trusting one cached cursor.
A pending observation is saved **before** its receipt is posted. POST-response loss
causes receipt lookup before any retry. Partial multi-comment records reuse their
original event metadata. Only the bot's status comment is edited; event history and
Human comments are not rewritten. Losing cached state restarts from the configured
baseline and surviving confirmed receipts; destroying both state and evidence cannot
be recovered by a promise.

A failed lane does not stop later independently verifiable records. Main coverage
stays behind a failed required revision even when later revisions are journaled.
Replays deliver only missing receipts and retain unavailable-source gaps. Global
permission/network failure is visible in Actions. A 403 does not unlock the notice,
request a broader token, or silently advance state. Current explicit safety limits:
200 API pages per list, 2,000 newly reachable revisions per scan, 16 MB Git output,
20 MB API response, and 55 KB per comment/state. Exceeding a limit reports a gap or
failure rather than silently truncating coverage; large installations need a reviewed
state-sharding/batch design. Documentation file lists are split into 40-file parts.

For recovery: **Actions → Documentation journal → Run workflow**, keep `main`.
`dry_run=true` checks without writing; set `false` for an authorized replay. All
triggers share a non-cancelling writer concurrency group. GitHub can coalesce queued
runs, delay/drop schedules or disable inactive public schedules; inspect last-run and
gap state, and use manual replay after an interruption.

## Tests and activation

Run `python -B -m unittest discover -s tests -p test_documentation_journal.py -v`.
The existing `scripts/check_all.py` also discovers these tests. Offline fixtures cover
snapshots, A/B/A, declaration/base corrections, cleared diffs, escaped input, receipt
provenance, chunking, POST loss, partial replay, old-head gaps, lane isolation, Git
renames, no-doc changes, change/revert, timeline recovery and API pagination.
They do not impersonate a real bot or prove access to locked #26.

Before marking ACTIVE, record the merged workflow SHA, successful real run and bot
comment IDs on locked #26, followed by a second run proving receipt deduplication.
A candidate PR or green CI alone is not activation. Do not change release tags or
claim a new release as part of this installation.

Technical references: [GitHub events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows),
[least-privilege permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions),
[workflow security](https://docs.github.com/en/actions/reference/security/secure-use).
