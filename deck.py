"""
Property of Sage L Mahmud (https://github.com/CactusDuud)
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

# TODO: Give this a proper name
ORCANA = {
    0: ('The Everyman (Normalcy)', 'The Madman (Lunacy)'),
    1: ('The Magus (Change)', 'The Occultist (Cost)'),
    2: ('The High Priestess (Virtue)', 'The Concubine (Vice)'),
    3: ('The Empress (Duty)', 'The Despot (Power)'),
    4: ('The Emperor (Sovereignty)', 'The Slave (Debt)'),
    5: ('The Hierophant (Truth)', 'The Sycophant (Parallel)'),
    6: ('The Lover (Love)', 'The Drunkard (Desire)'),
    7: ('The Farmer (Patience)', 'The Soldier (War)'),
    8: ('The Judge (Justice)', 'The Dungeon (Consequence)'),
    9: ('The Monk (Focus)', 'The Old One (Isolation)'),
    10: ('The Gambler (Chance)', 'The Executioner (Doom)'),
    11: ('The Giant (Fortitude)', 'The Gnome (Finesse)'),
    12: ('The Muse (Inspiration)', 'The Dreamer (Fantasy)'),
    13: ('The Sprout (Life)', 'The Scythe (Death)'),
    14: ('The Maiden (Purity)', 'The Leper (Pestilence)'),
    15: ('The Lantern (Light)', 'The Shadow (Secret)'),
    16: ('The Sundial (Time)', 'The Blasted Tree (Adversity)'),
    17: ('The Dwarf (Stance)', 'The Current (Flow)'),
    18: ('The Undine (Memory)', 'The Imp (Unconscious)'),
    19: ('The Salamander (Will)', 'The Chicken (Fear)'),
    20: ('The Sylph (Breath)', 'The Crypt (Silence)'),
    21: ('The World (Existence)', 'The Beast (Apathy)')
}


class DeckException(Exception):
    pass


class Deck:
    # TODO: have a short description of every card in 'orcana'
    def __init__(self, command: str):
        self.draws = []
        self.deck = []
        if command == '52' or command == 'standard':
            self.deck_type = 'Standard Deck'
            self.deck = [c for c in CARD_DICT.keys()]
            self.deck.remove('J')
        elif command == '53' or command == 'standard+':
            self.deck_type = 'Standard Deck (w/ Joker)'
            self.deck = [c for c in CARD_DICT.keys()]
        elif command == 'orcana':
            self.deck_type = 'Orcana Deck'
            self.deck = [c for c in ORCANA.keys()]
        elif command == 'orcana+':
            self.deck_type = 'Orcana Deck (Face only)'
            self.deck = [c for c in ORCANA.keys()]
        elif command == 'orcana-':
            self.deck_type = 'Orcana Deck (Mirror only)'
            self.deck = [c for c in ORCANA.keys()]
        else:
            raise DeckException("Unknown deck type")

    def __str__(self):
        return self.deck_type

    def __len__(self):
        return len(self.deck)

    def draw(self, n: int = 1):
        """Draws n cards from the deck"""
        for _ in range(0, n):
            draw = choice(self.deck)
            self.deck.remove(draw)
            if self.deck_type == 'Orcana Deck':
                # Draw a card and randomly decide face or mirror
                self.draws.append((ORCANA[draw])[randint(0, 1)])
            elif self.deck_type == 'Orcana Deck (Face only)':
                # Draw a card and force face
                self.draws.append((ORCANA[draw])[0])
            elif self.deck_type == 'Orcana Deck (Mirror only)':
                # Draw a card and force mirror
                self.draws.append((ORCANA[draw])[1])
            else:
                # Draw a card
                self.draws.append(draw)

    def result(self, n: int = 1) -> str:
        """Returns the result of the last n draws as a string"""
        if 'Orcana' in self.deck_type:
            # 1 to n cards in drawn list in reverse chronological order
            return_draw = '\n'.join(self.draws[::-1][0:n])
            return return_draw
        else:
            # 1 to n cards in drawn list in reverse chronological order w/ formatting
            return_draw = '\n'.join([f'{c} ({CARD_DICT[c]})' for c in self.draws[::-1][0:n]])
            return f"{return_draw}"

    def reshuffle(self):
        """Resets the deck"""
        if self.deck_type == 'Standard Deck':
            self.deck = [c for c in CARD_DICT.keys()]
            self.deck.remove('J')
        elif self.deck_type == 'Standard Deck (w/ Joker)':
            self.deck = [c for c in CARD_DICT.keys()]
        elif 'Orcana' in self.deck_type:
            self.deck = [c for c in ORCANA.keys()]
        else:
            raise DeckException("Deck type lost; please create a new deck")
