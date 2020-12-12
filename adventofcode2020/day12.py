from math import cos, radians, sin

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    print_call,
    read_line_separated_list,
    submit,
)


@print_call
def solve_part1(file_name):
    instructions = read_line_separated_list(file_name)
    direction = 0
    pos_y, pos_x = 0, 0

    for instruction in instructions:
        opr, val = instruction[:1], int(instruction[1:])
        if opr == "L":
            direction += val
        elif opr == "R":
            direction -= val
        elif opr == "F":
            direction_rad = radians(direction)
            pos_x += round(cos(direction_rad) * val)
            pos_y += round(sin(direction_rad) * val)
        elif opr == "N":
            pos_y += val
        elif opr == "S":
            pos_y -= val
        elif opr == "E":
            pos_x += val
        elif opr == "W":
            pos_x -= val

    return int(abs(pos_x) + abs(pos_y))


@print_call
def solve_part2(file_name):
    instructions = read_line_separated_list(file_name)
    pos_y, pos_x = 0, 0
    w_pos_y, w_pos_x = 1, 10

    def rotate(deg):
        deg_rad = radians(deg)
        return (
            round(cos(deg_rad) * w_pos_x - sin(deg_rad) * w_pos_y),
            round(sin(deg_rad) * w_pos_x + cos(deg_rad) * w_pos_y),
        )

    for instruction in instructions:
        opr, val = instruction[:1], int(instruction[1:])
        if opr == "L":
            w_pos_x, w_pos_y = rotate(val)
        elif opr == "R":
            w_pos_x, w_pos_y = rotate(-val)
        elif opr == "F":
            pos_x += w_pos_x * val
            pos_y += w_pos_y * val
        elif opr == "N":
            w_pos_y += val
        elif opr == "S":
            w_pos_y -= val
        elif opr == "E":
            w_pos_x += val
        elif opr == "W":
            w_pos_x -= val

    return int(abs(pos_x) + abs(pos_y))


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 25
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_1) == 286
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
