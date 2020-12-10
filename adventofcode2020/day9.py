from itertools import accumulate, combinations

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    print_call,
    read_line_separated_list,
    submit,
)


@print_call
def solve_part1(file_name, prev_n=25):
    numbers = read_line_separated_list(file_name, int)
    return _first_with_no_combo_in_prev_n(numbers, prev_n)


@print_call
def solve_part2(file_name, prev_n=25):
    numbers = read_line_separated_list(file_name, int)
    n = _first_with_no_combo_in_prev_n(numbers, prev_n)
    i, j = _find_contiguous_sum(numbers, n)
    return max(numbers[i:j]) + min(numbers[i:j])


def _first_with_no_combo_in_prev_n(numbers, prev_n):
    i = 0
    while 1:
        n = numbers[prev_n + i]
        if not _any_combination(numbers[i : prev_n + i], 2, n):
            return n
        i += 1


def _any_combination(values, combo_length, n):
    for combo in combinations(values, combo_length):
        if sum(combo) == n:
            return True
    return False


def _find_contiguous_sum(numbers, n):
    acc = list(accumulate(numbers))
    acc.append(0)  # acc[-1] => 0
    for i in range(len(numbers)):
        for j in range(i, len(numbers)):
            if (s := acc[j] - acc[i - 1]) == n:
                return i, j
            if s > n:
                break


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    solve_part1(DataName.SAMPLE_1, 5)
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    solve_part2(DataName.SAMPLE_1, 5)
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
