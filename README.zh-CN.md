# AI Software Factory OSS

**Quirmn 出品。**

[English](README.md)

一个以仓库为中心、由 Human 主导的软件工程协作框架，用于组织 ChatGPT 管理角色与 Codex 开发角色。角色、权限、项目状态与证据可以跨越单次对话持续存在；模型名称或账号凭据本身并不授予任何 Factory 权限。

通过让 ChatGPT 负责规划、治理、任务路由与评审协调，并把 Codex 尽量留给真正需要实现能力的开发工作，这套 Factory 的目标是显著减少不必要的 Codex token 消耗。再结合可复用的 skills 与角色化工作流，可以提高整套 AI 工具链的利用率，并让相同的 token 与订阅预算产生更高的实际回报。具体节省幅度取决于任务类型、模型选择与 Factory 配置方式；这是一个运营效率目标，不是固定额度承诺。

**1.5.0 是 AI Software Factory OSS 当前最新的正式发布版本。** 它保留 v1.4 的有边界恢复与审计模型，并加入首次使用产品化改进：更清晰的 Human／AI／审计入口、精确 release 本地获取、Windows 友好的第一次运行说明、minimal safe AI boot、静态 cockpit 教学快照标识，以及 GitHub 原生 Fresh Factory Audit Issue 入口。

当前 `main` 还包含一组 **v1.5 之后、尚未单独发布的新维护能力**：长期仓库文档公告墙、已经实际启用的 GitHub 原生文档变更自动日志，以及面向公开直接 fork 的可选自助初始化流程。这些 main-only 改进在未来发布之前**不属于不可移动的 `v1.5.0` tag**。实际已发布版本状态以 GitHub Releases 与对应 release coordination Issue 为准；历史 tag 不会为了追随未来 `main` 而移动。

发布说明见 [1.5.0 Release Notes](docs/releases/1.5.0.md)、[1.4.0 历史 Release Notes](docs/releases/1.4.0.md) 与 [1.0.0 历史 Release Notes](docs/releases/1.0.0.md)，安全报告方式见 [SECURITY.md](SECURITY.md)。

## 从这里开始

**文档公告墙：**[仓库文档索引与变更记录](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/26)。正文导航，评论记变更；规则见 [公告与自动记账契约](docs/REPOSITORY_NOTICES.md)。[本仓自动日志已启用](https://github.com/AAAlcest/AI-Software-Factory-OSS/issues/28#issuecomment-5736870432)：配置范围内进入 `main` 的文档改动和已观察到的 PR 候选会异步记入，不是每次本地保存即刻记账。fork 不会继承公告或已启用的 writer；请看 [fork 自助初始化](docs/DOCUMENTATION_JOURNAL.md#fork-self-setup)。

**第一次使用的 Human：**先看 [快速开始](docs/QUICKSTART_ZH.md)，再看 [推荐的 ChatGPT + Codex 角色配置](docs/RECOMMENDED_ROLE_SETUP.md)。如果暂时不想运行脚本，可先浏览 [合成 Factory 实例](examples/factory-instance/README.md) 看整体结构。

**要 fork 本仓库：**fork 会复制文件，但不会继承本仓的公告 Issue 或已经激活的日志状态。对于 GitHub.com 上默认分支为 `main` 的公开直接 fork，可以使用 [fork 自助初始化](docs/DOCUMENTATION_JOURNAL.md#fork-self-setup) 创建自己仓库的公告墙并准备 writer 配置。是否真正启用仍由 fork 仓主明确决定：检查生成改动、开启 Actions、主动 opt-in，并用真实机器人写入／读回与无重复重跑完成本仓验收。

**AI Agent：**先读 [AGENTS.md](AGENTS.md)，再读 [AI_ENTRYPOINT.md](AI_ENTRYPOINT.md)。如果当前已经有明确的项目、角色和低风险小任务，应使用其中的 minimal safe boot，而不是每次都重读全部机制文档。

**要审计一个运行中的 Factory：**使用 [Fresh Factory Audit](docs/FRESH_FACTORY_AUDIT.md)，也可以直接从 GitHub **New issue** 里选择 Fresh Factory Audit 模板。

推荐配置：**ChatGPT 负责 Factory 管理与职能岗位；Codex 负责项目开发、Development Lead 与 Console。** 副厂长可以兼任记录、厂务维护与基础设施规划等兼容职责。独立验收应与作者分离；Work 应谨慎使用，不应用于普通状态同步或 ACK 循环。这是一种可配置的协作建议，不是厂商权限规则。

## Project cockpit、恢复与有边界工作

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

**[FlowThread](https://flowthread.quirmn.com/)** 是另一款 **Quirmn 产品**。它由这套 AI Software Factory 孵化，并被作者实际用于日常 AI 开发与协作。真实使用中发现的问题可以重新进入 Factory 工作流，Factory 则为持续改进产品提供长期、可追踪的协作方式。

这个仓库展示的是**如何工作**；FlowThread 展示的是**用这种工作方式可以做出怎样的真实产品**。

**使用 AI Software Factory 不需要安装或购买 FlowThread。**
FlowThread 是产品案例和作者自己的工作流工具，不是框架依赖、必备配套软件，也不是使用本仓库的前提。

了解 FlowThread：https://flowthread.quirmn.com/

## V1 包含什么

V1 包含：可配置的 Human / executive / role 组合；Staff Offices 与 Project Rooms；current 与 pending 状态；Issue 会议与精确候选 PR；可选的一体化正文邮件、Reply-All 与仅用于可见性的 CC；Console / open-loop 记录；Work result receipts；首次任命、同一 incumbent 恢复与经授权的真实 succession 示例；可重复的软件检查；覆盖 8 类冷启动场景的 9 个 fixture 变体；Project cockpit 与 skills；可执行的 cockpit / Project-view 生成与 drift 检查；用于有边界长线程恢复的 work-item checkpoint；带合成 governance-drift 示例的 Fresh Factory Audit 模式；V1.5 的首次使用入口、精确版本获取、minimal safe boot 与原生审计入口改进；以及当前 post-v1.5 `main` 中的仓库文档公告墙、已启用的文档自动日志和公开 fork 自助初始化能力。

它**不是**自主调度器、权限服务、生产部署系统或经过认证的邮件传输系统。其 helper 只检查声明的一致性；详细边界见 [V1 状态说明](docs/V1_BASELINE_STATUS.md)。

## 发布与安全

1.5.0 以及后续版本应按照变更风险使用 [发布检查清单](docs/PUBLICATION_CHECKLIST.md)、[公开隐私标准](docs/PUBLIC_PRIVACY_STANDARD.md) 与 [cold-start 验收流程](docs/COLD_TAKEOVER_EXERCISE.md)。不要把私有运行历史重新包装成示例，不要提交凭据，也不要通过 README、配置或示例暗中改变许可证或权限边界。

MIT License 只覆盖本仓库的这份发行内容。`factory.yaml` 中未配置的 publication defaults 与 synthetic Human gates 面向各自单独运行的 Factory instance；它们不会给 MIT License 增加额外限制，也不会自动批准其他项目的发布。

[文档索引](docs/README.md) · [贡献指南](CONTRIBUTING.md) · [安全说明](SECURITY.md)
