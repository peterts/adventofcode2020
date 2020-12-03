from functools import partial

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    product,
    read_line_separated_list,
    solve_and_print,
)


def solve_part1(wood):
    return _count_trees(wood, (1, 3))


def solve_part2(wood):
    return product([_count_trees(wood, s) for s in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]])


def _count_trees(wood, steps):
    n = len(wood[0])
    r = c = 0
    count = 0
    steps_r, steps_c = steps
    while (r := r + steps_r) < len(wood):
        c = (c + steps_c) % n
        count += wood[r][c] == "#"
    return count


def read_and_parse_input(file_name):
    return (read_line_separated_list(file_name),)


if __name__ == "__main__":
    print(read_and_parse_input(DataName.SAMPLE_1))

    fetch_input_data_if_not_exists()
    _solve_and_print_a = partial(solve_and_print, read_and_parse_input, solve_part1, "a")
    _solve_and_print_b = partial(solve_and_print, read_and_parse_input, solve_part2, "b")

    _solve_and_print_a(DataName.SAMPLE_1)
    _solve_and_print_a(DataName.PUZZLE, do_submit=False)

    _solve_and_print_b(DataName.SAMPLE_1)
    _solve_and_print_b(DataName.PUZZLE, do_submit=False)
