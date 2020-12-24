from __future__ import annotations

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    print_call,
    read_line_separated_list,
    submit,
    pattern_extract_all,
    add_tuples
)
from more_itertools import first
from collections import defaultdict


directions = {
    "ne": (-1, 0.5), "nw": (-1, -0.5),
    "se": (1, 0.5), "sw": (1, -0.5),
    "e": (0, 1), "w": (0, -1)
}


@print_call
def solve_part1(file_name):
    tiles = _get_start_tiles(file_name)
    return sum(tiles.values())


@print_call
def solve_part2(file_name):
    tiles = _get_start_tiles(file_name)
    _expand(tiles)
    for _ in range(100):
        next_tiles = defaultdict(lambda: False)
        for pos in set(tiles):
            state = tiles[pos]
            n_black_nb = sum(map(lambda d: tiles[add_tuples(pos, d)], directions.values()))
            if state:
                state = False if (n_black_nb == 0 or n_black_nb > 2) else True
            else:
                state = True if n_black_nb == 2 else False
            next_tiles[pos] = state
        tiles = next_tiles
        _expand(tiles)
    return sum(tiles.values())


def _expand(tiles):
    for pos in set(tiles):
        for d in directions.values():
            tiles[add_tuples(pos, d)]  # Simply visit the position to add it as a key


def _get_start_tiles(file_name):
    tiles = defaultdict(lambda: False)
    for line in read_line_separated_list(file_name):
        pos = (0, 0)
        for ins in map(first, pattern_extract_all("(se|sw|ne|nw|e|w)", line, str)):
            pos = add_tuples(pos, directions[ins])
        tiles[pos] = not tiles[pos]
    return tiles


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 10
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_1) == 2208
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
