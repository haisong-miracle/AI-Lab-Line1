# -*- coding: utf-8 -*-
"""toc.py —— 生成格式良好的目录索引。

输出一份 Markdown 文件：
    - 每份文档一行，链接指向该文档
    - 该文档的二级及以下标题缩进列出（一级标题就是文档本身，不重复）

这样拿到一个陌生目录，打开 TOC.md 就能知道里面有哪些文档、
每篇都讲了什么。
"""


def build_toc(files, headings_map, root):
    """生成目录索引文本。

    参数:
        files:        scanner 找到的 .md 文件列表
        headings_map: {文件Path: [(层级, 标题), ...]}，来自 headings.heading_list
        root:         扫描根目录

    返回:
        完整的目录索引字符串（Markdown 格式）。
    """
    lines = [
        "# 文档目录索引",
        "",
        f"> 由 mdcheck 自动生成，共收录 {len(files)} 份文档。",
        "",
    ]

    for f in files:
        # 报告里统一用相对路径，跨系统可读（Windows 的 \ 换成 /）
        rel = f.relative_to(root).as_posix()
        lines.append(f"- [{rel}]({rel})")

        # 二级及以下标题缩进展示，形成层级感
        for level, title in headings_map.get(f, []):
            if level >= 2:
                indent = "  " * (level - 2)  # 二级不缩进，三级缩 2 格...
                lines.append(f"{indent}- {title}")

        lines.append("")

    return "\n".join(lines) + "\n"
