"""Task 07 练习二：流程控制与格式化输出。

STUDENTS 中 None 表示缺考，-1 表示提前结束录入。

运行：python 02_control_flow.py
自检：python ../selfcheck.py
"""

STUDENTS: list[tuple[str, float | None]] = [
    ("张伟", 92),
    ("李静", 78),
    ("王强", None),
    ("赵敏", 65),
    ("陈晨", 88),
    ("刘洋", -1),
    ("孙悦", 55),
]


def grade_of(score: float) -> str:
    """分数转等级：>=90 A，>=80 B，>=70 C，>=60 D，其余 F。"""
    # 从高往低判断：先满足大门槛，剩下的自然落到下一档
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def summarize(students: list[tuple[str, float | None]]) -> dict:
    """汇总成绩。

    规则：
    - 分数为 -1 时立刻 break，它和它之后的记录都不处理
    - 分数为 None 时计入 absent，然后 continue
    - 其余计入 total，其中 >=60 的计入 pass_count

    返回 dict 的键：
    total / absent / pass_count / pass_rate / grades / records
    """
    total = 0
    absent = 0
    pass_count = 0
    grades: dict[str, int] = {}
    records = []
    for name, score in students:
        if score == -1:
            break  # 哨兵值：它和它之后全部不处理，直接跳出循环
        if score is None:
            absent += 1
            continue  # 缺考：只记人数，跳过后面的统计
        grade = grade_of(score)
        grades[grade] = grades.get(grade, 0) + 1
        records.append((name, score, grade))
        total += 1
        if score >= 60:
            pass_count += 1
    # 注意 total 为 0 时不能做除法，用条件表达式兜底
    rate = pass_count / total if total else 0.0
    return {
        "total": total,
        "absent": absent,
        "pass_count": pass_count,
        "pass_rate": rate,
        "grades": grades,
        "records": records,
    }


def sum_until(threshold: int = 1000) -> int:
    """用 while 求最小 n，使 1+2+...+n > threshold。"""
    total = 0
    n = 0
    # 还没超过门槛就继续加；一旦超过，循环结束，n 就是答案
    while total <= threshold:
        n += 1
        total += n
    return n


def format_table(records: list[tuple[str, float, str]]) -> str:
    """把 (姓名, 分数, 等级) 列表排成对齐的多行表格字符串。

    要求：
    - 第一行表头：姓名 / 分数 / 等级
    - 第二行分隔线（如 "-" * 20）
    - 数据行：姓名左对齐 8，分数右对齐 6 且保留 1 位小数，等级居中 4

    提示：f"{name:<8}{score:>6.1f}{grade:^4}"
    """
    # f-string 的对齐符号：< 左对齐  > 右对齐  ^ 居中，数字是占位宽度
    header = f"{'姓名':<8}{'分数':>6}{'等级':^4}"
    lines = [header, "-" * 20]
    for name, score, grade in records:
        lines.append(f"{name:<8}{score:>6.1f}{grade:^4}")
    # 用换行符把所有行拼成一整个字符串交出去
    return "\n".join(lines)


if __name__ == "__main__":
    result = summarize(STUDENTS)
    print("有效成绩：", result.get("total"))
    print("缺考人数：", result.get("absent"))
    print("及格率：", result.get("pass_rate"))
    print(format_table(result.get("records", [])))
    print("sum_until(1000) =", sum_until(1000))
