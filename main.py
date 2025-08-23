from card import *
from deck import *

class Game:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.tableaus = []
        for i in range(7):
            pile = {"face_down": [], "face_up": []}
            for j in range(i):
                pile["face_down"].append(self.deck.draw())
            pile["face_up"].append(self.deck.draw()) 
            self.tableaus.append(pile)  
        self.foundations = {"♠": [], "♥": [], "♦": [], "♣": []}
        self.waste = []
        self.stock = self.deck.deck
        self.deck.deck = []

    def print_state(self):
        print("Tableaus:")
        for idx, pile in enumerate(self.tableaus):
            print(f"Pile {idx+1}: ", end="")
            for card in pile["face_down"]:
                print("XX", end=" ")
            for card in pile["face_up"]:
                print(card, end=" ")
            print()
        
        print("\nFoundations:")
        for suit in self.foundations:
            if self.foundations[suit]:
                print(f"{suit}: ", end="")
                for card in self.foundations[suit]:
                    print(card, end=" ")
                print()
            else:
                print(f"{suit}: -")
        
        print("\nStock cards remaining:", len(self.stock))
        print("Top of Waste:", self.waste[-1] if self.waste else "-")
        print("-"*40)


    def recycle_stock(self):
        if self.waste:
            self.stock = self.waste[:]  # keep the same order
            self.waste = []

    def draw_from_stock(self):
        if not self.stock:
            self.recycle_stock()
        
        if self.stock:
            card = self.stock.pop(0)  # remove the first card (FIFO)
            self.waste.append(card)
            return card
        return None

    def can_place_on_tableau(self, card, tableau_index):
        if 0 <= tableau_index < len(self.tableaus):
            tableau = self.tableaus[tableau_index]
            if tableau["face_up"]:
                top_card = tableau["face_up"][-1]
                return top_card.rank == card.rank + 1 and top_card.color != card.color
            elif not tableau["face_up"] and not tableau["face_down"]:
                return card.rank == 13
        return False

    def move_from_waste_to_tableau(self, tableau_index):
        if 0 <= tableau_index < len(self.tableaus):
            if self.waste:
                card = self.waste[-1]
                if self.can_place_on_tableau(card, tableau_index):
                    self.waste.pop()
                    self.tableaus[tableau_index]["face_up"].append(card)
                    return True
        return False

    def move_from_tableau_to_tableau(self, from_tableau, to_tableau, start_index):
        if 0 <= from_tableau < len(self.tableaus) and 0 <= to_tableau < len(self.tableaus):
            if start_index < len(self.tableaus[from_tableau]["face_up"]):
                moving_card = self.tableaus[from_tableau]["face_up"][start_index]
                if self.can_place_on_tableau(moving_card, to_tableau):
                    for i in range(start_index, len(self.tableaus[from_tableau]["face_up"])):
                        self.tableaus[to_tableau]["face_up"].append(self.tableaus[from_tableau]["face_up"][i])  
                    del self.tableaus[from_tableau]["face_up"][start_index:]
                    if self.tableaus[from_tableau]["face_down"] and not self.tableaus[from_tableau]["face_up"]:
                        self.tableaus[from_tableau]["face_up"].append(self.tableaus[from_tableau]["face_down"].pop())                   
                    self.flip_next_card_if_needed(from_tableau)
                    return True
        return False
    
    def can_move_to_foundation(self, card):
        foundation = self.foundations[card.suit]
        if not foundation:
            return card.rank == 1
        return card.rank == foundation[-1].rank + 1

    def move_from_tableau_to_foundation(self, tableau_index):
        if 0 <= tableau_index < len(self.tableaus) and self.tableaus[tableau_index]["face_up"]:
            card = self.tableaus[tableau_index]["face_up"][-1]
            if self.can_move_to_foundation(card):
                card = self.tableaus[tableau_index]["face_up"].pop()
                self.foundations[card.suit].append(card)
                self.flip_next_card_if_needed(tableau_index)
                return True
        return False
    
    def move_from_waste_to_foundation(self):
        if self.waste:
            card = self.waste[-1]
            if self.can_move_to_foundation(card):
                card = self.waste.pop()
                self.foundations[card.suit].append(card)
                return True
        return False
    
    def move_from_foundation_to_tableau(self, suit, tableau_index):
        if 0 <= tableau_index < len(self.tableaus):
            if suit in self.foundations and self.foundations[suit]:
                card = self.foundations[suit][-1]
                if self.can_place_on_tableau(card, tableau_index):
                    card = self.foundations[suit].pop()
                    self.tableaus[tableau_index]["face_up"].append(card)
                    return True
        return False
    
    def flip_next_card_if_needed(self, tableau_index):
        tableau = self.tableaus[tableau_index]
        if not tableau["face_up"] and tableau["face_down"]:
            tableau["face_up"].append(tableau["face_down"].pop())