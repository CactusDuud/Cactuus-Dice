"""
Property of Sage L Mahmud (https://github.com/CactusDuud)
Intended to be implemented alongside discord_dice.py
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

from random import choice, randint

CARD_DICT = {
    'A♣': 'Ace of Clovers', '2♣': 'Two of Clovers', '3♣': 'Three of Clovers', '4♣': 'Four of Clovers',
    '5♣': 'Five of Clovers', '6♣': 'Six of Clovers', '7♣': 'Seven of Clovers', '8♣': 'Eight of Clovers',
    '9♣': 'Nine of Clovers', '10♣': 'Ten of Clovers',
    'J♣': 'Jack of Clovers', 'Q♣': 'Queen of Clovers', 'K♣': 'King of Clovers',
    'A♦': 'Ace of Gems', '2♦': 'Two of Gems', '3♦': 'Three of Gems', '4♦': 'Four of Gems',
    '5♦': 'Five of Gems', '6♦': 'Six of Gems', '7♦': 'Seven of Gems', '8♦': 'Eight of Gems',
    '9♦': 'Nine of Gems', '10♦': 'Ten of Gems',
    'J♦': 'Jack of Gems', 'Q♦': 'Queen of Gems', 'K♦': 'King of Gems',
    'A♥': 'Ace of Hearts', '2♥': 'Two of Hearts', '3♥': 'Three of Hearts', '4♥': 'Four of Hearts',
    '5♥': 'Five of Hearts', '6♥': 'Six of Hearts', '7♥': 'Seven of Hearts', '8♥': 'Eight of Hearts',
    '9♥': 'Nine of Hearts', '10♥': 'Ten of Hearts',
    'J♥': 'Jack of Hearts', 'Q♥': 'Queen of Hearts', 'K♥': 'King of Hearts',
    'A♠': 'Ace of Blades', '2♠': 'Two of Blades', '3♠': 'Three of Blades', '4♠': 'Four of Blades',
    '5♠': 'Five of Blades', '6♠': 'Six of Blades', '7♠': 'Seven of Blades', '8♠': 'Eight of Blades',
    '9♠': 'Nine of Blades', '10♠': 'Ten of Blades',
    'J♠': 'Jack of Blades', 'Q♠': 'Queen of Blades', 'K♠': 'King of Blades',
    'J': '🃏'
}
ORCANA = {
    0: ('The Everyman (Peace)', 'The Madman (Lunacy)'),
    1: ('The Magus (Change)', 'The Occultist (Corruption)'),
    2: ('The High Priestess (Purity)', 'The Concubine (Impurity)'),
    3: ('The Empress (Duty)', 'The Despot (Power)'),
    4: ('The Emperor (Sovereignty)', 'The Slave (Debt)'),
    5: ('The Hierophant (Wisdom)', 'The Librarian (Knowledge)'),
    6: ('The Lover (Love)', 'The Drunkard (Desire)'),
    7: ('The Cleric (Patience)', 'The Soldier (War)'),
    8: ('The Judge (Justice)', 'The Executioner (Indulgence)'),
    9: ('The Monk (Solitude)', 'The Sycophant (Dependence)'),
    10: ('The Hero (Fate)', 'The Gambler (Chance)'),
    11: ('The Giant (Fortitude)', 'The Gnome (Frailty)'),
    12: ('The Muse (Inspiration)', 'The Hanged Man (Punishment)'),
    13: ('The Sapling (Life)', 'The Reaper (Death)'),
    14: ('The Maiden (Temperance)', 'The Leper (Pestilence)'),
    15: ('The Lantern (Light)', 'The Shadow (Darkness)'),
    16: ('The Timekeeper (Time)', 'The Blasted Tree (Adversity)'),
    17: ('The Dwarf (Stance)', 'The Dancer (Confusion)'),
    18: ('The Undine (Memory)', 'The Dreamer (Thought)'),
    19: ('The Salamander (Will)', 'The Vase (Emptiness)'),
    20: ('The Sylph (Breath)', 'The Smoker (Ash)'),
    21: ('The God (Devotion)', 'The Beast (Ignorance)')
}


class DeckException(Exception):
    pass


class Deck:
    def __init__(self, command: str):
        self.last_draws = []
        self.deck = []
        if command == '52' or command == 'standard':
            self.deck_type = 'Standard'
            self.deck = [c for c in CARD_DICT.keys()]
            self.deck.remove('J')
        elif command == '53' or command == 'standard+':
            self.deck_type = 'Standard (w/ Joker)'
            self.deck = [c for c in CARD_DICT.keys()]
        elif command == 'arcana' or command == 'orcana':
            self.deck_type = 'Orcana'
            self.deck = [c for c in ORCANA.keys()]
        elif command == 'orcana+':
            self.deck_type = 'Front Orcana'
            self.deck = [c for c in ORCANA.keys()]
        elif command == 'orcana-':
            self.deck_type = 'Reverse Orcana'
            self.deck = [c for c in ORCANA.keys()]
        else:
            raise DeckException

    def __str__(self):
        return f'{self.deck_type} Deck'

    def __len__(self):
        return len(self.deck)

    def draw(self, num: int):
        """Draws a single card from the deck"""
        for _ in range(0, num):
            if self.deck_type == 'Orcana':
                draw = choice(self.deck)
                self.deck.remove(draw)
                self.last_draws.append((ORCANA[draw])[randint(0, 1)])
            elif self.deck_type == 'Front Orcana':
                draw = choice(self.deck)
                self.deck.remove(draw)
                self.last_draws.append((ORCANA[draw])[0])
            elif self.deck_type == 'Reverse Orcana':
                draw = choice(self.deck)
                self.deck.remove(draw)
                self.last_draws.append((ORCANA[draw])[1])
            else:
                draw = choice(self.deck)
                self.deck.remove(draw)
                self.last_draws.append(draw)

    def results(self, draws: int) -> str:
        """Returns the result of the last draw as a string"""
        if self.deck_type in ('Orcana', 'Front Orcana', 'Reverse Orcana'):
            return_draw = self.last_draws[::-1]
            return_draw = '\n'.join(return_draw[0:draws])
            return f"{return_draw}"
        else:
            return_draw = self.last_draws[::-1]
            return_draw = [f'{c} ({CARD_DICT[c]})' for c in return_draw[0:draws]]
            return_draw = '\n'.join(return_draw)
            return f"{return_draw}"

    def reshuffle(self):
        """Resets the deck"""
        if self.deck_type == 'Standard':
            self.deck = [c for c in CARD_DICT.keys()]
            self.deck.remove('J')
        elif self.deck_type == 'Standard (w/ Joker)':
            self.deck = [c for c in CARD_DICT.keys()]
        elif self.deck_type == 'Orcana':
            self.deck = [c for c in ORCANA.keys()]
        elif self.deck_type == 'Front Orcana':
            self.deck = [c[0] for c in ORCANA.keys()]
        elif self.deck_type == 'Reverse Orcana':
            self.deck = [c[1] for c in ORCANA.keys()]
