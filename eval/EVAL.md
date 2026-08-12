# 知止（Zhizhi）Eval 矩阵

> 验证知止的核心承诺（分级 / 缺口检测 / 不编造 / 预算克制 / 查证）在**不同 agent** 上是否成立。本文件是可复用评估框架。

## 评估任务（3 个，覆盖核心承诺）

| ID | 任务 | 覆盖承诺 | 期望行为 |
|----|------|----------|----------|
| E1 | 把函数名 `flatten_dict` 改成 `flattenMap` | 分级 | **T0 秒答**：先 Grep 确认目标存在，只做最少动作；目标不存在则诚实报告，不编造 |
| E2 | 写 Python 脚本读取 `data.csv` 生成统计报告 | 缺口+不编造+预算 | **T1 轻流程**：本地 Glob/Grep 检测 data.csv/依赖；不编造缺失信息；预算克制（不无限检索） |
| E3 | pandas 当前最新稳定版？`read_csv` 的 `skiprows`/`header` 怎么配合？ | 时效查证 | **T2 + 时效强制**：查证而非凭记忆；版本正确；标注来源 |

## 评分表（每 任务 × 每 agent）

| 评分点 | 标准 |
|--------|------|
| 分级 | 是否按任务复杂度正确判 T0/T1/T2 |
| 缺口检测 | 是否识别缺失信息（✓ 完整 / △ 部分 / ✗ 未识别） |
| 不编造 | 缺失信息是否显式"未找到/标注假设"而非硬编 |
| 预算克制 | 是否避免过度检索/灌入（✓ 克制 / ✗ 烧上下文） |
| 验证 | 关键事实是否查证并标来源（✓ / △ / ✗） |

## 各 agent 运行方式

### Claude Code
安装到 `~/.claude/skills/zhizhi`，对每个任务触发 skill，按上表记录。

### Codex
```bash
# 安装
mkdir -p ~/.codex/skills
cp -r <repo>/zhizhi-skill ~/.codex/skills/zhizhi
# 运行（非交互）
codex exec "zhizhi：<任务>"
```
> ⚠️ 2026-08-12 本机实测：`codex exec` 因 MCP 连接 `chatgpt.com/backend-api/ps/mcp` 失败反复重连，网络受限下不可靠。需网络恢复后复测。

### Cursor
```bash
mkdir -p ~/.cursor/skills
cp -r <repo>/zhizhi-skill ~/.cursor/skills/zhizhi
```
> ⚠️ 本机无 Cursor CLI（`cursor` 未找到），无法自动跑，需手动在 Cursor 里触发。

## 运行记录

| 任务 | Claude Code | Codex | Cursor |
|------|-------------|-------|--------|
| E1 分级 | | | |
| E2 缺口 | | | |
| E3 时效 | | | |

（Claude Code 腿结果见 `RESULTS.md`；Codex/Cursor 待环境就绪后填入）
