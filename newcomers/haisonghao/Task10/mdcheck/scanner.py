# -*- coding: utf-8 -*-
"""scanner.py —— 扫描目录，收集 Markdown 文件。

核心思路（来自 Task 08 的 scan_md.py）：
用 pathlib 的 rglob("*.md") 递归找出目录下所有 .md 文件。
"""

from pathlib import Path


def find_markdown_files(root):
    """找出 root 目录下（含所有子目录）的 .md 文件。

    参数:
        root: 要扫描的目录（字符串或 Path 对象）。

    返回:
        按路径排序的 Path 列表。

    异常:
        NotADirectoryError: root 不是目录时抛出（由 main.py 捕获后给出友好提示）。
    """
    root = Path(root)
    if not root.is_dir():
        raise NotADirectoryError(f"目录不存在或不是文件夹: {root}")

    # rglob("*.md") = 递归匹配所有 .md 文件（不含大小写变体，如 .MD；
    # 洛谷式的严格匹配对中文文档场景足够用了）
    return sorted(root.rglob("*.md"))
