from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    increase_dimensions,
    print_call,
    read_and_parse_board,
    submit,
    update_board,
)


@print_call
def solve_part1(file_name):
    return _solve(file_name, 1)


@print_call
def solve_part2(file_name):
    return _solve(file_name, 2)


def _solve(file_name, n_extra_dim):
    board, dimensions = read_and_parse_board(file_name, n_extra_dim)

    for _ in range(6):
        dimensions = increase_dimensions(dimensions)
        updated_board = update_board(board, dimensions, _get_new_state)
        board = updated_board

    return "".join(board.values()).count("#")


def _get_new_state(state, nb_counts):
    if state == "#":
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
