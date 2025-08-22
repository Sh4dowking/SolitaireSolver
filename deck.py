from card import Card
import random

class Deck:
    def __init__(self):
        self.deck = self.make_deck()

    def make_deck(self):
        RANKS = list(range(1, 14))
        SUITS = ["♠", "♥", "♦", "♣"]
        return [Card(rank, suit) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        if len(self.deck) > 0:
            return self.deck.pop()
        else:
            return None
