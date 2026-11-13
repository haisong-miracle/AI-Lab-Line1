# -*- coding: utf-8 -*-
"""links.py —— 检测 Markdown 中的死链与损坏图片。

Markdown 链接的两种形态：
    [显示文字](目标)      普通链接
    ![替代文字](目标)     图片链接（多个 ! 前缀）

本模块只检查【相对路径】目标：
    - b.md            → 检查文件是否存在
    - img/logo.png    → 检查图片文件是否存在
    - http(s)://...   → 外部链接，离线环境不验证，跳过
    - #锚点           → 页内跳转，跳过
    - mailto:         → 邮件链接，跳过
"""

import re
from pathlib import Path
from urllib.parse import unquote

# 匹配所有链接/图片：
# (!?)      捕获组1：可有可无的 ! （有 = 图片）
# \[...\]   方括号里的显示文字（内容任意，但不允许嵌套 ]）
# \(([^)\s]+)\)  圆括号里的目标（不含空格和右括号）
_LINK_RE = re.compile(r"(!?)\[[^\]]*\]\(([^)\s]+)\)")

# 这些开头的目标不是本地相对路径，直接跳过
_SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")


def check_links(md_path, root):
    """检查一个 Markdown 文件里的相对链接与图片。

    参数:
        md_path: 要检查的 .md 文件路径
        root:    扫描根目录（用于把绝对路径转成报告里好看的相对路径）

    返回:
        问题列表，每项为 (问题类型, 目标, 相对位置)，
        问题类型是 "死链" 或 "坏图"；没有问题则返回空列表。
    """
    problems = []
    base = md_path.parent  # 相对路径以该 md 文件所在目录为基准
    text = Path(md_path).read_text(encoding="utf-8")

    for line_no, line in enumerate(text.splitlines(), start=1):
        for is_img, target in _LINK_RE.findall(line):
            if target.startswith(_SKIP_PREFIXES):
                continue

            # 目标可能带锚点（如 b.md#section），锚点部分不影响文件存在性
            file_part = target.split("#")[0]
            if not file_part:  # 纯锚点 "#xxx"
                continue

            # 网址里的空格会写成 %20，解码成真实文件名
            file_part = unquote(file_part)

            resolved = (base / file_part).resolve()

            kind = "坏图" if is_img else "死链"
            ok = resolved.is_file() if is_img else resolved.exists()
            if not ok:
                rel_pos = Path(md_path).relative_to(root).as_posix()
                problems.append((kind, target, f"{rel_pos}:{line_no}"))

    return problems
