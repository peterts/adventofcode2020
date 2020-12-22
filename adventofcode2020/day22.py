from collections import defaultdict
from itertools import starmap

from adventofcode2020.utils import (
    DataName,
    a_is_subset_of_b,
    fetch_input_data_if_not_exists,
    multiply,
    pattern_extract,
    print_call,
    read,
    read_line_separated_list,
    submit,
)


@print_call
def solve_part1(file_name):
    cards = read(file_name).split("\n\n")
    player1_cards = list(map(int, cards[0].splitlines()[1:]))
    player2_cards = list(map(int, cards[1].splitlines()[1:]))

    i = 0
    while len(player1_cards) and len(player2_cards):
        if (c1 := player1_cards.pop(0)) > (c2 := player2_cards.pop(0)):
            player1_cards.extend([c1, c2])
        else:
            player2_cards.extend([c2, c1])
        i += 1

    if len(player1_cards):
        return sum(
            starmap(lambda a, b: a * b, zip(player1_cards[::-1], range(1, len(player1_cards) + 1)))
        )
    return sum(
        starmap(lambda a, b: a * b, zip(player2_cards[::-1], range(1, len(player2_cards) + 1)))
    )


@print_call
def solve_part2(file_name):
    ...


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 306
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_1) == "mxmxvkd,sqjhc,fvjkl"
    answer = solve_part2(DataName.PUZZLE)
    assert answer == "phc,spnd,zmsdzh,pdt,fqqcnm,lsgqf,rjc,lzvh"
    submit(answer, part)
