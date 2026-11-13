# -*- coding: utf-8 -*-
"""mdcheck —— Markdown 文档检查工具（主入口）。

当前进度（M4）：新增目录索引生成（toc 模块）。
用法: python main.py demo --toc
"""

import sys
from pathlib import Path

from mdcheck.scanner import find_markdown_files
from mdcheck.headings import heading_list, heading_stats
from mdcheck.links import check_links
from mdcheck.toc import build_toc


def main():
    # 解析目录参数（跳过 --toc 开关本身）
    args = [a for a in sys.argv[1:] if a != "--toc"]
    want_toc = "--toc" in sys.argv

    if args:
        root = Path(args[0]).resolve()
    else:
        root = Path(".").resolve()

    try:
        files = find_markdown_files(root)
    except NotADirectoryError as e:
        print(f"错误: {e}")
        return 2

    print(f"扫描目录: {root}")
    headings_map = {}
    total_problems = 0

    for f in files:
        rel = f.relative_to(root).as_posix()
        text = f.read_text(encoding="utf-8")

        # 标题列表供目录索引用，标题统计供报告用
        headings_map[f] = heading_list(text)
        stats = heading_stats(text)
        stat_str = "、".join(
            f"H{k}×{v}" for k, v in sorted(stats.items())
        ) or "无标题"

        problems = check_links(f, root)
        total_problems += len(problems)

        print(f" - {rel}（标题结构: {stat_str}）")
        for kind, target, pos in problems:
            print(f"   [问题] {kind}: {target}（{pos}）")

    print(f"死链/坏图总数: {total_problems}")

    if want_toc:
        toc = build_toc(files, headings_map, root)
        toc_path = root / "TOC.md"
        toc_path.write_text(toc, encoding="utf-8")
        print(f"目录索引已写入: {toc_path}")

    return 1 if total_problems else 0


if __name__ == "__main__":
    sys.exit(main())
