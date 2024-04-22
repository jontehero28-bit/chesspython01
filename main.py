#Import Modules/Libraries
import pygame
import sys

# Initialize
pygame.init()

#Some initial variables
width, height = 512, 512
dimension = 8
squareSize = width // dimension
timer = pygame.time.Clock()
fps = 60

# ChessPiece class that has the main functionalities that all the chesspieces have.
class ChessPiece:
    def __init__(self, symbol, color, imageLoad):
        self.symbol = symbol
        self.color = color
        self.image_path = imageLoad
        self.image = pygame.image.load(imageLoad)
        self.position = None  # To track the piece's position

    def get_symbol(self):
        return self.symbol

    def get_color(self):
        return self.color

    def get_image(self):
        return self.image

    def set_position(self, position):
        self.position = position

class King(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('K', color, image_path)
        self.position = None

    def get_moves(self, board):
        moves = []
        current_row, current_col = self.position

        # Define all possible directions for the King to move
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, 1), (1, -1), (-1, -1)]

        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece_at(new_row, new_col)
                if not target_piece or target_piece.color != self.color:
                    moves.append((new_row, new_col))

        return moves
        pass  # TODO: Needs logic for the "castling" rule


class Queen(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('Q', color, image_path)
        self.position = None

    def get_moves(self, board):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),  # vertical and horizontal movement
                      (1, 1), (-1, 1), (1, -1), (-1, -1)]  # diagonal movement

        current_row, current_col = self.position

        for dr, dc in directions:
            for i in range(1, 8):  # Queen can move up to 7 squares in any direction
                new_row, new_col = current_row + i * dr, current_col + i * dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board.get_piece_at(new_row, new_col)
                    if not target_piece:
                        moves.append((new_row, new_col))
                    elif target_piece.color != self.color:
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return moves
        pass


