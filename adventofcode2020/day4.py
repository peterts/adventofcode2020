from functools import partial
from typing import Literal

from more_itertools import quantify
from pydantic import BaseModel, ValidationError, conint, constr, validator

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    pattern_extract_all,
    print_call,
    read,
    submit,
)

REQUIRED_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}


class PassportA(BaseModel):
    byr: str
    iyr: str
    eyr: str
    hgt: str
    hcl: str
    ecl: str
    pid: str
    cid: str = ""


class PassportB(BaseModel):
    byr: conint(ge=1920, le=2002)
    iyr: conint(ge=2010, le=2020)
    eyr: conint(ge=2020, le=2030)
    hgt: constr(regex="^\d+(?:cm|in)")
    hcl: constr(regex="^#[a-z0-9]{6}$")
    ecl: Literal["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    pid: constr(regex="^\d{9}$")
    cid: str = ""

    @validator("hgt")
    def validate_height(cls, height):
        num, unit = int(height[:-2]), height[-2:]
        if unit == "cm" and (num < 150 or num > 195):
            raise ValueError
        if unit == "in" and (num < 59 or num > 75):
            raise ValueError
        return height


def _validate_with_model(model, data):
    try:
        model(**data)
        return True
    except ValidationError:
        return False


@print_call
def solve_part1(file_name):
    passports = read(file_name).split("\n\n")
    return quantify(map(_parse_passport, passports), pred=partial(_validate_with_model, PassportA))


@print_call
def solve_part2(file_name):
    passports = read(file_name).split("\n\n")
    return quantify(map(_parse_passport, passports), pred=partial(_validate_with_model, PassportB))


def _parse_passport(passport):
    return dict(pattern_extract_all("([a-z]{3}):(\S+)", passport, str, str))


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    solve_part1(DataName.SAMPLE_1)
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    solve_part2(DataName.SAMPLE_1)
    solve_part2(DataName.SAMPLE_2)
    solve_part2(DataName.SAMPLE_3)
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
