# Token-efficiency objective

AI Software Factory does not promise a fixed percentage of token savings. The operating mechanism can instead be measured with facts the environment actually exposes.

## Mechanism

- ChatGPT handles planning, governance, routing, overview and recovery work.
- Skills compress repeated context into bounded project/role packages.
- Codex is used primarily for implementation-heavy work.
- Repository pointers replace repeated transmission of unrelated history.
- A task package expands only when implementation finds a real dependency or conflict.

## Executable local measurement

After generating a fresh cockpit, compare the broader cockpit source set with the selected workstream's bounded engineering source set:

```sh
python -B scripts/measure_context.py \
  --root examples/factory-instance \
  --bundle ../factory-cockpit
```

The report records only observable values:

- source files in the broader cockpit set;
- bytes in that broader source set;
- files and bytes in the bounded task source set;
- excluded files/bytes;
- generated task-package size.

The command first checks source drift. It reports token counts as `NOT_EXPOSED` unless a platform actually provides them. File/byte reduction is evidence of context narrowing, **not** a guaranteed token-saving percentage and not proof of equal task difficulty.

## Repeatable comparison scenario

Choose one project task with a known accepted answer and compare two runs:

**Whole-Factory run** — give the engineering agent the broader relevant Factory/Office/project source set and ask it to discover task context itself.

**Packaged run** — use the generated workstream bundle plus `task-packaging` so the engineering agent starts from only the selected project state, role cursor, workstream/continuity registers and explicit pointers.

When available, record input token/context size, repository files/messages read before implementation, retries caused by missing context, elapsed interaction turns, output correctness and test result. Do not invent hidden platform measurements.

A lower context cost is useful only if correctness and authority discipline are preserved. The design goal is to make **bounded context the default** and whole-Factory rereading the exception, without using token economy as a reason to skip required evidence, security review or Human gates.
