from typing import Dict, List, Any  # Importing type hints
import chess  # Importing the chess library for chess board and game functionalities
import sys  # Importing the sys library for system-specific parameters and functions
import time  # Importing the time library for time-related functions
from evaluate import evaluate_board, move_value, check_end_game  # Importing evaluation functions from evaluate module

debug_info: Dict[str, Any] = {}  # Dictionary to store debugging information

MATE_SCORE     = 1000000000  # Constant representing a checkmate score
MATE_THRESHOLD =  999000000  # Threshold for considering a move as almost a checkmate

def next_move(depth: int, board: chess.Board, debug=True) -> chess.Move:
    """
    What is the next best move?
    """
    debug_info.clear()  # Clear the debugging information dictionary
    debug_info["nodes"] = 0  # Initialize nodes count to zero
    t0 = time.time()  # Get current time

    move = minimax_root(depth, board)  # Get the best move using minimax algorithm

    debug_info["time"] = time.time() - t0  # Calculate the time taken
    if debug == True:
        print(f"info {debug_info}")  # Print debugging information
    return move  # Return the best move

def get_ordered_moves(board: chess.Board) -> List[chess.Move]:
    """
    Get legal moves.
    Attempt to sort moves by best to worst.
    Use piece values (and positional gains/losses) to weight captures.
    """
    end_game = check_end_game(board)  # Check if it's the endgame

    # Define a function to order moves based on their value
    def orderer(move):
        return move_value(board, move, end_game)

    # Sort legal moves using the orderer function
    in_order = sorted(
        board.legal_moves, key=orderer, reverse=(board.turn == chess.WHITE)
    )
    return list(in_order)  # Return the ordered moves

def minimax_root(depth: int, board: chess.Board) -> chess.Move:
    """
    What is the highest value move per our evaluation function?
    """
    maximize = board.turn == chess.WHITE  # Determine if we should maximize the score
    best_move = -float("inf") if maximize else float("inf")  # Initialize best move value
    moves = get_ordered_moves(board)  # Get ordered legal moves
    best_move_found = moves[0]  # Initialize best move found

    # Loop through each move and evaluate its score
    for move in moves:
        board.push(move)  # Apply the move to the board
        if board.can_claim_draw():  # Check if draw can be claimed
            value = 0.0  # Set value to 0 if draw can be claimed
        else:
            value = minimax(depth - 1, board, -float("inf"), float("inf"), not maximize)  # Evaluate the move using minimax
        board.pop()  # Undo the move
        # Update best move if a better move is found
        if maximize and value >= best_move:
            best_move = value
            best_move_found = move
        elif not maximize and value <= best_move:
            best_move = value
            best_move_found = move

    return best_move_found  # Return the best move found

def minimax(
    depth: int,
    board: chess.Board,
    alpha: float,
    beta: float,
    is_maximising_player: bool,
) -> float:
    """
    Minimax algorithm to evaluate moves and choose the best one.
    """
    debug_info["nodes"] += 1  # Increment nodes count

    if board.is_checkmate():  # Check if the game is checkmate
        return -MATE_SCORE if is_maximising_player else MATE_SCORE  # Return checkmate score

    elif board.is_game_over():  # Check if the game is over
        return 0  # Return neutral result

    if depth == 0:  # Check if maximum depth is reached
        return evaluate_board(board)  # Return the evaluated board score

    if is_maximising_player:  # If it's maximizing player's turn
        best_move = -float("inf")  # Initialize best move value
        moves = get_ordered_moves(board)  # Get ordered legal moves
        # Loop through each move and evaluate its score
        for move in moves:
            board.push(move)  # Apply the move to the board
            curr_move = minimax(depth - 1, board, alpha, beta, not is_maximising_player)  # Evaluate the move using minimax
            # Adjust scores for faster checkmates
            if curr_move > MATE_THRESHOLD:
                curr_move -= 1
            elif curr_move < -MATE_THRESHOLD:
                curr_move += 1
            best_move = max(best_move, curr_move)  # Update best move value
            board.pop()  # Undo the move
            alpha = max(alpha, best_move)  # Update alpha
            if beta <= alpha:  # Prune if beta is less than or equal to alpha
                return best_move  # Return best move

        return best_move  # Return best move

    else:  # If it's minimizing player's turn
        best_move = float("inf")  # Initialize best move value
        moves = get_ordered_moves(board)  # Get ordered legal moves
        # Loop through each move and evaluate its score
        for move in moves:
            board.push(move)  # Apply the move to the board
            curr_move = minimax(depth - 1, board, alpha, beta, not is_maximising_player)  # Evaluate the move using minimax
            # Adjust scores for faster checkmates
            if curr_move > MATE_THRESHOLD:
                curr_move -= 1
            elif curr_move < -MATE_THRESHOLD:
                curr_move += 1
            best_move = min(best_move, curr_move)  # Update best move value
            board.pop()  # Undo the move
            beta = min(beta, best_move)  # Update beta
            if beta <= alpha:  # Prune if beta is less than or equal to alpha
                return best_move  # Return best move

        return best_move  # Return best move
