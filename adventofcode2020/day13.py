from more_itertools import flatten, unzip

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    multiply,
    pattern_extract_all,
    print_call,
    read_line_separated_list,
    submit,
)


@print_call
def solve_part1(file_name):
    schedule = read_line_separated_list(file_name)
    earlist_ts = int(schedule[0])
    buses = list(flatten(pattern_extract_all("(\d+)", schedule[1], int)))

    ts = earlist_ts
    while 1:
        for b in buses:
            if ts % b == 0:
                return (ts - earlist_ts) * b
        ts += 1


@print_call
def solve_part2(file_name):
    buses = read_line_separated_list(file_name)[1].split(",")
    modulus, remainders = map(list, unzip((int(x), -i) for i, x in enumerate(buses) if x != "x"))
    return chinese_remainder(modulus, remainders)


# Source: https://fangya.medium.com/chinese-remainder-theorem-with-python-a483de81fbb8
def chinese_remainder(modulus, remainders):
    prod = multiply(modulus)
    residual = 0
    for m, r in zip(modulus, remainders):
        residual += r * mul_inv(p := prod // m, m) * p
    return residual % prod


# Source: https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python/4798776
def mul_inv(a, b):
    return pow(a, -1, b)


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 295
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_1) == 1068781
    assert solve_part2(DataName.SAMPLE_2) == 1261476
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
