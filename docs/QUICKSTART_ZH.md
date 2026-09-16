# 中文上手说明

## 先配置人和角色，不要先复制组织图

建议：**ChatGPT 负责厂内管理与职务；Codex 负责开发执行、开发组组长和 Console。**
副厂长可以兼任书记员、厂务维护、基建规划；不必每个头衔都开一个聊天。
各项目的开发交给 Codex，项目层面的管理对话仍可由 ChatGPT 承担。
最终独立审查必须与作者分开，不能换个头衔就自己批准自己。
详细规则见 [角色配置建议](RECOMMENDED_ROLE_SETUP.md)。

普通查阅、协调、短文档和状态更新就在管理聊天里用现有仓库工具完成，
**少用 Work**。只有确实需要不同能力或较重执行任务，才进入单独的执行会话；
不为“收到、准备开始、再确认一次”另开 Work。已有接管上下文时只刷新有关增量，
不把每次任务升级成全厂审计。

## 先把精确版本拿到本地

当前正式发布版本是 `v1.4.0`。如果你希望结果可复现，不要直接假定未来某个
`main` 仍然等于这个版本。

### 不用 Git：Source ZIP

打开 [v1.4.0 Release](https://github.com/AAAlcest/AI-Software-Factory-OSS/releases/tag/v1.4.0)，
下载 **Source code (zip)**，解压后在该目录打开终端。

### 使用 Git

```sh
git clone https://github.com/AAAlcest/AI-Software-Factory-OSS.git
cd AI-Software-Factory-OSS
git checkout v1.4.0
```

先确认版本：

```sh
cat VERSION
```

Windows PowerShell：

```powershell
Get-Content VERSION
```

应看到 `1.4.0`。

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

`v1.4.0` 已正式发布。历史 fresh-Agent、隐私与后续版本证据各自只对记录的精确目标
和范围负责；不要把一个旧验收结果扩张成对未来 `main` 的 blanket approval。