class Rook(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('R', color, image_path)
        self.position = None

    def get_moves(self, board):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # vertical and horizontal movement

        current_row, current_col = self.position

        for dr, dc in directions:
            for i in range(1, 8):  # Rook can move up to 7 squares in any direction
                new_row, new_col = current_row + i * dr, current_col + i * dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board.get_piece_at(new_row, new_col)
                    if not target_piece:
                        moves.append((new_row, new_col))
                    elif target_piece.color != self.color:
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return moves
        pass


class Bishop(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('B', color, image_path)
        self.position = None

    def get_moves(self, board):
        moves = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]  # diagonal

        current_row, current_col = self.position

        for dr, dc in directions:
            for i in range(1, 8):  # Bishop can move up to 7 squares in any direction
                new_row, new_col = current_row + i * dr, current_col + i * dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board.get_piece_at(new_row, new_col)
                    if not target_piece:
                        moves.append((new_row, new_col))
                    elif target_piece.color != self.color:
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break

        return moves
        pass


class Knight(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('N', color, image_path)
        self.position = None

    def get_moves(self, board):
        moves = []
        offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                   (1, -2), (1, 2), (2, -1), (2, 1)]

        current_row, current_col = self.position

        for dr, dc in offsets:
            new_row, new_col = current_row + dr, current_col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece_at(new_row, new_col)
                if not target_piece or target_piece.color != self.color:
                    moves.append((new_row, new_col))

        return moves
        pass


class Pawn(ChessPiece):
    # Previous move coordinates
    previous_move = None

    def __init__(self, color, image_path):
        super().__init__('P', color, image_path)
        self.position = None
        self.starting_row = None  # Define position and starting row

    def get_moves(self, board):
        moves = []
        current_row, current_col = self.position

        # Define the direction in which the pawn moves based on its color
        direction = 1 if self.color == 'white' else -1

        # Check one square ahead
        if 0 <= current_row + direction < 8:
            if not board.get_piece_at(current_row + direction, current_col):
                moves.append((current_row + direction, current_col))

                # Check two squares ahead if it's the pawn's starting position
                if current_row == self.starting_row and not board.get_piece_at(current_row + 2 * direction,
                                                                               current_col):
                    moves.append((current_row + 2 * direction, current_col))

        # Check diagonal squares for capturing
        for col_offset in [-1, 1]:
            new_row = current_row + direction
            new_col = current_col + col_offset
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece_at(new_row, new_col)
                if target_piece and target_piece.color != self.color:
                    moves.append((new_row, new_col))
                elif target_piece is None and (new_row, new_col) == self.previous_move:
                    moves.append((new_row, new_col))

        return moves
        pass  # TODO: Needs logic for the "en passant" rule

# Additional code for Queen, Rook, Bishop, Knight, and Pawn classes

# Initialize ChessBoard class
class ChessBoard:
    def __init__(self):
        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ]
        # Initialize the position of each piece
        self.initialize_pieces()

    def initialize_pieces(self):
        piece_map = {
            "r": Rook("black", "images/bR.png"),
            "n": Knight("black", "images/bN.png"),
            "b": Bishop("black", "images/bB.png"),
            "q": Queen("black", "images/bQ.png"),
            "k": King("black", "images/bK.png"),
            "p": Pawn("black", "images/bP.png"),
            "R": Rook("white", "images/wR.png"),
            "N": Knight("white", "images/wN.png"),
            "B": Bishop("white", "images/wB.png"),
            "Q": Queen("white", "images/wQ.png"),
            "K": King("white", "images/wK.png"),
            "P": Pawn("white", "images/wP.png"),
        }

        # Set the initial position for each piece
        for row in range(8):
            for col in range(8):
                symbol = self.board[row][col]
                if symbol:
                    piece = piece_map[symbol]
                    piece.set_position((row, col))

    def get_piece_at(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            piece_symbol = self.board[row][col]
            if piece_symbol:
                piece_map = {
                    "r": Rook("black", "images/bR.png"),
                    "n": Knight("black", "images/bN.png"),
                    "b": Bishop("black", "images/bB.png"),
                    "q": Queen("black", "images/bQ.png"),
                    "k": King("black", "images/bK.png"),
                    "p": Pawn("black", "images/bP.png"),
                    "R": Rook("white", "images/wR.png"),
                    "N": Knight("white", "images/wN.png"),
                    "B": Bishop("white", "images/wB.png"),
                    "Q": Queen("white", "images/wQ.png"),
                    "K": King("white", "images/wK.png"),
                    "P": Pawn("white", "images/wP.png"),
                }
                color = "white" if piece_symbol.isupper() else "black"
                piece = piece_map[piece_symbol]
                piece.set_position((row, col))
                return piece
        return None

    def remove_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = ""

# Game loop
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Game")

# Initialize ChessBoard
chess_board = ChessBoard()
selected_piece = None
# Main game loop
while True:
  
    timer.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check if mouse is being clicked and where it is selecting
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked_row = mouse_pos[1] // squareSize
            clicked_col = mouse_pos[0] // squareSize
            clicked_piece = chess_board.get_piece_at(clicked_row, clicked_col)

            if clicked_piece:
                selected_piece = clicked_piece
            else:
                selected_piece = None

            if selected_piece:
                target_piece = chess_board.get_piece_at(clicked_row, clicked_col)
                if target_piece:
                    # Capture the target piece if it exists and it's of the opposite color
                    if target_piece.color != selected_piece.color:
                        # Check if the selected piece is capable of capturing the target piece
                        if (clicked_row, clicked_col) in selected_piece.get_moves(chess_board):
                            target_piece.position = None  # Reset target piece position
                            chess_board.remove_piece(clicked_row, clicked_col)  # Remove the captured piece
                            selected_piece.move_to(clicked_row, clicked_col)

                else:
                    # Move the selected piece to the empty square
                    selected_piece.move_to(clicked_row, clicked_col)

    # Draw the chessboard
    colors = [pygame.Color("beige"), pygame.Color("dark green")]      
    for r in range(dimension): #for 8 rows (dimension = 8)
        for c in range(dimension): #for 8 columns
            color = colors[((r+c)%2)]  #chatGPT hepled me here, (from chatGPT) color = BOARD_COLOR_1 if (row + col) % 2 == 0 else BOARD_COLOR_2v
            pygame.draw.rect(screen, color, pygame.Rect(c*squareSize, r*squareSize, squareSize, squareSize))

    # Draw the pieces
    for row in range(8):
        for col in range(8):
            piece = chess_board.get_piece_at(row, col)
            if piece:
                screen.blit(piece.get_image(), (col * squareSize, row * squareSize))

    pygame.display.flip()  # Update the screen