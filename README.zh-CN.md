# AI Software Factory OSS

**Quirmn 出品。**

[English](README.md)

一个**不绑定 AI 厂商**、以仓库为中心、由 Human 主导的软件工程协作框架。Human 决定方向；用户选择的 AI 管理角色规划、协调和制定验收标准，具备工具能力的工程 Agent 执行开发和测试。ChatGPT、Claude、Gemini、Codex、Claude Code 等只是可选工具，不是准入条件。角色、权限、项目状态与证据可跨对话持续存在，但模型名称或账号凭据本身不授予组织权限。

**正在建厂的用户和你的 AI Agent：** 请在建厂过程中阅读[不绑定厂商的角色配置建议](docs/RECOMMENDED_ROLE_SETUP.md)，让 Human 选择管理、工程与必要的审查角色。AI 应主动提出岗位建议，不要建完空仓库后才让用户另找入口。参见 [中文上手说明](docs/QUICKSTART_ZH.md) 和 [AI 建厂入口](AI_ENTRYPOINT.md)。

## 5 分钟快速演示 · Quick Demo

**能看到什么：** 在本机生成完全虚构的 Factory，并实际检查角色、项目与授权记录，而不是只看概念图。  
**立即体验：** [**运行 5 分钟 Quick Demo →**](docs/QUICK_DEMO.md)；只需 Python 3.10+，不需要 AI 账号、API Key 或真实私有 Factory。  
**安全拒绝：** 虚构项目 Atlas 可以得到结构性 `VALID`，但未配置的 starter 会按预期返回 `BLOCKED`（退出码 `3`）；两者的 `execution_authorized` 均为 `false`，不代表任命或执行许可。  
**架构路径：** [仓库原生角色与项目](docs/AI_FACTORY_IN_30_SECONDS.md) → [实例授权记录](docs/INSTANCE_BOOT_PROTOCOL.md) → 只读验证；不自动派发 Agent、不部署云服务、不操作生产环境。

让用户选用的 AI 管理角色负责规划、治理、任务拆解和评审协调，把实际代码编辑与测试交给具备权限和工具的工程 Agent，Factory 希望减少不必要的编码 Agent token 或套餐额度消耗。管理和开发可由同一家或不同厂商的 AI 承担，**ChatGPT + Codex 只是一种示例组合**。具体节省取决于任务、模型和配置，不承诺固定比例。

**当前源码版本线：1.7.1。** 本补丁明确建厂过程中的聊天管理与工程执行分工；建厂预览提示阅读岗位指南，新私有 starter 携带该指南。保留 v1.7.0 的诊断、Quick Demo、日志默认行为与小范围私厂升级能力；完整差异见本版发布说明。

