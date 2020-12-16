from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    print_call,
    read,
    submit,
)


@print_call
def solve(starting_numbers_str, n_iterations):
    starting_numbers = list(map(int, starting_numbers_str.split(",")))

    last_spoken = {}
    i = 1
    for x in starting_numbers:
        last_spoken[x] = (None, i)
        i += 1

    while i <= n_iterations:
        if x in last_spoken:
            a, b = last_spoken[x]
            x = 0 if a is None else b - a
        else:
            x = 0
        b = None if x not in last_spoken else last_spoken[x][1]
        last_spoken[x] = (b, i)
        i += 1

    return x


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve("0,3,6", 2020) == 436
    assert solve("1,3,2", 2020) == 1
    assert solve("2,1,3", 2020) == 10
    assert solve("2,3,1", 2020) == 78
    answer = solve(read(DataName.PUZZLE), 2020)
    submit(answer, part)

    part = "b"
    answer = solve(read(DataName.PUZZLE), 30000000)
    submit(answer, part)
