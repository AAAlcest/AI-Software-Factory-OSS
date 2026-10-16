# Portable Factory Doctor

`scripts/factory_doctor.py` is a cross-platform, Python-stdlib, **read-only**
diagnostic for a framework checkout or operating Factory repository.

It is a health/readiness aid, not an authority service.

## Run

Human-readable local checks:

```sh
python -B scripts/factory_doctor.py
```

Machine-readable output:

```sh
python -B scripts/factory_doctor.py --json
```

Optional read-only GitHub CLI/auth/repository reachability checks:

```sh
python -B scripts/factory_doctor.py --json --github
```

Use `--root <path>` only when deliberately inspecting another local
Factory/repository root.

## What it checks

The current bounded Doctor can inspect:

- root `AGENTS.md` and `AI_ENTRYPOINT.md`;
- whether the surface looks like the public framework distribution or an operating
  instance;
- Execution-First and rationale-index surfaces;
- Git availability, selected root, HEAD, branch/detached state, worktree cleanliness
  and origin presence;
- tracked filenames matching a small secret-like pattern set;
- the root instance contract, when present, using the existing
  `validate_instance.py` semantics;
- `SOURCE_PROVENANCE.json`, when present;
- documentation-journal repository/visibility/notice/baseline binding, when present;
- optional `gh` availability, authentication and repository readback.

Warnings remain distinct from failures. An unconfigured private starter can be
structurally healthy while its instance validator reports `BLOCKED`; that is the
expected state before real Human authority/project configuration.

## Read-only boundary

Doctor does not:

- edit files;
- stage, commit, checkout, reset, fetch, pull or push Git;
- create Issues/PRs/repositories;
- set repository variables/settings;
- write credentials;
- activate the documentation journal;
- execute an instance's declared next action.

Default mode performs no GitHub/network check. `--github` only invokes read-only
GitHub CLI/auth/repository queries.

## Result meaning

`PASS` means the checks actually run by Doctor found no failures or warnings.
`WARN` means no hard failure was found but one or more bounded checks could not
establish their preferred condition. `FAIL` means at least one checked condition
failed.

Every result has `execution_authorized: false`.

Doctor PASS does **not** prove organizational authority, evidence authenticity,
privacy, release/deployment readiness, production permission, operating-system
isolation or fresh-Agent acceptance. Keep those gates and evidence separate.

Doctor output may still contain repository-local evidence such as a Git SHA. Treat
output from a private Factory as private unless reviewed for publication.
