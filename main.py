from card import *
from deck import *

class Game:
    def __init__(self):
        # Deck
        self.deck = Deck()
        self.deck.shuffle()
        
        # Tableaus
        self.tableaus = []
        for i in range(7):
            pile = {"face_down": [], "face_up": []}
            for j in range(i):
                pile["face_down"].append(self.deck.draw())
            pile["face_up"].append(self.deck.draw()) 
            self.tableaus.append(pile)  
        
        # Foundations
        self.foundations = {"♠": [], "♥": [], "♦": [], "♣": []}

        # Stock / Waste
        self.waste = []
        self.stock = self.deck.deck
        self.deck.deck = []

    def print_state(self):
        print("Tableaus:")
        for pile in self.tableaus:
            for card in pile["face_down"]:
                print("XX", end=" ")
            for card in pile["face_up"]:
                print(card, end=" ")
            print()
        

        for suit in self.foundations:
            if self.foundations[suit]:
                print(f"{suit}: {self.foundations[suit][-1]}")
            else:
                print(f"{suit}: -")


        print("Stock cards remaining:", len(self.stock))
        print(f"Waste: {self.waste[-1] if self.waste else ': -'}")

    def draw_from_stock(self):
        if self.stock:
            card = self.stock.pop()
            self.waste.append(card)
            return card
        else:
            return None

    def can_place_on_tableau(self, card, tableau_index):
        if 0 <= tableau_index < len(self.tableaus):
            tableau = self.tableaus[tableau_index]
            if tableau["face_up"]:
                top_card = tableau["face_up"][-1]
                return (top_card.rank == card.rank + 1 and
                        top_card.color != card.color)
            else:
                if card.rank == 13:
                    return True
        return False

    def move_from_waste_to_tableau(self, tableau_index):
        if 0 <= tableau_index < len(self.tableaus):
            if self.waste:
                card = self.waste[-1]
                if self.can_place_on_tableau(card, tableau_index):
                    self.waste.pop()
                    self.tableaus[tableau_index]["face_up"].append(card)
                    return card
        return None

game = Game()
game.draw_from_stock()
game.print_state()
moved_card = game.move_from_waste_to_tableau(0)
print("Moved card:", moved_card)
game.print_state()
