from collections import Counter

from more_itertools import quantify

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    print_call,
    read,
    submit,
)


@print_call
def solve_part1(file_name):
    total = 0
    for answers in read(file_name).split("\n\n"):
        total += len(set(answers.replace("\n", "")))
    return total


@print_call
def solve_part2(file_name):
    total_all_in_group_answered_yes = 0
    for answers in read(file_name).split("\n\n"):
        questions_answered_yes = Counter()

        for answers_from_person in (answers_per_person := answers.split("\n")) :
            questions_answered_yes.update(answers_from_person)

        for v in questions_answered_yes.values():
            total_all_in_group_answered_yes += v == len(answers_per_person)

    return total_all_in_group_answered_yes


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    solve_part1(DataName.SAMPLE_1)
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    solve_part2(DataName.SAMPLE_1)
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
