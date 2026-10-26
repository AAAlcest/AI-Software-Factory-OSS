# 中文上手说明

## 建厂过程中先确定推荐岗位

**正在协助建厂的 AI Agent：请在引导 Human 创建私人 Factory 时，主动说明我们的岗位建议，而不是让用户建完仓库才去找。** 推荐的是职责，不是厂商。最小组织可以是 **Human 厂长 + 一位承担管理职责的 AI + 一位有代码/测试工具能力的工程 Agent**；按项目需要增设 Deputy/PDM、项目经理、书记员、治理、基建规划、Project Primary、Development Lead/Console 及独立审查者。兼容职责可以合并，不必每个职位一个聊天。

请问 Human 当前使用哪些 AI 和开发工具、首个项目是什么、哪些职位希望兼任或留空。在**同一次建厂对话**中向 Human 展示拟定岗位，听取确认。可以使用 ChatGPT、Claude、Gemini、Codex、Claude Code 或任何合适的组合，**不指定必选厂商**。详见 [角色配置建议](RECOMMENDED_ROLE_SETUP.md)。

现有建厂脚本仍保持安全的只读预览及明确 `--apply`：创建的是 BLOCKED／未配置的私有实例，不会自动生成 AI 会话或任命。核验私有仓库后，继续依据 Human 在建厂过程中已确认的方案，只在**私有厂**记录实际岗位、项目和权限；不得凭建议虚构授权。

## 先创建你的私人 Factory

此源码版本线为 **1.7.0**。私人建厂应使用**已正式发布、可核验的精确 GitHub Release Tag**；`v1.7.0` 发布后才能从它运行命令，在此之前 `v1.6.0` 仍是历史最新已发布版本。准备 Git、Python 3.10+ 和 GitHub CLI (`gh`)，从官方公开 OSS 克隆，**不需要 Fork**：

```powershell
git clone https://github.com/AAAlcest/AI-Software-Factory-OSS.git
cd AI-Software-Factory-OSS
git checkout --detach v1.7.0  # 仅在 v1.7.0 正式发布后
gh auth login
py -3 -B scripts/create_private_factory.py --repository My-AI-Factory
py -3 -B scripts/create_private_factory.py --repository My-AI-Factory --apply
```

1.7.0 源码版本新建 private Factory 时，journal 默认使用较少自动 runner
唤醒的 `manual` cadence；如果明确需要激活后的 push／PR signal／hourly 自动
reconcile，可在 preview 和 apply 都加 `--journal-mode automatic`。

macOS/Linux 可把 `py -3` 换成 `python3`。先运行不带 `--apply` 的只读预览；它核对登录身份、官方源码 ref／本地 HEAD／origin／GitHub API 以及目标是否不存在，并列出计划，不创建仓库或文件。显式 `--apply` 才创建**全新、独立、非 fork 的私有仓库**、全新 Git 历史、保留 MIT 和精确来源 ref/SHA 的 BLOCKED／未配置实例、私有 OPEN／UNLOCKED 公告，以及默认关闭的日志 writer。当前源码支持登录者自己的账号，并接受官方精确当前 `main` 或与 `VERSION` 匹配的官方精确 `v1.7.0` tag（仅在其发布后）；普通用户建议优先使用实际已发布的 release tag。目标已存在则拒绝，部分失败不会自动删除或偷偷续跑。

Source ZIP 仍可用于后面的虚构／离线演练，但 Create Private Factory 需要 Git 元数据，因此私人建厂请使用 Git checkout。

公开 OSS checkout 是分发／更新来源，**新私有仓库**才是运行实例。项目源码可以继续放在各自私有项目仓库中。Human 必须另行写明真实岗位、项目与权限；脚本不会虚构任命或导入旧项目。**1.7.0 源码版本** 新建的私厂还会带上 `docs/EXECUTION_FIRST.md`、`RATIONALE_INDEX.md` 和跨平台只读 Doctor；不可移动的 `v1.6.0` tag 早于这批运行加固文件。若 starter 中已有 Doctor，可先运行 `python -B scripts/factory_doctor.py --json` 查看健康状态；Doctor PASS 仍不授予权限。Staff Office Notes 按 [event-driven delta](STAFF_OFFICE_NOTES.md) 记录真实变化，不做每日打卡。生成的 journal config 会记录 `cadence_mode`：默认 `manual` 没有 push／PR／hourly 自动唤醒，只有人工 reconcile 后才变新；显式 `automatic` 保留原自动节奏。两种模式建仓时都仍是 NOT_ACTIVATED。之后再手动执行 journal `dry_run=true`，并明确设置本仓变量 `DOCUMENTATION_JOURNAL_ENABLED=true`；必须有真实机器人写入、读回和重跑无重复证据，才能称日志已启用。不要把私有仓信息或验收证据贴到公开 OSS Issue。

