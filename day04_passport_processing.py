""" Solutions for https://adventofcode.com/2020/day/4 """

# import modules used below.
from collections import UserDict
import re


# Part 1: In the provided data file, how many "passports" are valid?


# Create data model for "passports" in data file.
class Passport(UserDict):
    """ Data Model for "passports" from data file """

    expected_components_for_part1 = {
        'byr': 'Birth Year',
        'iyr': 'Issue Year',
        'eyr': 'Expiration Year',
        'hgt': 'Height',
        'hcl': 'Hair Color',
        'ecl': 'Eye Color',
        'pid': 'Passport ID',
    }

    validation_rules_for_part2 = {
        'byr': re.compile(r'^(19[2-9]\d|200[0-2]$)'),
        'iyr': re.compile(r'^20(1\d|20)$'),
        'eyr': re.compile(r'^20(2\d|30)$'),
        'hgt': re.compile(r'^(1([5-8]\d|9[0-3])cm|(59|6\d|7[0-6])in)$'),
        'hcl': re.compile(r'^#[0-9a-f]{6}$'),
        'ecl': re.compile(r'^(amb|blu|brn|gry|grn|hzl|oth)$'),
        'pid': re.compile(r'^\d{9}$'),
    }

    def is_valid_for_part1(self):
        """ Determine whether "passport" has all components for Part 1 """
        return all(
            component in self.keys()
            for component in self.expected_components_for_part1
        )

    def is_valid_for_part2(self):
        """ Determine whether "passport" has valid components for Part 2 """
        return all(
                rule.search(self.get(component, ''))
                for component, rule in self.validation_rules_for_part2.items()
            )

# Read "passports" from data file.
passports = []
current_passport = Passport()
with open('data/day04_passport_processing-data.txt') as fp:
    for line in fp:
        if line == '\n':
            passports.append(current_passport)
            current_passport = Passport()
            continue
        current_passport.update(
                component.split(':')
                for component in line.rstrip().split(' ')
        )
    passports.append(current_passport)

# Count number of valid "passports" for Part 1.
number_of_valid_passports1 = sum([p.is_valid_for_part1() for p in passports])
print(f'Number of passports in data file: {len(passports)}')
print(f'Number of valid passports for Part 1: {number_of_valid_passports1}')


# Part 2: In the provided data file, how many "passports" have valid values?


# Count number of valid "passports" for Part 2.
number_of_valid_passports2 = sum([p.is_valid_for_part2() for p in passports])
print(f'Number of valid passports for Part 2: {number_of_valid_passports2}')
