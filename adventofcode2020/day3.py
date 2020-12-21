from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    multiply,
    print_call,
    read_line_separated_list,
    submit,
)


@print_call
def solve_part1(file_name):
    wood = read_line_separated_list(file_name)
    return _count_trees(wood, (1, 3))


@print_call
def solve_part2(file_name):
    wood = read_line_separated_list(file_name)
    return multiply([_count_trees(wood, s) for s in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]])


def _count_trees(wood, steps):
    n = len(wood[0])
    r = c = 0
    count = 0
    steps_r, steps_c = steps
    while (r := r + steps_r) < len(wood):
        c = (c + steps_c) % n
        count += wood[r][c] == "#"
    return count


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