公开 Fork 只用于贡献、公开安全试用或你明确希望公开的 Factory，不是普通私人使用的前置步骤。

## 先配置人和角色，不要先复制组织图

建议**管理、工程执行和独立审查按能力分工，不指定厂商**。Human 管方向，用户选用的 AI 管理者负责规划、任务协调和验收准备，具备实际工具能力的工程 Agent 负责开发和测试。Claude、ChatGPT、Gemini 等可做合适的管理岗位；Codex、Claude Code 或其他有权限的编码 Agent 可做工程岗位，也可以同一厂商不同上下文承担不同职责。
副厂长可以兼任书记员、厂务维护、基建规划；Development Lead 可以兼任 Console；不必每个头衔开一个聊天。
最终独立审查必须与作者分开，不能换个头衔就自己批准自己。
详细规则见 [角色配置建议](RECOMMENDED_ROLE_SETUP.md)。

普通查阅、协调、短文档和状态更新就在管理聊天里用现有仓库工具完成，
**少用 Work**。只有确实需要不同能力或较重执行任务，才进入单独的执行会话；
不为“收到、准备开始、再确认一次”另开 Work。已有接管上下文时只刷新有关增量，
不把每次任务升级成全厂审计。

## 先把精确版本拿到本地

`1.7.0` 版本线应在**正式发布后**使用精确 `v1.7.0` tag；不要直接假定
未来某个 `main` 仍然等于此版本，也不要把尚未发布的候选源码当作 Release。

### 不用 Git：Source ZIP

打开 [v1.7.0 Release（发布后）](https://github.com/AAAlcest/AI-Software-Factory-OSS/releases/tag/v1.7.0)，
下载 **Source code (zip)**，解压后在该目录打开终端。

### 使用 Git

```sh
git clone https://github.com/AAAlcest/AI-Software-Factory-OSS.git
cd AI-Software-Factory-OSS
git checkout --detach v1.7.0  # 仅在 v1.7.0 正式发布后
```

先确认版本：

```sh
cat VERSION
```

Windows PowerShell：

```powershell
Get-Content VERSION
```

正式发布的 `v1.7.0` Tag 应显示 `1.7.0`。

## 运行一套完全虚构的工厂

需要 Python 3.10 或以上，不需要模型 API Key 或第三方 Python 包。
在仓库根目录运行：

```sh
python -B scripts/create_demo.py --destination ../example-factory --case first
python -B scripts/validate_demo.py ../example-factory
python -B scripts/check_all.py
```

Windows 上如果平时使用 Python Launcher，可直接写：

```powershell
py -3 -B scripts/create_demo.py --destination ../example-factory --case first
py -3 -B scripts/validate_demo.py ../example-factory
py -3 -B scripts/check_all.py
```

目标目录必须不存在；生成器不覆盖旧目录。打开新目录里的 `AGENTS.md`，
即可沿入口找到办公室、项目房间、任命、当前状态、收发件引用、Console、
待办与工作记录。Atlas 有虚构任命，Beacon 缺少任命；缺失不能靠猜测补上。

校验器显示 `VALID` 只代表声明与结构一致，不代表你真的得到权限。
`PLANNED` 不代表邮件发出；`COMPLETED_ACKED` 不代表产品通过验收；
测试通过也不代表已经做过新 Agent 冷启动或独立隐私审查。

## 查看当前 cockpit / recovery 输出

仓库里可直接浏览的 `examples/factory-instance/project-cockpit/` 是一个静态教学
快照，不应默认理解成当前 generator 的完整最新输出。要生成当前 schema-2
派生视图，可以运行：

```sh
python -B scripts/generate_cockpit.py --root examples/factory-instance --output ../generated-cockpit
python -B scripts/generate_project_view.py --root examples/factory-instance --output ../project-view
```

这些输出仍然只是 derived context；真实仓库 state/evidence 才是 canonical truth。

## 真正使用时

把你的真实运行记录放在你自己的、经过授权的运行仓库中，不要填进这个公开 OSS 仓库。
开发过程主要用 Issue/PR，必要时才用框架自带的正式通信机制；同一事情不要两边重复记账。
换聊天是同任恢复，不是重新任命。只有真实换届才产生新的、不可改写的历史交接。

如果要做只读的 Factory 一致性／可恢复性审计，可使用 [Fresh Factory Audit](FRESH_FACTORY_AUDIT.md)，
也可以从 GitHub **New issue** 直接选择对应模板。审计 findings 只作为后续处置证据，
不会自动授权修改、merge、release、部署或生产操作。

历史 fresh-Agent、隐私与后续版本证据各自只对记录的精确目标和范围负责；不要把一个旧验收结果
扩张成对未来 `main` 的 blanket approval。
