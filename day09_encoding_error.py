""" Solutions for https://adventofcode.com/2020/day/9 """

# import modules used below.
from collections import UserList


# Part 1: What is the first number, excluding the first 25 in the data file,
# that is not the sum of two of the 25 numbers before it?


# Create data model for cypher data in data file.
class CypherData(UserList):
    """ Data Model for cypher data from data file """

    @classmethod
    def from_file(cls, file_path):
        """ Read cypher data from specified file """
        with open(file_path) as fp:
            return cls(int(line.rstrip()) for line in fp)

    def find_encryption_flaw_for_part1(self, preamble_length):
        """ Find encryption flaw for Part 1 """
        for line_number in range(preamble_length+1, len(self)+1):
            target_value = self[line_number-1]
            evaluation_window = self[
                line_number-preamble_length-1:line_number-1
            ]
            differences_from_target_value = {
                target_value - value
                for value in evaluation_window
            }
            for window_value in evaluation_window:
                if window_value in differences_from_target_value:
                    break
            else:
                break
        return line_number, target_value

    def find_encryption_weakness_for_part2(self, preamble_length):
        """ Find encryption weakness for Part 2 """
        _, target_value = self.find_encryption_flaw_for_part1(preamble_length)
        for window_length in range(2, len(self)):
            for position in range(len(self)-window_length+1):
                values_window = self[position:position+window_length]
                if sum(values_window) == target_value:
                    return values_window
        return None

# Read cypher data from data file.
cypher_data = CypherData.from_file('data/day09_encoding_error-data.txt')

# Find encryption flaw in cypher data for Part 1.
line_in_file, flaw = cypher_data.find_encryption_flaw_for_part1(25)
print(f'Number of cypher values in data file: {len(cypher_data)}')
print(f'Line number in file of encryption flaw for Part 1: {line_in_file}')
print(f'Value of encryption flaw for Part 1: {flaw}')


# Part 2: What sequence of consecutive values in the data file add up to the
# result obtained in Part 1?


# Find encryption weakness in cypher data for Part 2.
weak_sequence = cypher_data.find_encryption_weakness_for_part2(25)
min_value = min(weak_sequence)
max_value = max(weak_sequence)
print(f'\nLength of weakness sequence for Part 2: {len(weak_sequence)}')
print(f'Minimum value of weakness sequence for Part 2: {len(weak_sequence)}')
print(f'Minimum value of weakness sequence for Part 2: {min_value}')
print(f'Maximum value of weakness sequence for Part 2: {max_value}')
print(f'Sum of min and max value for Part 2: {min_value + max_value}')
