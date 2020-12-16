from itertools import product

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    pattern_extract,
    print_call,
    read_line_separated_list,
    submit,
)


@print_call
def solve_part1(file_name):
    memory = {}
    mask = None

    for ins in _read_and_parse_instructions(file_name):
        name = ins[0]
        if name == "mask":
            mask = ins[1]
        else:
            adr, val = ins[1:]
            val = _to_bitstring(val)
            if mask is not None:
                val = _apply_mask(val, mask)
            memory[adr] = val

    return sum(map(lambda x: int(x, 2), memory.values()))


def _read_and_parse_instructions(file_name):
    for row in read_line_separated_list(file_name):
        res = pattern_extract("(mem)\[(\d+)\] = (\d+)", row, str, int, int)
        if res is None:
            name, val = row.split(" = ")
            yield [name, val]
        else:
            yield res


def _apply_mask(val, mask):
    res = ""
    for x, y in zip(val, mask):
        if y != "X":
            res += y
        else:
            res += x
    return "".join(res)


def _to_bitstring(num, length=36):
    return "{0:b}".format(num).zfill(length)


@print_call
def solve_part2(file_name):
    memory = {}
    mask = None

    for ins in _read_and_parse_instructions(file_name):
        name = ins[0]
        if name == "mask":
            mask = ins[1]
        else:
            adr, val = ins[1:]
            if mask is not None:
                adr = _apply_mask2(_to_bitstring(adr), mask)

            for rep in product([1, 0], repeat=adr.count("X")):
                _adr = int(_replace_floating(adr, rep), 2)
                memory[_adr] = val

    return sum(memory.values())


def _replace_floating(val, rep):
    res = ""
    i = 0
    for x in val:
        if x == "X":
            res += str(rep[i])
            i += 1
        else:
            res += x
    return res


def _apply_mask2(val, mask):
    res = ""
    for x, y in zip(val, mask):
        if y == "0":
            res += x
        elif y == "1":
            res += "1"
        elif y == "X":
            res += "X"
    return res


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 165
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_2) == 208
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
