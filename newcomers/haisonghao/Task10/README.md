# mdcheck —— Markdown 文档检查与清洗工具

> Task 10 通识收官项目　｜　作者：海嵩皓　｜　Python 标准库实现，零第三方依赖

一个轻量命令行工具（CLI），用于批量检查 Markdown 文档库：**检测死链与损坏图片、统计标题层级结构、自动生成目录索引**。后续 Line1（文档智能）业务中高频涉及本地文档解析，本工具即为其雏形。

## 功能特性

| 功能 | 说明 |
|---|---|
| 目录扫描 | 递归扫描指定目录，找出所有 `.md` 文件 |
| 死链检测 | 检查 `[]()` 相对链接指向的文件是否存在（跳过 http/锚点/邮件链接） |
| 坏图检测 | 检查 `![]()` 图片引用的文件是否存在 |
| 标题统计 | 统计每份文档 H1~H6 各级标题的数量 |
| 目录索引 | 汇总所有文档及其标题，生成格式良好的 `TOC.md` |
| 退出码约定 | 发现问题时退出码为 1，方便接入脚本 / CI 自动化 |

## 环境要求

- Python 3.8+（仅标准库，无需 `pip install` 任何东西）
- 或：Docker（无需安装 Python）

## 本地运行

```bash
# 基本用法：扫描 demo 目录
python main.py --dir demo

# 精简模式：只显示有问题的文档
python main.py --dir demo --quiet

# 生成报告文件与目录索引
python main.py --dir demo --output report.md --toc TOC.md
```

### 输出展示

对 `demo/` 目录（内含 2 个故意写坏的链接）运行 `python main.py --dir demo`：

```text
# mdcheck 检查报告

- 扫描目录：`E:/Task10/demo`
- 发现文档：**3** 份

## a.md
- 标题结构：H1×1、H2×3
- [问题] 死链: `not-exist.md`（a.md:19）
- [问题] 坏图: `img/missing.png`（a.md:23）

## b.md
- 标题结构：H1×1、H2×2
- 链接与图片：全部正常

## sub/c.md
- 标题结构：H1×1、H2×2
- 链接与图片：全部正常

## 汇总

- 文档总数：3
- 死链/坏图总数：**2**
```

生成的 `TOC.md`：

```markdown
# 文档目录索引

> 由 mdcheck 自动生成，共收录 3 份文档。

- [a.md](a.md)
  - 简介
  - 安装
  - 参考
- [b.md](b.md)
  - 背景
  - 使用说明
- [sub/c.md](sub/c.md)
  - 说明
  - 相对路径
```

## 容器化运行

项目附带 Dockerfile，其他成员无需装 Python，两条命令即可复现运行：

```bash
# 1. 构建镜像
docker build -t mdcheck .

# 2. 运行：把要检查的目录挂载进容器的 /data
#    （Linux / macOS / WSL 写法）
docker run --rm -v "$(pwd)/demo:/data" mdcheck

#    Windows PowerShell 写法
docker run --rm -v "${PWD}/demo:/data" mdcheck
```

容器默认执行 `python main.py --dir /data --quiet`；也可以自行追加参数：

```bash
docker run --rm -v "$(pwd)/demo:/data" mdcheck --dir /data --toc /data/TOC.md
```

## 项目结构

```
Task10/
├── main.py           # 主入口 + argparse 命令行接口
├── mdcheck/          # 功能模块包
│   ├── __init__.py
│   ├── scanner.py    # 目录扫描
│   ├── headings.py   # 标题层级解析与统计
│   ├── links.py      # 死链 / 坏图检测
│   └── toc.py        # 目录索引生成
├── demo/             # 演示样例（含故意写坏的链接，用于展示检测效果）
│   ├── a.md
│   ├── b.md
│   ├── img.png
│   └── sub/c.md
├── assets/           # 运行截图
├── requirements.txt  # 依赖清单（仅标准库，保留规范格式）
├── Dockerfile        # 容器封装
└── README.md
```

## 设计说明

- **模块化**：四个功能各占一个模块（scanner / headings / links / toc），`main.py` 只负责串流程与命令行参数，改任何一个功能不影响其余部分。
- **只查相对链接**：外链（http/https）在离线容器里无法验证，锚点与邮件链接无需文件存在，均跳过并在报告中不计为问题。
- **退出码约定**：正常退出 0、发现死链/坏图退出 1、参数错误退出 2，`docker run` 与 CI 都能据此判断结果。

## Git 提交历史

本项目按「每个功能模块一次提交」的规范开发，`git log` 可看到完整的迭代过程：

```text
feat: 项目初始化与目录扫描（scanner）
feat: 标题层级解析与统计（headings）
feat: 死链与坏图检测（links）
feat: 目录索引生成（toc）
feat: argparse 命令行接口与 requirements.txt
docs+docker: README 与容器封装
docs: 补充本地与容器化运行截图
```
