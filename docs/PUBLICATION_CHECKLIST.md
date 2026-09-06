# Final publication checklist

The output of preparation is a **candidate**, not a public release. Keep a single
final report in Issue #1 with candidate commit/tree, test commands/results/skips,
actual defects fixed, remaining findings and exact evidence links. Do not
reclassify author checks or CI as an independent opinion.

## Engineering readiness

Run the complete `scripts/check_all.py` suite on the final tree. Review the net
change and all generated-template inputs. Record actual interpreter/platform and
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

## Human gates and export preparation

The Human chooses the license and authorizes any transition to Public. Neither
is inferred from a merge, a public-safe candidate name or successful tests.
After a license decision, add exactly the approved license and reconcile its
metadata; inspect that delta. Before changing visibility, recheck the final target
and the independently reviewed disclosure inventory. Do not publish while a
blocking privacy/acceptance finding remains.

A source-only archive can be prepared locally with `git archive` from the exact
approved commit; it need not contain `.git` or any other repository's history.
Preparing an archive does not authorize upload or a public release. An archive
checksum is integrity evidence, not license or privacy approval. Actual release
creation and visibility change remain Human-gated operations.
