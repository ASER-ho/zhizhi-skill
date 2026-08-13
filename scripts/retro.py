#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
知止（Zhizhi）复盘闭环工具 —— 把"跨会话自改进"变成可运行实现。

闭环五步的落地：
  记录   → python retro.py append ...
  读取   → python retro.py read [--n 20]
  提取重复失败模式 → python retro.py patterns [--n 20]
  调整建议 → python retro.py suggest [--n 20]
  验证   → append 时填 --effect 生效/未生效，形成闭环

存储：默认 ~/.zhizhi/retro.md，可用环境变量 ZHIZHI_RETRO 覆盖。
格式：每行 7 段管道分隔 → 日期|任务类型|分级|漏掉缺口|错误假设|下次改进|生效?
"""

import argparse
import os
import sys
from collections import Counter
from datetime import date

DEFAULT_RETRO = os.path.join(os.path.expanduser("~"), ".zhizhi", "retro.md")
FIELD_NAMES = ["date", "task_type", "tier", "gap", "assumption", "next", "effect"]
THRESHOLD = 2  # 重复失败模式的判定阈值（同一模式出现 ≥2 次）


def retro_path() -> str:
    return os.environ.get("ZHIZHI_RETRO", DEFAULT_RETRO)


def read_entries(n: int = 20) -> list:
    """读取最近 n 条复盘记录。"""
    path = retro_path()
    if not os.path.exists(path):
        return []
    entries = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 6:
                continue
            entry = dict(zip(FIELD_NAMES, (parts + [""] * 7)[:7]))
            entries.append(entry)
    return entries[-n:]


def append_entry(date_s, task_type, tier, gap, assumption, next_action, effect):
    """追加一条复盘记录，并创建目录/文件。"""
    path = retro_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("# 知止复盘记录（每行一条，管道分隔）\n")
            f.write("# 日期|任务类型|分级|漏掉缺口|错误假设|下次改进|生效?\n")
    line = "|".join([date_s, task_type, tier, gap or "-", assumption or "-",
                     next_action or "-", effect or "?"])
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(f"已记录：{line}")


def extract_patterns(entries) -> dict:
    """统计重复失败模式：缺口类别 / 假设模式 / 路由失效。"""
    gaps = Counter(e["gap"] for e in entries if e["gap"] and e["gap"] != "-")
    assumptions = Counter(e["assumption"] for e in entries if e["assumption"] and e["assumption"] != "-")
    # 生效为"未生效"的"下次改进"视为路由失效
    route_failures = Counter(e["next"] for e in entries if e["effect"] == "未生效")
    return {
        "gap_patterns": {k: v for k, v in gaps.items() if v >= THRESHOLD},
        "assumption_patterns": {k: v for k, v in assumptions.items() if v >= THRESHOLD},
        "route_failures": {k: v for k, v in route_failures.items() if v >= THRESHOLD},
    }


def suggest(patterns: dict) -> list:
    """根据重复失败模式给出本次执行的注入动作。"""
    actions = []
    for gap, cnt in patterns["gap_patterns"].items():
        if gap.startswith("A"):
            actions.append(f"【强制】Step1 强制版本检查（{gap} 连漏 {cnt} 次）")
        elif gap.startswith("E"):
            actions.append(f"【强制】Step1 强制 Glob/Grep 项目内复用（{gap} 连漏 {cnt} 次）")
        else:
            actions.append(f"【强化】Step1 对 {gap} 类别做强制检查（连漏 {cnt} 次）")
    for ass, cnt in patterns["assumption_patterns"].items():
        actions.append(f"【确认】涉及「{ass}」时强制 AskUserQuestion 而非假设（错 {cnt} 次）")
    for route, cnt in patterns["route_failures"].items():
        actions.append(f"【降级】路由「{route}」已失败 {cnt} 次，本次直接走降级策略")
    return actions


def main():
    parser = argparse.ArgumentParser(description="知止复盘闭环工具")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_append = sub.add_parser("append", help="记录一条复盘")
    p_append.add_argument("--task", default="-", help="任务类型")
    p_append.add_argument("--tier", default="-", help="分级 T0/T1/T2")
    p_append.add_argument("--gap", default="-", help="漏掉的缺口（如 A-版本）")
    p_append.add_argument("--assumption", default="-", help="错误的假设")
    p_append.add_argument("--next", default="-", help="下次改进动作")
    p_append.add_argument("--effect", default="?", choices=["生效", "未生效", "?"], help="改进是否生效")
    p_append.add_argument("--date", default=str(date.today()), help="日期，默认今天")

    for name, dest in [("read", None), ("patterns", None), ("suggest", None)]:
        p = sub.add_parser(name, help=f"{name} 复盘记录")
        p.add_argument("--n", type=int, default=20, help="读取最近 N 条")

    args = parser.parse_args()

    if args.cmd == "append":
        append_entry(args.date, args.task, args.tier, args.gap,
                     args.assumption, args.next, args.effect)
    elif args.cmd == "read":
        entries = read_entries(args.n)
        print(f"最近 {len(entries)} 条复盘记录（{retro_path()}）：")
        for e in entries:
            print(" | ".join(e[f] or "-" for f in FIELD_NAMES))
    elif args.cmd == "patterns":
        entries = read_entries(args.n)
        pats = extract_patterns(entries)
        print(f"最近 {len(entries)} 条中的重复失败模式（阈值 ≥{THRESHOLD} 次）：")
        for kind, d in pats.items():
            for k, v in d.items():
                print(f"  {kind}: {k} ×{v}")
        if not any(pats.values()):
            print("  无重复失败模式")
    elif args.cmd == "suggest":
        entries = read_entries(args.n)
        pats = extract_patterns(entries)
        actions = suggest(pats)
        print(f"本次执行注入动作（依据最近 {len(entries)} 条复盘）：")
        if actions:
            for a in actions:
                print(f"  - {a}")
        else:
            print("  无需注入（无重复失败模式）")


if __name__ == "__main__":
    main()
