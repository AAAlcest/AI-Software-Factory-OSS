# Synthetic Work Invocation History exercise

Every person/role, project, date and `fixture:` reference in
[completed-session.json](completed-session.json) is invented. The referenced
observations, result and receipt are labels only, not files or real evidence.
The fixture is not exported or renamed operating history. Provider session ID
and working directory deliberately remain `NOT_EXPOSED`.

The worker returns documentation with an unresolved review. The originating
management role acknowledges receipt, so the invocation reaches
`COMPLETED_ACKED`; the outstanding product review is not thereby passed.

Run from the repository root:

```sh
python -B scripts/validate_work_history.py examples/work-history/completed-session.json
python -B scripts/validate_work_history.py templates/work-history/session.json
python -B -m unittest discover -s tests -p 'test_work_history.py' -v
```

Expected outcomes (not a claim of execution):

| Input | Result |
| --- | --- |
| Completed synthetic record | `VALID`, `COMPLETED_ACKED`, exit 0. |
| Copy with only the first event | `VALID`, `ACTIVE`; not proof of current liveness. |
| Copy with the first two events | `VALID`, `DONE_UNACKED`; management receipt still outstanding. |
| Unconfigured starter | `BLOCKED`, exit 3; no session invented. |
| Worker role substituted for the final receipt actor | `INVALID`, `ACK_ROLE_MISMATCH`. |
| Old event edited when compared with the original via `--previous` | `INVALID`, `HISTORY_REWRITTEN`. |

Every result keeps execution, liveness, evidence-verification and independent
review flags false. Tests exercise copies in memory/temporary directories; never
edit fixture files to pretend an actual invocation happened.

For fields, limitations and snapshot rules, read the
[contract](../../docs/WORK_HISTORY_CONTRACT.md). Actual test results belong in the
candidate PR with its exact revision and platform limitations. This exercise is
not a fresh-agent cold-takeover run.
