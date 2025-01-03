from time import localtime
from time import strftime


def now_formatter(formator="t"):
    """
    Formats the current time according to the specified format.

    Args:
        formator (str, optional): The format to use. Defaults to "t".
            "s" : 20220730121212
            "t" : 2022-07-30 12:12:12
            "d" : 2022-07-30

    Returns:
        str: The formatted current time string.
    """

    formats = {
        "s": "%Y%m%d%H%M%S",
        "t": "%Y-%m-%d %H:%M:%S",
        "d": "%Y-%m-%d",
    }
    formator = formats.get(formator, formator)
    return strftime(formator, localtime())


def test_now_formatter():
    """测试 now_formatter 函数的各种格式输出"""
    # 测试默认格式 't'
    assert len(now_formatter()) == 19
    assert now_formatter().count("-") == 2
    assert now_formatter().count(":") == 2

    # 测试 's' 格式
    assert len(now_formatter("s")) == 14
    assert now_formatter("s").isdigit()

    # 测试 'd' 格式
    assert len(now_formatter("d")) == 10
    assert now_formatter("d").count("-") == 2

    # 测试无效格式
    assert now_formatter("invalid") == "invalid"

    print("所有测试通过!")


if __name__ == "__main__":
    test_now_formatter()
