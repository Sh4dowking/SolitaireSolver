from main import Game
from card import Card
import os
import random
import time

# Move weights for the bot
MOVE_WEIGHTS = {
    "waste_to_foundation": 100,
    "tableau_to_foundation": 100,
    "tableau_to_tableau": 70,
    "foundation_to_tableau": 50,
    "waste_to_tableau": 60,
    "draw": 40
}

def create_test_game():
    game = Game()

    # Clear stock and tableaus
    game.stock = []
    game.waste = []
    for pile in game.tableaus:
        pile["face_down"] = []
        pile["face_up"] = []

    # Let's create a very simple setup:
    # Foundation should be able to receive cards in order immediately

    # Tableaus: only one card each, ordered to allow sequential moves
    # We'll put Ace on tableau 0 (face_up), 2 on tableau 1, etc.
    suits = ["♠", "♥", "♦", "♣"]
    ranks = list(range(1, 14))  # Ace=1 .. King=13

    # Put a single card in each tableau, starting with Ace of Spades in pile 0
    for i in range(7):
        rank = i + 1  # Ace, 2, 3, ...
        suit = suits[i % 4]  # cycle suits
        card = Card(rank, suit)
        game.tableaus[i]["face_up"].append(card)

    # Stock: remaining cards, in order so bot can solve
    for suit in suits:
        for rank in ranks:
            # Skip the ones already on tableaus
            if not any(card.rank == rank and card.suit == suit for pile in game.tableaus for card in pile["face_up"]):
                game.stock.append(Card(rank, suit))

    return game

def play(bot_mode=True, delay=0.01):
    game = create_test_game()

    while True:
        os.system('cls')  # clear console (Windows)
        print("\n=== Current State ===")
        game.print_state()

        if game.is_won():
            print("🎉 You won!")
            break

        legal_moves = game.get_all_legal_moves()

        # Include draw from stock as a legal move
        if game.stock or game.waste:
            legal_moves["draw"] = ["Draw from stock"]

        # Flatten moves
        flat_moves = []
        for move_type, details in legal_moves.items():
            for detail in details:
                if isinstance(detail, tuple):
                    flat_moves.append((move_type, *detail))
                else:
                    flat_moves.append((move_type, detail))

        if not flat_moves:
            print("No more legal moves. Game over.")
            break

        # Detect softlocks
        current_snapshot = game.snapshot()
        if current_snapshot in game.history and game.moves_since_progress >= 50:
            print("Softlock detected! No real progress can be made.")
            break
        else:
            game.history.append(current_snapshot)
            if len(game.history) > 20:  # keep only last 20 snapshots
                game.history.pop(0)

        if bot_mode:
            # Weighted random selection for the bot
            weighted_moves = []
            for move in flat_moves:
                move_type = move[0]
                weight = MOVE_WEIGHTS.get(move_type, 50)
                weighted_moves.append((move, weight))
            moves, weights = zip(*weighted_moves)
            selected_move = random.choices(moves, weights=weights, k=1)[0]
            print(f"\nBot chooses: {selected_move}")
            time.sleep(delay)
        else:
            # Manual mode
            print("\nLegal moves:")
            for idx, move in enumerate(flat_moves):
                print(f"{idx}: {move}")
            choice = input("\nEnter move number (q to quit): ").strip()
            if choice.lower() == 'q':
                print("Exiting game.")
                break
            if not choice.isdigit() or int(choice) not in range(len(flat_moves)):
                print("Invalid choice. Try again.")
                input("Press Enter to continue...")
                continue
            selected_move = flat_moves[int(choice)]

        # Execute the chosen move
        move_type = selected_move[0]
        if move_type == "draw":
            game.draw_from_stock()
        elif move_type == "waste_to_foundation":
            game.move_from_waste_to_foundation()
        elif move_type == "waste_to_tableau":
            game.move_from_waste_to_tableau(selected_move[1])
        elif move_type == "tableau_to_foundation":
            game.move_from_tableau_to_foundation(selected_move[1])
        elif move_type == "tableau_to_tableau":
            game.move_from_tableau_to_tableau(selected_move[1], selected_move[2], selected_move[3])
        elif move_type == "foundation_to_tableau":
            game.move_from_foundation_to_tableau(selected_move[1], selected_move[2])

if __name__ == "__main__":
    #mode = input("Enter 'b' for bot mode or 'm' for manual mode: ").strip().lower()
    #play(bot_mode=(mode == 'b'))
    play()