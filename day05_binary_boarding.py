""" Solutions for https://adventofcode.com/2020/day/5 """

# import modules used below.
from dataclasses import dataclass, field


# Part 1: In the provided data file, what is the highest seat ID on a boarding
# pass?


# Create data model for "boarding passes" in data file.
@dataclass
class BoardingPass:
    """ Data Model for "boarding passes" from data file """
    directions: str
    row: int = field(init=False)
    seat: int = field(init=False)
    seat_id: int = field(init=False)

    def __post_init__(self):
        self.row = int(
            self.directions[0:7].replace('F', '0').replace('B', '1'),
            2
        )
        self.seat = int(
            self.directions[7:].replace('L', '0').replace('R', '1'),
            2
        )
        self.seat_id = self.row * 8 + self.seat

# Read "boarding passes" from data file.
with open('data/day05_binary_boarding-data.txt') as fp:
    data_values = [BoardingPass(line.rstrip()) for line in fp]

# Count number of valid "boarding passes" for Part 1.
max_seat_id = max(v.seat_id for v in data_values)
print(
    f'Highest seat ID on a boarding pass for Part 1: {max_seat_id}'
)


# Part 2: What "boarding passes" are missing in the sequence between the
# smallest and largest "boarding pass" ids from Part 1?


# Find missing "boarding pass" for Part 2.
min_seat_id = min(v.seat_id for v in data_values)
missing_seat_id = (
    set(range(min_seat_id, max_seat_id)) -
    set(v.seat_id for v in data_values)
)
print(
    f'Missing seat IDs for Part 2: {missing_seat_id}'
)
