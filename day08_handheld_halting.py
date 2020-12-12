""" Solutions for https://adventofcode.com/2020/day/8 """

# import modules used below.
from collections import UserList


# Part 1: Immediately before any instruction is executed a second time, what
# value is in the accumulator?


# Create data model for boot code program in data file.
class BootCode(UserList):
    """ Data Model for boot code program from data file """

    @classmethod
    def from_file(cls, file_path):
        """ Read boot code program from specified file """
        with open(file_path) as fp:
            return cls(line.rstrip() for line in fp)

    def execute_without_looping(self):
        """ Find accumulator value at point immediately before code loops """
        accumulator = 0
        execution_log = []

        line_number = 1
        while (
            line_number not in execution_log and
            1 <= line_number <= len(self)
        ):
            current_instruction_name = self[line_number-1][0:3]
            current_instruction_argument = int(self[line_number-1][4:])
            execution_log.append(line_number)

            if current_instruction_name == 'acc':
                accumulator += current_instruction_argument
                line_number += 1
            elif current_instruction_name == 'jmp':
                line_number += current_instruction_argument
            else:
                line_number += 1

        return accumulator, execution_log

    def find_corrupted_instruction(self):
        """ Find corrupted jmp/nop instruction in boot code """
        for line_number in range(1, len(self)+1):
            current_instruction = self[line_number-1]
            current_instruction_name = current_instruction[0:3]
            if current_instruction_name == 'acc':
                continue

            self[line_number-1] = (
                f'{["jmp", "nop"][current_instruction_name == "jmp"]}'
                f'{current_instruction[3:]}'
            )

            accumulator, log = self.execute_without_looping()
            self[line_number-1] = current_instruction
            if log[-1] == len(self):
                break

        return accumulator, log, line_number, current_instruction

# Read boot code program from data file.
boot_code = BootCode.from_file('data/day08_handheld_halting-data.txt')

# Find accumulator value for Part 1.
result1, log1 = boot_code.execute_without_looping()
print(f'Number of boot code lines in data file: {len(boot_code)}')
print(f'Number of instructions executed for Part 1: {len(log1)}')
print(f'Value of accumulator value for Part 1: {result1}')


# Part 2: After fixing the corrupted jmp or nop instruction causing an infinite
# loop, what value is in the accumulator?


# Find accumulator value for Part 2.
result2, log2, line_no2, instruction2 = boot_code.find_corrupted_instruction()
print(f'\nNumber of instructions executed for Part 2: {len(log2)}')
print(
    f'Corrupted instruction in original boot code found at '
    f'line {line_no2}: {instruction2}'
)
print(f'Value of accumulator value for Part 2: {result2}')
