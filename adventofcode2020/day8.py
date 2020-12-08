from adventofcode2020.utils import (
    DataName,
    GameConsole,
    fetch_input_data_if_not_exists,
    print_call,
    submit,
)


@print_call
def solve_part1(file_name):
    computer = GameConsole(file_name)
    computer.run()
    return computer.accumulator


@print_call
def solve_part2(file_name):
    instructions = GameConsole.read_and_parse_instructions(file_name)
    for i, (opr, val) in enumerate(instructions):
        if opr in {"jmp", "nop"}:
            _instructions = list(instructions)
            _instructions[i] = ("jmp" if opr == "nop" else "nop", val)
            computer = GameConsole(_instructions)
            computer.run()
            if computer.terminated:
                return computer.accumulator
    return -1


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
