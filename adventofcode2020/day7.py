from collections import defaultdict

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    pattern_extract_all,
    print_call,
    read_line_separated_list,
    submit,
)


@print_call
def solve_part1(file_name):
    text = read_line_separated_list(file_name)
    contained_by = defaultdict(list)
    for line in text:
        head, tail = line.split(" bags contain ")
        for rule in pattern_extract_all("\d+ (\w+ \w+) bags?", tail, str):
            contained_by[rule[0]].append(head)

    seen = set()
    q = ["shiny gold"]
    while q:
        node = q.pop()
        seen.add(node)
        for other_node in contained_by.get(node, []):
            if other_node not in seen:
                q.append(other_node)

    return len(seen) - 1


@print_call
def solve_part2(file_name):
    text = read_line_separated_list(file_name)

    contains = defaultdict(list)
    for line in text:
        head, tail = line.split(" bags contain ")
        contains[head].extend(pattern_extract_all("(\d+) (\w+ \w+) bags?", tail, int, str))

    return _cost_of_bag("shiny gold", 1, contains) - 1


def _cost_of_bag(bag_name, count, contains):
    total_for_children = 0
    for child_count, child_node in contains[bag_name]:
        total_for_children += _cost_of_bag(child_node, child_count, contains)
    return total_for_children * count + count


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    solve_part1(DataName.SAMPLE_1)
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    solve_part2(DataName.SAMPLE_1)
    solve_part2(DataName.SAMPLE_2)
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
