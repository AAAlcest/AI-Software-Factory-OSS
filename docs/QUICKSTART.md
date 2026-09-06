# Quickstart

## 1. Understand the split

Read [the recommended role setup](RECOMMENDED_ROLE_SETUP.md). Use ChatGPT for
Factory staff/management and Codex for engineering roles. A Human owns decisions;
no example appoints its reader. Unconfigured values remain unknown.

## 2. Run the fictional exercise locally

Use Python 3.10+ from a checkout of the exact candidate. No package installation
or AI credential is needed for the scripts. Choose a new sibling directory:

```sh
python -B scripts/create_demo.py --destination ../factory-first --case first
python -B scripts/validate_demo.py ../factory-first
python -B scripts/validate_instance.py --root ../factory-first/projects/atlas
python -B scripts/plan_reply.py ../factory-first/reply-request.json
python -B scripts/validate_work_history.py ../factory-first/offices/management/wardrobe/atlas.json
```

The builder is the only command above that creates files, and only in its new
explicit destination. A pre-existing destination is rejected; it is never erased.
The generated entrypoint explains where authority, state, inbox, current/pending,
Console and immutable continuity records live. All records are fictional.

Atlas has a declared assignment and a changed candidate requiring new review.
Beacon has no current assignment. Console sees both; it cannot create a worker.
The reply planner's output matches the generated recipient body and sent/CC
references. Work completion acknowledges a BLOCKED result, not product success.

## 3. Verify the distribution

```sh
python -B scripts/check_all.py
```

It runs all tests, checks local Markdown file targets/JSON syntax, and exercises
all nine generated variants through the three helper contracts. It reports
actual test counts/skips and interpreter/platform. Nonzero means fix the reported
problem; never call a skipped or blocked check a PASS. No external link uptime,
semantic privacy, real authority, fresh-agent behavior or production is verified.

## 4. Instantiate your own Factory separately

Use [the starters](../templates/README.md), not copied private histories. Put
real assignments, state, credentials policy and operational records in your own
authorized operating repository; do not fill them into this distributable repo.
Record the Human, explicit role scope, reporting line, current project repository
and environment. Framework `factory.yaml` is configuration guidance, not that
assignment record. A copied template intentionally remains BLOCKED until those
facts are supplied. This guide does not authorize access to an external company.

## 5. Use normal work surfaces

For a bounded task, discuss scope and decisions in an Issue; put implementation,
exact target, tests and review in a PR. Avoid parallel email/ACK bookkeeping.
Optional Factory mail still supports cross-role routing with one canonical body.
Keep current state and unresolved work durable, not hidden in a chat.

For actual fresh-agent verification use [the evaluator procedure](COLD_TAKEOVER_EXERCISE.md).
That is a separate observed run, not this walkthrough or the software test suite.
