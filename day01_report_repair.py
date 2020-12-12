""" Solutions for https://adventofcode.com/2020/day/1 """


# Part 1: Find the two entries that sum to 2020 in the provided data file
# and then multiply those two numbers together.


# Read positive integer values from data file.
with open('data/day01_report_repair-data.txt') as fp:
    data_values = [int(line.rstrip()) for line in fp]

# In order to minimize the number of comparisons needed, calculate 2020 - v
# for each value v in the data file. If 2020 - v is also in the data file,
# then (2020 - v) + v = 2020. Consequently, the desired solution will be
# (2020-v)*v.
differences_from_2020 = {
    2020 - v
    for v in data_values
}

# Search the collection of difference for value in the data file, and stop
# once a solution has been found for Part 1.
for v in data_values:
    if v in differences_from_2020:
        print(f'Values from data file for Part 1: {(2020-v, v)}')
        print(f'Solution for Part 1: {2020-v}*{v} = {(2020-v)*v}')
        break


# Part 2: What is the product of the three entries that sum to 2020?


# Generalizing, calculate 2020 - (v1 + v2) for each pair of values (v1, v2)
# in the data file. If v = 2020 - (v1 + v2) is also in the data file, then
# v + v1 + v2 = 2020. Consequently, the desired solution will be v*v1*v2.
pairwise_differences_from_2020 = {
    2020 - (v1 + v2): (v1, v2)
    for v1 in data_values
    for v2 in data_values
}

# Search the collection of difference for value in the data file, and stop
# once a solution has been found for Part 2.
for v in data_values:
    if v in pairwise_differences_from_2020.keys():
        v1, v2 = pairwise_differences_from_2020[v]
        print(f'Values from data file for Part 2: {(v, v1, v2)}')
        print(f'Solution for Part 2: {v}*{v1}*{v2} = {v*v1*v2}')
        break
