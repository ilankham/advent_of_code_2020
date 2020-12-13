""" Solutions for https://adventofcode.com/2020/day/10 """

# import modules used below.
from collections import Counter, UserList
from itertools import chain, combinations
from math import prod


# Part 1: What is the number of 1-jolt differences multiplied by the number of
# 3-jolt differences in the provided data file?


# Create data model for output "joltages" in data file.
class OutputJoltages(UserList):
    """ Data Model for output joltages from data file """

    @classmethod
    def from_file(cls, file_path):
        """ Read output joltages from specified file and add min/max """
        with open(file_path) as fp:
            values_in_file = [int(line.rstrip()) for line in fp]
            return cls(chain([0], values_in_file, [max(values_in_file)+3]))

    def sorted_pairwise_differences(self, joltages=None):
        """ Find sorted pairwise differences for Part 1 """
        if joltages is None:
            joltages = self
        sorted_data_values = sorted(joltages)
        pairwise_differences = [
            sorted_data_values[i] - sorted_data_values[i-1]
            for i in range(1, len(joltages))
        ]
        return pairwise_differences

    def partition_into_valid_joltage_subsequences(self):
        """ Find all possible joltage subsequences for Part 2 """
        sorted_data_values = sorted(self)
        joltage_diffs = self.sorted_pairwise_differences()
        data_partitions = {}
        partition_lower_bound_index = 0
        for i in range(len(self)-1):
            if joltage_diffs[i] == 3:
                data_partitions[
                    frozenset(
                        sorted_data_values[partition_lower_bound_index:i+1]
                    )
                ] = []
                partition_lower_bound_index = i + 1
        for partition in data_partitions:
            if len(partition) == 1:
                continue
            partition_interior = partition - {min(partition), max(partition)}
            partition_interior_powerset = list(chain.from_iterable(
                combinations(partition_interior, n)
                for n in range(len(partition_interior)+1)
            ))
            for subset in partition_interior_powerset:
                partition_subset = (
                    set(subset) |
                    {min(partition), max(partition)}
                )
                if max(self.sorted_pairwise_differences(partition_subset)) < 4:
                    data_partitions[partition].append(partition_subset)
        return data_partitions

# Read "joltage" values from data file.
output_joltages = OutputJoltages.from_file('data/day10_adapter_array-data.txt')

# Find "joltages" differences for Part 1.
diffs = output_joltages.sorted_pairwise_differences()
counts = Counter(diffs)
print(f'Number of joltages values in data file: {len(output_joltages)}')
print(f'Number of differences of 1 for Part 1: {counts[1]}')
print(f'Number of differences of 3 for Part 1: {counts[3]}')
print(f'Product for Part 1: {counts[1]}*{counts[3]}={counts[1]*counts[3]}')


# Part 2: What is the total number of valid "joltage" sequences?


# Find total number of valid "joltage" sequences for Part 2.
partitions = output_joltages.partition_into_valid_joltage_subsequences()
number_of_sequences = prod(
    len(v) for v in partitions.values() if len(v) != 0
)
print(f'\nLength of partitions for Part 2: {len(partitions)}')
print(f'Minimum partition length for Part 2: {min(partitions)}')
print(f'Maximum partition length for Part 2: {max(partitions)}')
print(f'Number of sequences for Part 2: {number_of_sequences}')
