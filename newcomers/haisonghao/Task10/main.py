# -*- coding: utf-8 -*-
"""mdcheck —— Markdown 文档检查与清洗工具（主入口）。

用法示例：
    python main.py --dir demo
    python main.py --dir demo --output report.md --toc TOC.md
    python main.py --dir demo --quiet
"""

import argparse
import sys
from pathlib import Path

from mdcheck.headings import heading_list, heading_stats
from mdcheck.links import check_links
from mdcheck.scanner import find_markdown_files
from mdcheck.toc import build_toc


def build_report(root, files, quiet):
    """逐份文档生成检查报告，返回 (报告文本, 死链坏图总数)。"""
    lines = [
        "# mdcheck 检查报告",
        "",
        f"- 扫描目录：`{root.as_posix()}`",
        f"- 发现文档：**{len(files)}** 份",
        "",
    ]
    total_problems = 0

    for f in files:
        rel = f.relative_to(root).as_posix()
        text = f.read_text(encoding="utf-8")

        # 标题统计：{1: 2, 3: 1} → "H1×2、H3×1"
        stats = heading_stats(text)
        stat_str = "、".join(
            f"H{k}×{v}" for k, v in sorted(stats.items())
        ) or "无标题"

        problems = check_links(f, root)
        total_problems += len(problems)

        lines.append(f"## {rel}")
        lines.append(f"- 标题结构：{stat_str}")
        if problems:
            for kind, target, pos in problems:
                lines.append(f"- [问题] {kind}: `{target}`（{pos}）")
        else:
            lines.append("- 链接与图片：全部正常")
        lines.append("")

        if quiet:
            # 精简模式：只打印有问题的文档名
            if problems:
                print(f"[问题] {rel}: "
                      + "、".join(f"{k}:{t}" for k, t, _ in problems))
            continue

    lines += [
        "## 汇总",
        "",
        f"- 文档总数：{len(files)}",
        f"- 死链/坏图总数：**{total_problems}**",
        "",
    ]
    return "\n".join(lines) + "\n", total_problems


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="mdcheck",
        description="Markdown 文档检查工具：死链/坏图检测、标题统计、目录索引生成",
    )
    parser.add_argument("--dir", default=".",
                        help="要扫描的目录（默认当前目录）")
    parser.add_argument("--output", default=None,
                        help="检查报告的输出文件（不指定则打印到屏幕）")
    parser.add_argument("--toc", default=None,
                        help="目录索引的输出文件（不指定则不生成）")
    parser.add_argument("--quiet", action="store_true",
                        help="精简模式：屏幕上只显示有问题的文档")
    args = parser.parse_args(argv)

    root = Path(args.dir).resolve()
    try:
        files = find_markdown_files(root)
    except NotADirectoryError as e:
        parser.error(str(e))  # argparse 会打印提示并退出（退出码 2）

    if not files:
        print(f"目录 {root} 下没有找到任何 .md 文件")
        return 0

    # 先解析所有文档的标题，供报告和目录索引共用
    headings_map = {
        f: heading_list(f.read_text(encoding="utf-8")) for f in files
    }

    report, total_problems = build_report(root, files, args.quiet)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"检查报告已写入: {args.output}")
    elif not args.quiet:
        # 精简模式下 build_report 已经逐条打印了问题行，不再重复输出全文
        print(report, end="")

    if args.toc:
        toc = build_toc(files, headings_map, root)
        Path(args.toc).write_text(toc, encoding="utf-8")
        print(f"目录索引已写入: {args.toc}")

    # 约定：发现问题时退出码为 1，方便脚本/CI 判断
    return 1 if total_problems else 0


if __name__ == "__main__":
    sys.exit(main())
