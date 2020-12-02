from functools import partial

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    read_line_separated_list,
    solve_and_print,
)


def solve_part1(is_valid):
    return sum(is_valid)


def solve_part2(is_valid):
    return sum(is_valid)


def read_and_parse_input1(file_name):
    return (read_line_separated_list(file_name, cast_to=_is_valid_password1),)


def read_and_parse_input2(file_name):
    return (read_line_separated_list(file_name, cast_to=_is_valid_password2),)


def _is_valid_password1(line):
    c_min, c_max, char, pw = _parse_line(line)
    return c_min <= pw.count(char) <= c_max


def _is_valid_password2(line):
    c_i, c_j, char, pw = _parse_line(line)
    return (pw[c_i] == char) != (pw[c_j] == char)


def _parse_line(line):
    rule, pw = line.split(":")
    limits, char = rule.split()
    i, j = map(int, limits.split("-"))
    return i, j, char, pw


if __name__ == "__main__":
    fetch_input_data_if_not_exists()
    _solve_and_print_a = partial(solve_and_print, read_and_parse_input1, solve_part1, "a")
    _solve_and_print_b = partial(solve_and_print, read_and_parse_input2, solve_part2, "b")

    _solve_and_print_a(DataName.SAMPLE_1)
    _solve_and_print_a(DataName.PUZZLE)

    _solve_and_print_b(DataName.SAMPLE_1)
    _solve_and_print_b(DataName.PUZZLE)
