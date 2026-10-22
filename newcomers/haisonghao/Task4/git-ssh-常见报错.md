# Git 与 SSH 常见报错记录

> 环境：Windows 11 + WSL2 (Ubuntu) + GitHub
> 记录时间：2026-10-18

---

## 一、`fatal: not a git repository (or any parent up to mount point /mnt)`

**现象**：执行 `git add` / `git commit` / `git push` 时反复报这一行，连续出现多次。

**根因**：当前目录不是 Git 仓库。当时先执行了 `cd /mnt/e/AI-Lab-Line1`，但该目录在本机并不存在（仓库只在另一台笔记本上），`cd` 失败后停留在 `/mnt/e`，后续所有 git 命令都在一个非仓库目录里执行。

**定位路径**：
1. `pwd` 确认当前所在目录
2. `ls -a` 看有没有 `.git` 文件夹
3. `git rev-parse --show-toplevel` 看 Git 能否找到仓库根

**解决**：先确认仓库真实位置再 `cd` 进去；`cd` 失败时不要继续执行后续命令 —— 用 `cd 路径 && git 命令` 串联，`&&` 会在前一步失败时中断后续动作。

---

## 二、`fatal: The current branch basic/duxinyi has no upstream branch`

**现象**：`git push` 后提示当前分支没有上游分支。

**根因**：本地用 `git checkout -b` 新建的分支，远程仓库还没有同名分支，Git 不知道该推到哪里。

**解决**：

```bash
git push --set-upstream origin basic/duxinyi
```

`--set-upstream`（简写 `-u`）会在远程创建同名分支并建立跟踪关系，之后直接 `git push` 即可。

---

## 三、`git config` 把占位符写进了配置

**现象**：执行了 `git config --global user.name "你的名字"`，结果用户名真的变成了「你的名字」三个字。

**根因**：文档里的占位符被当成实际参数执行。

**解决**：

```bash
git config --global user.name "真实姓名"
git config --global user.email "GitHub 注册邮箱"
git config --global --list          # 核对
```

**经验**：提交记录的作者信息来自 `user.name` / `user.email`，与 GitHub 账号不一致时，提交不会挂到你的头像下。配置完务必 `--list` 自查一遍。

---

## 四、`error: garbage option` / `+: command not found`

**现象**：`ps aux / df -h / free -m` 报 `error: garbage option`，随后 `+` 报 `command not found`。

**根因**：把文档排版用的 `/` 当成了命令分隔符整行粘贴。Shell 的多命令分隔符是 `;` 或 `&&`，`/` 会被当作命令参数。

**解决**：一条命令一行；或用 `;`（顺序执行）、`&&`（前一条成功才执行）。

---

## 五、待补充

- SSH 首次连接 GitHub 的 `Permission denied (publickey)` 排查
- 校园网 22 端口被封时的 SSH over 443 配置
