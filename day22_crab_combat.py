""" Solutions for https://adventofcode.com/2020/day/22 """

# import modules used below.
from collections import deque, UserDict
import re


# Part 1: After Combat is played with the Space Card decks in the provided data
# file, what is the winning player's score?


# Create data model for space-card decks and games.
class SpaceCardDeck(deque):
    """ Data Model for a deck of space cards """

    def deal_from_top(self):
        """ Delete and return card from top of deck """
        return self.popleft() if len(self) > 0 else None

    def top_cards(self, number_of_cards):
        """ Return copy of top cards of deck """
        return SpaceCardDeck(list(self)[:number_of_cards])

    def stack_on_bottom(self, card):
        """ Add card to bottom of deck """
        self.append(card)

    def score(self):
        """ Return score for deck using monotonic decreasing values """
        return sum(
            card*value
            for card, value
            in zip(self, range(len(self), 0, -1))
        )

class CombatGame(UserDict):
    """ Data Model for a (possibly recursive) combat game with two players """

    player_number_regex = re.compile(r'Player ([0-9]+):')

    def find_winning_deck(self, recurse=False):
        """ Return winning player and deck for combat game """

        def play_subgame(deck1=None, deck2=None, recursive_game=False):
            """ Return winning player and deck for sub-game """
            if deck1 is None:
                deck1 = self[1].copy()
            if deck2 is None:
                deck2 = self[2].copy()
            previous_game_states = set()
            while deck1 and deck2:
                current_game_state = (tuple(deck1), tuple(deck2))
                if current_game_state in previous_game_states:
                    return 1, deck1
                previous_game_states.add(current_game_state)
                top_card_from_deck1 = deck1.deal_from_top()
                top_card_from_deck2 = deck2.deal_from_top()
                if (
                    recursive_game and
                    len(deck1) >= top_card_from_deck1 and
                    len(deck2) >= top_card_from_deck2
                ):
                    winning_player, _ = play_subgame(
                        deck1=deck1.top_cards(top_card_from_deck1),
                        deck2=deck2.top_cards(top_card_from_deck2),
                        recursive_game=True,
                    )
                    winning_deck = deck1 if winning_player == 1 else deck2
                elif top_card_from_deck1 > top_card_from_deck2:
                    winning_player = 1
                    winning_deck = deck1
                else:
                    winning_player = 2
                    winning_deck = deck2
                if winning_player == 1:
                    winning_deck.stack_on_bottom(top_card_from_deck1)
                    winning_deck.stack_on_bottom(top_card_from_deck2)
                else:
                    winning_deck.stack_on_bottom(top_card_from_deck2)
                    winning_deck.stack_on_bottom(top_card_from_deck1)
            return winning_player, winning_deck
        return play_subgame(recursive_game=recurse)

    @classmethod
    def read_multiple_decks_from_file(cls, file_path, dlm='\n'):
        """ Read multiple Space Card decks from specified file """
        with open(file_path) as fp:
            decks = {}
            for line in fp:
                if (
                        player_number_regex_match := (
                            cls.player_number_regex.fullmatch(line.rstrip())
                        )
                ):
                    player_number = int(player_number_regex_match.group(1))
                    decks[player_number] = SpaceCardDeck()
                    continue
                elif line == dlm:
                    continue
                decks[player_number].append(int(line.strip()))
        return cls(decks)

# Read nutritional labels from data file.
combat_game = CombatGame.read_multiple_decks_from_file(
    'data/day22_crab_combat-data.txt'
)

# Find winning score for Part 1.
part1_winner, part1_winning_deck = combat_game.find_winning_deck(recurse=False)
print(f'Number of Space Card Decks read from data file: {len(combat_game)}')
print(
    f'Number of cards read per player from data file: '
    f'{dict((player,len(deck)) for player, deck in combat_game.items())}'
)
print(f'Winning player for Part 1: Player {part1_winner}')
print(f'Winning score for Part 1: {part1_winning_deck.score()}')


# Part 2: After Recursive Combat is played with the Space Card decks in the
# provided data file, what is the winning player's score?


# Find winning score for Part 2.
part2_winner, part2_winning_deck = combat_game.find_winning_deck(recurse=True)
print(f'\nWinning player for Part 2: Player {part2_winner}')
print(f'Winning score for Part 2: {part2_winning_deck.score()}')
