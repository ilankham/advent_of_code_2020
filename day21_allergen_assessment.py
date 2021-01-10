""" Solutions for https://adventofcode.com/2020/day/21 """

# import modules used below.
from collections import defaultdict, UserString
import re


# Part 1: Using the ingredients/allergens lists in the provided data file, how
# many times do ingredients appear that cannot possibly contain any allergens?


# Create data model for nutritional labels.
class NutritionalLabel(UserString):
    """ Data Model for nutritional labels with ingredients and allergens """
    allergens_map: dict = {}
    ingredient_counts: defaultdict = defaultdict(int)
    label_re = re.compile(r'([\w ]+) \(contains ([\w, ]+)\)')

    def __init__(self, label_as_string):
        super().__init__(label_as_string)
        label_components = self.label_re.search(label_as_string)
        self.ingredients = set(label_components.group(1).split())
        self.allergens = {
            allergen.strip()
            for allergen
            in label_components.group(2).split(',')
        }

    @classmethod
    def read_multiple_labels_from_file(cls, file_path):
        """ Read multiple nutritional labels and build global allergens map """
        labels_found = []
        with open(file_path) as fp:
            for line in fp:
                current_label = cls(line)
                labels_found.append(current_label)
                for allergen in current_label.allergens:
                    if cls.allergens_map.get(allergen, None) is None:
                        cls.allergens_map[allergen] = current_label.ingredients
                    else:
                        cls.allergens_map[allergen] = (
                            cls.allergens_map[allergen] &
                            current_label.ingredients
                        )
                for ingredient in current_label.ingredients:
                    cls.ingredient_counts[ingredient] += 1
            while (
                non_singleton_allergens := [
                    allergen
                    for allergen, ingredients_list
                    in cls.allergens_map.items() if len(ingredients_list) > 1
                ]
            ):
                singleton_ingredients = {
                    tuple(ingredients_list)[0]
                    for ingredients_list
                    in cls.allergens_map.values() if len(ingredients_list) == 1
                }
                for allergen in non_singleton_allergens:
                    cls.allergens_map[allergen] = (
                        cls.allergens_map[allergen] -
                        singleton_ingredients
                    )
            cls.allergens_map = {
                    allergen: tuple(ingredients_list)[0]
                    for allergen, ingredients_list
                    in sorted(cls.allergens_map.items())
                }
        return labels_found

# Read nutritional labels from data file.
nutritional_labels = NutritionalLabel.read_multiple_labels_from_file(
    'data/day21_allergen_assessment-data.txt'
)

# Find allergen-free ingredients count for Part 1.
allergen_free_ingredients = {
    ingredient: ingredient_count
    for ingredient, ingredient_count
    in NutritionalLabel.ingredient_counts.items()
    if ingredient not in NutritionalLabel.allergens_map.values()
}
print(f'Number of labels read from data file: {len(nutritional_labels)}')
print(
    f'Number of allergens reads from data file: '
    f'{len(NutritionalLabel.allergens_map)}'
)
print(
    f'Number of allergens reads from data file: '
    f'{len(NutritionalLabel.ingredient_counts)}'
)
print(
    f'Number of occurrences of allergen-free ingredients for Part 1: '
    f'{sum(allergen_free_ingredients.values())}'
)


# Part 2: After sorting allergens in alphabetical order, what are their
# corresponding "dangerous" ingredients"?


# Find canonical dangerous ingredient list for Part 2.
print(
    f'Canonical dangerous ingredient list for Part 2: '
    f'{",".join(v for k, v in NutritionalLabel.allergens_map.items())}'
)
