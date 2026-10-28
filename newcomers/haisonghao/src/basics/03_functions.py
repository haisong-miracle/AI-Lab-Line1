"""Task 07 练习三：函数设计。

覆盖默认参数、*args、**kwargs、闭包与作用域。

运行：python 03_functions.py
自检：python ../selfcheck.py
"""

TOTAL_CALLS = 0


def stats(*args: float) -> dict:
    """返回 {"count", "sum", "mean", "min", "max"}。

    没有参数时，所有值都返回 0（避免除以 0）。
    """
    # args 是一个元组，装着所有按位置传进来的参数
    if not args:  # 空元组按布尔值看是 False
        return {"count": 0, "sum": 0, "mean": 0, "min": 0, "max": 0}
    return {
        "count": len(args),
        "sum": sum(args),
        "mean": sum(args) / len(args),
        "min": min(args),
        "max": max(args),
    }


def build_report(*args: float, **kwargs) -> str:
    """生成多行文本报告。

    kwargs：
    - title: 标题，默认 "成绩报告"
    - precision: 平均分保留小数位，默认 2
    - show_list: 是否逐行列出每个值，默认 False

    返回的字符串里必须包含标题和平均分（按 precision 格式化）。
    """
    # kwargs 是一个字典，装着所有"名字=值"形式传进来的配置
    title = kwargs.get("title", "成绩报告")
    precision = kwargs.get("precision", 2)
    show_list = kwargs.get("show_list", False)
    lines = [title, "-" * 20]
    if args:
        mean = sum(args) / len(args)
        lines.append(f"数量：{len(args)}")
        # 精度是变量时用嵌套大括号：.{precision}f 会展开成 .2f 或 .1f
        lines.append(f"平均分：{mean:.{precision}f}")
    else:
        lines.append("没有数据")
    if show_list:
        for index, value in enumerate(args, start=1):
            lines.append(f"第{index}项：{value}")
    return "\n".join(lines)


def add_item(item, bucket=None):
    """把 item 追加到 bucket 并返回 bucket。

    注意：默认值不能写成 []，否则多次调用会共享同一个列表。
    """
    # 可变默认值陷阱的正确解法：占位用 None，进函数再新建
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


def make_counter():
    """返回一个闭包：每调用一次返回值加 1，第一次调用返回 1。"""
    count = 0  # 这个变量被内层函数"记住"了，这就是闭包

    def counter():
        nonlocal count  # 声明：我要改的是外层的 count，不是新建一个
        count += 1
        return count

    # 返回函数本身（不带括号），调用方拿到的是"机器"而不是"结果"
    return counter


def bump() -> int:
    """把全局 TOTAL_CALLS 加 1 并返回新值（需要 global 关键字）。"""
    global TOTAL_CALLS  # 声明：接下来改的是模块顶层那个 TOTAL_CALLS
    TOTAL_CALLS += 1
    return TOTAL_CALLS


if __name__ == "__main__":
    print("stats:", stats(88, 92, 79))
    print(build_report(88, 92, 79, title="期末成绩", precision=1))
    print("add_item:", add_item("apple"))
    counter = make_counter()
    print("counter:", counter(), counter(), counter())
    print("bump:", bump(), "TOTAL_CALLS =", TOTAL_CALLS)
