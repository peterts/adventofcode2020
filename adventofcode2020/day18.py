import re
from itertools import product

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    multiply,
    print_call,
    read_line_separated_list,
    submit,
)


def zum_or_mul(match):
    nums_str = match.group()
    return _mul(nums_str) if "*" in nums_str else _zum(nums_str)


def mul(match):
    return _mul(match.group())


def zum(match):
    return _zum(match.group())


def _mul(nums_str):
    return str(multiply(map(int, nums_str.split(" * "))))


def _zum(nums_str):
    return str(sum(map(int, nums_str.split(" + "))))


@print_call
def solve_part1(file_name):
    texts = read_line_separated_list(file_name)
    total = 0
    for line in texts:
        total += solve(line)
    return total


def solve(text):
    while "(" in text:
        text = re.sub("\(\d+(?: (?:\*|\+) \d+)+\)", sub_solve, text, count=1)
    while "*" in text or "+" in text:
        text = re.sub("\d+ (\*|\+) \d+(?: \1 \d+)*", zum_or_mul, text, count=1)
    return int(text)


def sub_solve(match):
    return str(solve(match.group()[1:-1]))


@print_call
def solve_part2(file_name):
    texts = read_line_separated_list(file_name)
    total = 0
    for line in texts:
        total += solve2(line)
    return total


def solve2(text):
    while "(" in text:
        text = re.sub("\(\d+(?: (?:\*|\+) \d+)+\)", sub_solve2, text)
    while "+" in text:
        text = re.sub("\d+(?: \+ \d+)+", zum, text)
    while "*" in text:
        text = re.sub("\d+(?: \* \d+)+", mul, text)
    return int(text)


def sub_solve2(match):
    return str(solve2(match.group()[1:-1]))


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 71
    assert solve_part1(DataName.SAMPLE_2) == 51
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_3) == 23340
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
