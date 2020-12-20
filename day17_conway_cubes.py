""" Solutions for https://adventofcode.com/2020/day/17 """

# import modules used below.
from copy import deepcopy
from functools import lru_cache
from itertools import product


# Part 1: Starting with the initial configuration in the provided data file,
# how many cubes are in an active state after six cycles of a form of Conway's
# Game of Life is iterated in three-dimensions?


# Create data model for which Conway Cubes are active within pocket dimension.
class ActiveConwayCubes(set):
    """ Data Model for active Conway Cubes within pocket dimension """

    def __init__(self, *args, dim=3):
        super().__init__(*args)
        self.dim = dim

    def set_active(self, position):
        """ Set Conway Cube at position to active """
        self.add(position)

    def cycle_cubes(self, iterations=6):
        """ Cycle states of Conway Cubes the specified number of iterations """
        @lru_cache()
        def get_neighbors(position):
            neighbors = set()
            position_adjustments = [
                permutation_with_repetition
                for permutation_with_repetition
                in product((-1, 0, 1), repeat=self.dim)
            ]
            for adjustment in position_adjustments:
                if any(element for element in adjustment):
                    neighbors.add(
                        tuple(
                            sum(coordinate)
                            for coordinate
                            in zip(position, adjustment)
                        )
                    )
            return neighbors

        for _ in range(iterations):
            updated_active_cubes = deepcopy(self)
            all_neighbors_of_active_cubes = []
            for active_cube in self:
                active_cube_neighbors = get_neighbors(active_cube)
                all_neighbors_of_active_cubes.extend(active_cube_neighbors)
                if len(
                    [cube for cube in self if cube in active_cube_neighbors]
                ) not in (2, 3):
                    updated_active_cubes.remove(active_cube)

            for neighbor in all_neighbors_of_active_cubes:
                if neighbor in self:
                    continue
                neighbors_of_neighbor = get_neighbors(neighbor)
                if len(
                    [cube for cube in self if cube in neighbors_of_neighbor]
                ) == 3:
                    updated_active_cubes.add(neighbor)

            self.clear()
            self.update(updated_active_cubes)

# Read initial state of pocket universe from data file for Part 1.
pocket_universe1 = ActiveConwayCubes(dim=3)
initial_active_cube_count = 0
with open('data/day17_conway_cubes-data.txt') as fp:
    for row_number, line in enumerate(fp):
        for column_number, char in enumerate(line):
            if char == '#':
                pocket_universe1.set_active((row_number, column_number, 0))
                initial_active_cube_count += 1

# Find number of active Conway Cubes after six iterations for Part 1.
pocket_universe1.cycle_cubes(iterations=6)
print(
    f'Number of initial active Conway Cubes in data file: '
    f'{initial_active_cube_count}'
)
print(
    f'Number of active Conway Cubes after 6 iterations for Part 1: '
    f'{len(pocket_universe1)}'
)


# Part 2: Starting with the initial configuration in the provided data file,
# how many cubes are in an active state after six cycles of a form of Conway's
# Game of Life is iterated in four-dimensions?


# Read initial state of pocket universe from data file for Part 2.
pocket_universe2 = ActiveConwayCubes(dim=4)
with open('data/day17_conway_cubes-data.txt') as fp:
    for row_number, line in enumerate(fp):
        for column_number, char in enumerate(line):
            if char == '#':
                pocket_universe2.set_active((row_number, column_number, 0, 0))

# Find number of active Conway Cubes after six iterations for Part 2.
pocket_universe2.cycle_cubes(iterations=6)
print(
    f'Number of active Conway Cubes after 6 iterations for Part 2: '
    f'{len(pocket_universe2)}'
)
