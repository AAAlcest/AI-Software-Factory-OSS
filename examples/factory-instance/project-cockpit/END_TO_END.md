# End-to-end management → Codex example

> DERIVED COCKPIT SNAPSHOT — synthetic example only; repository records remain canonical.

This walk-through shows how a Human can use ChatGPT management to prepare a bounded engineering task for Codex without asking Codex to reread the whole Factory.

## 1. Human request

The Human asks `role:management` to prepare the next safe Atlas work item.

ChatGPT management starts from the cockpit, then refreshes only the canonical sources relevant to Atlas:

- `projects/atlas/STATE.md`
- `projects/atlas/README.md`
- `offices/management/desk/CURRENT.md`
- the active Atlas pending/review pointer when needed

It does **not** replay unrelated Office histories, Beacon details, old handoffs or the whole Factory conversation history.

## 2. Management finding

The refreshed Atlas state says:

- current candidate: `fixture:atlas-candidate-b`
- reviewed candidate: `fixture:atlas-candidate-a`
- status: ACTIVE

The current candidate differs from the reviewed candidate, so the prior review cannot be reused silently. Management keeps publication, credentials and production actions outside this task.

## 3. Bounded package

Management produces [CODEX_TASK_PACKAGE.md](CODEX_TASK_PACKAGE.md). The package gives Codex:

- the exact task;
- target project;
- only the relevant paths;
- current/reviewed candidate facts;
- the accepted review rule;
- explicit exclusions and Human gates;
- expected output and checks;
- source pointers if a refresh is required.

The package is derived context, not authority by itself.

## 4. Codex execution boundary

Codex begins with the bounded package and the two target Atlas files. It should expand beyond them only if implementation reveals a concrete dependency, conflict or missing fact.

In this synthetic scenario Codex does **not** need to read:

- `offices/runtime/`
- `offices/governance/` history
- `projects/beacon/`
- Factory-wide historical handoffs
- unrelated correspondence

That reduction is the token/context-efficiency mechanism: fewer irrelevant reads while preserving the sources required for correctness.

## 5. Result return

Codex returns a scoped patch/result note to the project workflow. It does not claim integration, publication or management approval.

ChatGPT management then refreshes the relevant canonical project state/evidence, records the result in the appropriate Issue/PR, and routes any needed review. If the candidate or authority changed during execution, management reports the conflict instead of trusting the stale package.

## 6. What this example proves — and does not prove

It demonstrates the intended operating sequence:

`Human → ChatGPT management → bounded canonical refresh → task package → Codex → result/evidence → ChatGPT reconciliation`

It does not prove a fixed token-saving percentage, a live ChatGPT Project integration, a real Codex session, organizational authority or independent privacy approval.
