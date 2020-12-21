from itertools import product

import numpy as np

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    multiply,
    pattern_extract_all,
    print_call,
    read,
    submit,
)


@print_call
def solve_part1(file_name):
    _, nearby_tickets, rules = _read_and_parse_data(file_name)

    invalid = []
    for ticket in nearby_tickets:
        for value in ticket:
            for rule in rules:
                if _is_within_limits(value, rule):
                    break
            else:
                invalid.append(value)

    return sum(invalid)


@print_call
def solve_part2(file_name, prefix):
    your_ticket, nearby_tickets, rules = _read_and_parse_data(file_name)

    drop_tickets = []
    for ticket_num, ticket in enumerate(nearby_tickets):
        for value in ticket:
            for rule in rules:
                if _is_within_limits(value, rule):
                    break
            else:
                drop_tickets.append(ticket_num)

    nearby_tickets = [t for i, t in enumerate(nearby_tickets) if i not in drop_tickets]

    n = len(rules)
    all_valid = np.zeros((n, n))
    for pos in range(n):
        for rule_num, rule in enumerate(rules):
            all_valid[pos][rule_num] = all(
                _is_within_limits(ticket[pos], rule) for ticket in nearby_tickets
            )
    valid_in_pos = all_valid.sum(axis=0)

    positions = [None] * n
    for _ in range(n):
        i = valid_in_pos.argmin()
        j = np.argmax(all_valid[:, i])
        valid_in_pos[i] = np.inf
        valid_in_pos -= all_valid[j]
        all_valid[j] = -1
        positions[j] = i

    prod = []
    for pos, rule_num in enumerate(positions):
        if rules[rule_num][0].startswith(prefix):
            prod.append(your_ticket[pos])

    return multiply(prod)


def _read_and_parse_data(file_name):
    data = read(file_name).split("\n\n")
    your_ticket = _parse_ticket_str(data[1].split("\n")[1])
    nearby_tickets = list(map(_parse_ticket_str, data[2].split("\n", maxsplit=1)[1].splitlines()))

    rules = pattern_extract_all(
        "([a-z ]+): (\d+)\-(\d+) or (\d+)\-(\d+)", data[0], str, int, int, int, int
    )
    return your_ticket, nearby_tickets, rules


def _parse_ticket_str(ticket_str):
    return list(map(int, ticket_str.split(",")))


def _is_within_limits(value, rule):
    _, x1, x2, y1, y2 = rule
    if not (x1 <= value <= x2 or y1 <= value <= y2):
        return False
    return True


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 71
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_2, "class") == 12
    answer = solve_part2(DataName.PUZZLE, "departure")
    submit(answer, part)
