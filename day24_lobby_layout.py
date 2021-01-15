""" Solutions for https://adventofcode.com/2020/day/24 """

# import modules used below.
from collections import Counter, UserDict
from copy import deepcopy
from dataclasses import dataclass


# Part 1: After flipping the tiles in a hexagonal grid specified in the
# provided data file, how many tiles will be black-side up?


# Create data model for hexagonal tile layout.
@dataclass
class HexagonalTile:
    """ Data Model for hexagonal tile using axial coordinate system specified
    by http://devmag.org.za/2013/08/31/geometry-with-hex-coordinates/ """
    x: int
    y: int

    def __post_init__(self):
        self.visit_count = 0
        self.black_side_up = False
        self.neighbors = {
            'ne': self.ne_neighbor_coordinates,
            'e': self.e_neighbor_coordinates,
            'se': self.se_neighbor_coordinates,
            'sw': self.sw_neighbor_coordinates,
            'w': self.w_neighbor_coordinates,
            'nw': self.nw_neighbor_coordinates,
        }

    @property
    def ne_neighbor_coordinates(self):
        """ ne neighbor: (x,y) -> (x,y+1) """
        return self.x, self.y + 1

    @property
    def e_neighbor_coordinates(self):
        """ e neighbor: (x,y) -> (x+1,y) """
        return self.x + 1, self.y

    @property
    def se_neighbor_coordinates(self):
        """ se neighbor: (x,y) -> (x+1,y-1) """
        return self.x + 1, self.y - 1

    @property
    def sw_neighbor_coordinates(self):
        """ sw neighbor: (x,y) -> (x,y-1) """
        return self.x, self.y - 1

    @property
    def w_neighbor_coordinates(self):
        """ w neighbor: (x,y) -> (x-1,y) """
        return self.x - 1, self.y

    @property
    def nw_neighbor_coordinates(self):
        """ nw neighbor: (x,y) -> (x-1,y+1) """
        return self.x - 1, self.y + 1

    @property
    def neighbor_coordinates(self):
        """ Return coordinates for all six immediately adjacent neighbors """
        return list(self.neighbors.values())

class TileLayout(UserDict):
    """ Data Model for tile layout """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reference_tile = HexagonalTile(0, 0)
        self[(0, 0)] = self.reference_tile

    @property
    def visit_counts(self):
        """ Return statistics about how many times tiles have been visited """
        return Counter(
            tile.visit_count
            for tile
            in self.values()
        )

    @property
    def number_of_black_tiles(self):
        """ Return number of black-side up tiles """
        return sum(
            tile.black_side_up
            for tile
            in self.values()
        )

    def flip_tile_at_end_of_path(self, path_str):
        """ Flip color of tile at end of specified path string for Part 1 """
        current_tile = self.reference_tile
        while len(path_str) > 0:
            if (direction := path_str[0:2]) in ('ne', 'se', 'sw', 'nw'):
                path_str = path_str[2:]
            elif (direction := path_str[0]) in ('e', 'w'):
                path_str = path_str[1:]
            current_tile = HexagonalTile(*current_tile.neighbors[direction])
        current_tile_coordinates = (current_tile.x, current_tile.y)
        if current_tile_coordinates not in self:
            self[current_tile_coordinates] = HexagonalTile(
                *current_tile_coordinates
            )
        self[current_tile_coordinates].black_side_up ^= True
        self[current_tile_coordinates].visit_count += 1

    def evolve_layout(self, number_of_evolutions):
        """ Evolve layout using rules specified for Part 2 """
        for _ in range(number_of_evolutions):
            black_tile_coordinates = set(
                tile_coordinates
                for tile_coordinates
                in self
                if self[tile_coordinates].black_side_up
            )
            tile_coordinates_to_consider = set()
            for tile_coordinates in black_tile_coordinates:
                tile_coordinates_to_consider.add(tile_coordinates)
                tile_coordinates_to_consider.update(
                    neighbor_coordinates
                    for neighbor_coordinates
                    in HexagonalTile(*tile_coordinates).neighbor_coordinates
                )
            white_tile_coordinates = (
                tile_coordinates_to_consider -
                black_tile_coordinates
            )
            tiles_to_flip = []
            for tile_coordinates in tile_coordinates_to_consider:
                tile_neighbor_coordinates = set(HexagonalTile(
                    *tile_coordinates
                ).neighbor_coordinates)
                black_neighbor_count = len(
                    tile_neighbor_coordinates &
                    black_tile_coordinates
                )
                if (
                    (
                        tile_coordinates in black_tile_coordinates and (
                            black_neighbor_count == 0 or
                            black_neighbor_count > 2
                        )
                    )
                    or (
                        tile_coordinates in white_tile_coordinates and
                        black_neighbor_count == 2
                    )
                ):
                    tiles_to_flip.append(tile_coordinates)
            for tile_coordinates in tiles_to_flip:
                if tile_coordinates not in self:
                    self[tile_coordinates] = HexagonalTile(*tile_coordinates)
                self[tile_coordinates].black_side_up ^= True

# Read tile paths data file.
with open('data/day24_lobby_layout-data.txt') as fp:
    tile_paths = [path.rstrip() for path in fp]

# Find tile layout for Part 1.
tile_layout1 = TileLayout()
for path in tile_paths:
    tile_layout1.flip_tile_at_end_of_path(path)
print(f'Number of tile paths read from data file: {len(tile_paths)}')
print(f'Tile visit counts for Part 1: {tile_layout1.visit_counts}')
print(
    f'Number of black-side up tiles for Part 1: '
    f'{tile_layout1.number_of_black_tiles}'
)


# Part 2: After using the specified version of Conway's Game of Life to
# evolve the tile layout from Part 1 one hundred times, how many tiles will be
# black-side up??


# Find tile layout for Part 2.
tile_layout2 = deepcopy(tile_layout1)
tile_layout2.evolve_layout(100)
print(
    f'Number of black-side up tiles for Part 2: '
    f'{tile_layout2.number_of_black_tiles}'
)
