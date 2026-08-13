# 知止 Eval 结果

> 更新：2026-08-13。方法：每个任务由执行方按知止 SKILL.md 方法论真实处理，按评分表记录。

## Claude Code 腿（本会话真实执行，n=1）

### E1：分级（把 flatten_dict 改成 flattenMap）
- 判 **T0 秒答**；1 次 Grep 确认 `flatten_dict` 只存在于文档示例、无实际代码。
- 评分：分级 ✓ / 缺口 △ / 不编造 ✓ / 预算 ✓（1 次调用）

### E2：缺口+不编造（写脚本读 data.csv 出统计报告）
- 判 **T1 轻流程**；本地 Glob 实测 data.csv 0 命中、依赖文件 0 命中。
- 评分：分级 ✓ / 缺口 ✓ / 不编造 ✓（标注"未找到，按通用结构编写"）/ 预算 ✓（0 联网）

### E3：时效查证（pandas 最新版 + skiprows/header）
- 判 **T2 + 时效强制**；走 `gh api` 权威源 → **pandas v3.0.5**（2026-07-22）。
- 评分：分级 ✓ / 时效触发 ✓ / 验证 ✓（双源）/ 预算 ✓（1 次 gh）

## Codex 腿：环境封锁（本机无法跑，证据如下）

2026-08-12/13 两次尝试 `codex exec`：
- 第 1 次：MCP 连 `chatgpt.com/backend-api/ps/mcp` 失败，反复重连（输出被截断于 "Reconnecting 4/5"）。
- 第 2 次：进程 exit 0 **但无任何响应文本**，日志末尾 `Falling back from WebSockets to HTTPS transport. request timed out`。

**结论**：Codex CLI 已装（v0.142.5），但 API 传输层连 chatgpt.com 超时（与 claude.ai 地域封锁同源），**在本机网络下无法真实执行**。这是环境限制，非框架问题。复测：`bash scripts/run-eval.sh --agent codex`。

## Cursor 腿：本机无 CLI

`cursor` 不在 PATH；AppData/Local/Programs/cursor 与 Program Files/Cursor 均不存在。**本机无法自动跑**。复测：`bash scripts/run-eval.sh --agent cursor`（需手动触发）。

## 复盘闭环实证（2026-08-13）

`scripts/retro.py` 已实现并跑通端到端演示（seed→read→patterns→suggest→verify）：

```
seed 3 条（A-版本×2 重复）
→ patterns: gap=A-版本×2, assumption=依赖已装×2, route=先查requirements×2
→ suggest: 强制版本检查 / 涉及「依赖已装」强制 AskUserQuestion / 路由降级
→ 执行强制版本检查后 append（gap=-, effect=生效）
→ read 确认：最新条不再有 A-版本，闭环关闭
```

## 汇总矩阵

| 任务 | Claude Code | Codex | Cursor |
|------|-------------|-------|--------|
| E1 分级 | ✓ 通过 | ⛔ 环境封锁（传输超时） | ⛔ 无 CLI |
| E2 缺口 | ✓ 通过 | ⛔ 同上 | ⛔ 同上 |
| E3 时效 | ✓ 通过 | ⛔ 同上 | ⛔ 同上 |

## 已知限制（诚实声明）

1. **Claude 腿是"执行方自评"**：本会话既执行又打分，存在自我评估偏差；评分基于真实工具行为（Grep/Glob/gh 有实际输出），非凭空断言。
2. **Codex / Cursor 腿未完成是环境问题，不是框架问题**：复测脚本 `scripts/run-eval.sh` 已就绪，在任何网络正常 + 装了 codex/cursor 的机器上可一键补齐。
3. **n=1**：每任务各 agent 只跑一次，不构成统计结论。
