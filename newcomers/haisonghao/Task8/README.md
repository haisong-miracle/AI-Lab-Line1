# Task 08 —— Python 文件 I/O、异常处理与工程基础

## 任务目标

扫描指定文件夹中的所有 `.md` 文件，统计每个文件的**行数**与**字符数**，并将结果写入 `summary.json`。同时通过 `try/except` 处理扫描过程中可能出现的异常（如把文件夹误当成文件打开）。

## 文件清单

| 文件 | 说明 |
|---|---|
| `scan_md.py` | 主程序（约 60 行，含中文注释） |
| `summary.json` | 程序生成的统计结果 |
| `运行结果.txt` | 一次完整运行的终端输出存档 |

## 如何运行

```powershell
cd E:\Task08
E:\miniconda3\envs\py310\python.exe scan_md.py
```

程序会读取同目录下 `samples/` 里的 4 个样本（3 个 `.md` 文件 + 1 个名为 `fake.md` 的**文件夹**），并在当前目录生成 `summary.json`。

## 实现要点

1. **路径与扫描**：`pathlib.Path("samples").glob("*.md")` 逐个取出 `.md` 文件，不再手写一层层拼接的路径字符串。
2. **读文件**：`with open(p, encoding="utf-8") as f: text = f.read()`，用 `with` 保证文件用完自动关闭，显式指定 UTF-8 避免中文乱码。
3. **统计口径**：
   - 行数 = `len(text.splitlines())`（按行切开成列表再数元素，空行也算一行）；
   - 字符数 = `len(text)`（整段字符串的长度，不用 `split()` 数单词）。
4. **数据组织**：每个文件统计成一条字典记录 `{"file": ..., "lines": ..., "chars": ...}`，`append` 进列表 `records`。
5. **结果落盘**：`json.dump(records, f, ensure_ascii=False, indent=2)`，`ensure_ascii=False` 保证中文原样写入，`indent=2` 让 json 有可读的缩进。
6. **异常处理**：见下。

## 异常处理：崩溃 → 优雅跳过（本次作业的重点）

`samples/` 里故意放了一个名为 `fake.md` 的**文件夹**来制造意外。三种处理方式的效果对比：

| 方式 | 结果 |
|---|---|
| 不做任何处理 | 循环走到第 4 个文件时抛出 `PermissionError`，程序当场崩溃，`summary.json` 不会生成 |
| 预先判断 `if not p.is_file(): continue` | 能跑通，但只能防"这一种"已知意外 |
| `try/except`（最终采用） | 试一把，出 `PermissionError` 就记一笔"打不开，跳过"并继续，能兜住 `open` 环节的所有意外 |

最终程序输出（完整版见 `运行结果.txt`）：

```
--- 第 3 步 ---
打不开，跳过： fake.md
[{'file': 'a.md', 'lines': 6, 'chars': 55}, {'file': 'b.md', 'lines': 6, 'chars': 74}, {'file': 'empty.md', 'lines': 0, 'chars': 0}]

--- 第 4 步 ---
已生成 summary.json，共 3 条记录
```

## summary.json 内容

```json
[
  { "file": "a.md",     "lines": 6, "chars": 55 },
  { "file": "b.md",     "lines": 6, "chars": 74 },
  { "file": "empty.md", "lines": 0, "chars": 0 }
]
```

## 环境说明

- Windows 11 + PowerShell
- Python 3.10.25（Miniconda `py310` 环境）
- 仅使用标准库：`pathlib`、`json`
