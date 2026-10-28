# Task 07 — Python 核心语法与常用数据结构

按仓库规范存放于 `newcomers/haisonghao/src/basics/`。

## 文件清单

| 文件 | 覆盖知识点 |
|---|---|
| `src/basics/01_collections.py` | list/dict/tuple/set：标点清洗、词频统计（dict.get）、双条件排序（sorted + lambda 元组 key）、切片、集合交并差（`& \| - ^`）、列表推导式 |
| `src/basics/02_control_flow.py` | if/elif/else 分级、break 哨兵值（-1）与 continue 缺考（None）、while 累加、f-string 对齐输出（`< > ^` 与精度控制） |
| `src/basics/03_functions.py` | `*args` / `**kwargs`、可变默认值陷阱（`bucket=None`）、闭包（nonlocal）、global 作用域、动态精度格式化 `.{precision}f` |

## 设计说明

- **练习一**以一段 Docker 语料为载体，走完"清洗 → 结构化 → 统计 → 排序"的完整数据处理链路；
- **练习二**的 `STUDENTS` 数据刻意埋入 `None`（缺考）与 `-1`（结束标记），用于区分 `continue` 与 `break` 的语义；
- **练习三**的 `add_item(item, bucket=None)` 现场演示可变默认值陷阱的正确解法，`make_counter` 演示闭包计数。

## 验收结果

- 自检器 `selfcheck.py`（15 个检查点，覆盖边界值）：**通过 15/15**
- `pycodestyle --max-line-length=79`：**零告警**
- 三个文件的完整运行输出见 `运行结果.txt`，自检与 PEP8 记录一并附于文末。

## 运行方式

```bash
python src/basics/01_collections.py
python src/basics/02_control_flow.py
python src/basics/03_functions.py
```
