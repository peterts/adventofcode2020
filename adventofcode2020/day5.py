from math import floor

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    print_call,
    read_line_separated_list,
    submit,
)


@print_call
def solve_part1(file_name):
    return max(read_line_separated_list(file_name, cast_to=compute_seat_id))


@print_call
def solve_part2(file_name):
    seats = sorted(read_line_separated_list(file_name, cast_to=compute_seat_id))
    for x, y in zip(seats, seats[1:]):
        if y != x + 1:
            return x + 1
    return -1


def compute_seat_id(instructions):
    row = search(0, 127, instructions[:7], "F")
    col = search(0, 7, instructions[-3:], "L")
    return row * 8 + col


def search(lo, hi, instructions, down):
    for x in instructions[:-1]:
        m = floor((lo + hi) / 2)
        if x == down:
            hi = m
        else:
            lo = m + 1
    return lo if instructions[-1] == down else hi


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
