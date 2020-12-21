from adventofcode2020.earlyparser import EarleyParse, Grammar, Rule
from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    print_call,
    read,
    submit,
)


@print_call
def solve_part1(file_name):
    return _count_words_valid_according_to_grammar(file_name)


@print_call
def solve_part2(file_name):
    return _count_words_valid_according_to_grammar(
        file_name, ["8: 42 | 42 8", "11: 42 31 | 42 11 31"]
    )


def _count_words_valid_according_to_grammar(file_name, replace=None):
    grammar_rules, words = map(lambda x: x.splitlines(), read(file_name).split("\n\n"))
    replace = dict(map(lambda r: r.split(": "), replace)) if replace is not None else {}

    grammar = Grammar()
    for line in grammar_rules:
        lhs, rhss = line.split(": ")
        rhss = replace.get(lhs, rhss).replace('"', "")
        lhs = "S" if lhs == "0" else lhs
        for rhs in rhss.split(" | "):
            grammar.add(Rule(lhs, rhs.split()))

    def run_parse(sentence):
        parse = EarleyParse(" ".join(x for x in sentence), grammar)
        parse.parse()
        return parse.get() is not None

    return sum(map(run_parse, words))


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 2
    answer = solve_part1(DataName.PUZZLE)
    assert answer == 235
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_2) == 12
    answer = solve_part2(DataName.PUZZLE)
    assert answer == 379
    submit(answer, part)
