""" Solutions for https://adventofcode.com/2020/day/20 """

# import modules used below.
from collections import defaultdict, UserList
from enum import Enum, IntEnum
from math import prod, sqrt
import re


# Part 1: After assembling the labelled image tiles in the provided data file,
# what is the product of the IDs of the four corner tiles?


# Create data model for image tiles.
class Orientation(Enum):
    """ Data Model for image tile orientations/transformations """
    DEFAULT = 0
    ROTATE_90 = 90
    ROTATE_180 = 180
    ROTATE_270 = 270
    FLIP_ACROSS_HAXIS = 1
    FLIP_ACROSS_MAJOR_AXIS = complex(1, 1)
    FLIP_ACROSS_VAXIS = complex(0, 1)
    FLIP_ACROSS_MINOR_AXIS = complex(-1, 1)

class Edge(IntEnum):
    """ Data Model for image tile edge directions """
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

class ImageTile(UserList):
    """ Data Model for image tiles """

    tile_ID_regex = re.compile(r'Tile ([0-9]+):')
    sea_monster_row1_regex = re.compile(r'([.#O]{18})#([.#O])')
    sea_monster_row1_replacement = r'\1O\2'
    sea_monster_row2_regex = re.compile(
        r'#([.#O]{4})##([.#O]{4})##([.#O]{4})###'
    )
    sea_monster_row2_replacement = r'O\1OO\2OO\3OOO'
    sea_monster_row3_regex = re.compile(
        r'([.#O])#([.#O]{2})#([.#O]{2})#([.#O]{2})'
        r'#([.#O]{2})#([.#O]{2})#([.#O]{3})'
    )
    sea_monster_row3_replacement = r'\1O\2O\3O\4O\5O\6O\7'

    def __init__(self, title_id, tile_data):
        """ top/bottom read left-to-right; left/right read top-to-bottom """
        super().__init__(tile_data)
        self.tile_id = title_id
        self.orientation = Orientation.DEFAULT
        self.positions = {
            Orientation.DEFAULT: self,
            Orientation.ROTATE_90: self.rotate(90),
            Orientation.ROTATE_180: self.rotate(180),
            Orientation.ROTATE_270: self.rotate(270),
            Orientation.FLIP_ACROSS_HAXIS: self.flip_along_haxis(),
            Orientation.FLIP_ACROSS_MAJOR_AXIS: self.flip_along_major_axis(),
            Orientation.FLIP_ACROSS_VAXIS: self.flip_along_vaxis(),
            Orientation.FLIP_ACROSS_MINOR_AXIS: self.flip_along_minor_axis(),
        }
        self.neighbors = {
            Edge.TOP: None,
            Edge.RIGHT: None,
            Edge.BOTTOM: None,
            Edge.LEFT: None,
        }
        self.neighbor_edge_map = {
            Edge.TOP: self.top,
            Edge.RIGHT: self.right,
            Edge.BOTTOM: self.bottom,
            Edge.LEFT: self.left,
        }
        self.edge_tile = False
        self.corner_tile = False

        self.x_coordinate = None
        self.y_coordinate = None

    def __str__(self):
        return_value = [f'Tile {self.tile_id}:']
        for row in self.positions[self.orientation]:
            return_value.append(''.join(row))
        return '\n'.join(return_value)

    @classmethod
    def read_multiple_tiles_from_file(cls, file_path, dlm='\n'):
        """ Read multiple image tiles from specified file """
        tile_id = None
        input_buffer = []
        image_tiles_found = []
        with open(file_path) as fp:
            for line in fp:
                if line == dlm:
                    image_tiles_found.append(cls(tile_id, input_buffer))
                    input_buffer = []
                    continue
                elif tile_id_components := cls.tile_ID_regex.search(line):
                    tile_id = int(tile_id_components.group(1))
                    continue
                input_buffer.append(list(line.rstrip()))
            image_tiles_found.append(cls(tile_id, input_buffer))
        return image_tiles_found

    def rotate(self, degrees):
        """ Rotate by increments of 90 degrees: (x, y) -> (-y, x) """
        number_of_rotations = int((degrees % 360) / 90)

        def _rotate(image, rotations):
            if rotations == 0:
                return image
            elif rotations == 1:
                return [
                    [row[-1 * (n + 1)] for row in image]
                    for n in range(len(image))
                ]
            else:
                return _rotate(_rotate(image, 1), rotations-1)
        return _rotate(self, number_of_rotations)

    def flip_along_haxis(self):
        """ Flip with respect to a horizontal axis: (x, y) -> (x, -y) """
        return [
            self[n] for n in range(len(self)-1, -1, -1)
        ]

    def flip_along_major_axis(self):
        """ Flip with respect to a major/positive axis: (x, y) -> (y, x) """
        return [
            [
                self[i][j] for i in range(len(self)-1, -1, -1)
            ]
            for j in range(len(self)-1, -1, -1)
        ]

    def flip_along_vaxis(self):
        """ Flip with respect to a vertical axis: (x, y) -> (-x, y) """
        return [
            self[n][::-1] for n in range(len(self))
        ]

    def flip_along_minor_axis(self):
        """ Flip with respect to a minor/negative axis: (x, y) -> (-y, -x) """
        return [
            [
                self[i][j] for i in range(len(self))
            ]
            for j in range(len(self))
        ]

    def top(self, orientation):
        """ Return top row with respect to a specific orientation """
        return self.positions[orientation][0]

    def right(self, orientation):
        """ Return right row with respect to a specific orientation """
        return [
            row[-1] for row in self.positions[orientation]
        ]

    def bottom(self, orientation):
        """ Return bottom row with respect to a specific orientation """
        return self.positions[orientation][-1]

    def left(self, orientation):
        """ Return left row with respect to a specific orientation """
        return [
            row[0] for row in self.positions[orientation]
        ]

    @property
    def all_possible_edges(self):
        """ Return all possible edges at all possible orientations """
        all_edges = {}
        for orientation in Orientation:
            all_edges[orientation] = {
                Edge.TOP: self.top(orientation),
                Edge.RIGHT: self.right(orientation),
                Edge.BOTTOM: self.bottom(orientation),
                Edge.LEFT: self.left(orientation),
            }
        return all_edges

    @property
    def unused_edges(self):
        """ Return all unused edges at current unused_image_orientation """
        unused_edges = {}
        for direction, neighbor in self.neighbors.items():
            if neighbor is None:
                unused_edges[direction] = self.neighbor_edge_map[direction](
                    self.orientation
                )
        return unused_edges

    @property
    def without_edges(self):
        """ Return current orientation without edges """
        return [
            row[1:-1]
            for n, row in enumerate(
                self.positions[self.orientation]
            )
            if n not in (0, len(top_left_corner_tile) - 1)
        ]

    def highlight_sea_monsters(self, orientation):
        """ Return specific orientation with sea monsters highlighted """
        image_width = len(self.positions[orientation][0]) + 1
        image_data = '\n'.join(
            ''.join(row)
            for row in self.positions[orientation]
        )
        image_position = 0
        while image_position < len(image_data):
            if (
                (
                    row3_regex_match := self.sea_monster_row3_regex.search(
                        image_data[image_position:]
                    )
                ) is None
            ):
                break
            row3_match_start = row3_regex_match.span()[0] + image_position
            row3_match_end = row3_regex_match.span()[1] + image_position
            row2_match_start = row3_match_start - image_width
            row2_match_end = row3_match_end - image_width
            row1_match_start = row3_match_start - 2*image_width
            row1_match_end = row3_match_end - 2*image_width
            if (
                self.sea_monster_row1_regex.fullmatch(
                    image_data[row1_match_start:row1_match_end]
                )
                and
                self.sea_monster_row2_regex.fullmatch(
                    image_data[row2_match_start:row2_match_end]
                )
            ):
                image_data = (
                    image_data[:row1_match_start] +
                    self.sea_monster_row1_regex.sub(
                        self.sea_monster_row1_replacement,
                        image_data[row1_match_start:row1_match_end],
                        count=1
                    )[0:20] +
                    image_data[row1_match_end:row2_match_start] +
                    self.sea_monster_row2_regex.sub(
                        self.sea_monster_row2_replacement,
                        image_data[row2_match_start:row2_match_end],
                        count=1
                    )[0:20] +
                    image_data[row2_match_end:row3_match_start] +
                    self.sea_monster_row3_regex.sub(
                        self.sea_monster_row3_replacement,
                        image_data[row3_match_start:row3_match_end],
                        count=1
                    )[0:20] +
                    image_data[row3_match_end:]
                )
            image_position += row3_regex_match.span()[0] + 1

        return image_data

