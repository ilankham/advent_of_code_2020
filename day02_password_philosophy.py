""" Solutions for https://adventofcode.com/2020/day/2 """

# import modules used below.
from dataclasses import dataclass, field
import re


# Part 1: How many passwords in the provided data file are valid according to
# their corresponding "policies"?


# Compile regex for extracting "policy" rule components and passwords.
day2_regex = re.compile(r'(\d+)-(\d+) (\w): (\w+)')

# Create data model for "policy" rule components and passwords.
@dataclass
class RuleComponentsAndPassword:
    """ Data Model for rule components and passwords read from data file """
    full_string: str
    min_times: int = field(init=False)
    max_times: int = field(init=False)
    char: str = field(init=False)
    pswd: str = field(init=False)

    def __post_init__(self):
        rule_components = day2_regex.search(self.full_string)
        self.min_times = int(rule_components.group(1))
        self.max_times = int(rule_components.group(2))
        self.char = rule_components.group(3)
        self.pswd = rule_components.group(4)

    def is_valid_for_part1(self):
        """ Determine whether password matches rules according to Part 1 """
        return self.min_times <= self.pswd.count(self.char) <= self.max_times

    def is_valid_for_part2(self):
        """ Determine whether password matches rules according to Part 2 """
        letter_at_min_position = self.pswd[self.min_times-1] == self.char
        letter_at_max_position = self.pswd[self.max_times-1] == self.char
        return letter_at_min_position != letter_at_max_position

# Read "policy" rule components and passwords from data file.
with open('data/day02_password_philosophy-data.txt') as fp:
    data_values = [
        RuleComponentsAndPassword(line.rstrip())
        for line in fp
    ]

# Count number of valid passwords for Part 1.
number_of_valid_passwords = sum([v.is_valid_for_part1() for v in data_values])
print(f'Number of valid passwords for Part 1: {number_of_valid_passwords}')


# Part 2: How many passwords in the provided data file are valid according to
# the alternate interpretation for their corresponding "policies"?


# Count number of valid passwords for Part 2.
number_of_valid_passwords = sum([v.is_valid_for_part2() for v in data_values])
print(f'Number of valid passwords for Part 2: {number_of_valid_passwords}')
