from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    print_call,
    read_line_separated_list,
    submit,
)


@print_call
def solve_part1(file_name):
    lines = read_line_separated_list(file_name)
    lines = filter(lambda l: l.strip(), lines)
    cards_pk, doors_pk = map(int, lines)

    i = 1
    while transform(i, 7) != cards_pk and transform(i, 7) != doors_pk:
        i += 1

    if transform(i, 7) == cards_pk:
        return transform(i, doors_pk)
    return transform(i, cards_pk)


def transform(iter, subject_number):
    return pow(subject_number, iter, 20201227)


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 14897079
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)
