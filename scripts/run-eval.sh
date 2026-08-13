#!/usr/bin/env bash
# 知止（Zhizhi）Eval 复测脚本（Claude Code + Codex）
#
# 用途：一键安装并跑 3 个 eval 任务，产出矩阵数据。
# 用法：bash run-eval.sh [--agent all|codex|claude]

set -e
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
AGENT="${1:-all}"

CLAUDE_DIR="$HOME/.claude/skills/zhizhi"
CODEX_DIR="$HOME/.codex/skills/zhizhi"

TASKS=(
  "zhizhi：把函数名 flatten_dict 改成 flattenMap"
  "zhizhi：写一个 Python 脚本，读取 data.csv 生成统计报告"
  "zhizhi：Python pandas 当前最新稳定版是多少？read_csv 的 skiprows 和 header 怎么配合？"
)

install() { # $1 = agent dir
  mkdir -p "$(dirname "$1")"
  if [ -e "$1" ]; then rm -rf "$1"; fi
  cp -r "$REPO_DIR" "$1"
  # 不需要把 eval/scripts 之外的调试产物装进去，保留核心即可
  echo "  已安装到 $1"
}

run_codex() {
  echo "== Codex =="
  install "$CODEX_DIR"
  i=1
  for t in "${TASKS[@]}"; do
    echo "-- 任务 E$i: $t --"
    codex exec "$t" 2>&1 | tee "/tmp/zhizhi-eval-codex-E$i.log" || echo "  [E$i] codex exec 失败"
    i=$((i+1))
  done
}

run_claude() {
  echo "== Claude Code（交互式，需手动触发）=="
  install "$CLAUDE_DIR"
  echo "  请手动打开 Claude Code，对每个任务输入："
  i=1
  for t in "${TASKS[@]}"; do
    echo "    E$i: $t"
    i=$((i+1))
  done
}

case "$AGENT" in
  all)   run_claude; echo; run_codex ;;
  codex) run_codex ;;
  claude) run_claude ;;
  *) echo "未知 agent: $AGENT"; exit 1 ;;
esac

echo
echo "完成。按 eval/RESULTS.md 的评分表记录各腿结果，填进汇总矩阵即可。"
