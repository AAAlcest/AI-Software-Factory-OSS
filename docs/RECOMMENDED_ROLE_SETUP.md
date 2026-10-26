# Recommended Factory setup — chat manages, engineering executes

**Discuss and think in chat. Give precise work to the Agent with hands.**

This division is the Factory's working method, not merely an organization
chart or a menu of interchangeable AI products. The chat-based manager spends
its attention on understanding Human intent, thinking through designs and
trade-offs, governing project direction and defining acceptance. The hands-on
engineering role spends its execution capacity on actual implementation,
builds, tests and debugging. Management then inspects the returned evidence
and decides whether the work meets the brief or needs correction, within its
authority and with independent review or Human decisions where required.

## Why use a chat role for management?

Routine requirements discussions, design iterations and management decisions
should stay in the ordinary chat surface rather than repeatedly launching the
coding/execution environment. That lets Human and manager reason carefully
without consuming **coding/execution runs for those management discussions**.
Reserve development execution usage for work that needs the project's actual
files, terminal, build tools and tests. Do not send an executor an unexamined
wish and make it spend its development budget discovering all the intent and
acceptance criteria itself.

This is not a promise that chat services are free or unlimited, that every
provider separates its usage pools, or that a fixed percentage will be saved.
Use the user's actual tools and quota arrangement. The operational objective
remains clear: **do not unnecessarily spend coding execution capacity on work
that can be thought through and managed in chat**.

## Two working surfaces, not just two titles

| Working role | Where and how it works | What it hands back |
| --- | --- | --- |
| **Chat-based manager** | Ordinary conversational context: discuss with Human, compare designs, make scoped decisions, manage priorities and dependencies. May use authorized GitHub/repository connectors to read evidence, write tasks and coordinate reviews without launching a coding session for routine management. | An actionable task with context, exact work surface, scope, non-goals, acceptance criteria and evidence requirements; later, a justified acceptance or correction decision. |
| **Hands-on engineering executor** | An authorized development environment with actual project files, editing, command execution, builds, tests and debugging tools. A model that merely prints code in chat is not equivalent to this execution environment. | Actual code/artifacts, test results, limitations and evidence for the manager/reviewer to inspect. |

The manager is **not merely a prompt formatter or task messenger**. It owns
real thinking, product design, coordination and scoped disposition. Engineers
still reason about implementation and may raise discoveries or ambiguities;
management/execution separation does not forbid engineering judgment. If the
brief cannot resolve a material product decision, return that decision to the
manager/Human instead of guessing and expanding scope.

A task handoff should specify: **what to change, why, where, what not to touch,
what counts as done, what evidence to return, and where to report it**. An
Issue is a durable coordination surface, not proof that another Agent was
automatically awakened. Never invent automatic communication or execution.

## Recommend this during private-Factory creation

**To the AI helping a Human build a Factory:** Explain the above mechanism
before proposing `--apply`. Then recommend a minimal setup:

**Human director + one chat-based manager + one hands-on project developer**,
with a separate reviewer when the work requires independence.

Ask which **chat management surface** and which **engineering execution
surface** the Human actually has, which first project to work on, and which
compatible duties should be combined or left vacant. Present those choices
as part of the same creation conversation. Do not begin with a list of brands
or with a new role-selection application.

The bootstrap preview remains read-only. `--apply` creates a separate private,
BLOCKED/UNCONFIGURED starter; it does not start AI sessions or make appointments.
After verifying the private destination, continue the same guided setup by
recording only the Human-approved roles, scopes and original decision pointers
there. Unknown or declined assignments stay unconfigured. Never put the
Human's private operating records in the public OSS distribution.

## Recommended positions within this separation

| Position | Recommended working side and responsibility |
| --- | --- |
| **Human Factory Director** | Human intent, priorities, appointments and protected final decisions |
| **Deputy / Product & Development Manager** | Chat management: think through product direction, designs, task packages and acceptance; coordinate the Factory |
| **Project Manager** (as needed) | Chat management: project scope, roadmap, decisions, reviews and delivery coordination |
| **Secretary / Records** (optional) | Chat management: maintain decisions, current-state pointers and unresolved work |
| **Governance / consistency** (optional) | Chat management: scoped checks of authority, policy, current state and evidence |
| **Runtime / infrastructure planner** (optional) | Chat management: architecture and environment plans, without implied server/production authority |
| **Project Primary / engineering executor** | Development execution: actual code, commands, tests, debugging and delivery evidence |
| **Development Lead / Portfolio Console** (optional) | Engineering context for technical coordination and portfolio visibility; not automatically the owner of every execution task |
| **Independent reviewer** (as required) | A separate appropriate review context/actor; technical review may need engineering tools, privacy review may use a separate chat context |

Compatible **management** duties may be combined in one chat; Development Lead
and Console may share an engineering context. This is not a recommendation to
collapse ordinary chat management into the coding executor. Add roles only
as projects or risks require. A position can persist across conversations;
creating its office file does not create a live worker. Independent review
must not be performed by the author merely changing hats.

## Providers can change; the working split stays

The framework is provider-neutral, but **not indifferent to where the work is
performed**. For illustration, a suitable ChatGPT, Claude, Gemini or other
chat context can handle management; Codex, Claude Code or another permitted
development Agent can handle hands-on implementation where actual tools are
available. The [ChatGPT + Codex profile](https://github.com/AAAlcest/AI-Software-Factory-OSS/blob/main/profiles/chatgpt-codex.json)
is one optional example of these two surfaces, not a vendor requirement.

The same provider may supply both surfaces. Verify their real capabilities,
permissions and usage arrangement; do not assume them from product names.
**Do not call a coding session a manager and claim the chat/execution quota
separation has been achieved. Do not call a code-writing chat a developer
and claim it has a working terminal.** Choosing another vendor must not erase
the reason for the management/development division.

## Carry the selected roles into work

Use the existing private-instance office, project and authority records with
the original Human decision. Give each selected AI context a concise brief
naming the private Factory, its role, project, allowed scope, current Issue/PR
and evidence route. The Agent must verify its actual authority and current
records. Neither a brief nor repository credentials grant new permissions.

The repeatable loop is **Human + chat manager clarify intent/design → manager
issues a precise task and acceptance criteria → developer implements/tests →
manager inspects evidence and decides the next step → independent review and
Human-retained approvals as applicable**. This is the workflow to teach during
creation and demonstrate to new users, not simply a model-selection exercise.
