from itertools import starmap

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    print_call,
    read,
    submit,
)


@print_call
def solve_part1(file_name):
    cards = read(file_name).split("\n\n")
    player1_cards = list(map(int, cards[0].splitlines()[1:]))
    player2_cards = list(map(int, cards[1].splitlines()[1:]))

    while len(player1_cards) and len(player2_cards):
        if (c1 := player1_cards.pop(0)) > (c2 := player2_cards.pop(0)):
            player1_cards.extend([c1, c2])
        else:
            player2_cards.extend([c2, c1])

    if len(player1_cards):
        return _score(player1_cards)
    return _score(player2_cards)


def _score(cards):
    return sum(starmap(lambda a, b: a * b, zip(cards[::-1], range(1, len(cards) + 1))))


@print_call
def solve_part2(file_name):
    cards = read(file_name).split("\n\n")
    player1_cards = list(map(int, cards[0].splitlines()[1:]))
    player2_cards = list(map(int, cards[1].splitlines()[1:]))
    winner, cards = _recursive_game(player1_cards, player2_cards)
    return _score(cards)


def _recursive_game(player1_cards, player2_cards):
    memo = set()

    while (l1 := len(player1_cards)) and (l2 := len(player2_cards)):
        if (key := (tuple(player1_cards), tuple(player2_cards))) in memo:
            return 0, player1_cards
        memo.add(key)

        c1 = player1_cards.pop(0)
        c2 = player2_cards.pop(0)

        if ((l1 - 1) >= c1) and ((l2 - 1) >= c2):
            winner, _ = _recursive_game(player1_cards[:c1], player2_cards[:c2])
        else:
            winner = 0 if c1 > c2 else 1

        if winner == 0:
            player1_cards.extend([c1, c2])
        else:
            player2_cards.extend([c2, c1])

    if len(player1_cards):
        return 0, player1_cards
    return 1, player2_cards


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 306
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_1) == 291
    assert solve_part2(DataName.SAMPLE_2) == 105
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
