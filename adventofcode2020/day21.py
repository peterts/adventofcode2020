from collections import defaultdict
from itertools import starmap

from adventofcode2020.utils import (
    DataName,
    a_is_subset_of_b,
    fetch_input_data_if_not_exists,
    pattern_extract,
    print_call,
    read_line_separated_list,
    submit,
)


@print_call
def solve_part1(file_name):
    (
        ingredients,
        cant_be_allergen,
        possible_ing_per_allergen,
    ) = _find_which_allergens_each_ingredient_cant_be(file_name)
    n_allergens = len(possible_ing_per_allergen)
    return sum(
        starmap(
            lambda k, v: len(ingredients[k]) if len(v) == n_allergens else 0,
            cant_be_allergen.items(),
        )
    )


@print_call
def solve_part2(file_name):
    _, _, possible_ing_per_allergen = _find_which_allergens_each_ingredient_cant_be(file_name)

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


def _find_which_allergens_each_ingredient_cant_be(file_name):
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

    return ingredients, cant_be_allergen, possible_ing_per_allergen


if __name__ == "__main__":
    fetch_input_data_if_not_exists()

    part = "a"
    assert solve_part1(DataName.SAMPLE_1) == 5
    answer = solve_part1(DataName.PUZZLE)
    assert answer == 2125
    submit(answer, part)

    part = "b"
    assert solve_part2(DataName.SAMPLE_1) == "mxmxvkd,sqjhc,fvjkl"
    answer = solve_part2(DataName.PUZZLE)
    assert answer == "phc,spnd,zmsdzh,pdt,fqqcnm,lsgqf,rjc,lzvh"
    submit(answer, part)
