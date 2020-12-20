""" Solutions for https://adventofcode.com/2020/day/14 """

# import standard library modules used below.
from collections import UserDict
from itertools import chain, combinations
import re


# Part 1: After executing the initialization program in the provided data file,
# what is the sum of all values left in memory using the execution rules for
# this Part?


# Create data model for sea port computer system initiation program in data
# file.
class SeaPortComputerSystem(UserDict):
    """ Data Model for sea port computer system """

    def __init__(self):
        super().__init__()
        self.instructions_log = []

    def update_for_part1(self, addr, val, bitmap):
        """ Update computer system memory values using rules for Part 1 """
        self.instructions_log.append(
            (addr, val, bitmap)
        )
        masked_value = list(f'{val:036b}')
        for i, bit in enumerate(bitmap):
            if bit == 'X':
                continue
            masked_value[i] = bit
        self[addr] = int(''.join(masked_value), 2)

    def update_for_part2(self, addr, val, bitmap):
        """ Update computer system memory values using rules for Part 2 """
        self.instructions_log.append(
            (addr, val, bitmap)
        )
        masked_address = list(f'{addr:036b}')
        positions_of_1s = [i for i, v in enumerate(bitmap) if v == "1"]
        for position in positions_of_1s:
            masked_address[position] = '1'
        positions_of_exes = [i for i, v in enumerate(bitmap) if v == "X"]
        positions_of_exes_powerset = chain.from_iterable(
            combinations(positions_of_exes, r) for r in
            range(len(positions_of_exes) + 1))
        for positions_set in positions_of_exes_powerset:
            positions_set_complement = (
                set(positions_of_exes) - set(positions_set)
            )
            for position in positions_set:
                masked_address[position] = '1'
            for position in positions_set_complement:
                masked_address[position] = '0'
            self[int(''.join(masked_address), 2)] = val

# Read sea port computer system initiation program from data file for Part 1.
instruction_regex = re.compile(r'mem\[([0-9]+)] = ([0-9]+)')
spcs1 = SeaPortComputerSystem()
current_bitmap = ''
with open('data/day14_docking_data-data.txt') as fp:
    for line in fp:
        if line[0:4] == 'mask':
            current_bitmap = line[7:].strip()
            continue
        elif not line.rstrip():
            break
        instruction_components = instruction_regex.search(line.rstrip())
        address = int(instruction_components.group(1))
        value = int(instruction_components.group(2))
        spcs1.update_for_part1(address, value, current_bitmap)

# Find wait computer system initiation program results for Part 1.
print(f'Number of instructions in data file: {len(spcs1.instructions_log)}')
print(f'Number of memory locations changed for Part 1: {len(spcs1.keys())}')
print(f'Sum of values in memory values for Part 1: {sum(spcs1.values())}')


# Part 2: After executing the initialization program in the provided data file,
# what is the sum of all values left in memory using the execution rules for
# this Part?


# Read sea port computer system initiation program from data file for Part 2.
spcs2 = SeaPortComputerSystem()
current_bitmap = ''
with open('data/day14_docking_data-data.txt') as fp:
    for line in fp:
        if line[0:4] == 'mask':
            current_bitmap = line[7:].strip()
            continue
        elif not line.rstrip():
            break
        instruction_components = instruction_regex.search(line.rstrip())
        address = int(instruction_components.group(1))
        value = int(instruction_components.group(2))
        spcs2.update_for_part2(address, value, current_bitmap)

# Find wait computer system initiation program results for Part 2.
print(f'\nNumber of memory locations changed for Part 2: {len(spcs2.keys())}')
print(f'Sum of values in memory values for Part 2: {sum(spcs2.values())}')
