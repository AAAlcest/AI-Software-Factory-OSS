# Reply routing contract — V1 slice B

This is a **read-only routing planner**, not a mail service or permission engine.
It implements the routing mechanics in [Correspondence and CC](CORRESPONDENCE_AND_CC.md)
and [Project Mailbox and Console](PROJECT_MAILBOX_AND_CONSOLE.md).
It does not depend on the instance preflight candidate or change its files.

## Run the synthetic example

From the repository root, using Python 3.10 or later (no third-party dependencies):

```sh
python -B scripts/plan_reply.py examples/correspondence/reply-request.json
python -B -m unittest discover -s tests -p 'test_plan_reply.py' -v
```

The example is entirely fictional; it is not a renamed real conversation.
A successful plan prints `PLANNED`, exits 0 and always includes
`execution_authorized: false` and `delivery_performed: false`.
Invalid or unsupported input prints a sanitized `INVALID` result and exits 2.
CLI argument errors also exit 2 using the normal argument-parser diagnostic.
Only the supplied request file is opened; generated mailbox paths are not read,
created or sent anywhere. No credentials, network, Git mutation or background work.

## Input contract

Use [the JSON example](../examples/correspondence/reply-request.json) as the shape.
Required fields: `schema_version: 1`, `actor`, `reply_id`, `parent`, `endpoints`.
Optional: `reply_mode` (default `REPLY_ALL`), `mandatory_cc` (default empty),
`console_role` (default `role:portfolio-console`). Unknown fields are rejected.

`parent` is the **immediate canonical message**, not a sent/CC reference or an
entire thread. It requires `record_type: MESSAGE`, `message_id`, `from_role`,
`to_role`, `cc_roles`; `project_id` is optional. Resolve a reference to its real
body before supplying it. The planner does not authenticate that resolution.

Role identifiers are `role:<slug>` or `project:<slug>`. Slugs use lowercase ASCII
letters, digits and hyphens, start with a letter/digit and have at most 80 characters.
Endpoint roots are unique `offices/<slug>` or `projects/<project-id>` paths.
No absolute paths, URL roots, traversal, arbitrary aliases or recipient display names.
One ordinary primary recipient is supported; alias resolution must happen first.

The caller must supply a **current, authority-checked** parent, endpoint registry
and complete mandatory-routing policy. These inputs are declarations, not proof.
The planner cannot discover a policy omitted by the caller, verify appointments,
validate cross-domain disclosure rights, or decide which historical CC was legitimate.
Uncertain or prohibited disclosure requires escalation, not silent policy removal.

## Deterministic rules

1. Only the parent's primary `To` can use this ordinary reply path; CC is visibility,
   not a task or reply obligation. Self-reply and reusing the parent message ID fail.
2. The reply goes to the parent sender. `REPLY_ALL` inherits only the immediate
   parent's CC set; `REPLY_ONLY` drops that discretionary set.
3. Add supplied mandatory CC. Project-scoped mail also requires the configured
   Portfolio Console; explicit `project_id` or an involved project endpoint triggers it.
4. Remove the reply sender and primary recipient from CC; deduplicate and sort.
   A directly involved Console needs no self-CC. Unknown endpoints fail even when
   `REPLY_ONLY` would drop them, so malformed parent metadata is not hidden.
5. Construct exactly one recipient-inbox body, a same-basename sender-outbox
   `SENT_REFERENCE`, and one `-CC_REFERENCE.md` per copied role. All references
   point to that one body. CC records explicitly carry no ACK/action expectation.

A role can still be assigned a separate task by another canonical message; the
CC rule does not remove that independent obligation. There is no recursive
thread scan or resurrection of recipients dropped in earlier generations.

## Delivery is a separate controlled operation

[The record template](../templates/CORRESPONDENCE_RECORDS_TEMPLATE.md) describes
body/reference metadata. A delivering adapter must independently verify identity,
source and disclosure authority, use trusted platform/server timestamps under the
instance's time policy, confirm destination/ref and avoid overwriting existing IDs.
Create the body and required references as one validated batch where supported;
report partial delivery honestly if an atomic mechanism is unavailable.
`PLANNED` does not prove any path exists or any message was delivered.

## Verification boundaries

Unit tests check routing, malformed requests, reference construction, sanitized CLI
failure and absence of request-directory writes. They do not prove actual mail
storage validation, reply content privacy, fresh-agent CT-05 acceptance, independent
review, live Git freshness or production reliability. Python 3.10+ is a target;
verified interpreter/platform results belong in the exact candidate PR.
The helper is not a filesystem security sandbox or a transport implementation.
Full mailbox fixtures, delivery validation, multi-project state/Console integration,
Wardrobe and real fresh-agent acceptance remain later work under Issue #1.
