import chess  # Import the chess library for chess board and game functionalities
import argparse  # Import the argparse library for command-line argument parsing
from movegeneration import next_move  # Import the next_move function from movegeneration module

def start():
    """
    Start the command line user interface.
    """
    board = chess.Board()  # Create a new chess board object
    user_side = (
        chess.WHITE if input("Choose color enter 'w' for white or 'b' for black:\n") == "w" else chess.BLACK  # Ask user to choose side: white or black
    )

    if user_side == chess.WHITE:
        print(render(board))  # Render and display the initial chess board
        board.push(get_move(board))  # Get user's move and apply it to the board

    # Continue the game until it's over
    while not board.is_game_over():
        board.push(next_move(get_depth(), board, debug=False))  # Get AI's move and apply it to the board
        print(render(board))  # Render and display the updated chess board
        board.push(get_move(board))  # Get user's move and apply it to the board

    print(f"\nResult: [w] {board.result()} [b]")  # Display the game result

def render(board: chess.Board) -> str:
    """
    Print a side-relative chess board with special chess characters.
    """
    board_string = list(str(board))  # Convert the board to string and convert it to a list
    uni_pieces = {  # Dictionary mapping chess piece notations to Unicode chess symbols
        "R": "♖",
        "N": "♘",
        "B": "♗",
        "Q": "♕",
        "K": "♔",
        "P": "♙",
        "r": "♜",
        "n": "♞",
        "b": "♝",
        "q": "♛",
        "k": "♚",
        "p": "♟",
        ".": "·",
    }
    for idx, char in enumerate(board_string):  # Loop through the board string
        if char in uni_pieces:
            board_string[idx] = uni_pieces[char]  # Replace chess piece notations with Unicode symbols
    ranks = ["1", "2", "3", "4", "5", "6", "7", "8"]  # List of chess ranks
    display = []
    for rank in "".join(board_string).split("\n"):  # Loop through the board ranks
        display.append(f"  {ranks.pop()} {rank}")  # Add rank number and board rank to display list
    if board.turn == chess.BLACK:
        display.reverse()  # Reverse the display list if it's Black's turn
    display.append("    a b c d e f g h")  # Add file labels to the display list
    return "\n" + "\n".join(display)  # Return the formatted board as a string

def get_move(board: chess.Board) -> chess.Move:
    """
    Try (and keep trying) to get a legal next move from the user.
    Play the move by mutating the game board.
    """
    legal_moves = list(board.legal_moves)  # Get the list of legal moves
    
    if not legal_moves:  # Check if there are no legal moves available
        print("No legal moves available. Game over.")
        exit()  # Exit the program
    
    move = input(f"\nEnter your move (e.g. {legal_moves[0]}):\n")  # Ask user for their move

    for legal_move in legal_moves:  # Loop through legal moves
        if move == str(legal_move):  # Check if user's input matches a legal move
            return legal_move  # Return the legal move
    
    print("Invalid move. Try again.")
    return get_move(board)  # If the input is not a legal move, ask again


def get_depth() -> int:
    parser = argparse.ArgumentParser()  # Create an ArgumentParser object
    parser.add_argument("--depth", default=3, help="provide an integer (default: 3)")  # Add a command-line argument for depth
    args = parser.parse_args()  # Parse command-line arguments
    return max([1, int(args.depth)])  # Return the maximum of 1 and the parsed depth value

if __name__ == "__main__":
    try:
        start()  # Start the game
    except KeyboardInterrupt:
        pass  # Handle KeyboardInterrupt to exit the game gracefully