# Read image tiles from data file.
image_tiles = ImageTile.read_multiple_tiles_from_file(
    'data/day20_jurassic_jigsaw-data.txt'
)

# Match image tile edges, including adjusting for transformations under the
# dihedral group D_4.
def find_matching_edge(images, used_indexes, unused_indexes):
    """ Find an edge in common between previously used and unused images """
    for unused_image_index in unused_indexes:
        unused_image = images[unused_image_index]
        for unused_orientation in Orientation:
            for unused_image_direction, unused_image_edge in (
                unused_image.all_possible_edges[unused_orientation].items()
            ):
                for used_index in used_indexes:
                    used_image = images[used_index]
                    for used_image_direction, used_image_edge in (
                        used_image.unused_edges.items()
                    ):
                        if (
                            unused_image_edge == used_image_edge and
                            abs(
                                unused_image_direction - used_image_direction
                            ) == 2
                        ):
                            return (
                                unused_orientation,
                                unused_image_index,
                                unused_image_direction,
                                used_index,
                                used_image_direction
                            )

used_image_indexes = {0}
unused_image_indexes = set(range(len(image_tiles))) - used_image_indexes
tile_coordinates = defaultdict(dict)
tile_coordinates[0][0] = image_tiles[0]
image_tiles[0].x_coordinate = 0
image_tiles[0].y_coordinate = 0
while unused_image_indexes:
    (
        unused_image_orientation,
        unused_index,
        unused_image_direction,
        used_index,
        used_image_direction
    ) = find_matching_edge(
        image_tiles, used_image_indexes, unused_image_indexes
    )
    unused_image = image_tiles[unused_index]
    unused_image.orientation = unused_image_orientation
    used_image = image_tiles[used_index]
    used_image.neighbors[used_image_direction] = unused_image
    unused_image.neighbors[unused_image_direction] = used_image

    if used_image_direction == Edge.TOP:
        unused_image.x_coordinate = used_image.x_coordinate
        unused_image.y_coordinate = used_image.y_coordinate + 1
    elif used_image_direction == Edge.RIGHT:
        unused_image.x_coordinate = used_image.x_coordinate + 1
        unused_image.y_coordinate = used_image.y_coordinate
    elif used_image_direction == Edge.BOTTOM:
        unused_image.x_coordinate = used_image.x_coordinate
        unused_image.y_coordinate = used_image.y_coordinate - 1
    elif used_image_direction == Edge.LEFT:
        unused_image.x_coordinate = used_image.x_coordinate - 1
        unused_image.y_coordinate = used_image.y_coordinate

    tile_coordinates[
        unused_image.x_coordinate
    ][unused_image.y_coordinate] = unused_image

    if (
        (north_neighbor_x := unused_image.x_coordinate)
        in tile_coordinates
        and
        (north_neighbor_y := unused_image.y_coordinate + 1)
        in tile_coordinates[north_neighbor_x]
    ):
        north_neighbor = (
            tile_coordinates[north_neighbor_x][north_neighbor_y]
        )
        north_neighbor.neighbors[Edge.BOTTOM] = unused_image
        unused_image.neighbors[Edge.TOP] = north_neighbor

    if (
        (east_neighbor_x := unused_image.x_coordinate + 1)
        in tile_coordinates
        and
        (east_neighbor_y := unused_image.y_coordinate)
        in tile_coordinates[east_neighbor_x]
    ):
        east_neighbor = tile_coordinates[east_neighbor_x][east_neighbor_y]
        east_neighbor.neighbors[Edge.LEFT] = unused_image
        unused_image.neighbors[Edge.RIGHT] = east_neighbor

    if (
        (south_neighbor_x := unused_image.x_coordinate)
        in tile_coordinates
        and
        (south_neighbor_y := unused_image.y_coordinate - 1)
        in tile_coordinates[south_neighbor_x]
    ):
        south_neighbor = tile_coordinates[south_neighbor_x][south_neighbor_y]
        south_neighbor.neighbors[Edge.TOP] = unused_image
        unused_image.neighbors[Edge.BOTTOM] = south_neighbor

    if (
        (west_neighbor_x := unused_image.x_coordinate - 1)
        in tile_coordinates
        and
        (west_neighbor_y := unused_image.y_coordinate)
        in tile_coordinates[west_neighbor_x]
    ):
        west_neighbor = tile_coordinates[west_neighbor_x][west_neighbor_y]
        west_neighbor.neighbors[Edge.RIGHT] = unused_image
        unused_image.neighbors[Edge.LEFT] = west_neighbor

    used_image_indexes.add(unused_index)
    unused_image_indexes = set(range(len(image_tiles))) - used_image_indexes