**`VERSION=1.7.1` 不代表 GitHub Release 已正式发布。** 已发布版本以 [GitHub Releases](https://github.com/AAAlcest/AI-Software-Factory-OSS/releases) 和 [v1.7.1 发布收尾记录](https://github.com/AAAlcest/AI-Software-Factory-OSS/pull/59) 为准。历史 Tag 保持不变。

发布说明见 [1.7.1 Release Notes](docs/releases/1.7.1.md)、[1.7.0 历史 Release Notes](docs/releases/1.7.0.md)、[1.6.0 历史 Release Notes](docs/releases/1.6.0.md)、[1.5.0 历史 Release Notes](docs/releases/1.5.0.md)、[1.4.0 历史 Release Notes](docs/releases/1.4.0.md)、[1.0.0 历史 Release Notes](docs/releases/1.0.0.md)，安全报告方式见 [SECURITY.md](SECURITY.md)。

## 从这里开始

**文档公告墙：**[仓库文档索引与变更记录](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/26)。正文导航，评论记变更；规则见 [公告与自动记账契约](docs/REPOSITORY_NOTICES.md)。[本仓自动日志已启用](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/28#issuecomment-5736870432)：配置范围内进入 `main` 的文档改动和已观察到的 PR 候选会异步记入，不是每次本地保存即刻记账。fork 不会继承公告或已启用的 writer；请看 [fork 自助初始化](docs/DOCUMENTATION_JOURNAL.md#fork-self-setup)。

**创建你的私人 Factory（普通使用入口）：**从公开 OSS 仓库取得当前 `main` 源码，先运行[只读的私有仓初始化预览](docs/QUICKSTART_ZH.md#先创建你的私人-factory)，确认后再显式执行。它创建一个**全新、独立、非 fork 的私有仓库**；正常私人使用**不需要 Fork**。新实例仍是 BLOCKED／未配置，日志 writer 也尚未启用。本源码版本可核对官方当前 `main`，或在 **`v1.7.1` 正式发布且 Tag 可核验之后** 接受对应精确 release tag。正式发布前请以 GitHub Releases 中实际存在的版本为准。

**已经拥有私人 Factory？** 请阅读[安全升级现有私厂（英文）](docs/PRIVATE_FACTORY_UPGRADE.md)。默认只读预览，历史来源不符或用户修改过的文件直接拒绝；显式授权后才允许在私有仓库创建 Draft PR，不覆盖私人运行状态、不自动合并。

**第一次使用的 Human：**先看 [快速开始](docs/QUICKSTART_ZH.md)，再看 [不绑定厂商的岗位配置建议](docs/RECOMMENDED_ROLE_SETUP.md)。如果暂时不想运行脚本，可先浏览 [合成 Factory 实例](examples/factory-instance/README.md) 看整体结构。

**Fork 本仓库（贡献／公开安全试用）：**公开 fork 是 OSS 分发／更新／贡献副本，**不是私人 Factory 的默认运行仓库**。fork 会复制文件，但不会继承本仓的公告 Issue 或已经激活的日志状态。公开 fork 的 [自助初始化](docs/DOCUMENTATION_JOURNAL.md#fork-self-setup) 只适合公开安全的试用、框架维护／贡献，或你明确愿意公开的 Factory；**不要把私人项目、真实任命、客户／公司资料或私有 Factory 历史放进公开 fork。**

真正运行私人 Factory 时，使用上述私有仓初始化命令从本框架／starters **另建一个 private operating repository**，把真实 Factory 状态放在那里；各项目源码仍可以分别留在自己的 private project repository，由 Factory 只记录受控引用与状态。公开 fork 可以继续只承担上游同步、更新和贡献。

如果你确实要运行一个公开 Factory，那么对于 GitHub.com 上默认分支为 `main` 的公开直接 fork，可以使用 fork 自助初始化创建公告墙并准备 writer 配置。如果该 fork 尚未开启 Issues，`--apply` 会在核对仓库身份与管理员权限后直接为**这个 fork**开启；默认检查仍保持只读。是否真正启用仍由 fork 仓主明确决定：检查生成改动、开启 Actions、主动 opt-in，并用真实机器人写入／读回与无重复重跑完成本仓验收。

**AI Agent：**先读 [AGENTS.md](AGENTS.md)，再读 [AI_ENTRYPOINT.md](AI_ENTRYPOINT.md)。Fresh Agent 第一次进入本公开 OSS 时，必须先判断自己是在做 **OSS／框架维护**、**公开安全试用**，还是要开始 **真实私人 Factory 运行**。如果 Human 要开始真实私人工作、但还没有 private Factory，最建议的建厂路径是：

```text
公开 OSS（只作为 distribution source）
→ Create Private Factory 只读 preview
→ 向 Human 说明计划与隐私边界
→ Human 明确授权
→ 创建全新 independent private repository
→ 核验 private / non-fork
→ 把真实运行上下文切入这个 private Factory
```

不要把真实任命、项目状态、客户／公司资料或私有历史写进本公开 OSS；如果已经存在 private Factory，就应直接进入那个实例，而不是重复建厂。Agent 可以自行完成路由判断和只读 preview，但 `--apply` 会创建真实 GitHub 远程状态，必须有 Human 明确授权。完整的 first-contact routing 见 [AI_ENTRYPOINT.md](AI_ENTRYPOINT.md)。如果当前已经有明确的项目、角色和低风险小任务，应使用其中的 minimal safe boot，而不是每次都重读全部机制文档。

**执行纪律与健康检查：**真实工作一旦已经授权，就遵循 [Execution-First](docs/EXECUTION_FIRST.md)：用可观察执行与证据替代“收到／准备做／正在做”式叙述。[`python -B scripts/factory_doctor.py --json`](docs/FACTORY_DOCTOR.md) 提供跨平台、只读的 Factory／仓库健康快照；Doctor PASS 永远不授予权限。[Design Rationale Index](docs/DESIGN_RATIONALE_INDEX.md) 只解释公开规则为什么存在及其 provenance，不成为第二权威来源。

**要审计一个运行中的 Factory：**使用 [Fresh Factory Audit](docs/FRESH_FACTORY_AUDIT.md)，也可以直接从 GitHub **New issue** 里选择 Fresh Factory Audit 模板。

推荐的是**岗位与能力分工**：Human 负责决策；自选 AI 管理者负责规划、协调和验收准备；具备工具能力的工程 Agent 负责开发与测试，必要时设置真正独立的审查者。**不指定任何必选 AI 厂商**。副厂长可兼任兼容职责，Development Lead 可兼任 Console；不要求一个头衔一个聊天。

## Project cockpit、恢复与有边界工作

**管理者的聊天快到上限了？** 可以用 [FlowThread](https://flowthread.quirmn.com/) 搜索并导出仍可获取的 ChatGPT 对话，保存为 Markdown、PDF 等格式，在换聊天前留下工作档案，辅助恢复或真正的任期交接。对话档案补充历史背景，不替代仓库当前记录。参见[对话备份与交接指南（中英文）](docs/HANDOFF_AND_SUCCESSION.md#conversation-backup)。

当前 operating layer 包含可选的 [ChatGPT Project cockpit](docs/CHATGPT_PROJECT_COCKPIT.md)，用于 Factory／项目／角色总览；[workstream recovery](docs/WORKSTREAM_RECOVERY.md)；[work-item checkpoint 与 Project-ready visibility](docs/WORK_ITEMS_AND_PROJECT_VIEW.md)；以及在仓库仍是 canonical truth 的前提下生成有边界的 Codex task package。

[Skill contracts](skills/README.md) 统一 overview、recovery、handoff、health 与 task-packaging 的输入输出规则；[Token 效率设计](docs/TOKEN_EFFICIENCY.md) 给出可重复的对比方法，不承诺固定节省比例。

仓库里直接可浏览的 cockpit 是**静态教学快照**。它自己的 [Project instructions](examples/factory-instance/project-cockpit/PROJECT_INSTRUCTIONS.md) 会说明：如果要看当前 schema-2 的最新输出，应运行当前 generator 生成新的 cockpit，而不是把旧静态快照当成最新完整输出。

## Fresh Factory Audit

当你希望用一个全新的 AI 上下文检查“运行中的 Factory 还能不能从当前仓库证据安全恢复”时，可以使用 [Fresh Factory Audit](docs/FRESH_FACTORY_AUDIT.md)。它默认先读有边界的当前状态，只在出现具体冲突、依赖或缺失事实时才扩大到历史 chronology，并把 governance / recovery drift 作为 findings 交给后续 Human／management disposition，而不是自行授权修复。

仓库提供可直接复制的 [审计 Issue 模板](templates/FRESH_FACTORY_AUDIT_ISSUE.md) 与 [Fresh Auditor Prompt](templates/FRESH_FACTORY_AUDITOR_PROMPT.md)。[合成审计示例](examples/factory-instance/audit/README.md) 演示了完全虚构的 missing project visibility、frozen-work resurrection、superseded direction 与 stale recovery queue 等 failure mode；其中不包含任何私有 Factory 审计历史。

## 不运行脚本也能先看懂一个 Factory

可以直接浏览仓库里的 [合成 Factory 实例](examples/factory-instance/README.md)。其中包含可见的 Staff Offices、Project Rooms、Factory state、registers、Meeting Hall、收发件引用、Work receipt 与 handoff archive 结构。

这套实例全部是公开安全的虚构内容，**不是**从任何私有 Factory 复制、删改或脱敏而来。它的用途是让你在 GitHub 页面上直接看懂“工厂长什么样”；需要生成可重复、可验证的临时 fixture 时，再使用 `scripts/create_demo.py`。

## 试用集成式虚构 Factory

需要 Python 3.10+；这些本地演练不需要第三方 Python 依赖、模型 API Key 或云部署。[中文上手说明](docs/QUICKSTART_ZH.md) 已加入无 Git 的 Source ZIP、Git 精确 tag checkout，以及 Windows `py -3` 的第一条命令路径。

```sh
python -B scripts/create_demo.py --destination ../example-factory --case first
python -B scripts/validate_demo.py ../example-factory
python -B scripts/validate_cockpit.py --root examples/factory-instance
python -B scripts/check_all.py
```

目标目录必须不存在。构建器只会创建合成数据，不会创建真实仓库、Agent 或凭据。现有 validator 串联 instance、reply-routing 与 Work History 契约；cockpit validator 只检查派生 bundle 的结构和引用。任何 `VALID` 都不会授予权限、发送消息，也不等于 fresh-Agent 验收结果。

仓库还包含原始的精简 [scenario](examples/demo-factory/scenario/WALKTHROUGH.md)、[可复用模板](templates/README.md)、PR/Issue 模板以及聚焦示例。生成的 Factory 不是产品源代码仓库的重复副本。

## 产品案例：[FlowThread](https://flowthread.quirmn.com/)

**聊天会到上限，工作历史不该随之丢失。**

**[FlowThread](https://flowthread.quirmn.com/)** 是一款独立的 **Quirmn 产品**，由这套 Factory 孵化，并被作者用于日常工作。目前公开产品是一款面向 ChatGPT 长对话的浏览器扩展：让长聊天更易使用，在上下文中搜索早先的消息，并把仍可获取的当前对话分支导出为 **PDF、Markdown、TXT、HTML 或 JSON**。最新平台支持和安装入口见产品官网。

对工厂的聊天管理者来说，这也是实用的恢复与任期交接工具。准备离开一段长对话，或聊天接近上限时，先把仍能获取的对话导出，留作私有工作档案。它可以保留需求讨论、设计取舍、被否决的方案和未解决的问题，补充简短交接摘要难以完整解释的背景。Markdown 可用于向新 AI 聊天提供相关材料，PDF 可用于人类阅读和存档。

**Factory 让岗位、当前状态与交接持续存在；FlowThread 帮你保存这些工作发生过的对话。** 实用流程是：导出 → 检查档案 → 更新恢复／交接摘要 → 只向新聊天补充所需背景，并核对仓库当前证据。详见[对话备份与交接指南（中英文）](docs/HANDOFF_AND_SUCCESSION.md#conversation-backup)。

仅仅换聊天属于恢复，不自动产生新任期。导出文件是历史补充，不是自动迁移 AI 记忆、替代仓库当前权限，或保证恢复已不可获取的消息。私有对话不要上传到公开 fork 或 Issue。

**使用 AI Software Factory 不需要安装或购买 FlowThread。** 也可使用其他合适的导出工具，尤其当聊天平台暂未被支持时。FlowThread 既是工厂孵化的真实产品，也是可选的工作流工具，而不是框架依赖。

[了解 FlowThread 与安装方式 →](https://flowthread.quirmn.com/)

## V1 包含什么

V1 包含：可配置的 Human / executive / role 组合；Staff Offices 与 Project Rooms；current 与 pending 状态；Issue 会议与精确候选 PR；可选的一体化正文邮件、Reply-All 与仅用于可见性的 CC；Console / open-loop 记录；Work result receipts；首次任命、同一 incumbent 恢复与经授权的真实 succession 示例；可重复的软件检查；覆盖 8 类冷启动场景的 9 个 fixture 变体；Project cockpit 与 skills；可执行的 cockpit / Project-view 生成与 drift 检查；用于有边界长线程恢复的 work-item checkpoint；带合成 governance-drift 示例的 Fresh Factory Audit 模式；V1.5 的首次使用入口、精确版本获取、minimal-safe-boot 和原生审计入口改进；以及 V1.6 的仓库文档公告墙、已启用的文档自动日志、公开 fork 自助初始化、面向普通私人使用的独立 private Factory 初始化、release-tag 来源记录与 Fresh Agent 私人建厂路由。

它**不是**自主调度器、权限服务、生产部署系统或经过认证的邮件传输系统。其 helper 只检查声明的一致性；详细边界见 [V1 状态说明](docs/V1_BASELINE_STATUS.md)。

## 发布与安全

1.5.0 以及后续版本应按照变更风险使用 [发布检查清单](docs/PUBLICATION_CHECKLIST.md)、[公开隐私标准](docs/PUBLIC_PRIVACY_STANDARD.md) 与 [cold-start 验收流程](docs/COLD_TAKEOVER_EXERCISE.md)。不要把私有运行历史重新包装成示例，不要提交凭据，也不要通过 README、配置或示例暗中改变许可证或权限边界。

MIT License 只覆盖本仓库的这份发行内容。`factory.yaml` 中未配置的 publication defaults 与 synthetic Human gates 面向各自单独运行的 Factory instance；它们不会给 MIT License 增加额外限制，也不会自动批准其他项目的发布。

[文档索引](docs/README.md) · [贡献指南](CONTRIBUTING.md) · [安全说明](SECURITY.md)
