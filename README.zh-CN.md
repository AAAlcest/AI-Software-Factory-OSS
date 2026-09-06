# AI Software Factory OSS

**Quirmn 出品。**

[English](README.md)

一个以仓库为中心、由 Human 主导的软件工程协作框架，用于组织 ChatGPT 管理角色与 Codex 开发角色。角色、权限、项目状态与证据可以跨越单次对话持续存在；模型名称或账号凭据本身并不授予任何 Factory 权限。

通过让 ChatGPT 负责规划、治理、任务路由与评审协调，并把 Codex 尽量留给真正需要实现能力的开发工作，这套 Factory 的目标是显著减少不必要的 Codex token 消耗。再结合可复用的 skills 与角色化工作流，可以提高整套 AI 工具链的利用率，并让相同的 token 与订阅预算产生更高的实际回报。具体节省幅度取决于任务类型、模型选择与 Factory 配置方式；这是一个运营效率目标，不是固定额度承诺。

**1.0.0 正处于公开发布流程中；GitHub Release 尚未发布。**
本项目已采用 [MIT License](LICENSE)，并已启用 GitHub Private Vulnerability Reporting，不公开私人邮箱作为安全报告联系方式。此前完成的软件验证、fresh-Agent 验收与隐私／公开安全结果继续保留在 Issue #1 的对应记录中；后续 README、品牌和发布文案调整不等同于重新执行这些验收。

发布说明见 [1.0.0 Release Notes](docs/releases/1.0.0.md)，安全报告方式见 [SECURITY.md](SECURITY.md)。

## 快速开始

Human 用户可先看：[快速开始](docs/QUICKSTART.md)、[中文上手说明](docs/QUICKSTART_ZH.md) 和 [推荐的 ChatGPT + Codex 角色配置](docs/RECOMMENDED_ROLE_SETUP.md)。
AI Agent 应先读 [AGENTS.md](AGENTS.md)，再读 [AI_ENTRYPOINT.md](AI_ENTRYPOINT.md)。

推荐配置：**ChatGPT 负责 Factory 管理与职能岗位；Codex 负责项目开发、Development Lead 与 Console。** 副厂长可以兼任记录、厂务维护与基础设施规划等兼容职责。独立验收应与作者分离；Work 应谨慎使用，不应用于普通状态同步或 ACK 循环。这是一种可配置的协作建议，不是厂商权限规则。

## 试用集成式虚构 Factory

需要 Python 3.10+；这些本地演练不需要第三方 Python 依赖、模型 API Key 或云部署。

```sh
python -B scripts/create_demo.py --destination ../example-factory --case first
python -B scripts/validate_demo.py ../example-factory
python -B scripts/check_all.py
```

目标目录必须不存在。构建器只会创建合成数据，不会创建真实仓库、Agent 或凭据。验证器会在一个真实生成的 Office / Project Room / mailbox / Console 布局中串联 instance、reply-routing 与 Work History 三类契约。`VALID` 只代表结构一致，不会授予权限、发送消息，也不等于 fresh-Agent 验收结果。

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

遵循 [发布检查清单](docs/PUBLICATION_CHECKLIST.md)、[公开隐私标准](docs/PUBLIC_PRIVACY_STANDARD.md) 与 [cold-start 验收流程](docs/COLD_TAKEOVER_EXERCISE.md)。不要把私有运行历史重新包装成示例，不要提交凭据，也不要通过 README 或配置暗中改变许可证或权限边界。

MIT License 只覆盖本仓库的这份发行内容。`factory.yaml` 中未配置的 publication defaults 与 synthetic Human gates 面向各自单独运行的 Factory instance；它们不会给 MIT License 增加额外限制，也不会自动批准其他项目的发布。

[文档索引](docs/README.md) · [贡献指南](CONTRIBUTING.md) · [安全说明](SECURITY.md)
