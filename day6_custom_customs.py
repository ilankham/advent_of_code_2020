""" Solutions for https://adventofcode.com/2020/day/6 """

# import modules used below.
from collections import UserDict


# Part 1: In the provided data file, how many group-wise "yeses" occur?


# Create data model for "group responses" in data file.
class GroupResponses(UserDict):
    """ Data Model for "question group_responses" from data file """

    def __init__(self):
        super().__init__()
        self.group_size = 0

    def add_responses(self, responses):
        """ Add questions responses for group, and increment group size """
        for response in responses:
            self[response] = self.get(response, 0) + 1
        self.group_size += 1

    @property
    def unanimous_yeses(self):
        """ Return questions for which the group unanimously responded """
        return [q for q in self if self[q] == self.group_size]

# Read "question group_responses" from data file.
group_responses = []
current_group = GroupResponses()
with open('data/day6_custom_customs-data.txt') as fp:
    for line in fp:
        if line == '\n':
            group_responses.append(current_group)
            current_group = GroupResponses()
            continue
        current_group.add_responses(line.rstrip())
    group_responses.append(current_group)

# Count number of group-wise "yeses" for Part 1.
number_of_gw_yeses = sum([len(r) for r in group_responses])
print(f'Number of response groups in data file: {len(group_responses)}')
print(f'Number of group-wise "yeses" for Part 1: {number_of_gw_yeses}')


# Part 2: In the provided data file, how many group-wise unanimous "yeses"
# occur?


# Count number of unanimous group-wise "yeses" for Part 2.
number_of_unanimous_gw_yeses = sum(
    [len(r.unanimous_yeses) for r in group_responses]
)
print(
    f'Number of unanimous group-wise "yeses" for Part 2: '
    f'{number_of_unanimous_gw_yeses}'
)
