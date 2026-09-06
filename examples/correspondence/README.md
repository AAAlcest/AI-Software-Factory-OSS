# Synthetic correspondence exercise

Everything here is authored fiction. The role IDs, project, message IDs and
mailbox roots are not actual appointments, operating history or service locations.

[reply-request.json](reply-request.json) describes a fictional management task to
Project Atlas, copied to Governance and Portfolio Console. Run the read-only
planner described in [the contract](../../docs/REPLY_ROUTING_CONTRACT.md).

Expected default plan:

- reply `To`: `role:management`;
- CC: `role:governance`, `role:portfolio-console`;
- one canonical body: `offices/management/inbox/synthetic-reply-002.md`;
- sender reference: `projects/atlas/outbox/synthetic-reply-002.md`;
- two CC references, each pointing to the same body.

Change only `reply_mode` to `REPLY_ONLY` in a disposable copy: Governance drops,
Console remains. Add Governance to `mandatory_cc`: it must remain in both modes.
Set `actor` to Governance: planning fails because a copied role cannot claim the
primary recipient's ordinary action/reply path.

The paths above are planned fixtures, not files this example claims to have
created or delivered. No real timestamp, Git commit, approval or agent result
is simulated as genuine evidence. Unit tests are not fresh-agent acceptance.
