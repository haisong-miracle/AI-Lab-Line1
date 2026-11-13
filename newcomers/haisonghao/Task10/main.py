# -*- coding: utf-8 -*-
"""mdcheck —— Markdown 文档检查工具（主入口）。

当前进度（M3）：新增死链与坏图检测（links 模块）。
"""

import sys
from pathlib import Path

from mdcheck.scanner import find_markdown_files
from mdcheck.headings import heading_stats
from mdcheck.links import check_links


def main():
    if len(sys.argv) > 1:
        root = Path(sys.argv[1]).resolve()
    else:
        root = Path(".").resolve()

    try:
        files = find_markdown_files(root)
    except NotADirectoryError as e:
        print(f"错误: {e}")
        return 2

    print(f"扫描目录: {root}")
    total_problems = 0
    for f in files:
        rel = f.relative_to(root).as_posix()
        text = f.read_text(encoding="utf-8")

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
    return 1 if total_problems else 0


if __name__ == "__main__":
    sys.exit(main())
