# Office Wardrobe / Work Invocation History

The Wardrobe is an optional recommended continuity facility that records an office role leaving its management context for a Work/Codex/agent execution session and returning with results.

It is not an authority source and does not replace project state, Git evidence, correspondence or handoffs.

Recommended state progression:

```text
ACTIVE -> DONE_UNACKED -> COMPLETED_ACKED
```

Suggested fields:

- role / office identity;
- session or thread id when exposed;
- session title / cwd / project when exposed;
- started and ended timestamps;
- triggering task / Issue / correlation reference;
- repository / branch / SHA context;
- bounded authority carried into the execution session;
- created / reused / resumed / requested-but-not-entered status;
- result summary;
- commit / evidence references;
- acknowledgement by the originating management context.

Unknown platform data must remain `UNKNOWN` or `NOT_EXPOSED`; never invent a session id or claim resumability that the provider does not support.

The Wardrobe is especially useful when heavy execution work is moved out of a long-running management chat.
