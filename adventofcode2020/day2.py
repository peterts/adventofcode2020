from more_itertools import quantify

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    pattern_extract,
    print_call,
    read_line_separated_list,
    submit,
)


@print_call
def solve_part1(file_name):
    return quantify(read_line_separated_list(file_name), pred=_is_valid_password1)


@print_call
def solve_part2(file_name):
    return quantify(read_line_separated_list(file_name), pred=_is_valid_password2)


def _is_valid_password1(line):
    c_min, c_max, char, pw = _parse_line(line)
    return c_min <= pw.count(char) <= c_max


def _is_valid_password2(line):
    c_i, c_j, char, pw = _parse_line(line)
    return (pw[c_i] == char) != (pw[c_j] == char)


def _parse_line(line):
    return pattern_extract("(\d+)-(\d+) (\w):( \w+)", line, int, int, str, str)


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    solve_part1(DataName.SAMPLE_1)
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    solve_part2(DataName.SAMPLE_1)
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
