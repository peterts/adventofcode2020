from __future__ import annotations

from dataclasses import dataclass

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    print_call,
    read,
    submit,
)


@dataclass
class Node:
    num: int
    prev: Node = None
    next: Node = None

    def set_next(self, other):
        self.next = other
        other.prev = self


@print_call
def solve_part1(file_name, iter):
    cups_dict = shuffle(file_name, iter)
    out = ""
    node = cups_dict[1]
    while (node := node.next).num != 1:
        out += str(node.num)
    return int(out)


@print_call
def solve_part2(file_name):
    cups_dict = shuffle(file_name, 10_000_000, 1_000_000)
    node = cups_dict[1]
    return node.next.num * node.next.next.num


def shuffle(file_name, iter, total=None):
    cups = list(map(int, read(file_name)))
    if total is not None:
        cups = cups + list(range(len(cups) + 1, total + 1))

    cups_dict = {}
    n = len(cups)
    for i, c1 in enumerate(cups):
        c2 = cups[(i + 1) % n]
        cups_dict.setdefault(c1, Node(c1))
        cups_dict.setdefault(c2, Node(c2))
        cups_dict[c1].set_next(cups_dict[c2])

    current_cup = cups_dict[cups[0]]
    for i in range(iter):
        cut_nums = []
        cut_end = current_cup
        for _ in range(3):
            cut_end = cut_end.next
            cut_nums.append(cut_end.num)
        cut_start = current_cup.next

        dest_cup_num = current_cup.num - 1
        while dest_cup_num < 1 or dest_cup_num in cut_nums:
            dest_cup_num = (dest_cup_num - 1) % (n + 1)
        dest_cup = cups_dict[dest_cup_num]

        current_cup.set_next(cut_end.next)
        cut_end.set_next(dest_cup.next)
        dest_cup.set_next(cut_start)

        current_cup = current_cup.next

    return cups_dict


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1, 10) == 92658374
    assert solve_part1(DataName.SAMPLE_1, 100) == 67384529
    answer = solve_part1(DataName.PUZZLE, 100)
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_1) == 149245887792
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
