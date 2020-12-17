from collections import defaultdict
from itertools import product

from adventofcode2020.utils import (
    DataName,
    add_tuples,
    count_neighbors,
    fetch_input_data_if_not_exists,
    print_call,
    read_line_separated_list,
    submit,
)


@print_call
def solve_part1(file_name):
    return _solve(file_name, 1)


@print_call
def solve_part2(file_name):
    return _solve(file_name, 2)


def _solve(file_name, n_extra_dim):
    board, dimensions = _read_and_parse_board(file_name, n_extra_dim)

    for _ in range(6):
        dimensions = _increase_dimensions(dimensions)
        updated_board = defaultdict(lambda: ".")
        for pos in _iterate_dimensions(dimensions):
            updated_board[pos] = _get_new_state(board, pos)
        board = updated_board

    return "".join(board.values()).count("#")


def _iterate_dimensions(dimensions):
    return product(*(range(i, j) for i, j in dimensions))


def _increase_dimensions(dimensions):
    return [add_tuples(dim, (-1, 1)) for dim in dimensions]


def _read_and_parse_board(file_name, n_extra_dim):
    board = read_line_separated_list(file_name)
    parsed_board = defaultdict(lambda: ".")
    pos_extra_dim = tuple(0 for _ in range(n_extra_dim))
    for r, row in enumerate(board):
        for c, char in enumerate(row):
            parsed_board[(r, c, *pos_extra_dim)] = char
    return parsed_board, [
        (0, len(board)),
        (0, len(board[0])),
        *((0, 1) for _ in range(n_extra_dim)),
    ]


def _get_new_state(board, pos):
    nb_counts = count_neighbors(board, pos)
    if board[pos] == "#":
        if 2 <= nb_counts["#"] <= 3:
            return "#"
        return "."
    if nb_counts["#"] == 3:
        return "#"
    return "."


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 112
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_1) == 848
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
