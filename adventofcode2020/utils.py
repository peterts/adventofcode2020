import inspect
import itertools
import re
from cmath import phase
from collections import Counter
from functools import lru_cache, reduce, wraps
from math import pi, sqrt
from pathlib import Path

import aocd
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parents[1] / ".env")


YEAR = 2020
PROJECT_ROOT_PATH = Path(__file__).parents[1]


class DataName:
    SAMPLE_1 = "sample1.txt"
    SAMPLE_2 = "sample2.txt"
    SAMPLE_3 = "sample3.txt"
    PUZZLE = "puzzle.txt"


def fetch_input_data_if_not_exists():
    """
    Meant to be used from run.py within a dayX-module

    Returns:
        str: The data
    """
    day_num = _get_day_num()
    output_filepath = _create_data_dirpath(day_num) / DataName.PUZZLE
    if output_filepath.is_file():
        print("Input data already fetched")
        return
    print("Fetching input data")
    output_filepath.write_text(aocd.get_data(day=day_num, year=YEAR))


def submit(solution, part):
    aocd.submit(solution, part, day=_get_day_num(), year=YEAR)


# It's ok to use lru_cache since we will never run solving for more than a single day in one process
@lru_cache()
def _get_day_num():
    caller_filepath = _get_caller_filepath()
    if (day_num_match := re.search("day(\d+)", caller_filepath.name)) is None:
        # Will happen in e.g. debug-mode
        day_num_str = input("Could not infer day number. Which day is it?")
        print()
    else:
        day_num_str = day_num_match.group(1)
    return int(day_num_str)


def angle(v1, v2):
    ang = phase(complex(*v1)) - phase(complex(*v2))
    if ang < 0:
        return 2 * pi + ang
    return ang


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def manhattan_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)


def read_comma_separated_list(input_file_name=DataName.PUZZLE, cast_to=str):
    return _read_list(input_file_name, ",", cast_to)


def read_line_separated_list(input_file_name=DataName.PUZZLE, cast_to=str):
    return _read_list(input_file_name, "\n", cast_to)


def _read_list(input_file_name, split_char, cast_to):
    return list(map(cast_to, read(input_file_name).split(split_char)))


@lru_cache()
def read(input_file_name=DataName.PUZZLE):
    with open(_create_data_dirpath(_get_day_num()) / input_file_name) as f:
        return f.read().strip()


def print_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _kwargs_str = _dict_to_str(inspect.getcallargs(func, *args, **kwargs))
        print("---")
        print(f">> {func.__name__}({_truncate_text(_kwargs_str, 50)})")
        print(return_val := func(*args, **kwargs))
        return return_val

    return wrapper


def _dict_to_str(_dict):
    return ", ".join(itertools.starmap(lambda k, v: f"{k}={repr(v)}", _dict.items()))


def _truncate_text(text, max_len):
    if len(text) < max_len:
        return text
    return text[:max_len] + "..."


def _get_caller_filepath():
    """
    To get the file path of the caller:
    https://stackoverflow.com/questions/13699283/how-to-get-the-callers-filename-method-name-in-python

    Returns:
        pathlib.Path: The path to the caller
    """
    caller = inspect.stack()[-1]
    return Path(caller[0].f_code.co_filename)


def _create_data_dirpath(day_num):
    return PROJECT_ROOT_PATH / "data" / f"day{day_num}"


def pattern_extract(pattern, text, *types):
    if (match := re.search(pattern, text)) is None:
        return None
    return _cast_match_groups(match, types)


def pattern_extract_iter(pattern, text, *types):
    for match in re.finditer(pattern, text):
        yield _cast_match_groups(match, types)


def pattern_extract_all(pattern, text, *types):
    return list(pattern_extract_iter(pattern, text, *types))


def _cast_match_groups(match, types):
    return [t(g) for g, t in zip(match.groups(), types)]


def product(iterable):
    return reduce(lambda a, b: a * b, iterable)


class GameConsole:
    def __init__(self, instructions_or_file_name):
        if isinstance(instructions_or_file_name, str):
            instructions = self.read_and_parse_instructions(instructions_or_file_name)
        else:
            instructions = instructions_or_file_name

        self.instructions = instructions
        self.accumulator = 0
        self.pos = 0
        self.traceback = []
        self.running = True

    @staticmethod
    def read_and_parse_instructions(file_name):
        instructions = []
        for instruction in read_line_separated_list(file_name):
            opr, val = pattern_extract("(\w{3}) ((?:\+|\-)\d+)", instruction, str, int)
            instructions.append((opr, val))
        return instructions

    @property
    def instruction(self):
        if self.terminated:
            return "exit", 0
        return self.instructions[self.pos]

    @property
    def terminated(self):
        return self.pos == len(self.instructions)

    def run(self):
        while self.running:
            self.traceback.append(self.pos)
            opr, val = self.instruction
            getattr(self, opr)(val)

    def acc(self, val):
        self.accumulator += val
        self.jmp(1)

    def nop(self, _):
        self.jmp(1)

    def jmp(self, val):
        self.pos += val
        self.running = self.pos not in self.traceback

    def exit(self, _):
        self.running = False


def add_tuples(tup1, tup2):
    return tuple(i + j for i, j in zip(tup1, tup2))


def count_neighbors(board, pos):
    counts = Counter()
    for diff in itertools.product((0, 1, -1), repeat=len(pos)):
        if not any(diff):
            continue
        counts[board[add_tuples(pos, diff)]] += 1
    return counts
