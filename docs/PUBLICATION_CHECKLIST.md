# Publication and release checklist

Use this checklist for the 1.0.0 release and future public release maintenance.
Keep the final release report in Issue #1 (or the applicable release Issue) with the
exact target commit/tree, reused evidence, delta checks, findings, exceptions and
release readback. Do not reclassify author checks or CI as an independent opinion.

## Engineering readiness

For code or behavior changes, run `scripts/check_all.py` on the exact target and
record the actual environment/results. For documentation, licensing, branding or
other public-surface-only changes, use proportionate delta checks and retain prior
behavioral/fresh-Agent evidence for unchanged inputs.

Do not restart the full CI/Agent/history review merely because README or release
packaging changed. Re-run only what the changed surface can materially invalidate.

Reconcile the README, entrypoint, role profile, examples and acceptance procedure.
The accepted behavioral matrix must continue to demonstrate fresh owner/role setup,
missing authority, recovery and authorized true succession, one-body reply/CC,
current-vs-reviewed candidate mismatch and refusal of reserved actions.

## Independent privacy/public-safety review

The reviewer must not be the author of the candidate being independently reviewed.
Inspect the public-facing delta and any newly exposed surfaces: files, generated
outputs, commit metadata, Issue/PR content, screenshots, Actions logs/artifacts,
release notes and assets as applicable.

No private operational transcripts, real appointment/handoff records,
customer/company facts, credentials, private runtime topology or identifying private
evidence belong in the public distribution. A keyword/secret scan is supplemental;
semantic disclosure review is required where risk warrants it.

Prior accepted reviews may be reused for unchanged material. A changed target needs
proportionate revalidation, not a silent inheritance of approval.

## Fresh-Agent acceptance

Follow [the evaluator procedure](COLD_TAKEOVER_EXERCISE.md) when behavior, Agent
inputs, role authority contracts or cold-start fixtures change in a way that can
affect the acceptance matrix. A documentation-only release delta does not by itself
require rerunning unchanged fresh-Agent observations.

A new title in the author's existing conversation is not a fresh Agent. Unknown
session IDs remain `UNKNOWN` or `NOT_EXPOSED`; never invent resumability or hidden
background work.

## Current 1.0.0 publication decisions

- License: **MIT**. See [LICENSE](../LICENSE).
- Repository visibility: **Public**.
- Security reporting: **GitHub Private Vulnerability Reporting**, enabled.
- Personal/private email: **not published** as a reporting contact.
- Release tag: `v1.0.0`.
- Release notes: [docs/releases/1.0.0.md](releases/1.0.0.md).

These decisions do not grant unrelated production, credential, destructive or
external-organization authority.

## Release sequence

1. Resolve the exact final release commit and verify `main` still points to it.
2. Confirm the repository is Public, MIT is present, and Private Vulnerability
   Reporting remains enabled. Verify the **Security -> Advisories -> Report a
   vulnerability** route when an authorized signed-in reporter view is available;
   do not submit a fake vulnerability merely to test the route.
3. Perform the narrow final public-surface delta check. Inspect any newly added
   README, translations, branding, examples, release notes or assets and record
   limitations instead of claiming unperformed checks.
4. Create `v1.0.0` at the exact approved commit. If the tag already exists, verify
   it instead of moving it.
5. Publish the GitHub Release from that tag using the prepared release notes. Do not
   attach private logs, credentials, unrelated archives or screenshots.
6. Read back repository visibility, tag-to-commit mapping, Release URL and security
   reporting state/entry. Record the actual result in Issue #1 and close the release
   Issue only when no blocking release item remains.

If the reporting route, target commit or release artifact cannot be verified, stop
before claiming release completion. Do not silently change the target or bypass the
security channel.

A source-only archive may be produced with `git archive` from the exact tagged
commit if a source archive is useful. Its checksum is integrity evidence, not a
license, privacy or security approval.
