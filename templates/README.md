# Framework templates

These files are generic starting points, not real appointments or operating
records. Instantiate only into an explicitly authorized destination. Do not
import a private repository or rename private histories into examples.

[instance/instance.json](instance/instance.json),
[instance/authority.json](instance/authority.json),
[instance/state.json](instance/state.json) and
[instance/CURRENT.md](instance/CURRENT.md) form one small starter. The directory
is intentionally unconfigured: preflight must return `BLOCKED`, exit 3.
Use the [instance contract](../docs/INSTANCE_BOOT_PROTOCOL.md) when configuring
an organization's own records. File existence is not proof of real authority.

[STAFF_OFFICE_TEMPLATE.md](STAFF_OFFICE_TEMPLATE.md) and
[PROJECT_ROOM_TEMPLATE.md](PROJECT_ROOM_TEMPLATE.md) define the durable facility
layout without creating one permanent chat per role. The compact demo uses flat
records for testing; it does not yet instantiate all facilities in this guide.

## Suggested instance layout

```text
instance.json                   # explicit pointers, not secret storage
factory/                        # current Factory state and governed rules
registers/                      # thin role/project/decision/evidence indexes
meeting-hall/                   # shared meeting indexes, not copied bodies
offices/<role>/
  README.md                     # scope, authority pointers, reporting line
  inbox/                        # canonical addressed messages or CC references
  outbox/                       # SENT_REFERENCE, not duplicate full bodies
  desk/CURRENT.md               # one rolling recovery cursor
  desk/pending/                 # unresolved items only
  wardrobe/                     # optional execution-session transition records
projects/<project>/
  README.md                     # project identity and product repo pointer
  authority.json                # declaration referencing original authority
  state.json                    # current state and evidence pointers
  inbox/                        # project-owned canonical correspondence
  outbox/                       # project-owned sent references
  evidence/                     # bounded facts or evidence references
```

Map logical roles to actual permitted endpoints. An executive display title can
change without changing its responsibility bundle. Register entries and cursors
reference canonical facts; they must not become conflicting copies of them.

Finalized handoffs are added only for a real tenure boundary. The starter does
not ship an invented predecessor. Record unknown session/thread identifiers as
`NOT_EXPOSED`, and do not represent a planned session as running.
