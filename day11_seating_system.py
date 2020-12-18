""" Solutions for https://adventofcode.com/2020/day/11 """

# import modules used below.
from collections import UserList
from copy import deepcopy
from math import inf


# Part 1: In the provided data file, how many "seats" end up occupied after
# the equivalent of Conway's Game of Life reaches an equilibrium state?


# Create data model for output "seat map" in data file.
class SeatMap(UserList):
    """ Data Model for seat map from data file """

    @classmethod
    def from_file(cls, file_path):
        """ Read seat map from specified file """
        with open(file_path) as fp:
            return cls(line.rstrip() for line in fp)

    def find_equilibrium(self, crowd_threshold, radius=inf):
        """ Find equilibrium under seat map occupancy rules for Part 1 """
        def used_seats(floor_map, x, y, r):
            nearby_occupied_seats = 0
            for y_adjustment in (-1, 0, 1):
                for x_adjustment in (-1, 0, 1):
                    current_radius = 1
                    while current_radius <= r:
                        adjusted_y = y + current_radius * y_adjustment
                        adjusted_x = x + current_radius * x_adjustment
                        if (
                            y_adjustment == x_adjustment == 0 or
                            adjusted_y < 0 or
                            adjusted_y >= len(self) or
                            adjusted_x < 0 or
                            adjusted_x >= len(floor_map[adjusted_y]) or
                            floor_map[adjusted_y][adjusted_x] == 'L'
                        ):
                            break
                        elif floor_map[adjusted_y][adjusted_x] == '#':
                            nearby_occupied_seats += 1
                            break
                        elif floor_map[adjusted_y][adjusted_x] == '.':
                            current_radius += 1
            return nearby_occupied_seats

        updated_seatmap = deepcopy(self)
        iteration_count = 0
        while True:
            current_seatmap = deepcopy(updated_seatmap)
            iteration_count += 1
            for j, row in enumerate(current_seatmap):
                for i, entity in enumerate(row):
                    occupancy_count = used_seats(current_seatmap, i, j, radius)
                    if entity == '.':
                        continue
                    elif entity == 'L' and occupancy_count == 0:
                        updated_seatmap[j] = (
                            updated_seatmap[j][:i] +
                            '#'
                            + updated_seatmap[j][i+1:]
                        )
                    elif entity == '#' and occupancy_count >= crowd_threshold:
                        updated_seatmap[j] = (
                            updated_seatmap[j][:i] +
                            'L' +
                            updated_seatmap[j][i+1:]
                        )
            if current_seatmap == updated_seatmap:
                break

        return iteration_count, updated_seatmap

# Read "seat map" values from data file.
seat_map = SeatMap.from_file('data/day11-seating_system-data.txt')

# Find "seat map" equilibrium for Part 1.
iterations1, equilibrium_map1 = seat_map.find_equilibrium(
    crowd_threshold=4,
    radius=1
)
filled_seats = sum(row.count('#') for row in equilibrium_map1)
print(f'Number of rows of seats in data file: {len(seat_map)}')
print(f'Number of columns of seats in data file: {len(seat_map[0])}')
print(f'Number of iterations to find equilibrium for Part 1: {iterations1}')
print(f'Number of occupied seats at equilibrium for Part 1: {filled_seats}')


# Part 2: How many "seats" end up occupied after the equivalent of Conway's
# Game of Life with slightly different rules reaches an equilibrium state?


# Find "seat map" equilibrium for Part 2.
iterations2, equilibrium_map2 = seat_map.find_equilibrium(crowd_threshold=5)
filled_seats2 = sum(row.count('#') for row in equilibrium_map2)
print(f'\nNumber of iterations to find equilibrium for Part 2: {iterations2}')
print(f'Number of occupied seats at equilibrium for Part 2: {filled_seats2}')
