# -*- coding: utf-8 -*-
"""headings.py —— 解析 Markdown 的标题层级结构。

Markdown 标题的写法：
    # 一级标题
    ## 二级标题
    ### 三级标题
规则：行首 1~6 个 # ，后面必须跟至少一个空格和文字。
注意 #必须顶格（行首有空格的不算标题，那是普通段落）。
"""

import re

# 匹配标题行：行首 1~6 个 # + 空格 + 非空内容
# ^       行首
# (#{1,6}) 捕获组1：1 到 6 个 #，层级就是 # 的个数
# \s+     # 后面的空白（至少一个）
# \S      第一个非空白字符（保证标题有内容，"## " 空标题不算）
_HEADING_RE = re.compile(r"^(#{1,6})\s+\S")


def heading_stats(text):
    """统计一份文档中各级标题的数量。

    返回 dict，例如 {1: 1, 2: 3} 表示 1 个一级标题、3 个二级标题。
    没有任何标题时返回空 dict。
    """
    stats = {}
    for line in text.splitlines():
        m = _HEADING_RE.match(line)
        if m:
            level = len(m.group(1))  # # 的个数就是层级
            stats[level] = stats.get(level, 0) + 1
    return stats


def heading_list(text):
    """按出现顺序返回所有标题，格式 [(层级, 标题文字), ...]。

    供 toc.py 生成目录索引使用。
    """
    result = []
    for line in text.splitlines():
        m = _HEADING_RE.match(line)
        if m:
            # 去掉标题结尾的 #（行内结束标记，如 "## 标题 ##"）和首尾空白
            title = line[len(m.group(1)):].lstrip()
            title = title.rstrip().rstrip("#").rstrip()
            result.append((len(m.group(1)), title))
    return result
