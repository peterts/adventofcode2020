from functools import partial
from itertools import combinations

from more_itertools import first_true

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    print_call,
    product,
    read_line_separated_list,
    submit,
)


@print_call
def product_where_sum_of_combo_equals_n(combo_length, n, file_name):
    values = read_line_separated_list(file_name, int)
    return product(first_true(combinations(values, combo_length), pred=lambda c: sum(c) == n))


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    solve_part1 = partial(product_where_sum_of_combo_equals_n, 2, 2020)
    solve_part2 = partial(product_where_sum_of_combo_equals_n, 3, 2020)

    part = "a"
    solve_part1(DataName.SAMPLE_1)
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    solve_part2(DataName.SAMPLE_1)
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
