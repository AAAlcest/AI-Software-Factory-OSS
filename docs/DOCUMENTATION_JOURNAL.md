# GitHub-native documentation journal

Owner: OSS Project Primary. Implementation/acceptance: [Issue #28](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/28).
Notice: [Issue #26](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/26).
Status: ACTIVE in this OSS repository only, as evidenced by the [actual writer/readback/replay](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/28#issuecomment-5736870432). Forks are separate installations.
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
main branch, notice #26, expected bot, watched paths and baseline. No event
text or manual input can select another destination. To adopt the mechanism in a
**different public repository**, its maintainer must review and change the repository
ID/name, notice, baseline and workflow guard together. This installation deliberately
rejects private repositories; exporting their records is not an implied capability.

## Fork self-setup

> **Privacy boundary:** this section configures the journal for a **public fork**.
> It is not the recommended bootstrap for a private operating Factory. Do not put
> private project metadata, assignments, company/customer information or private
> Factory history into a public fork. Real private instances belong in a separate
> authorized private operating repository; the public fork may remain an
> upstream/update/contribution copy. See
> [Quickstart §2](QUICKSTART.md#2-create-your-private-factory).

A GitHub fork copies files, not the upstream #26 Issue or its bot records. GitHub
Actions in a fork require the fork owner's own enablement. The copied writer has
the **upstream repository ID** in its guard and will not write to a fork unchanged.
Do not point a fork at upstream #26 or reuse the upstream baseline/state.

For a **public, direct fork of this exact repository whose default branch is
`main`**, a maintainer with push and Issue access can use the bounded initializer
from a clean local checkout of that branch. The tool binds the verified
`origin` GitHub repository, its API identity/default-branch tip, and local HEAD;
it never uses `gh`'s implicit default repository as a write target. Other
remote forms or default branches stop before creating an Issue. It requires
authenticated `gh` and Git. No token is printed or stored in the repository.
If the fork's **Issues** feature is disabled, the read-only check reports that;
`--apply` enables Issues on that same verified fork when the authenticated
maintainer has admin access, verifies the setting, and only then creates/reuses
the notice. There is no separate Settings prerequisite for a normal fork owner.
Without admin access it stops instead of changing another surface.
First run it without `--apply` to inspect the plan:

```sh
python -B scripts/bootstrap_documentation_journal.py
python -B scripts/bootstrap_documentation_journal.py --apply
```

`--apply` creates or reuses one OPEN/UNLOCKED notice in **that fork** and edits
only its local journal config, writer guard/concurrency key, and English/Chinese
README notice links. It records the fork's exact current default-branch HEAD as
its baseline and a fresh observation start time. It does **not** commit, push,
enable Actions, set the writer variable, or claim activation. Review the diff,
run `python -B scripts/check_all.py`, then commit/push deliberately. If the upstream source
patterns have changed, the initializer stops for manual review rather than
guessing a replacement. Reuse requires the marked Issue to have been created
by the currently authenticated fork maintainer; an ordinary user's copy of
the marker cannot be adopted automatically. A different maintainer must
resolve that situation explicitly rather than silently selecting a destination.

Next, the fork owner enables Actions, runs `Documentation journal` manually on
its default branch with `dry_run=true`, and checks the output/gaps. The fork
workflow remains write-disabled while repository variable
`DOCUMENTATION_JOURNAL_ENABLED` is absent or not `true`; a manual dry run is the
only permitted job before that gate. Only after reviewing scope and the dry run
should the owner set that variable to `true`. A subsequent authorized writer run
must be checked for a real bot comment, readback and a repeated run without a
duplicate receipt before that fork may call its journal ACTIVE. The OSS upstream's
ACTIVE result does not transfer to it. A private repository requires a separately
reviewed visibility/authentication adaptation; this initializer refuses it.

### Independent private Factory path

For normal private use, do **not** fork this public repository. The bounded
[Create Private Factory](QUICKSTART.md#2-create-your-private-factory) command
creates a new independent private repository and BLOCKED starter from an exact
public OSS `main` commit. It preserves MIT/source provenance and reuses this
recorder, not a second journal. The generated configuration explicitly sets
`visibility: private` and fixes its own repository ID/name, `main`, notice,
baseline and watched paths. The writer workflow is gated by that repository's
`DOCUMENTATION_JOURNAL_ENABLED` variable; a manual `dry_run=true` is allowed
before opt-in, but automatic writes are not. This OSS installation keeps its
existing public-only default and its own #26 state.

Private missing-object fetch uses only the **same repository's** Actions token
through a Git askpass process. The token is not put in a URL, argv, persistent
Git config, committed file or diagnostic. The private notice must be OPEN,
UNLOCKED and read back as belonging to the configured repository. Its owner
must review a manual dry run, explicitly opt in, then inspect real bot
write/readback and a no-duplicate replay before calling the journal ACTIVE.
Authentication failure is a gap, not permission to substitute another token
or public destination. Private names, paths, SHAs and run evidence stay in
that private repository; do not post them to public OSS Issues.

### Notice access: OPEN and UNLOCKED

The Human-approved policy is recorded in [#28 comment 5736793940](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/28#issuecomment-5736793940):
#26 remains OPEN but is not conversation-locked. The original locked-target trial
returned `403 / LOCKED_CONVERSATION` with the actual Actions token; see
[diagnostic evidence](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/28#issuecomment-5736585363).
The guard now requires an explicitly false `locked` value and an open notice.
If an operator later locks or closes the notice, recording stops; the program never
unlocks, reopens, grants access, or substitutes credentials itself.

Public users can now comment, so maintainers moderate unrelated discussion and
route it to normal Issues/PRs. Public comments are not commands, authority, or
trusted journal receipts. The existing bot identity/run-provenance checks remain
unchanged; copied markers from ordinary users must not advance the cursor.
The token, permissions, destination and event scope have not been expanded.

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

HTTP failures expose only a fixed endpoint category, allowlisted error class and
strictly validated bounded diagnostic headers when present: GitHub request ID,
accepted-permissions requirement, rate-limit remaining/reset and numeric Retry-After.
Accepted permissions describe the endpoint requirement, not the token's actual
grant. Tokens, request bodies, complete headers and raw response bodies are never
printed; malformed or unrecognized responses remain `UNKNOWN`.

For recovery: **Actions → Documentation journal → Run workflow**, keep `main`.
`dry_run=true` checks without writing; set `false` for an authorized replay. All
triggers share a non-cancelling writer concurrency group. GitHub can coalesce queued
runs, delay/drop schedules or disable inactive public schedules; inspect last-run and
gap state, and use manual replay after an interruption.

## Tests and activation

Run `python -B -m unittest discover -s tests -p 'test_documentation_journal*.py' -v`.
The existing `scripts/check_all.py` also discovers these tests. Offline fixtures cover
snapshots, A/B/A, declaration/base corrections, cleared diffs, escaped input, receipt
provenance, chunking, POST loss, partial replay, old-head gaps, lane isolation, Git
renames, no-doc changes, change/revert, timeline recovery and API pagination.
Access-policy regressions cover unlocked acceptance, relocked/closed/unknown-state
rejection and retention of repository/public/default-branch restrictions.
These tests do not impersonate a real bot or prove actual comment access.

Before marking ACTIVE, record the merged workflow SHA, successful real run and bot
comment IDs on the approved OPEN/UNLOCKED #26, followed by a second run proving
receipt deduplication. A candidate PR or green CI alone is not activation. Historical
locked-thread failures remain recorded, not rewritten as successful tests. Do not
change release tags or claim a new release as part of this installation.

Technical references: [GitHub events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows),
[least-privilege permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions),
[workflow security](https://docs.github.com/en/actions/reference/security/secure-use).
