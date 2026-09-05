# GitHub-Native Workflow

## Issue = Factory Meeting / Coordination Surface

An Issue may be used for:

- product or architecture deliberation;
- cross-project discussion;
- `DECISION_REQUIRED`;
- evidence gathering;
- gate discussion;
- Human decision points;
- long-running open loops.

GitHub assignee or username state does not by itself grant Factory authority.

## PR = Candidate Change Envelope

A PR represents a bounded candidate state plus evidence and review context.

```text
Working branch
  -> exact candidate HEAD
  -> PR Candidate Change Envelope
  -> implementation evidence
  -> role-specific review
  -> APPROVE_SUBMIT or RETURN_FOR_REVISION
  -> exact candidate integration
  -> post-integration readback
```

The exact-head concept is most useful when review precision matters. Small low-risk changes should not be burdened with ceremony that adds no safety value.

## Credential vs organization

The same GitHub credential may technically create branches, comments, Issues or PRs for several logical AI roles. The Factory should separately record which role/authority caused the action.
