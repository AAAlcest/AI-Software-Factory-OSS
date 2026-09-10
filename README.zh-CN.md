# AI Software Factory OSS

**Quirmn 出品。**

[English](README.md)

一个以仓库为中心、由 Human 主导的软件工程协作框架，用于组织 ChatGPT 管理角色与 Codex 开发角色。角色、权限、项目状态与证据可以跨越单次对话持续存在；模型名称或账号凭据本身并不授予任何 Factory 权限。

通过让 ChatGPT 负责规划、治理、任务路由与评审协调，并把 Codex 尽量留给真正需要实现能力的开发工作，这套 Factory 的目标是显著减少不必要的 Codex token 消耗。再结合可复用的 skills 与角色化工作流，可以提高整套 AI 工具链的利用率，并让相同的 token 与订阅预算产生更高的实际回报。具体节省幅度取决于任务类型、模型选择与 Factory 配置方式；这是一个运营效率目标，不是固定额度承诺。

**1.0.0 是 AI Software Factory OSS 的首个公开发布版本线。**
仓库已经公开，采用 [MIT License](LICENSE)，并已启用 GitHub Private Vulnerability Reporting；不公开私人邮箱作为漏洞报告联系方式。此前完成的软件验证、fresh-Agent 验收与隐私／公开安全结果继续保留在 Issue #1 的对应记录中；后续公开文档、品牌或示例调整采用与风险相称的增量检查，不会把它们说成重新执行了原有验收。

发布说明见 [1.0.0 Release Notes](docs/releases/1.0.0.md)，安全报告方式见 [SECURITY.md](SECURITY.md)。

## 快速开始

Human 用户可先看：[快速开始](docs/QUICKSTART.md)、[中文上手说明](docs/QUICKSTART_ZH.md) 和 [推荐的 ChatGPT + Codex 角色配置](docs/RECOMMENDED_ROLE_SETUP.md)。
AI Agent 应先读 [AGENTS.md](AGENTS.md)，再读 [AI_ENTRYPOINT.md](AI_ENTRYPOINT.md)。

推荐配置：**ChatGPT 负责 Factory 管理与职能岗位；Codex 负责项目开发、Development Lead 与 Console。** 副厂长可以兼任记录、厂务维护与基础设施规划等兼容职责。独立验收应与作者分离；Work 应谨慎使用，不应用于普通状态同步或 ACK 循环。这是一种可配置的协作建议，不是厂商权限规则。

## V1.1 Project cockpit 与 Skills

下一层加入可选的 [ChatGPT Project cockpit](docs/CHATGPT_PROJECT_COCKPIT.md)，用于对 Factory、项目和角色做总览，辅助 recovery / handoff，并给 Codex 生成有边界的任务包；**仓库仍然是唯一 canonical truth**。

[Skill contracts](skills/README.md) 统一 `factory-overview`、`project-overview`、`role-overview`、recovery、handoff、health 和 task-packaging 的输入输出规则。[Token 效率设计](docs/TOKEN_EFFICIENCY.md) 给出可重复的对比方法，不承诺固定节省比例。

可直接浏览虚构示例：[`examples/factory-instance/project-cockpit`](examples/factory-instance/project-cockpit/PROJECT_INSTRUCTIONS.md)。

## 不运行脚本也能先看懂一个 Factory

可以直接浏览仓库里的 [合成 Factory 实例](examples/factory-instance/README.md)。其中包含可见的 Staff Offices、Project Rooms、Factory state、registers、Meeting Hall、收发件引用、Work receipt 与 handoff archive 结构。

这套实例全部是公开安全的虚构内容，**不是**从任何私有 Factory 复制、删改或脱敏而来。它的用途是让你在 GitHub 页面上直接看懂“工厂长什么样”；需要生成可重复、可验证的临时 fixture 时，再使用 `scripts/create_demo.py`。

## 试用集成式虚构 Factory

需要 Python 3.10+；这些本地演练不需要第三方 Python 依赖、模型 API Key 或云部署。

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

V1 包含：可配置的 Human / executive / role 组合；Staff Offices 与 Project Rooms；current 与 pending 状态；Issue 会议与精确候选 PR；可选的一体化正文邮件、Reply-All 与仅用于可见性的 CC；Console / open-loop 记录；Work result receipts；首次任命、同一 incumbent 恢复与经授权的真实 succession 示例；可重复的软件检查；以及覆盖 8 类冷启动场景的 9 个 fixture 变体。

它**不是**自主调度器、权限服务、生产部署系统或经过认证的邮件传输系统。其 helper 只检查声明的一致性；详细边界见 [V1 状态说明](docs/V1_BASELINE_STATUS.md)。

## 发布与安全

1.0.0 以及后续版本应按照变更风险使用 [发布检查清单](docs/PUBLICATION_CHECKLIST.md)、[公开隐私标准](docs/PUBLIC_PRIVACY_STANDARD.md) 与 [cold-start 验收流程](docs/COLD_TAKEOVER_EXERCISE.md)。不要把私有运行历史重新包装成示例，不要提交凭据，也不要通过 README、配置或示例暗中改变许可证或权限边界。

MIT License 只覆盖本仓库的这份发行内容。`factory.yaml` 中未配置的 publication defaults 与 synthetic Human gates 面向各自单独运行的 Factory instance；它们不会给 MIT License 增加额外限制，也不会自动批准其他项目的发布。

[文档索引](docs/README.md) · [贡献指南](CONTRIBUTING.md) · [安全说明](SECURITY.md)
