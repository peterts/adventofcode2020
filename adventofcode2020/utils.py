import inspect
import re
from cmath import phase
from functools import lru_cache, reduce, wraps
from itertools import starmap
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
        return_val = func(*args, **kwargs)
        _kwargs_str = _dict_to_str(inspect.getcallargs(func, *args, **kwargs))
        print("---")
        print(f">> {func.__name__}({_truncate_text(_kwargs_str, 50)})")
        print(f"{return_val}")
        return return_val

    return wrapper


def _dict_to_str(_dict):
    return ", ".join(starmap(lambda k, v: f"{k}={repr(v)}", _dict.items()))


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
        return []
    return [t(g) for g, t in zip(match.groups(), types)]


def product(iterable):
    return reduce(lambda a, b: a * b, iterable)
