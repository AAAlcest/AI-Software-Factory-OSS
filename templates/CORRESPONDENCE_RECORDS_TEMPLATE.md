# One-body correspondence record templates

These are unconfigured shapes, not real records or authority. Replace every
placeholder in a separately authorized instance. For routing see the
[reply contract](../docs/REPLY_ROUTING_CONTRACT.md).
Never copy real private messages into a distributable example.

## Canonical body: recipient inbox

```yaml
record_type: MESSAGE
message_id: UNCONFIGURED
created_at: UNKNOWN
from_role: UNCONFIGURED
to_role: UNCONFIGURED
cc_roles: []
project_id: null
message_type: UNCONFIGURED
in_reply_to: null
reply_mode: REPLY_ALL
classification: UNCONFIGURED
requested_next_action: UNCONFIGURED
```

Only this file holds the subject and message body. `To` owns the stated action
within separately verified authority. Use a fresh unique identifier and trusted
remote time at delivery; never infer actual receipt from creation time.
Add `received_at` or a receipt record only after actual recipient processing.

## Sender outbox: SENT_REFERENCE

```yaml
record_type: SENT_REFERENCE
sent_at: UNKNOWN
from_role: UNCONFIGURED
to_role: UNCONFIGURED
canonical_body: UNCONFIGURED
```

Use the body's basename. This is an index pointer, not a second message body.
Do not claim `sent_at` until canonical delivery has actually occurred.

## Copied recipient inbox: CC_REFERENCE

```yaml
record_type: CC_REFERENCE
copied_at: UNKNOWN
from_role: UNCONFIGURED
primary_to_role: UNCONFIGURED
cc_role: UNCONFIGURED
canonical_body: UNCONFIGURED
cc_action_expected: false
ack_required: false
```

Use `<body-basename-without-extension>-CC_REFERENCE.md`. No duplicated body,
automatic task ownership, review approval or response obligation. If the copied
role must act, address a separate action-bearing message to that role.
A subject/summary is optional only after confirming it does not disclose protected
content to recipients lacking access to the canonical body.
