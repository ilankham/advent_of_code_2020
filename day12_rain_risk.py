""" Solutions for https://adventofcode.com/2020/day/12 """

# import modules used below.
from dataclasses import dataclass, field
from math import cos, radians, sin
from typing import List, Tuple


# Part 1: Using the provided data file and the movement rules for Part 1, what
# is the Manhattan distance between the final location of the ship and the
# ship's starting position1?


# Create data model for ship position based on movement indicated in data file.
@dataclass
class ShipPosition:
    """ Data Model for ship position1, with movement indicated in data file """
    ship_x: int = 0
    ship_y: int = 0
    ship_theta: int = 0
    movements_for_part1: List[Tuple[str, str]] = field(default_factory=list)
    waypoint_x: int = 10
    waypoint_y: int = 1
    movements_for_part2: List[Tuple[str, str]] = field(default_factory=list)

    def move_for_part1(self, cmd, arg):
        """ Apply movement rules for Part 1 """
        if cmd == 'N':
            self.ship_y += arg
        elif cmd == 'S':
            self.ship_y -= arg
        elif cmd == 'E':
            self.ship_x += arg
        elif cmd == 'W':
            self.ship_x -= arg
        elif cmd == 'L':
            self.ship_theta += arg
            self.ship_theta %= 360
        elif cmd == 'R':
            self.ship_theta -= arg
            self.ship_theta %= 360
        elif cmd == 'F':
            self.ship_x += round(arg * cos(radians(self.ship_theta)))
            self.ship_y += round(arg * sin(radians(self.ship_theta)))
        self.movements_for_part1.append((cmd, arg))

    def move_for_part2(self, cmd, arg):
        """ Apply movement rules for Part 2 """
        if cmd == 'N':
            self.waypoint_y += arg
        elif cmd == 'S':
            self.waypoint_y -= arg
        elif cmd == 'E':
            self.waypoint_x += arg
        elif cmd == 'W':
            self.waypoint_x -= arg
        elif cmd == 'L':
            self.waypoint_x, self.waypoint_y = (
                round(
                    self.waypoint_x * cos(radians(arg)) -
                    self.waypoint_y * sin(radians(arg))
                ),
                round(
                    self.waypoint_x * sin(radians(arg)) +
                    self.waypoint_y * cos(radians(arg))
                )
            )
        elif cmd == 'R':
            self.waypoint_x, self.waypoint_y = (
                round(
                    self.waypoint_x * cos(radians(-1*arg)) -
                    self.waypoint_y * sin(radians(-1*arg))
                ),
                round(
                    self.waypoint_x * sin(radians(-1*arg)) +
                    self.waypoint_y * cos(radians(-1*arg))
                )
            )
        elif cmd == 'F':
            self.ship_x += arg * self.waypoint_x
            self.ship_y += arg * self.waypoint_y
        self.movements_for_part2.append((cmd, arg))

    def manhattan_distance_from(self, x, y):
        """ Calculate Manhattan distance from self """
        return int(abs(self.ship_x - x) + abs(self.ship_y - y))

# Read ship movement rules from data file.
with open('data/day12_rain_risk-data.txt') as fp:
    ship_movements = [line.rstrip() for line in fp]

# Find ship position1 after applying movement rules for Part 1.
position1 = ShipPosition()
for m in ship_movements:
    position1.move_for_part1(m[0], int(m[1:]))
print(f'Number of ship movements in data file: {len(ship_movements)}')
print(
    f'Position of ship after movements for Part 1: '
    f'({position1.ship_x}, {position1.ship_y})'
)
print(f'Direction of ship after movements for Part 1: {position1.ship_theta}')
print(
    f'Manhattan distance from origin for Part 1: '
    f'{position1.manhattan_distance_from(0, 0)}'
)


# Part 2: Using the provided data file and the movement rules for Part 2, what
# is the Manhattan distance between the final location of the ship and the
# ship's starting position1?


# Find ship position1 after applying movement rules for Part 2.
position2 = ShipPosition()
for m in ship_movements:
    position2.move_for_part2(m[0], int(m[1:]))
print(
    f'\nPosition of ship after movements for Part 2: '
    f'({position2.ship_x}, {position2.ship_y})'
)
print(
    f'Relative position of waypoint after movements for Part 2: '
    f'({position2.waypoint_x}, {position2.waypoint_y})'
)
print(
    f'Manhattan distance from origin for Part 2: '
    f'{position2.manhattan_distance_from(0, 0)}'
)
