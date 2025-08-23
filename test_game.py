import unittest
from card import Card
from deck import Deck
from main import Game

class TestSolitaire(unittest.TestCase):

    def setUp(self):
        """Initialize a clean game before each test"""
        self.game = Game()
        # Clear tableaus and stock for controlled testing
        for pile in self.game.tableaus:
            pile["face_down"] = []
            pile["face_up"] = []
        self.game.stock = []
        self.game.waste = []
        for suit in self.game.foundations:
            self.game.foundations[suit] = []

    # ---------------------------------------------
    # Stock / Waste Tests
    # ---------------------------------------------
    def test_draw_from_stock_adds_to_waste(self):
        card = Card(1, "♠")
        self.game.stock.append(card)
        drawn = self.game.draw_from_stock()
        self.assertEqual(drawn, card)
        self.assertEqual(self.game.waste[-1], card)
        self.assertEqual(len(self.game.stock), 0)

    def test_draw_from_empty_stock_returns_none(self):
        self.assertIsNone(self.game.draw_from_stock())

    def test_recycle_stock(self):
        self.game.stock = []
        card1 = Card(1, "♠")
        card2 = Card(2, "♥")
        self.game.waste = [card1, card2]
        drawn = self.game.draw_from_stock()
        self.assertEqual(drawn, card1)
        self.assertEqual(len(self.game.stock), 1)
        self.assertEqual(self.game.stock[0], card2)
        self.assertEqual(len(self.game.waste), 1)
        self.assertEqual(self.game.waste[-1], card1)


    # ---------------------------------------------
    # Tableau placement tests
    # ---------------------------------------------
    def test_king_can_move_to_empty_tableau(self):
        king = Card(13, "♥")
        self.game.waste.append(king)
        success = self.game.move_from_waste_to_tableau(0)
        self.assertTrue(success)
        self.assertEqual(self.game.tableaus[0]["face_up"][-1], king)

    def test_non_king_cannot_move_to_empty_tableau(self):
        queen = Card(12, "♠")
        self.game.waste.append(queen)
        success = self.game.move_from_waste_to_tableau(0)
        self.assertFalse(success)
        self.assertNotIn(queen, self.game.tableaus[0]["face_up"])

    def test_can_place_on_tableau_normal_case(self):
        top_card = Card(7, "♠")
        bottom_card = Card(6, "♥")
        self.game.tableaus[0]["face_up"].append(top_card)
        self.assertTrue(self.game.can_place_on_tableau(bottom_card, 0))

    def test_cannot_place_wrong_color_or_rank(self):
        top_card = Card(7, "♠")
        self.game.tableaus[0]["face_up"].append(top_card)
        invalid_card = Card(6, "♠")  # same color
        self.assertFalse(self.game.can_place_on_tableau(invalid_card, 0))
        invalid_card2 = Card(5, "♥")  # wrong rank
        self.assertFalse(self.game.can_place_on_tableau(invalid_card2, 0))

    # ---------------------------------------------
    # Tableau -> Tableau moves
    # ---------------------------------------------
    def test_move_single_card_tableau_to_tableau(self):
        card = Card(7, "♠")
        moving_card = Card(6, "♥")
        self.game.tableaus[0]["face_up"].append(card)
        self.game.tableaus[1]["face_up"].append(moving_card)
        success = self.game.move_from_tableau_to_tableau(1, 0, 0)
        self.assertTrue(success)
        self.assertEqual(self.game.tableaus[0]["face_up"][-1], moving_card)
        self.assertEqual(len(self.game.tableaus[1]["face_up"]), 0)

    def test_move_multiple_cards_tableau_to_tableau(self):
        self.game.tableaus[0]["face_up"] = [Card(9, "♠")]
        self.game.tableaus[1]["face_up"] = [Card(8, "♥"), Card(7, "♠")]
        success = self.game.move_from_tableau_to_tableau(1, 0, 0)
        self.assertTrue(success)
        self.assertEqual(len(self.game.tableaus[0]["face_up"]), 3)
        self.assertEqual(len(self.game.tableaus[1]["face_up"]), 0)

    def test_flip_face_down_after_moving(self):
        # Setup: face_down pile with 1 card, 1 face_up card
        self.game.tableaus[0]["face_down"].append(Card(5, "♦"))
        self.game.tableaus[0]["face_up"].append(Card(6, "♠"))
        # Move face_up card away
        self.game.tableaus[1]["face_up"].append(Card(7, "♥"))
        success = self.game.move_from_tableau_to_tableau(0, 1, 0)
        self.assertTrue(success)
        # Check that face_down card flipped
        self.assertEqual(len(self.game.tableaus[0]["face_up"]), 1)
        self.assertEqual(self.game.tableaus[0]["face_up"][0].rank, 5)

    # ---------------------------------------------
    # Foundations
    # ---------------------------------------------
    def test_move_ace_to_empty_foundation(self):
        ace = Card(1, "♠")
        self.game.tableaus[0]["face_up"].append(ace)
        success = self.game.move_from_tableau_to_foundation(0)
        self.assertTrue(success)
        self.assertEqual(self.game.foundations["♠"][-1], ace)

    def test_cannot_move_non_ace_to_empty_foundation(self):
        card = Card(5, "♠")
        self.game.tableaus[0]["face_up"].append(card)
        success = self.game.move_from_tableau_to_foundation(0)
        self.assertFalse(success)

    def test_move_to_foundation_normal_case(self):
        self.game.foundations["♠"].append(Card(1, "♠"))
        card = Card(2, "♠")
        self.game.tableaus[0]["face_up"].append(card)
        success = self.game.move_from_tableau_to_foundation(0)
        self.assertTrue(success)
        self.assertEqual(self.game.foundations["♠"][-1], card)

    def test_waste_to_foundation(self):
        self.game.foundations["♠"].append(Card(1, "♠"))
        card = Card(2, "♠")
        self.game.waste.append(card)
        success = self.game.move_from_waste_to_foundation()
        self.assertTrue(success)
        self.assertEqual(self.game.foundations["♠"][-1], card)

    # ---------------------------------------------
    # Foundation -> Tableau
    # ---------------------------------------------
    def test_move_from_foundation_to_tableau(self):
        self.game.foundations["♠"].append(Card(5, "♠"))
        self.game.tableaus[0]["face_up"].append(Card(6, "♥"))
        success = self.game.move_from_foundation_to_tableau("♠", 0)
        self.assertTrue(success)
        self.assertEqual(self.game.tableaus[0]["face_up"][-1].rank, 5)
        self.assertEqual(len(self.game.foundations["♠"]), 0)

    def test_invalid_move_from_foundation(self):
        self.game.foundations["♠"].append(Card(5, "♠"))
        self.game.tableaus[0]["face_up"].append(Card(4, "♥"))
        success = self.game.move_from_foundation_to_tableau("♠", 0)
        self.assertFalse(success)
        self.assertEqual(len(self.game.foundations["♠"]), 1)

if __name__ == "__main__":
    unittest.main()
