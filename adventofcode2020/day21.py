import re
from collections import Counter, defaultdict
from itertools import product
from pprint import pprint

from more_itertools import unzip

from adventofcode2020.utils import (
    DataName,
    fetch_input_data_if_not_exists,
    multiply,
    pattern_extract,
    print_call,
    read_line_separated_list,
    submit,
)


@print_call
def solve_part1(file_name):
    allergens = defaultdict(set)
    ingredients = defaultdict(set)

    for i, line in enumerate(read_line_separated_list(file_name)):
        _ingredients, _allergens = pattern_extract(
            "(\w+(?: \w+)+) \(contains (\w+(?:, \w+)*)\)", line, str, str
        )
        for ing in _ingredients.split():
            ingredients[ing].add(i)
        for al in _allergens.split(", "):
            allergens[al].add(i)

    total = 0
    for ing, ing_in_recipe in ingredients.items():
        for al_in_recipe in allergens.values():
            if a_is_subset_of_b(al_in_recipe, ing_in_recipe):
                break
        else:
            total += len(ing_in_recipe)
    return total


def a_is_subset_of_b(a, b):
    return all(x in b for x in a)


@print_call
def solve_part2(file_name):
    allergens = defaultdict(set)
    ingredients = defaultdict(set)
    possible_ing_per_allergen = defaultdict(set)

    for i, line in enumerate(read_line_separated_list(file_name)):
        _ingredients, _allergens = pattern_extract(
            "(\w+(?: \w+)+) \(contains (\w+(?:, \w+)*)\)", line, str, str
        )
        for ing in _ingredients.split():
            ingredients[ing].add(i)
        for al in _allergens.split(", "):
            allergens[al].add(i)
            possible_ing_per_allergen[al].update(_ingredients.split())

    cant_be_allergen = defaultdict(set)
    for ing, ing_in_recipe in ingredients.items():
        for al, al_in_recipe in allergens.items():
            if a_is_subset_of_b(al_in_recipe, ing_in_recipe):
                continue
            cant_be_allergen[ing].add(al)

    for ing, _cant_be_allergen in cant_be_allergen.items():
        for al in _cant_be_allergen:
            if ing in possible_ing_per_allergen[al]:
                possible_ing_per_allergen[al].remove(ing)

    fixed = {}
    while possible_ing_per_allergen:
        new_fixed = {}
        for al, options in possible_ing_per_allergen.items():
            if len(options) == 1:
                new_fixed[al] = list(options)[0]
        for ing in new_fixed.values():
            for v in possible_ing_per_allergen.values():
                if ing in v:
                    v.remove(ing)
        possible_ing_per_allergen = {
            k: v for k, v in possible_ing_per_allergen.items() if k not in new_fixed
        }
        fixed.update(new_fixed)

    return ",".join(fixed[x] for x in sorted(fixed))


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 5
    answer = solve_part1(DataName.PUZZLE)
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_1) == "mxmxvkd,sqjhc,fvjkl"
    answer = solve_part2(DataName.PUZZLE)
    submit(answer, part)
