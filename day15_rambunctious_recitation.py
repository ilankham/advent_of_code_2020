""" Solutions for https://adventofcode.com/2020/day/15 """

# import standard library modules used below.
from collections import defaultdict
from copy import deepcopy


# Part 1: Following the rules for the described memory game using the starting
# values in the provided data file, what will be the 2020th number spoken?


# Create data model for memory game sequence with specified starting values.
class MemoryGameSequence:
    """ Data Model for memory game sequence with specified starting values """

    def __init__(self, starting_values):
        self._sequence = deepcopy(starting_values)
        self.starting_values = starting_values
        self.number_usage = defaultdict(list)
        for i, v in enumerate(self.starting_values):
            self.number_usage[v].append(i+1)

    @classmethod
    def from_file(cls, file_path, dlm=','):
        """ Read starting values from specified file """
        with open(file_path) as fp:
            return cls([int(v) for v in fp.readline().rstrip().split(dlm)])

    def __getitem__(self, n):
        """ Get memory game sequence value for Turn n """
        if n > len(self._sequence):
            for i in range(len(self._sequence), n):
                most_recent_value = self._sequence[-1]
                next_value = (
                    0
                    if len(self.number_usage[most_recent_value]) == 1
                    else self.number_usage[most_recent_value][-1] -
                    self.number_usage[most_recent_value][-2]
                )
                self._sequence.append(next_value)
                self.number_usage[next_value].append(i + 1)

        return self._sequence[n-1]

# Read starting values from data file.
memory_game_sequence = MemoryGameSequence.from_file(
    'data/day15_rambunctious_recitation-data.txt'
)

# Find 2020th memory game sequence value for Part 1.
value_for_2020 = memory_game_sequence[2020]
print(
    f'Number of starting values read from data file: '
    f'{len(memory_game_sequence.starting_values)}'
)
print(f'2020th memory game sequence value: {value_for_2020}')
print(
    f'Turns 2020th memory game sequence value occurred: '
    f'{memory_game_sequence.number_usage[value_for_2020]}'
)


# Part 2: Following the rules for the described memory game using the starting
# values in the provided data file, what will be the 30000000th number spoken?


# Find 30000000th memory game sequence value for Part 2.
value_for_30000000 = memory_game_sequence[30000000]
print(f'\n30000000th memory game sequence value: {value_for_30000000}')
print(
    f'Turns 30000000th memory game sequence value occurred: '
    f'{memory_game_sequence.number_usage[value_for_30000000]}'
)
