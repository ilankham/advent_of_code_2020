""" Solutions for https://adventofcode.com/2020/day/3 """

# import modules used below.
from collections import UserList
from math import ceil, prod


# Part 1: Starting at the top-left corner of the "map" in the provided data
# file and following a slope of right 3 and down 1, how many "trees" are
# encountered?


# Create data model for "map" in data file.
class TobogganMap(UserList):
    """ Data Model for toboggan map from data file """

    @classmethod
    def from_file(cls, file_path):
        """ Read toboggan map from specified file """
        with open(file_path) as fp:
            return cls(line.rstrip() for line in fp)

    def get_object(self, x, y):
        """ Return map component relative to top-left corner being (1,1) """
        current_row = self[y-1]
        return current_row[(x-1) % len(current_row)]

    def traverse_path(self, right, down):
        """ Return objects along step path right/down from top-left corner """
        objects_along_path = []
        number_of_iterations = ceil(len(self)/down)
        for n in range(1, number_of_iterations):
            objects_along_path.append(
                toboggan_map.get_object(right * n + 1, down * n + 1)
            )
        return objects_along_path

# Read "map" from data file.
toboggan_map = TobogganMap.from_file('data/day3_toboggan_trajectory-data.txt')

# Count number of "trees" for Part 1.
print(
    f'Number of trees encountered for Part 1: '
    f'{toboggan_map.traverse_path(3, 1).count("#")}'
)


# Part 2: Starting at the top-left corner of the "map" in the provided data
# file and following a slope of right x and down y, what is the product of the
# number of "trees" encountered for each of the "paths formed using
# (x,y) = (1,1), (3,1), (5,1), (7,1), (1,2)?


# Determine number of "trees" along each path through "map".
paths = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]
number_of_trees = {
    path: toboggan_map.traverse_path(*path).count('#')
    for path in paths
}

# Calculate product of number of "trees" along each path for Part 2.
print(
    f'Product of number of trees encountered along each path for Part 2: '
    f'{prod(number_of_trees.values())}'
)
