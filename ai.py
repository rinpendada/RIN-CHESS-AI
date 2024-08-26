import chess
import chess.svg
import cairosvg
from PIL import Image
import io

# list to store each frames image
frames = []

def save_frame(board):
    # Generate SVG data and convert to PNG
    svg_data = chess.svg.board(board)
    png_data = cairosvg.svg2png(bytestring=svg_data.encode('utf-8'))
    image = Image.open(io.BytesIO(png_data))
    frames.append(image)

# Function to save the current board as an image using cairosvg
def save_board_image(board, output_filename="board.png"):
    # Generate SVG data of the board
    svg_data = chess.svg.board(board)
    
    # Convert the SVG data to a PNG image using cairosvg
    cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), write_to=output_filename)

# Basic evaluation function (e.g., material count)
def evaluate_board(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # King is invaluable
    }
    
    score = 0
    for piece in chess.PIECE_TYPES:
        score += len(board.pieces(piece, chess.WHITE)) * piece_values[piece]
        score -= len(board.pieces(piece, chess.BLACK)) * piece_values[piece]
    
    return score

# Alpha-Beta Pruning minimax function
def minimax_alpha_beta(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    if is_maximizing:
        max_eval = float('-inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        if depth == initial_depth:  # Only return the move at the root level
            return best_move
        return max_eval
    else:
        min_eval = float('inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cutoff
        if depth == initial_depth:  # Only return the move at the root level
            return best_move
        return min_eval

# Function to choose the best move
initial_depth = 3

def choose_best_move(board):
    return minimax_alpha_beta(board, initial_depth, float('-inf'), float('inf'), True)

# Initialize the board
board = chess.Board()

# Main game loop
while not board.is_game_over():
    print(board)
    
    # White move
    move = choose_best_move(board)
    board.push(move)
    save_frame(board)  # Save after White's move
    
    # Black move
    if not board.is_game_over():
        move = choose_best_move(board)
        board.push(move)
        save_frame(board)  # Save after Black's move

# Save the frames as a GIF
frames[0].save("game.gif", save_all=True, append_images=frames[1:], duration=500, loop=0)

print("Game over!")
print(board.result())
