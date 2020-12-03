from functools import partial
from itertools import combinations

from more_itertools import first_true

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    product,
    read_line_separated_list,
    solve_and_print,
)


def product_where_sum_of_combo_equals_n(values, combo_length, n):
    return product(first_true(combinations(values, combo_length), pred=lambda c: sum(c) == n))


def solve_part1(values):
    return product_where_sum_of_combo_equals_n(values, 2, 2020)


def solve_part2(values):
    return product_where_sum_of_combo_equals_n(values, 3, 2020)


def read_and_parse_input(file_name):
    return (read_line_separated_list(file_name, int),)


if __name__ == "__main__":
    fetch_input_data_if_not_exists()
    _solve_and_print_a = partial(solve_and_print, read_and_parse_input, solve_part1, "a")
    _solve_and_print_b = partial(solve_and_print, read_and_parse_input, solve_part2, "b")

    _solve_and_print_a(DataName.SAMPLE_1)
    _solve_and_print_a(DataName.PUZZLE, submit=False)

    _solve_and_print_b(DataName.SAMPLE_1)
    _solve_and_print_b(DataName.PUZZLE, submit=False)
