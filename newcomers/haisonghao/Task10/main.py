# -*- coding: utf-8 -*-
"""mdcheck —— Markdown 文档检查工具（主入口）。

当前进度（M2）：新增标题层级解析与统计（headings 模块）。
"""

import sys
from pathlib import Path

from mdcheck.scanner import find_markdown_files
from mdcheck.headings import heading_stats


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
    print(f"发现 {len(files)} 份 Markdown 文档:")
    for f in files:
        rel = f.relative_to(root).as_posix()
        # 统计标题：{1: 2, 3: 1} → "H1×2、H3×1"
        stats = heading_stats(f.read_text(encoding="utf-8"))
        stat_str = "、".join(
            f"H{k}×{v}" for k, v in sorted(stats.items())
        ) or "无标题"
        print(f" - {rel}（标题结构: {stat_str}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
