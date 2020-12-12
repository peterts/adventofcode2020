from collections import Counter, defaultdict
from itertools import combinations, product, starmap

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    print_call,
    read_line_separated_list,
    submit,
)


@print_call
def solve_part1(file_name):
    board, n_rows, n_cols = _read_and_parse_board(file_name)
    step = 0
    while 1:
        updated_board = defaultdict(lambda: ".")
        for r in range(n_rows):
            for c in range(n_cols):
                updated_board[(r, c)] = _get_new_state(board, r, c)
        if (board_str := _board_to_str(board, n_rows, n_cols)) == _board_to_str(
            updated_board, n_rows, n_cols
        ):
            break
        board = updated_board
        step += 1
    return Counter(board_str)["#"]


def _get_new_state(board, r, c):
    n_occupied = 0
    for dr, dc in product((0, 1, -1), repeat=2):
        if 0 == dr == dc:
            continue
        r2, c2 = r + dr, c + dc
        if board[(r2, c2)] == "#":
            n_occupied += 1
        if n_occupied == 4:
            break
    if board[(r, c)] == "L" and n_occupied == 0:
        return "#"
    if board[(r, c)] == "#" and n_occupied == 4:
        return "L"
    return board[(r, c)]


def _board_to_str(board, n_rows, n_cols):
    board_str = ""
    for r in range(n_rows):
        row = ""
        for c in range(n_cols):
            row += board.get((r, c), ".")
        board_str += row + "\n"
    return board_str


def _read_and_parse_board(file_name):
    board = read_line_separated_list(file_name)
    parsed_board = defaultdict(lambda: ".")
    for r, row in enumerate(board):
        for c, char in enumerate(row):
            parsed_board[(r, c)] = char
    return parsed_board, len(board), len(board[0])


@print_call
def solve_part2(file_name):
    board = read_line_separated_list(file_name)
    n_rows, n_cols = len(board), len(board[0])
    while 1:
        board_str = "\n".join(board)

        updated_board = []
        for r in range(n_rows):
            row = ""
            for c in range(n_cols):
                row += _get_new_state2(board, r, c, n_rows, n_cols)
            updated_board.append(row)

        if board_str == "\n".join(updated_board):
            break

        board = updated_board

    return Counter(board_str)["#"]


def _get_new_state2(board, r, c, n_rows, n_cols):
    n_occupied = 0
    for dr, dc in filter(lambda d: d != (0, 0), product((0, 1, -1), repeat=2)):
        n = 1
        while (-1 < (r + dr * n) < n_rows) and (-1 < (c + dc * n) < n_cols):
            char = board[r + dr * n][c + dc * n]
            if char == "#":
                n_occupied += 1
                break
            elif char != ".":
                break
            n += 1
    if board[r][c] == "L" and n_occupied == 0:
        return "#"
    if board[r][c] == "#" and n_occupied >= 5:
        return "L"
    return board[r][c]


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 37
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_1) == 26
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
