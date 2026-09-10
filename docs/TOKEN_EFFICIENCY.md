# Token-efficiency objective

AI Software Factory does not promise a fixed percentage of token savings. V1.1 instead defines an operating mechanism that can be measured.

## Mechanism

- ChatGPT handles planning, governance, routing, overview and recovery work.
- Skills compress repeated context into bounded project/role packages.
- Codex is used primarily for implementation-heavy work.
- Repository pointers replace repeated transmission of unrelated history.
- A task package expands only when implementation finds a real dependency or conflict.

## Repeatable comparison scenario

Choose one project task with a known accepted answer and compare two runs:

**Whole-Factory run** — give the engineering agent the full Factory/Office/project history and ask it to discover the task context itself.

**Packaged run** — use `project-overview` plus `task-packaging` to provide only the selected project state, active Issue/PR, applicable constraints, relevant paths and expected checks.

Record for each run:

- input token/context size where the platform exposes it;
- number of repository files/messages read before implementation begins;
- implementation retries caused by missing context;
- elapsed interaction turns;
- output correctness and test result.

A lower context cost is useful only if correctness and authority discipline are preserved. Do not count hidden platform behavior that is not exposed, and do not fabricate token numbers.

## Practical target

The design goal is to make **bounded context the default** and whole-Factory rereading the exception. This increases useful work per model/subscription budget without treating token economy as a reason to skip required evidence, security review or Human gates.
