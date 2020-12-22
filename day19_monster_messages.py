""" Solutions for https://adventofcode.com/2020/day/19 """

# import modules used below.
from collections import UserDict
import re

# import third-party modules used below.
import regex


# Part 1: Using the parsing rules and messages in the provided data file, how
# many messages satisfy Rule 0?


# Create data model for expression parsing rules.
class ParsingRules(UserDict):
    """ Data Model for expression parsing rules """

    rules_regex = re.compile(r'([0-9]+): (.+)')

    def add_rule(self, rule_str):
        """ Add parsing rule to self """
        rule_components = self.rules_regex.search(rule_str)
        rule_number = int(rule_components.group(1))
        rule_text = rule_components.group(2).replace('"', '')
        self[rule_number] = rule_text

    def as_regex(self, rule_index, prefix='^', suffix='$'):
        """ Return regex corresponding to rule at specified index """
        rule_components = self[rule_index].split(' ')
        position = 0
        while any(component.isdigit() for component in rule_components):
            component = rule_components[position]
            if component.isdigit():
                component_replacement = self[int(component)].split(' ')
                include_parentheses = len(component_replacement) > 1
                rule_components = (
                    rule_components[:position] +
                    (['('] if include_parentheses else []) +
                    component_replacement +
                    ([')'] if include_parentheses else []) +
                    rule_components[position+1:]
                )
            else:
                position += 1
        return re.compile(prefix+''.join(rule_components)+suffix)

# Read rules and messages from data file.
parsing_rules = ParsingRules()
messages = []
with open('data/day19_monster_messages-data.txt') as fp:
    while (line := fp.readline().rstrip()) != '':
        if line == '':
            break
        parsing_rules.add_rule(line)
    for line in fp:
        messages.append(line.rstrip())

# Find messages matching Rule 0 for Part 1.
rule_0_for_part1_regex = parsing_rules.as_regex(0)
messages_matching_rule_0_part1 = []
for message in messages:
    if rule_0_for_part1_regex.search(message):
        messages_matching_rule_0_part1.append(message)
print(f'Number of parsing rules read from data file: {len(parsing_rules)}')
print(f'Number of messages read from data file: {len(messages)}')
print(
    f'Number of messages satisfying Rule 0 for Part 1: '
    f'{len(messages_matching_rule_0_part1)}'
)


# Part 2: Using the parsing rules and messages in the provided data file, but
# with Rule 8 modified to be 42+ and 11 modified to be 42+ 31+, how many
# messages satisfy Rule 0 = 8 11?


# Find messages matching Rule 0 for Part 2.
rule_31_for_part2 = parsing_rules.as_regex(31, prefix='', suffix='').pattern
rule_42_for_part2 = parsing_rules.as_regex(42, prefix='', suffix='').pattern
rule_0_for_part2 = (
    '(' + rule_42_for_part2 + ')+'
    '(?P<rule11>' +
        '(' + rule_42_for_part2 + ')' +
        '(?&rule11)?' +
        '(' + rule_31_for_part2 + ')' +
    ')'
)
rule_0_part2_regex = regex.compile(rule_0_for_part2)
messages_matching_rule_0_part2 = []
for n, message in enumerate(messages):
    if rule_0_part2_regex.fullmatch(message):
        messages_matching_rule_0_part2.append(message)
print(
    f'Number of messages satisfying Rule 0 for Part 2: '
    f'{len(messages_matching_rule_0_part2)}'
)
