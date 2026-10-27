# Five-minute Quick Demo

Run a **fictional, local-only AI Software Factory** and observe both successful structural checks and an intentional **fail-closed** result. The demos are synthetic; they do not start Agents, contact a production system, or appoint anyone.

**Time:** about 3–5 minutes after you have the source and Python. **Requirements:** Python 3.10+ and an official OSS source checkout (or Source ZIP); no Python packages, GitHub login, ChatGPT account, API key, cloud runtime, or network access is required *for the commands below*.

> The following exercises run against the **checked-out source**, not against a real private operating Factory. The historical `v1.6.0` release is immutable. This source line is 1.7.1, but a checked-in `VERSION` or release note does not mean that `v1.7.1` has already been published. Verify a real GitHub Release before checking out its exact tag. For reproducibility, record `git rev-parse HEAD` when Git metadata is available.

## What you will see

1. A newly generated fictional Factory, with **Atlas** (structurally `VALID`) and **Beacon** (unassigned/`BLOCKED`).
2. A full synthetic-bundle check confirming its declared records and references agree.
3. A starter template that deliberately returns `BLOCKED` because no real owner/appointment/authority is configured.

**Important:** `VALID` means *structurally consistent*, **not** “this Agent may execute.” Every result keeps `execution_authorized: false`. This walkthrough is not a fresh-Agent test or independent privacy/security approval.

## Run the demo

Open a terminal **at the repository root** (where `scripts/` and `templates/` exist). The destination is a new **sibling** directory, not a tracked repository path. **It must not exist yet.** If you have run the demo before, select a different unused name rather than overwriting it.

**macOS / Linux / a terminal with `python` configured:**

```sh
python -B scripts/create_demo.py --destination ../factory-quick-demo --case first
python -B scripts/validate_demo.py ../factory-quick-demo
python -B scripts/validate_instance.py --root ../factory-quick-demo/projects/atlas
python -B scripts/validate_instance.py --root templates/instance
```

**Windows PowerShell (when Python uses the `py` launcher):**

```powershell
py -3 -B scripts/create_demo.py --destination ../factory-quick-demo --case first
py -3 -B scripts/validate_demo.py ../factory-quick-demo
py -3 -B scripts/validate_instance.py --root ../factory-quick-demo/projects/atlas
py -3 -B scripts/validate_instance.py --root templates/instance
```

Run the commands **one at a time**, and inspect each result. The last command is *supposed to return a nonzero exit code*; do not interpret it as a failed safety check or place it in a success-only `&&` command chain.

## Expected observations

Each tool prints JSON. The table shows the relevant fields and process exit codes (additional JSON fields may be present):

| Command | Relevant JSON fields | Expected exit |
| --- | --- | --- |
| `create_demo.py` | `"status": "SYNTHETIC_PACKAGE_CREATED"`, `"case": "first"`, `"execution_authorized": false` | `0` |
| `validate_demo.py` | `"status": "VALID"`, `"atlas": "VALID"`, `"beacon": "BLOCKED"`, `"fresh_agent_validated": false` | `0` |
| `validate_instance.py --root ../factory-quick-demo/projects/atlas` | `"status": "VALID"`, `"execution_authorized": false` | `0` |
| `validate_instance.py --root templates/instance` | `"status": "BLOCKED"`, `"mode": "TEMPLATE"`, `"execution_authorized": false`, nonempty `diagnostics` | **`3` (expected)** |

To inspect the last exit code, run `echo $?` immediately afterward in a POSIX shell; in PowerShell, use `$LASTEXITCODE`. The synthetic example is permitted to be structurally valid while **real-world execution remains unauthorized**.

If you get `INVALID`, or an unexpected status/exit code, stop and inspect the printed diagnostics. The generator refuses an existing destination (exit `2`) instead of silently replacing it. Do not try to “fix” a `BLOCKED` template by inventing an appointment, assigning credentials, or transferring real private data into this public distribution.

### What this proves — and what it does not

```text
public, synthetic inputs
    -> create a NEW disposable Factory directory
    -> validate declared records and role/project links
    -> observe VALID structural data and BLOCKED missing authority
    -> no dispatch, no remote writes, no granted execution permission
```

This is an **offline structural and helper-integration demonstration**, not a live multi-Agent communication test, private instance migration, independent code/privacy review, Human UAT, or release acceptance.

For the broader installed experience, see the [full Quickstart](QUICKSTART.md) / [中文上手说明](QUICKSTART_ZH.md). If you intend to operate a **real** Factory, follow the distinct, Human-authorized [Create Private Factory](QUICKSTART.md#2-create-your-private-factory) workflow. Never treat a public fork or this synthetic exercise as a home for real staff records, project authority, secrets, or customer data.

## Validation evidence and cleanup

The repository's `tests/test_quick_demo.py` exercises these CLI statuses and exit codes in a temporary directory. The [V1 validation workflow](../.github/workflows/validation.yml) runs the integrated suite on Linux and Windows with Python 3.10 and 3.13. Consult the actual **PR exact-head CI run** for observed results; a green workflow proves only its declared checks, not independent acceptance.

When finished, inspect the generated `../factory-quick-demo` directory. **Only if it is the disposable directory you just created**, you may delete it:

```sh
rm -r ../factory-quick-demo
```

PowerShell equivalent:

```powershell
Remove-Item -LiteralPath ../factory-quick-demo -Recurse
```

These cleanup commands are *instructions for your own disposable exercise*, not commands run by the Factory or a preflight. Do not run them on an operating repository or on a path you did not verify.

---

**中文速览：** 本演示只使用虚构数据，不需要 API Key；运行前确认目标目录尚不存在。Atlas 的 `VALID` 仅代表结构检查通过，`execution_authorized` 仍为 `false`；未配置的模板返回 `BLOCKED`（退出码 3）是正确的安全拒绝行为。任何真实私人 Factory 必须单独创建并取得 Human 授权。
