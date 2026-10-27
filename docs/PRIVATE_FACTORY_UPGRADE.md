# Upgrade an existing private Factory (minimal framework slice)

**Status:** bounded V1 source implementation accepted in [#39](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/39), with independently reviewed code and a [disposable-private live tester PASS receipt](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/52#issuecomment-6274622130). This is not a Release announcement: check [GitHub Releases](https://github.com/AAAlcest/AI-Software-Factory-OSS/releases) for actual publication. It is not an automatic migration. An operating private Factory is **not a fork** of this public repository. Its state, correspondence and project data are not synchronized with OSS.

## What this version can update

The first supported managed set is intentionally **only three exact-copy files**:

- `scripts/validate_instance.py`
- `templates/STAFF_OFFICE_TEMPLATE.md`
- `templates/PROJECT_ROOM_TEMPLATE.md`

These files exist in the v1.6.0-era [Create Private Factory](QUICKSTART.md#2-create-your-private-factory) starter. Their original copies can be verified against the old recorded OSS commit, so an unmodified private copy may be replaced. This does **not** update every framework file.

**Not managed:** root `instance.json`, `authority.json`, `state.json`, `CURRENT.md`, `README.md`, `AGENTS.md`, `AI_ENTRYPOINT.md`, `projects/**`, `offices/**`, evidence, correspondence, handoffs, user files, `scripts/documentation_journal.py`, `.github/**`, private journal configuration/workflows, repository variables, secrets and credentials.

The new `FRAMEWORK_MANAGED_LOCK.json` records these three public source paths, SHA-256 hashes, source ref and source commit; `SOURCE_PROVENANCE.json` advances to the reviewed upstream source and explicitly records `managed_scope=EXPLICIT_PARTIAL_FRAMEWORK_UPGRADE`. **That source pointer means only the locked managed subset was upgraded.** Other framework/instance files retain their own content and history. A subsequent upgrade must verify the lock and actual prior public source again; it must not infer ownership from a filename alone.

This is not a generic migration engine, schema upgrader, file merge tool or background synchronizer. New framework features outside the three-file set are not delivered by this slice.

## Requirements

1. A **clean, full-history** checkout of the official `AAAlcest/AI-Software-Factory-OSS` repository from either **exact current official `main`** or **the exact official version-matching `v1.7.1` release tag after it is published**. Main mode requires local HEAD, origin main and GitHub API main equality. Detached tag mode requires the local version tag, remote tag and GitHub API tag target to resolve to exactly the same commit; unsupported annotated tags fail closed. Existing Factories may have been created from an older tag or main; their recorded source commit must be locally available and an ancestor of the selected source commit. Shallow/incomplete histories fail closed.
2. Python 3.10+, Git and GitHub CLI; authenticate explicitly with `gh auth login`. The tool accepts only an authenticated-user-owned **private, non-fork, `main`-default** repository with push permission.
3. A valid `SOURCE_PROVENANCE.json` in the private Factory, its root instance anchor and all three managed files. For old #37 starters without a managed lock, their bytes must **exactly** equal historical OSS source counterparts. Edited/missing/ambiguous files cause a stop, not overwrite.
4. If private documentation-journal configuration exists, it must still identify that private repository, private visibility, `main`, its notice, a valid baseline and a known cadence. No journal setting or existing private notice/history is edited.

## Preview first — **no mutations**

From a clean official OSS checkout, use **exact current `main`** or the verified **detached `v1.7.1` release-tag checkout only after publication**. Do not run from a feature branch or assume the unreleased tag already exists:

~~~powershell
py -3 -B scripts/update_private_factory.py --repository YOUR_LOGIN/Your-Private-Factory
~~~

On macOS/Linux, use `python3` instead of `py -3`.

Preview reads current Git/GitHub and the **three bounded target files** to compare public hashes. It prints a sanitized plan with `source_ref`, `changed_managed_paths`, prior/new OSS source SHAs and whether a legacy lock must be reconstructed. It does not clone a private repository, copy its records, create a branch, open a PR or change a variable. It does not write a local upgrade workspace.

If old public source history cannot be verified, the repository is not private/non-fork, journal identity is inconsistent, an upgrade branch/PR already exists, or any managed file has changed locally, **preview fails closed**. Do not force the update or hide a conflict by replacing private files.

## Apply only after reviewing the preview

**This is a separate explicit Human-authorized remote write**, not something a public OSS Agent may infer from a passing preview:

~~~powershell
py -3 -B scripts/update_private_factory.py --repository YOUR_LOGIN/Your-Private-Factory --apply
~~~

After repeating the validations, `--apply` creates:

1. Git blobs and a commit derived from the **verified private `main` tree**, changing only the proven managed files, `SOURCE_PROVENANCE.json` and the new lock.
2. A new **private upgrade branch**, named `factory-upgrade/<old-source>-to-<new-source>`.
3. Exactly one **draft private PR** targeting `main` for explicit inspection.

It never pushes private `main`, merges a PR, changes repository visibility/permissions, alters writer opt-in, modifies instance-owned records or creates a public Issue/PR with private repository identity. A failed partial apply is intentionally **not auto-recovered or deleted**; inspect private branch/PR state manually before trying again. Never paste private repository identifiers, SHA coordinates, run IDs or logs into the public OSS Issue.

**Review inside the private repository**: confirm target `main` is unchanged, PR diff contains only the three allowed managed paths plus lock/provenance, private state files are byte-identical, journal config/history/notice/opt-in unchanged, and your local/private candidate checks pass. Merge is a separate Human/repository decision. A private PR is not acceptance, and a successful preview is not execution authorization.

## Limits and evidence

- First slice operates only on verified user-owned repositories. Organization-owned Factories, arbitrary tags/branches or unsupported annotated tags, schema migration, user-edited file merging, implicit branch/PR resume, journal workflow/runtime changes and automatic release selection are **NOT_SUPPORTED**. The selected exact official source is limited to current main or the matching published release tag.
- A conflicting upgrade branch or any open upgrade PR requires manual disposition, not duplicate PRs or force-push.
- Synthetic tests in `tests/test_update_private_factory.py` mock GitHub and use disposable fixtures; they prove fail-closed logic but **do not substitute for private live acceptance**. The separately authorized [#52 disposable private run](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/52#issuecomment-6274622130) reported real remote PASS for the existing **official-main source mode**. The new exact-release-tag source mode needs a read-only post-publication smoke check against the actual immutable tag; its RC verification before publication is synthetic.
- Do not run this on an actual operating Factory as a validation shortcut. Full private evidence is retained in the tester's private workspace, and fresh release-tag verification must remain read-only on a disposable test instance. Any real `--apply` remains separately Human-authorized.
