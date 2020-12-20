""" Solutions for https://adventofcode.com/2020/day/16 """

# import standard library modules used below.
from collections import defaultdict, UserList
from itertools import chain
from math import prod
import re


# Part 1: Considering just the "nearby tickets" and the validation rules for
# ticket fields in the provided data file, what is ticket scanning error rate
# (i.e., the sum of all invalid values across all "nearby tickets"?


# Create data model for "tickets" with validation rules for ticket fields.
class Ticket(UserList):
    """ Data Model for tickets with validation rules for ticket fields """

    validation_rule_regex = re.compile(
        r'^([\w ]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)'
    )
    validation_rules = {}

    @classmethod
    def add_validation_rule(cls, rule_str):
        """ Add new validation rule for ticket fields """
        rule_components = cls.validation_rule_regex.search(rule_str)
        rule_name = rule_components.group(1)
        rule_group1_lb = int(rule_components.group(2))
        rule_group1_ub = int(rule_components.group(3))
        rule_group2_lb = int(rule_components.group(4))
        rule_group2_ub = int(rule_components.group(5))
        rule_value_set = (
            set(range(rule_group1_lb, rule_group1_ub+1)) |
            set(range(rule_group2_lb, rule_group2_ub+1))
        )
        cls.validation_rules[rule_name] = rule_value_set

    @property
    def invalid_values(self):
        """ Return all invalid values for ticket """
        values_violating_validation_rules = []
        for value in self:
            for rule in self.validation_rules.values():
                if value in rule:
                    break
            else:
                values_violating_validation_rules.append(value)
        return values_violating_validation_rules

    @property
    def is_valid(self):
        """ Return boolean indicating whether ticket has only valid values """
        return not bool(self.invalid_values)

    @property
    def is_invalid(self):
        """ Return boolean indicating whether ticket has invalid values """
        return bool(self.invalid_values)

# Read validation rules and tickets from data file.
with open('data/day16_ticket_translation-data.txt') as fp:
    while (line := fp.readline().rstrip()) != '':
        Ticket.add_validation_rule(line)
    if line := fp.readline().rstrip() == 'your ticket:':
        your_ticket = Ticket(int(v) for v in fp.readline().rstrip().split(','))
    if line := fp.readline().rstrip() == '':
        pass
    nearby_tickets = []
    if line := fp.readline().rstrip() == 'nearby tickets:':
        for line in fp:
            nearby_tickets.append(
                Ticket(int(v) for v in line.rstrip().split(','))
            )

# Find ticket scanning error rate for nearby "tickets" for Part 1.
print(
    f'Number of validation rules in data file: '
    f'{len(Ticket.validation_rules)}'
)
print(f'Number of nearby tickets in data file: {len(nearby_tickets)}')
print(
    f'Number of invalid nearby tickets for Part 1: '
    f'{sum(ticket.is_invalid for ticket in nearby_tickets)}'
)
print(
    f'Ticket scanning error rate for Part 1: '
    f'{sum(chain.from_iterable(t.invalid_values for t in nearby_tickets))}'
)


# Part 2: After determining "ticket field" order, what is the product of the
# values on your "ticket" that start with the word "departure"?


# Impute "validation rule" order.
valid_tickets = [ticket for ticket in nearby_tickets if ticket.is_valid]
ticket_length = len(valid_tickets[0])
ticket_field_positions = defaultdict(list)
for field_position in range(0, ticket_length):
    ticket_values_at_position = set(
        ticket[field_position] for ticket in valid_tickets
    )
    for name, rule_values in Ticket.validation_rules.items():
        if all(value in rule_values for value in ticket_values_at_position):
            ticket_field_positions[field_position].append(name)
while max((len(value) for value in ticket_field_positions.values())) > 1:
    singleton_fields = [
        fields[0]
        for fields
        in ticket_field_positions.values()
        if len(fields) == 1
    ]
    for position, fields_set in ticket_field_positions.items():
        if len(fields_set) == 1:
            continue
        for field in singleton_fields:
            if field in fields_set:
                ticket_field_positions[position].remove(field)

# Find product of "departure" fields in "your ticket" for Part 2.
departure_field_values = [
    value
    for position, value
    in enumerate(your_ticket)
    if 'departure' in ticket_field_positions[position][0]
]
print(
    f'\nDeparture fields in your ticket for Part 2: '
    f'{departure_field_values}'
)
print(
    f'Product of departure field values for Part 2: '
    f'{prod(departure_field_values)}'
)
