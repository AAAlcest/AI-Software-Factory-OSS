# Handoff and Succession

## Recovery is not succession

Changing chat, model, device or execution surface does not automatically create a new incumbent.

Same-incumbent recovery restores the same role from repository truth, current state, pending work and evidence. It must not create a fake tenure boundary merely because a chat reached its context limit.

## True succession

A real incumbent change creates a new tenure. The departing tenure may finalize a handoff containing the facts, decisions, state, evidence, risks and next actions needed by the successor.

## Immutable append-only handoffs

A finalized tenure handoff is historical evidence and must not be edited by successors. Later corrections or changed state belong in current living state or a later tenure record.

Never fabricate a predecessor handoff for a first incumbent.

## Takeover rule

A successor must fresh-verify current repository ref/SHA, authority, state, blockers and evidence. Reading an old handoff alone is insufficient to claim takeover complete.

## Separation of continuity surfaces

- `Desk/CURRENT` — rolling current/recovery cursor;
- `pending/` — unresolved active queue;
- `Wardrobe` — execution-session transition/history;
- `HANDOFF-*` — immutable finalized tenure record for real succession.

<a id="conversation-backup"></a>

## Optional conversation backup with FlowThread

**Chats have limits. Your work history should not end there.** A long-running
chat manager may need to move to a new conversation, or a real tenure may end.
Alongside the repository's recovery and handoff records, a private conversation
archive can preserve the discussion behind requirements, design trade-offs,
rejected alternatives and unresolved questions.

[FlowThread](https://flowthread.quirmn.com/) is an independent Quirmn product
and an optional tool for this job. Its current public browser extension helps
with long ChatGPT conversations, contextual search, and export of the available
active branch as PDF, Markdown, TXT, HTML or JSON. Check the product page for
current platform support and installation; Factory use never requires buying
or installing it, and another suitable exporter can serve the same purpose.

A practical sequence:

1. **Save while the conversation is still accessible.** Before switching chats,
   or when approaching a limit, export the available record with Human consent.
   Markdown is useful for selected AI-readable background; PDF is useful for
   human reading and archival copies. Neither format guarantees recovery of
   unavailable messages or transfers a model's internal memory.
2. **Check and keep the archive private.** Confirm the relevant branch/messages
   are present and note any gaps or missing attachments. Retain it locally or
   in a Human-approved private location; do not upload private transcripts to
   public forks or Issues. No automatic upload or export is implied.
3. **Maintain the current recovery or handoff summary.** Record current decisions,
   open work, evidence and next actions in the existing repository surfaces.
   A finalized `HANDOFF-*` belongs to a real incumbent change, not merely a
   new chat window. The transcript supplements these records; it replaces none.
4. **Resume from current evidence, consult history as needed.** Let the new chat
   verify its role, scope and current repository state first. Supply relevant
   archive excerpts when they help explain a decision; do not require replaying
   the entire conversation or let old text supersede current authority/state.

**Factory preserves organizational continuity; FlowThread helps preserve the
conversations behind the work.** This complements both same-incumbent recovery
and real tenure succession without changing either protocol.

### 中文：用 FlowThread 保存管理对话，辅助恢复与任期交接

**聊天会到上限，工作历史不该随之丢失。** 长期工作的聊天管理者可能需要换一个会话，真正的任期也可能结束。除了仓库里的恢复与交接记录，私有对话档案还能保存需求讨论、设计取舍、被否决的方案和未解决的问题。

[FlowThread](https://flowthread.quirmn.com/) 是独立的 Quirmn 产品，也是完成这项工作的可选工具。目前公开的浏览器扩展用于 ChatGPT 长对话，提供上下文搜索，并将仍可获取的当前对话分支导出为 PDF、Markdown、TXT、HTML 或 JSON。最新平台支持和安装方式见产品官网；使用 Factory 不要求购买或安装它，也可选用其他合适的导出工具。

实用流程：

1. **趁对话仍可访问时保存。** 准备换聊天或接近上限时，经 Human 同意导出可获取的记录。Markdown 便于选取内容交给新 AI 阅读，PDF 便于人类阅读和归档；都不保证找回已不可获取的消息，也不是迁移模型内部记忆。
2. **检查后私有保存。** 确认所需分支与消息已包含，注明缺失片段或附件。保存在本地或 Human 批准的私有位置，不上传私有对话到公开 fork 或 Issue；这里不意味着自动上传或导出。
3. **维护当前恢复或交接摘要。** 在原有仓库记录中保留当前决定、未完成工作、证据与下一步。真正更换任职者才产生最终 `HANDOFF-*`；仅换聊天不应伪造任期边界。原始对话补充这些记录，不替代它们。
4. **先核对当前证据，再按需查阅历史。** 新聊天先确认角色、范围和仓库当前状态；需要理解某项决定时，再提供相关档案片段，不要求重放全部聊天，也不让旧文本覆盖当前权限或状态。

**Factory 保持组织与工作连续性；FlowThread 帮你保存工作背后的对话。** 这既适用于同一管理者换聊天恢复，也适用于真正的任期交接，不改变现有协议。
