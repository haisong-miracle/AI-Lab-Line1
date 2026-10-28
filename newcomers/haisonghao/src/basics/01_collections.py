"""Task 07 练习一：四大集合类型综合练习。

覆盖 list / dict / tuple / set 的增删改查、切片、推导式与集合运算。

运行：python 01_collections.py
自检：python ../selfcheck.py
"""
import string

TEXT = (
    "Docker packages an application with its dependencies into a single "
    "image. An image is a read only template, and a container is a running "
    "instance of that image. Images are built in layers, and every layer is "
    "cached, so a new build only rebuilds the layers that changed. Pull an "
    "image once, run it many times, and the same image keeps the environment "
    "stable across machines."
)

TAG_A = {"docker", "linux", "git", "python", "shell"}
TAG_B = {"python", "numpy", "linux", "pandas", "docker"}


def clean_words(text: str) -> list[str]:
    """把文本切成小写单词列表，并去掉标点。

    规则：
    - 全部转小写
    - 去掉 , . ! ? ; : " ' ( ) 等标点
    - 按空白切分，不保留空字符串

    例如 "Hello, Docker!" -> ["hello", "docker"]
    """
    table = str.maketrans("", "", string.punctuation)
    cleaned = text.lower().translate(table)
    return cleaned.split()


def word_freq(words: list[str]) -> dict[str, int]:
    """统计词频，返回 {单词: 出现次数}。

    要求：所有次数之和等于 len(words)。
    提示：dict.get(word, 0) 可以省掉 if 判断。
    """
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """取出现次数最多的前 n 个词，返回 [(单词, 次数), ...]。

    排序规则：次数降序；次数相同按字母升序。
    提示：sorted 的 key 可以返回元组，逗号后面再写次要条件。
    """
    # freq.items() 把字典变成一对对的 (单词, 次数)
    # key 返回元组：-kv[1] 让次数降序，次数相同时再比 kv[0] 单词升序
    ranked = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked[:n]


def middle_slice(
    words: list[str], start: int = 10, stop: int = 20
) -> list[str]:
    """用切片返回 words[start:stop]。"""
    # 切片包左不包右：start 在内，stop 不在内
    return words[start:stop]


def set_operations(a: set[str], b: set[str]) -> dict[str, set[str]]:
    """返回两个集合的交、并、差、对称差。

    键名固定为 and / or / only_a / xor。
    """
    return {
        "and": a & b,  # 交集：两边都有的
        "or": a | b,  # 并集：合在一起并自动去重
        "only_a": a - b,  # 差集：只在 a 里的
        "xor": a ^ b,  # 对称差：只属于其中一边的
    }


def long_words(words: list[str], min_len: int = 5) -> list[str]:
    """用列表推导式返回长度 >= min_len 的词，保持原顺序。"""
    # 推导式读法：对 words 里每个 word，若长度达标就收进新列表
    return [word for word in words if len(word) >= min_len]


if __name__ == "__main__":
    all_words = clean_words(TEXT)
    freq = word_freq(all_words)
    print("单词总数：", len(all_words))
    print("不同单词数：", len(set(all_words)))
    print("前 5 高频：", top_n(freq, 5))
    print("第 10~20 个词：", middle_slice(all_words))
    print("长度 >= 5 的词：", long_words(all_words))
    print("集合运算：", set_operations(TAG_A, TAG_B))