for tile in image_tiles:
    number_of_neighbors = len(
        [
            neighbor
            for neighbor in tile.neighbors.values()
            if neighbor is not None
        ]
    )
    if number_of_neighbors < 4:
        tile.edge_tile = True
    if number_of_neighbors == 2:
        tile.corner_tile = True

# Find product of ids for corner tiles for Part 1.
edge_tiles = [tile for tile in image_tiles if tile.edge_tile]
print(f'Number of tiles read from data file: {len(image_tiles)}')
print(
    f'Number of corner tiles read from data file: '
    f'{len(edge_tiles)}'
)
print(
    f'Number of edge tiles read from data file: '
    f'{len([tile for tile in image_tiles if tile.corner_tile])}'
)
print(
    f'Product of corner-tile ids for Part 1: '
    f'{prod([tile.tile_id for tile in image_tiles if tile.corner_tile])}'
)


# Part 2: After discarding edges, assembling tiles, and discarding octothorpes
# corresponding to "sea monsters," how many octothorpes remain?


# Find octothorpe count for Part 2.
for tile in edge_tiles:
    if tile.neighbors[Edge.TOP] is None and tile.neighbors[Edge.LEFT] is None:
        top_left_corner_tile = tile
        break
assembled_borderless_image_data = (
    top_left_corner_tile.without_edges
)
grid_length = int(sqrt(len(image_tiles)))
row_length = len(assembled_borderless_image_data[0])
column_length = len(assembled_borderless_image_data)
current_row_tile = top_left_corner_tile
for x in range(grid_length):
    current_column_tile = current_row_tile.neighbors[Edge.RIGHT]
    for y in range(grid_length-1):
        for row_number in range(column_length):
            row_to_extend = assembled_borderless_image_data[
                row_number + row_length * x
                ]
            row_to_extend.extend(
                current_column_tile.without_edges[row_number]
            )
        current_column_tile = current_column_tile.neighbors[Edge.RIGHT]
    current_row_tile = current_row_tile.neighbors[Edge.BOTTOM]
    assembled_borderless_image_data.extend(
        current_row_tile.without_edges if current_row_tile else []
    )
complete_image = ImageTile(None, assembled_borderless_image_data)
complete_image_with_highlighting = {}
octothorpe_count = {}
for transformation in Orientation:
    complete_image_with_highlighting[transformation] = (
        complete_image.highlight_sea_monsters(transformation)
    )
    octothorpe_count[transformation] = (
        complete_image_with_highlighting[transformation].count('#')
    )
print(f'Habitat water roughness for Part 2: {min(octothorpe_count.values())}')
