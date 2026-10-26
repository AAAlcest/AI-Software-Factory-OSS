# Recommended Factory roles — provider-neutral

**The Factory recommends responsibilities, not AI vendors.** Humans direct
the work and retain approvals; management Agents reason, plan, coordinate and
specify acceptance; engineering Agents actually edit code, test and deliver
evidence; independent reviewers evaluate when required. Any capable AI tools
may be used—ChatGPT, Claude, Gemini, Codex, Claude Code, mixed providers or
alternatives. None is mandatory.

## Read this while creating your private Factory

**To the AI Agent helping a Human build a Factory:** Before proposing
`--apply`, show the Human the roles below and ask:

1. Which AI models/tools do you already use for planning, coding, and review?
   What repository/tools may each access? Never ask for passwords/API secrets.
2. What is the first project? Do you want a small team or separate departments?
   Which duties can safely be combined in one AI context?
3. Who will hold management, engineering and separate-review roles, and which
   assignments are not decided yet?

Present a **role map for the Human to approve as part of this creation
conversation**. The private-bootstrap command is intentionally noninteractive:
the preview is read-only; `--apply` makes a separate private repository whose
roles/authority are **BLOCKED/UNCONFIGURED** until real Human decisions are
recorded. Once the private destination is verified, continue this same guided
creation process by recording approved roles only in the private Factory;
leave unknown/declined roles unconfigured. Do not invent or auto-launch Agents.

## Recommended organizational positions

| Role (may be combined when compatible) | Responsibility |
| --- | --- |
| **Human Factory Director** | Intent, priorities, appointments, final protected decisions |
| **Deputy / Product & Development Manager** | Product direction, planning, coordination, task packages, acceptance criteria |
| **Secretary / Records** (optional) | Decisions, current state, unresolved work and evidence pointers |
| **Governance / consistency** (optional) | Scoped authority, policy, state and evidence checks |
| **Runtime / infrastructure planning** (optional) | Architecture and environments; no automatic server permission |
| **Project Manager** (optional) | Project scope, roadmap and acceptance preparation |
| **Project Primary / engineering executor** | Code changes, debugging, tests, reproducible delivery evidence |
| **Development Lead / Portfolio Console** (optional) | Engineering coordination and portfolio visibility; not ownership of every execution |
| **Independent reviewer** (as required) | Separate technical/privacy assessment of actual candidate and evidence |

**Small-team default:** one Human director, one AI management context
(Deputy/PM/records can share compatible duties), and one tool-capable
engineering Agent per active project. Add more roles only as projects and
risks require. One logical role can outlast many conversations. An office
file or model identity does not mean there is a running Agent.

**Choose by capabilities, not brand:** For illustration, ChatGPT + Codex,
Claude + Claude Code, Gemini + a coding Agent, or a cross-provider mixture
are all valid if the chosen tools can actually access needed context, edit
files, run tests and return evidence. The same AI provider can perform
planning and engineering in **separate scoped roles**.
The [ChatGPT + Codex profile](https://github.com/AAAlcest/AI-Software-Factory-OSS/blob/main/profiles/chatgpt-codex.json)
is one optional example, **not a universal default** or an actual appointment.

## Carry the chosen structure into the new Factory

After creating and verifying the private destination, help the Human set up
the selected office, project and role/authority records using the existing
templates and original Human decision; keep any unapproved tool, scope or
incumbent UNCONFIGURED/BLOCKED. Provide each selected AI role a short
first-contact brief that names the private Factory, role, project, allowed
scope, current Issue/PR and relevant evidence. The new Agent must verify
its assignment; instructions do not create sessions or grant authority.

Work follows **Human intent → AI management planning/task/acceptance →
tool-capable engineering implementation/tests → independent review where
needed → Human decisions**. Separating inexpensive planning from costly
coding may use quotas more efficiently, but no fixed token or cost saving
is guaranteed. The public OSS never receives private roles or projects.
