# Bounded Codex task package

> DERIVED COCKPIT SNAPSHOT — synthetic example; package scope is not authority by itself.

Task: prepare the Atlas documentation candidate so it clearly states that the current candidate requires fresh review because it differs from the reviewed candidate.

Target project: `project:atlas`
Relevant paths: `projects/atlas/README.md`, `projects/atlas/STATE.md`
Current candidate: `fixture:atlas-candidate-b`
Reviewed candidate: `fixture:atlas-candidate-a`
Accepted decision: prior review does not transfer to changed bytes
Constraints: documentation-only; do not integrate/publish; do not touch Beacon; no credentials or external systems
Expected output: bounded patch plus a concise validation/result note
Required checks: preserve synthetic-only markings and current/reviewed candidate mismatch
Source pointers: `projects/atlas/STATE.md`, `offices/management/desk/CURRENT.md`

Expansion rule: Codex should not reread unrelated Office/Factory history. Expand scope only if the target files reveal a concrete dependency, conflict or missing fact.
