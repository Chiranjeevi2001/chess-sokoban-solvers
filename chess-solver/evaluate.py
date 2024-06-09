import chess  # Importing the chess library for chess-related functionalities

# Define values for each chess piece
piece_value = {
    chess.PAWN: 100,
    chess.ROOK: 500,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# Define evaluation tables for pawn positioning
pawnEvalWhite = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -20, -20, 10, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0
]
pawnEvalBlack = list(reversed(pawnEvalWhite))  # Reverse the white pawn values for black

# Define evaluation tables for knight positioning
knightEval = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

# Define evaluation tables for bishop positioning
bishopEvalWhite = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
bishopEvalBlack = list(reversed(bishopEvalWhite))  # Reverse the white bishop values for black

# Define evaluation tables for rook positioning
rookEvalWhite = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]
rookEvalBlack = list(reversed(rookEvalWhite))  # Reverse the white rook values for black

# Define evaluation tables for queen positioning
queenEval = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

# Define evaluation tables for king positioning
kingEvalWhite = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]
kingEvalBlack = list(reversed(kingEvalWhite))  # Reverse the white king values for black

# Define endgame king evaluation tables
kingEvalEndGameWhite = [
    50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30,  0,  0,  0,  0, -30, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -20, -10,  0,  0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50
]
kingEvalEndGameBlack = list(reversed(kingEvalEndGameWhite))  # Reverse the white king endgame values for black

# Define move_value function to evaluate the value of a move
def move_value(board: chess.Board, move: chess.Move, endgame: bool) -> float:
    """
    Evaluate the value of a move based on its promotion, capture, and piece position.
    """
    # Check if the move is a promotion
    if move.promotion is not None:
        return -float("inf") if board.turn == chess.BLACK else float("inf")

    # Get the piece at the from_square
    _piece = board.piece_at(move.from_square)
    if _piece:
        # Evaluate the piece's value at the from_square and to_square
        _from_value = evaluate_piece(_piece, move.from_square, endgame)
        _to_value = evaluate_piece(_piece, move.to_square, endgame)
        position_change = _to_value - _from_value
    else:
        raise Exception(f"A piece was expected at {move.from_square}")

    # Check if the move is a capture
    capture_value = 0.0
    if board.is_capture(move):
        capture_value = evaluate_capture(board, move)

    # Calculate the move value
    current_move_value = capture_value + position_change
    if board.turn == chess.BLACK:
        current_move_value = -current_move_value

    return current_move_value

# Define evaluate_capture function to evaluate the value of a capture
def evaluate_capture(board: chess.Board, move: chess.Move) -> float:
    """
    Given a capturing move, weight the trade being made.
    """
    # Check if the move is an en passant
    if board.is_en_passant(move):
        return piece_value[chess.PAWN]
    
    # Get the piece at the to_square and from_square
    _to = board.piece_at(move.to_square)
    _from = board.piece_at(move.from_square)
    
    # Check if both pieces are present
    if _to is None or _from is None:
        raise Exception(
            f"Pieces were expected at _both_ {move.to_square} and {move.from_square}"
        )
    
    # Calculate the capture value
    return piece_value[_to.piece_type] - piece_value[_from.piece_type]

# Define evaluate_piece function to evaluate the value of a piece based on its position
def evaluate_piece(piece: chess.Piece, square: chess.Square, end_game: bool) -> int:
    """
    Evaluate the value of a piece based on its position.
    """
    piece_type = piece.piece_type
    mapping = []
    
    # Determine which evaluation table to use based on the piece type and color
    if piece_type == chess.PAWN:
        mapping = pawnEvalWhite if piece.color == chess.WHITE else pawnEvalBlack
    elif piece_type == chess.KNIGHT:
        mapping = knightEval
    elif piece_type == chess.BISHOP:
        mapping = bishopEvalWhite if piece.color == chess.WHITE else bishopEvalBlack
    elif piece_type == chess.ROOK:
        mapping = rookEvalWhite if piece.color == chess.WHITE else rookEvalBlack
    elif piece_type == chess.QUEEN:
        mapping = queenEval
    elif piece_type == chess.KING:
        # Use endgame piece-square tables if neither side has a queen
        if end_game:
            mapping = (
                kingEvalEndGameWhite
                if piece.color == chess.WHITE
                else kingEvalEndGameBlack
            )
        else:
            mapping = kingEvalWhite if piece.color == chess.WHITE else kingEvalBlack

    # Return the piece's value at the given square
    return mapping[square]

# Define evaluate_board function to evaluate the entire board
def evaluate_board(board: chess.Board) -> float:
    """
    Evaluate the entire board to determine which player is in a most favorable position.
    """
    total = 0
    end_game = check_end_game(board)  # Check if it's the endgame

    # Loop through each square on the board
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue

        # Calculate the value of the piece and add it to the total
        value = piece_value[piece.piece_type] + evaluate_piece(piece, square, end_game)
        total += value if piece.color == chess.WHITE else -value

    return total

# Define check_end_game function to check if it's the endgame
def check_end_game(board: chess.Board) -> bool:
    """
    Check if it's the endgame.
    """
    queens = 0
    minors = 0

    # Loop through each square on the board
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.QUEEN:
            queens += 1
        if piece and (
            piece.piece_type == chess.BISHOP or piece.piece_type == chess.KNIGHT
        ):
            minors += 1

    # Determine if it's the endgame based on the number of queens and minors
    if queens == 0 or (queens == 2 and minors <= 1):
        return True

    return False
