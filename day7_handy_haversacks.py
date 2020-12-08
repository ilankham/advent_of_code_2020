""" Solutions for https://adventofcode.com/2020/day/6 """

# import modules used below.
from collections import UserDict
import re


# Part 1: In the provided data file, how many bag colors can eventually contain
# at least one shiny gold bag?


# Create data model for graph of "bag-containment rules" in data file.
class Rule(UserDict):
    """ Data Model for "bag-containment rules" from data file """

    name_match = re.compile(r'^([\w ]+) bags? contain')
    component_match = re.compile(r'([0-9]+) ([\w ]+) bags?\.?')

    def __init__(self, rule):
        """ Read "bag-containment rule" map from sentence """
        super().__init__()
        name_component = self.name_match.search(rule)
        self.name = name_component.group(1)
        rule_components = [
            component.strip().replace('.', '')
            for component in rule[name_component.span()[1]:].split(',')
        ]

        for component in rule_components:
            component_parts = self.component_match.search(component)
            if component_parts is None:
                break
            self[component_parts.group(2)] = int(component_parts.group(1))

    @staticmethod
    def search_for_color(rule_set, target_color):
        """ Search for color in rule set """

        def _reachable(target, current_color):
            if target in rule_set[current_color]:
                return True

            reachable = False
            for color_inside in rule_set[current_color]:
                reachable = reachable or _reachable(target, color_inside)
            return reachable

        top_level_colors = set()
        for color in rule_set:
            if _reachable(target_color, color):
                top_level_colors.add(color)
        return top_level_colors

    @staticmethod
    def bag_containment_count(rule_set, starting_color):
        """ Search bags contained within a given color bag """

        def _search(current_color):
            if not rule_set[current_color]:
                return 0

            return_value = 0
            for color, count in rule_set[current_color].items():
                return_value += count * (1 + _search(color))
            return return_value

        return _search(starting_color)

# Read "bag-containment rules" from data file.
with open('data/day7_handy_haversacks-data.txt') as fp:
    rules = {
        rule.name: rule
        for rule in [Rule(line.rstrip()) for line in fp if line != '']
    }

# Count number of bags that can contain shiny gold for Part 1.
print(f'Number of bag-containment rules in data file: {len(rules)}')
print(
    f'Number of bags that can contain shiny gold bags for Part 1: '
    f'{len(Rule.search_for_color(rules, "shiny gold"))}'
)


# Part 2: How many individual bags are required inside a single shiny gold bag?


# Find number of bags within a single shiny gold bag for Part 2.
print(
    f'Number of bags contained within a shiny gold bags for Part 2: '
    f'{Rule.bag_containment_count(rules, "shiny gold")}'
)
