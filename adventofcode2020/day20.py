from itertools import product
from math import sqrt

import numpy as np
from more_itertools import unzip

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    multiply,
    print_call,
    read,
    submit,
)


@print_call
def solve_part1(file_name):
    tiles = _read_tiles(file_name)
    _, tile_nums = next(_get_tile_positions(tiles))
    n2 = len(tiles)
    n = int(sqrt(n2))
    return multiply(map(lambda i: tiles[tile_nums[i]][0], (0, n - 1, n2 - n, n2 - 1)))


def _read_tiles(file_name):
    def _get_id_and_tile(block):
        _id, *tile = block.split("\n")
        return int(_id[len("Tile ") : -1]), np.asarray([[x for x in row] for row in tile])

    return list(map(_get_id_and_tile, read(file_name).split("\n\n")))


@print_call
def solve_part2(file_name):
    tiles = _read_tiles(file_name)

    mask = seamonster_mask()
    n_in_mask = mask.sum()
    h, w = mask.shape

    for tiles_positioned, _ in _get_tile_positions(tiles):
        n = int(sqrt(len(tiles_positioned)))

        image = np.vstack(
            [
                np.hstack([tiles_positioned[r * n + c][1:-1, 1:-1] for c in range(n)])
                for r in range(n)
            ]
        )

        image_bool = image == "#"

        positions = []
        for i, j in product(range(image.shape[0] - h), range(image.shape[1] - w)):
            image_slice = image_bool[i : i + h, j : j + w]
            if (image_slice & mask).sum() == n_in_mask:
                positions.append((i, j))

        if positions:
            for i, j in positions:
                image_bool[i : i + h, j : j + w] = image_bool[i : i + h, j : j + w] & ~mask
            return image_bool.sum()

    return None


def seamonster_mask():
    seamonster_str = """
                      # 
    #    ##    ##    ###
     #  #  #  #  #  #   
    """
    seamonster_lines = list(
        map(lambda line: line[4:], filter(lambda x: x.strip(), seamonster_str.splitlines()))
    )
    return np.asarray([[x == "#" for x in line] for line in seamonster_lines])


def _get_tile_positions(tiles):
    _, tiles = unzip(tiles)
    tiles = list(tiles)
    n2 = len(tiles)
    n = int(sqrt(n2))

    def index(r, c):
        if r < 0:
            r = n + r
        if c < 0:
            c = n + c
        return r * n + c

    option_per_tile = list(map(_get_all_orientations, tiles))
    assert all(len(o) == 8 for o in option_per_tile)

    q = []
    for tile_num in range(n2):
        for orientation in range(8):
            q.append(((tile_num,), (orientation,)))

    while q:
        tile_positions, tile_orientations = q.pop()

        if len(tile_positions) == n2:
            tiles_positioned = [
                option_per_tile[tile_num][orientation]
                for tile_num, orientation in zip(tile_positions, tile_orientations)
            ]
            yield tiles_positioned, tile_positions

        next_num = len(tile_positions)
        r, c = next_num // n, next_num % n
        above, left = None, None
        if r:
            i = index(r - 1, c)
            above = option_per_tile[tile_positions[i]][tile_orientations[i]]
        if c:
            i = index(r, c - 1)
            left = option_per_tile[tile_positions[i]][tile_orientations[i]]

        for tile_num in filter(lambda k: k not in tile_positions, range(n2)):
            for orientation, tile in enumerate(option_per_tile[tile_num]):
                if above is not None and (tile[0] != above[-1]).any():
                    continue
                if left is not None and (tile[:, 0] != left[:, -1]).any():
                    continue
                q.append((tile_positions + (tile_num,), tile_orientations + (orientation,)))


class HashableArray:
    def __init__(self, values):
        self.values = values

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.values))


def _get_all_orientations(tile):
    orientations = set()
    for i in range(4):
        tile = np.rot90(tile)
        orientations.add(HashableArray(tile))
        orientations.add(HashableArray(np.fliplr(tile)))
        orientations.add(HashableArray(np.flipud(tile)))
    return list(map(lambda arr: arr.values, orientations))


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 20899048083289
    answer = solve_part1(DataName.PUZZLE)
    assert answer == 54755174472007
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_1) == 273
    answer = solve_part2(DataName.PUZZLE)
    assert answer == 1692
    submit(answer, part)
