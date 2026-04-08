import random
import time

def print_board(board):
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")

def check_win(board, player):
    win_conditions = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
    return any(all(board[i] == player for i in cond) for cond in win_conditions)

def is_board_full(board):
    return all(spot in ["X", "O"] for spot in board)

def get_available_moves(board):
    return [i for i, spot in enumerate(board) if spot not in ["X", "O"]]

# --- Difficulty: Easy ---
def get_computer_move_easy(board):
    """Picks a random available spot."""
    return random.choice(get_available_moves(board))

# --- Difficulty: Medium ---
def get_computer_move_medium(board):
    """
    Priority:
    1. Take a winning move if available.
    2. Block the human from winning.
    3. Otherwise, play randomly.
    """
    available = get_available_moves(board)

    # Check if AI can win
    for move in available:
        board[move] = "O"
        if check_win(board, "O"):
            board[move] = str(move + 1)
            return move
        board[move] = str(move + 1)

    # Check if human is about to win and block
    for move in available:
        board[move] = "X"
        if check_win(board, "X"):
            board[move] = str(move + 1)
            return move
        board[move] = str(move + 1)

    return random.choice(available)

# --- Difficulty: Hard (Minimax) ---
def minimax(board, is_maximizing):
    """Recursively scores all possible game states."""
    if check_win(board, "O"):
        return 1
    if check_win(board, "X"):
        return -1
    if is_board_full(board):
        return 0

    available = get_available_moves(board)

    if is_maximizing:
        best_score = -float("inf")
        for move in available:
            board[move] = "O"
            score = minimax(board, False)
            board[move] = str(move + 1)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for move in available:
            board[move] = "X"
            score = minimax(board, True)
            board[move] = str(move + 1)
            best_score = min(score, best_score)
        return best_score

def get_computer_move_hard(board):
    """Finds the optimal move using minimax."""
    best_score = -float("inf")
    best_move = None
    for move in get_available_moves(board):
        board[move] = "O"
        score = minimax(board, False)
        board[move] = str(move + 1)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def choose_difficulty():
    """Prompts the player to select a difficulty level."""
    difficulties = {"1": "Easy", "2": "Medium", "3": "Hard"}
    print("\nSelect difficulty:")
    print("  1 - Easy   (random moves)")
    print("  2 - Medium (blocks your wins)")
    print("  3 - Hard   (unbeatable)")
    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in difficulties:
            print(f"\nDifficulty set to: {difficulties[choice]}")
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")

def get_computer_move(board, difficulty):
    """Routes to the correct AI strategy based on difficulty."""
    if difficulty == "1":
        return get_computer_move_easy(board)
    elif difficulty == "2":
        return get_computer_move_medium(board)
    else:
        return get_computer_move_hard(board)

def tic_tac_toe_ai():
    board = [str(i + 1) for i in range(9)]
    print("Welcome to Tic-Tac-Toe vs AI!")
    print("You are 'X', AI is 'O'.")

    difficulty = choose_difficulty()

    for turn in range(9):
        print_board(board)

        if turn % 2 == 0:  # Human's turn
            while True:
                try:
                    move = int(input("Choose your move (1-9): ")) - 1
                    if 0 <= move <= 8 and board[move] not in ["X", "O"]:
                        board[move] = "X"
                        break
                    print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter a number.")
        else:  # AI's turn
            print("AI is thinking...")
            time.sleep(1)
            move = get_computer_move(board, difficulty)
            board[move] = "O"
            print(f"AI chose position {move + 1}")

        if check_win(board, "X"):
            print_board(board)
            print("You beat the machines! Victory!")
            return
        if check_win(board, "O"):
            print_board(board)
            print("The AI wins! Better luck next time.")
            return

    print_board(board)
    print("It's a draw!")

if __name__ == "__main__":
    tic_tac_toe_ai()