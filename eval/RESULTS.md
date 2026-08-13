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

## Codex 腿（VPN 后手动触发，真实执行，n=1）

> 环境：Codex CLI 0.142.5 + ChatGPT 账号，VPN 开启后由用户在 codex 内手动触发知止。**未修改任何文件**。

### E1：分级（把 flatten_dict 改成 flattenMap）
- 判 **T0 秒答**；检索整个工作区未找到 `flatten_dict`；`rg.exe` 权限被拒后**自动切 PowerShell `Select-String` 兜底**。
- 未猜文件位置、未批量替换。评分：分级 ✓ / 缺口 ✓ / 不编造 ✓ / 预算 ✓

### E2：缺口+不编造（写脚本读 data.csv 出统计报告）
- 判 **T1 轻流程**；确认 data.csv 未找到、Python 3.12.10 可用、pandas 未安装。
- **拒绝写虚构脚本**："列结构和报告要求无法验证，本次没有创建脚本"。评分：分级 ✓ / 缺口 ✓ / 不编造 ✓✓ / 预算 ✓

### E3：时效查证（pandas 最新版 + skiprows/header）
- 判 **T2 + 时效强制**；双源（官方 whatsnew + PyPI）→ **pandas 3.0.5**（2026-07-22），正确。
- 附 skiprows/header 配合规则与代码示例。评分：时效触发 ✓ / 验证 ✓（双源）/ 不编造 ✓

### 关键发现：工具映射生效
`rg.exe` 权限被拒 → 自动降级 PowerShell `Select-String`，印证知止"方法论跨 agent、工具名以 Claude Code 为例、其他 agent 映射等价工具"的设计成立。

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

| 任务 | Claude Code | Codex |
|------|-------------|-------|
| E1 分级 | ✓ 通过 | ✓ 通过 |
| E2 缺口 | ✓ 通过 | ✓ 通过 |
| E3 时效 | ✓ 通过 | ✓ 通过 |

## 已知限制（诚实声明）

1. **Claude 腿是"执行方自评"**：本会话既执行又打分，存在自我评估偏差；评分基于真实工具行为（Grep/Glob/gh 有实际输出），非凭空断言。
2. **Codex 腿是"用户手动触发 + 用户转述结果"**：非自动采集，评分基于用户提供的执行描述，未经工具日志逐条核验。
3. **n=1**：每任务各 agent 只跑一次，不构成统计结论。
