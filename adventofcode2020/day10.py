from collections import Counter, defaultdict
from itertools import islice

from cachetools import cached

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    print_call,
    product,
    read_line_separated_list,
    submit,
)


@print_call
def solve_part1(file_name):
    diff_counts = Counter(_read_and_compute_diffs(file_name))
    return diff_counts[1] * diff_counts[3]


@print_call
def solve_part2(file_name):
    diffs = tuple(_read_and_compute_diffs(file_name))
    all_n_combos_less_than_3 = []
    i = 0
    while i < len(diffs):
        j = i + 1
        while j < len(diffs) and diffs[j] != 3:
            j += 1
        all_n_combos_less_than_3.append(n_combos_less_than_3(diffs[i:j]))
        i = j
    return product(all_n_combos_less_than_3)


def _read_and_compute_diffs(file_name):
    jolts = sorted(read_line_separated_list(file_name, int))
    jolts = [0, *jolts, jolts[-1] + 3]
    diffs = []
    for x, y in zip(jolts, jolts[1:]):
        diffs.append(y - x)
    return diffs


@cached(cache={}, key=lambda x, i=0: x)
def n_combos_less_than_3(x, i=0):
    if i == len(x) - 1:
        return 1
    count = n_combos_less_than_3(x, i + 1)
    if x[i] + x[i + 1] <= 3:
        x_reduced = (*islice(x, i), x[i] + x[i + 1], *islice(x, i + 2, None))
        count += n_combos_less_than_3(x_reduced, i)
    return count


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 35
    assert solve_part1(DataName.SAMPLE_2) == 220
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_1) == 8
    assert solve_part2(DataName.SAMPLE_2) == 19208
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
