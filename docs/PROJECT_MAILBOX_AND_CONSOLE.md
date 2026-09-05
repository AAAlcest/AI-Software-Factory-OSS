# Project Mailbox and Development Portfolio Console

## Durable project identity

A formal project may own:

```text
projects/<project>/inbox/
projects/<project>/outbox/
```

The durable identity is the project. A Project Primary chat/model is only the current operator.

## Portfolio visibility

Material durable project correspondence may automatically create a visibility-only reference for the Development Portfolio Console.

Desired route:

```text
project-related durable message
  -> primary action owner
  -> sender sent-reference
  -> Development Portfolio Console CC reference
```

Console visibility is not implementation authority.

The Console may track cross-project priority, stale state, blockers, missing handoffs and missing evidence. It must not silently become Project Primary, change scope, approve release or open a parallel implementation lane merely because it was copied.

If Console action is required, address Console explicitly as the action owner.

Routine coding chatter, tests and tiny refactors should remain inside the executing workflow instead of generating mail solely to feed the Console.
