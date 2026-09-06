# Final publication checklist

The output of preparation is a **candidate**, not a public release. Keep a single
final report in Issue #1 with candidate commit/tree, test commands/results/skips,
actual defects fixed, remaining findings and exact evidence links. Do not
reclassify author checks or CI as an independent opinion.

## Engineering readiness

For code or behavior changes, run `scripts/check_all.py` on the exact target.
For the Human-approved MIT/security/documentation-only preparation, check only
the delta and its direct links. Verify code, tests, examples, templates, profiles
and workflows are unchanged; retain their previous test and acceptance evidence.
Do not restart the full CI/Agent/history review for this metadata-only change.
Review changed content and any affected generated-template inputs. Record actual interpreter/platform and
unverified cases. Reconcile the README, entrypoint, role profile, examples and
acceptance procedure. Demonstrate fresh owner/role setup, missing authority,
recovery and **authorized true succession**, one-body reply/CC, current-vs-reviewed
candidate mismatch and refusal of reserved actions.

## One independent privacy/public-safety review

The reviewer must not be the final candidate's author. Inspect the integrated
files, generated outputs and outward-facing surfaces: all branches/commit history,
commit metadata, Issues/PRs/comments, releases/assets, Actions logs/artifacts and
any screenshots/attachments intended to be visible. Start with an inventory; list
uninspected surfaces rather than claiming universal clearance. No private
operational transcripts, real assignments/handoffs, customer/company facts,
credentials, runtime topology or identifying private evidence belong here.

A keyword/secret scan is supplemental; semantic disclosure review is required.
Use only public-safe findings in the product Issue. Keep confidential evidence in
an already-authorized private location; do not create duplicate routine mail.
Prior slice reviews can be reused as scoped evidence, but final additions and
integration must actually be considered. Record target SHA/tree, scope, findings,
limitations and PASS / RETURN_FOR_REVISION / BLOCKED. A changed target needs
proportionate revalidation, not silently inherited approval.

## Actual fresh-Agent cold start

Follow [the evaluator procedure](COLD_TAKEOVER_EXERCISE.md). A new role title in
the author's existing conversation is not a new Agent. Record the test checkout,
fixture manifests, new-session/isolation facts, available tools, actual transcript,
attempted prohibited actions, and expected-versus-observed results. Do not supply
the answer rubric to the participant. Unknown session IDs remain NOT_EXPOSED.
This is a read-only simulation; it does not exercise real publication or secrets.

## Human decisions implemented in this preparation

The Human selected **MIT** and **GitHub Private Vulnerability Reporting**, with no
personal email published. See [LICENSE](../LICENSE) and [SECURITY.md](../SECURITY.md).
The prepared version is **1.0.0**; proposed tag `v1.0.0` and Release are not created.
The final commit/tree and exact delta are reported in Issue #1. License selection
is not authority to change visibility, enable the channel now or publish a Release.

Reuse the completed acceptance/privacy results at their original targets. The
existing independent privacy reviewer considers only this license/security/docs
delta and any newly proposed publication surface, not another whole-history audit.
Author checks are not that independent opinion. Do not proceed with a blocking
finding or silently apply old approval to new bytes.

## Owner-authorized Public rollout (not performed during preparation)

1. Obtain explicit Human approval identifying the final SHA and the allowed
   operations: Public visibility and Release publication. Confirm the target,
   accepted evidence, MIT file and any narrow disclosure-delta disposition.
2. Recheck the exact branch/commit and publication scope, then change this
   repository to Public using authorized access. Do not alter other repositories,
   expose private material, expand credentials or rewrite history.
3. Enable **GitHub Private Vulnerability Reporting** and verify its enabled status
   plus the **Security -> Advisories -> Report a vulnerability** entry and private
   form for this repository, as described in SECURITY.md. This is deliberately
   after the authorized visibility change because the feature is for public
   repositories. A written link is not a passed live check. Do not submit a fake
   report; verify only with already-authorized access. If tooling or access is
   insufficient, hand the bounded action to the owner rather than bypass it.
4. Only after that activation/readback succeeds, create `v1.0.0` pointing to the
   explicitly approved SHA, verifying an existing tag instead of moving it. Publish
   the Release only if that operation was explicitly approved. Use the
   [prepared release notes](releases/1.0.0.md); no extra asset upload is assumed.
5. Record actual Public status, license recognition, reporting status/entry,
   tag-to-commit mapping and Release URL in Issue #1. A partial rollout stays
   partial: if reporting verification fails after Public, stop before Release
   and report the issue; do not invent successful closure or silently roll back.

No Public change, PVR enablement, tag or Release is authorized merely by completing
this checklist. Further content, license or asset changes require a newly
identified target and proportionate checks, not a full restart of unchanged work.

A source-only archive can be prepared locally with `git archive` from the exact
approved commit; it need not contain `.git` or any other repository's history.
Preparing an archive does not authorize upload or a public release. An archive
checksum is integrity evidence, not license or privacy approval. Actual release
creation and visibility change remain Human-gated operations.
