"""Task 08 —— 扫描文件夹里的 .md 文件，统计行数与字符数，输出 summary.json

第 1 步：把 samples 里所有 .md 列出来（已写好，跑通了）
第 2 步：读一个文件，算出它的行数和字符数（下面留了两个空，你自己填）
第 3~5 步：循环、写 json、加 try/except，都由你自己往上加
"""

import json

from pathlib import Path


# ---- 第 1 步：把 samples 里所有 .md 列出来（只看，不读内容）----
for p in Path("samples").glob("*.md"):
    print(p.name, "| 是文件吗:", p.is_file())


# ---- 第 2 步：只读 a.md 这一个文件，看看能不能算出 6 行、55 个字符 ----
print("\n--- 第 2 步 ---")

with open("samples/a.md", encoding="utf-8") as f:
    text = f.read()


print(len(text.splitlines()))   # 空 1：算出「行数」
print(len(text))   # 空 2：算出「字符数」


# ---- 第 3 步：循环处理每个文件，把结果一条条装进 records ----
# p 现在是循环里「当前转到的那一个文件」，不再写死 a.md
print("\n--- 第 3 步 ---")

records = []          # 空列表：用来装每个文件的统计结果

for p in Path("samples").glob("*.md"):
    try:
        with open(p, encoding="utf-8") as f:
            text = f.read()
    except PermissionError:
        print("打不开，跳过：", p.name)
        continue
    records.append({
        "file": p.name,
        "lines": len(text.splitlines()),   # 空 3：行数（跟第 2 步空 1 一模一样的写法）
        "chars": len(text),   # 空 4：字符数（跟第 2 步空 2 一模一样的写法）
    })

print(records)


# ---- 第 4 步：把统计结果写进 summary.json ----
# 能跑到这里，说明循环全部走完，records 里装着所有成功统计的文件
print("\n--- 第 4 步 ---")

with open("summary.json", "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print("已生成 summary.json，共", len(records), "条记录")
