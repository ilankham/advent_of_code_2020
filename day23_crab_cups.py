""" Solutions for https://adventofcode.com/2020/day/23 """

# import modules used below.
from collections import UserList
from dataclasses import dataclass
from math import prod


# Part 1: After 100 moves in the crab cup game using the starting configuration
# specified in the provided data file, what are the labels of all cups after
# the cup labeled "1"?


# Create data model for crab cup game.
@dataclass
class CrabCub:
    """ Data Model for crab cup """
    label: int
    clockwise_neighbor = None

class CrabCubGame(UserList):
    """ Data Model for crab cup game """

    def __init__(self, initial_labels):
        """ circular linked list w/ dict of nodes for direct access """
        super().__init__(initial_labels)
        self.smallest_cup_label = min(initial_labels)
        self.largest_cup_label = max(initial_labels)
        self.current_cup_label = initial_labels[0]
        self.initial_cup = current_cup = CrabCub(self.current_cup_label)
        self.neighbor_map = {
            self.current_cup_label: current_cup
        }
        for next_cup_label in initial_labels[1:]:
            next_cup = CrabCub(next_cup_label)
            self.neighbor_map[next_cup_label] = next_cup
            current_cup.clockwise_neighbor = next_cup
            current_cup = next_cup
        next_cup.clockwise_neighbor = self.initial_cup

    def __str__(self):
        string_representation_of_linked_list = ''
        current_cup = self.initial_cup
        for _ in range(len(self)):
            string_representation_of_linked_list += f'{current_cup.label} '
            current_cup = current_cup.clockwise_neighbor
        string_representation_of_linked_list += f'-> {current_cup.label}'
        return string_representation_of_linked_list

    def move_cups(self, number_of_moves, number_of_cards_to_pickup):
        """ Update self.neighbor_map using game rules """
        current_cup = self.initial_cup
        for _ in range(number_of_moves):
            picked_up_card_labels = []
            picked_up_card = current_cup.clockwise_neighbor
            for _ in range(number_of_cards_to_pickup):
                picked_up_card_labels.append(picked_up_card.label)
                picked_up_card = picked_up_card.clockwise_neighbor
            current_cup.clockwise_neighbor = picked_up_card
            possible_destination_label = current_cup.label
            while True:
                possible_destination_label -= 1
                if possible_destination_label < self.smallest_cup_label:
                    possible_destination_label += self.largest_cup_label
                if possible_destination_label not in picked_up_card_labels:
                    destination_cup_label = possible_destination_label
                    break
            destination_cup = self.neighbor_map[destination_cup_label]
            destination_cup_neighbor = destination_cup.clockwise_neighbor
            insertion_point = destination_cup
            for label in picked_up_card_labels:
                insertion_point.clockwise_neighbor = self.neighbor_map[label]
                insertion_point = insertion_point.clockwise_neighbor
            insertion_point.clockwise_neighbor = destination_cup_neighbor
            current_cup = current_cup.clockwise_neighbor

    def get_labels_after_cup(self, cup_label, number_of_cup_labels):
        """ Return labels immediately following cup with specified label """
        cup_labels_to_return = []
        current_cup = self.neighbor_map[cup_label].clockwise_neighbor
        for _ in range(number_of_cup_labels):
            cup_labels_to_return.append(current_cup.label)
            current_cup = current_cup.clockwise_neighbor
        return cup_labels_to_return

# Read cup labels from data file.
with open('data/day23_crab_cups-data.txt') as fp:
    cup_labels_for_part1 = [int(digit) for digit in fp.readline().rstrip()]

# Find cup arrangement for Part 1.
crab_cup_game1 = CrabCubGame(cup_labels_for_part1)
crab_cup_game1.move_cups(100, 3)
cup_labels_after_1_for_part1 = crab_cup_game1.get_labels_after_cup(1, 8)
concatenated_cup_labels_for_part1 = ''.join(
    str(digit)
    for digit in cup_labels_after_1_for_part1
)
print(f'Number of cup labels read from data file: {len(cup_labels_for_part1)}')
print(f'Number of cup labels used for Part 1: {len(cup_labels_for_part1)}')
print(
    f'Cups immediately following Cup 1 for Part 1: '
    f'{cup_labels_after_1_for_part1}'
)
print(
    f'Concatenated cup labels for Part 1: '
    f'{concatenated_cup_labels_for_part1}'
)


# Part 2: After 10M moves in the crab cup game using an augmented version of
# the starting configuration specified in the provided data file, what are the
# labels of the first two cups after the cup labeled "1"?


# Find cup arrangement for Part 2.
cup_labels_for_part2 = (
    cup_labels_for_part1 +
    list(range(max(cup_labels_for_part1) + 1, 1_000_001))
)
crab_cup_game2 = CrabCubGame(cup_labels_for_part2)
crab_cup_game2.move_cups(10_000_000, 3)
cup_labels_after_1_for_part2 = crab_cup_game2.get_labels_after_cup(1, 2)
product_of_cup_labels_for_part2 = prod(cup_labels_after_1_for_part2)
print(f'\nNumber of cup labels used for Part 2: {len(cup_labels_for_part2):,}')
print(
    f'Cups immediately following Cup 1 for Part 2: '
    f'{cup_labels_after_1_for_part2}'
)
print(
    f'Product of cup labels for Part 2: '
    f'{product_of_cup_labels_for_part2}'
)
