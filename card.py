class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.color = "red" if suit in ["♥", "♦"] else "black"

    def __str__(self):
        RANK_VALUES = {1:"A", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 10:"10", 11:"J", 12:"Q", 13:"K"}
        return f"{RANK_VALUES[self.rank]}{self.suit}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Card) and self.rank == other.rank and self.suit == other.suit