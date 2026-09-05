# Correspondence and CC

## One canonical body

Durable correspondence should avoid duplicating full message bodies.

```text
Sender
  -> Primary recipient inbox: canonical body
  -> Sender outbox: SENT_REFERENCE
  -> copied recipient inbox: CC_REFERENCE
```

`To` owns the ordinary action/reply obligation.

`CC_REFERENCE` is visibility only. It does not create task ownership, approval duty, response duty, SLA, blocking state or authority transfer.

If a copied role must act, send an explicit action-bearing message or task to that role.

## Reply-All

A durable reply should resolve its immediate parent, reply to the parent sender, inherit the legitimate parent CC set for one generation, remove self/duplicates, then apply any independently mandatory routing.

`REPLY_ONLY` may drop discretionary CC but must not suppress mandatory security, Human-only or project-portfolio visibility rules.

Prefer deterministic helpers over asking every AI to reconstruct recipient routing from memory.
