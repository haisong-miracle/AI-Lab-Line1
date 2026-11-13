# -*- coding: utf-8 -*-
"""mdcheck —— Markdown 文档检查工具（主入口）。

当前进度（M1）：扫描指定目录，列出所有 Markdown 文件。
后续里程碑将逐步加入：标题统计、死链检测、目录索引。
"""

import sys
from pathlib import Path

from mdcheck.scanner import find_markdown_files


def main():
    # 早期版本：目录参数直接取 sys.argv[1]，M5 会升级为 argparse
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
        print(" -", f.relative_to(root).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
