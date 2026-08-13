# 知止（Zhizhi）— 元认知"先查后做"

> **知止而后有定。** 一个元认知"先查后做"skill：打破 AI 智能体"埋头硬推、不检索、硬编造"的封闭执行习惯——先按任务轻重分级，再扫描信息缺口、自适应检索、校验方案、显式标注假设。**方法论跨 Agent，当前封装以 Claude Code 工具模型为参考。**

## 三层"知止"

1. **知道何时停止埋头硬推** → 转向外部检索
2. **知道何时停止检索** → 预算止损，不烧上下文
3. **知道何时承认查不到** → 假设显式化，不编造

## 灵感与定位

知止属于"元认知/先查后做"这一通用方法论家族。其设计吸收了同类实践的经验，包括：

- **ascetic-breaker**（苦行僧破执术）——"打破埋头硬推、先搜后做"这一核心问题的提出者
- **doubt-driven-development**——交付前的对抗性复查
- **verification-before-completion / skill-creator**——验证与触发设计的最佳实践

**知止是一次独立重构与进化，不是内容搬运**：
- 方法论层面（缺口检测、资源路由、交叉校验、反模式）属于通用工程实践，知止用自己的语言重新表达，并补上了分级、预算、复盘等新机制；
- 表达层面（哲学框架、术语、叙述方式）全部原创——知止的哲学锚点是《大学》"知止而后有定"，未沿用 ascetic-breaker 的苦行僧/禅宗公案/精神分析框架。

## 相比 ascetic-breaker 的进化点

| 进化方向 | ascetic-breaker | 知止 |
|----------|-----------------|------|
| 任务分级 | 无，所有任务同一套流程 | **T0/T1/T2 分级**，轻任务秒退、重任务全流程 |
| 检索委托 | 硬绑 domain-research，引用不存在的 skill | **自适应委托**：探测可用调研 skill，无则降级交叉检索 |
| 触发与预算 | description 冗长、无检索预算 | **精简触发 + 明确"不适用"边界 + 检索预算**（防烧上下文） |
| 复盘闭环 | 无 | **记录→读取→提取模式→调整→验证**，真正的跨会话自改进 |
| 评分/来源 | 固定权重 + 单轴 S/A/B/C/D | **硬约束 + 任务相关模板** + **来源多轴判定** |
| 协作 | 仅 domain-research | **协作地图**对接 doubt-driven-development、grilling 等 |

## 依据个人 CLAUDE.md 的强化

知止还蒸馏了作者个人 CLAUDE.md 的原则（证据优先、不附和、先拆前提），形成 4 个额外机制：

| 原则 | 机制 |
|------|------|
| 拆解前提、列反例、说明成立条件、给出验证方式 | **前提拆解与反例检查**（T2 任务先拆隐含前提再动手） |
| 区分事实、推断、观点和不确定项 | **证据分级输出**（✅事实/🔶推断/⚠️假设/❓未核实） |
| 不要为了迎合而附和、不要默认用户正确 | **独立判断不附和**（用户断言与证据矛盾时带证据反驳） |
| 信息可能过期/涉时效领域必须查证；高风险结论额外复核 | **查证强化**（时效强制检索 + 高风险双源复核 + 检索不越界） |

## 定位边界（元认知交通警察，不做万能 workflow）

知止的价值在**判断"什么时候不该继续凭脑子干、该把任务交给谁"**，不是把所有事情干完。刻意不扩展为万能 agent workflow，保持最小可辨识边界：

**知止不做**：深度研究、网页爬取、代码审查、GitHub 分析、安全扫描、实现、测试——这些交给专门 skill/工具。知止只负责：缺口检测、路由、校验、假设标注。

## 安装（跨 agent）

知止的**方法论跨 Agent**（Claude Code / Codex / Cursor / OpenCode 适用）；**当前封装（allowed-tools、工具命名、shell）以 Claude Code 为参考**，其他 Agent 需映射等价工具：

| Agent | skills 目录 |
|-------|-------------|
| Claude Code | `~/.claude/skills/zhizhi` |
| Codex | `~/.codex/skills/zhizhi` |
| Cursor | `~/.cursor/skills/zhizhi` |
| OpenCode 等 | 各自 skills 目录 |

```bash
# 复制（或 symlink）到目标 agent 的 skills 目录
cp -r zhizhi-skill ~/.claude/skills/zhizhi
```

**工具名适配**：SKILL.md 中的 `allowed-tools` 与检索工具（WebSearch/WebFetch/Glob/Grep）是 Claude Code 的命名；其他 agent 需把工具映射为各自等价能力（如 Codex 的 WebSearch/Bash/Grep）。**方法论跨 Agent，但封装不是"复制即用"，需按 agent 工具模型适配。**

触发示例：
```text
zhizhi：帮我写个解析 CSV 的脚本（先查项目里有没有现成的）
```

## 目录结构

```text
zhizhi-skill/
├── SKILL.md                    # 主技能（分级 + 四步工作流 + 复盘闭环 + trace）
├── README.md
├── references/
│   ├── triage.md               # 任务分级判定细则
│   ├── gap-detection.md        # 5 类缺口检测清单
│   ├── routing.md              # 自适应路由、委托与检索预算
│   ├── validation.md           # 方案评分、可信度、冲突处理
│   ├── anti-patterns.md        # 反模式与自检清单
│   └── retro.md                # 复盘闭环方法
├── scripts/
│   └── retro.py                # 复盘闭环工具（append/read/patterns/suggest）
└── eval/
    ├── EVAL.md                 # 三 agent 评估框架
    └── RESULTS.md              # 评估结果
```

## License

MIT（本项目自用与自由修改）。知止为独立创作，方法论不受单一来源限制；使用时注明灵感来源即可。
