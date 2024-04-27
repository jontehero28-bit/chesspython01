# Import Modules/Libraries
import pygame
import sys

# Initialize
pygame.init()

# ChessPiece Class
class ChessPiece:
    def __init__(self, symbol, color, image_path):
        self.symbol = symbol
        self.color = color
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        self.position = None

    def set_position(self, position):
        self.position = position

# Piece Subclasses with Movement Functions
class Pawn(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('P', color, image_path)
        self.starting_row = 6 if color == 'white' else 1
    
    def get_moves(self, r, c, board):
        moves = []
        if self.color == 'white':
            # 1-square move
            if board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), board))
            # 2-square move if on starting row
            if r == self.starting_row and board[r-2][c] == "--":
                moves.append(Move((r, c), (r-2, c), board))
            # Capture moves
            if c - 1 >= 0 and board[r-1][c-1][0] == 'b':
                moves.append(Move((r, c), (r-1, c-1), board))
            if c + 1 < 8 and board[r-1][c+1][0] == 'b':
                moves.append(Move((r, c), (r-1, c+1), board))
        else:  # Black pawns
            if board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), board))
            if r == self.starting_row and board[r+2][c] == "--":
                moves.append(Move((r, c), (r+2, c), board))
            if c - 1 >= 0 and board[r+1][c-1][0] == 'w':
                moves.append(Move((r, c), (r+1, c-1), board))
            if c + 1 < 8 and board[r+1][c+1][0] == 'w':
                moves.append(Move((r, c), (r+1, c+1), board))
        
        return moves

class Rook(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('R', color, image_path)
    
    def get_moves(self, r, c, board):
        moves = []
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        enemyColor = "b" if self.color == "white" else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), board))
                        break
                    else:
                        break
                else:
                    break
        return moves

class Bishop(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('B', color, image_path)
    
    def get_moves(self, r, c, board):
        moves = []
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.color == "white" else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), board))
                        break
                    else:
                        break
                else:
                    break
        return moves

class Queen(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('Q', color, image_path)
    
    def get_moves(self, r, c, board):
        moves = []
        # Queen moves are a combination of Rook and Bishop
        moves.extend(Rook(self.color, "").get_moves(r, c, board))
        moves.extend(Bishop(self.color, "").get_moves(r, c, board))
        return moves

class King(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('K', color, image_path)
    
    def get_moves(self, r, c, board):
        moves = []
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.color == "white" else "b"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), board))
        return moves

class Knight(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('N', color, image_path)
    
    def get_moves(self, r, c, board):
        moves = []
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.color == "white" else "b"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), board))
        return moves

# ChessBoard Class with Updated getValidMoves
class ChessBoard:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.whiteTurnMove = True
        self.moveLog = []
    
    def MovePiece(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteTurnMove = not self.whiteTurnMove
    
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteTurnMove = not self.whiteTurnMove
    
    def get_piece_at(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            piece_symbol = self.board[row][col]
            if piece_symbol == "--":
                return None
            piece_map = {
                "bR": Rook("black", "images/bR.png"),
                "bN": Knight("black", "images/bN.png"),
                "bB": Bishop("black", "images/bB.png"),
                "bQ": Queen("black", "images/bQ.png"),
                "bK": King("black", "images/bK.png"),
                "bP": Pawn("black", "images/bP.png"),
                "wR": Rook("white", "images/wR.png"),
                "wN": Knight("white", "images/wN.png"),
                "wB": Bishop("white", "images/wB.png"),
                "wQ": Queen("white", "images/wQ.png"),
                "wK": King("white", "images/wK.png"),
                "wP": Pawn("white", "images/wP.png"),
            }
            if piece_symbol in piece_map:
                piece = piece_map[piece_symbol]
                piece.set_position((row, col))
                return piece
        return None
    
    def getValidMoves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.get_piece_at(r, c)
                if piece:
                    if (piece.color == "white" and self.whiteTurnMove) or (piece.color == "black" and not self.whiteTurnMove):
                        moves.extend(piece.get_moves(r, c, self.board))
        return moves

# Move Class
class Move:
    def __init__(self, startSquare, endSquare, board):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    
    def __eq__(self, other):
        return isinstance(other, Move) and self.moveID == other.moveID
    
    def getChessLikeNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return f"{self.colToFiles[c]}{self.rowToRank[r]}"

# Draw Class for Drawing the Board and Pieces
class Draw:
    width, height = 512, 512
    dimension = 8
    squareSize = width // dimension
    images = {}
     
    def drawBoard(screen, dimension, squareSize):
        colors = [pygame.Color("beige"), pygame.Color("dark green")]
        for r in range(dimension):
            for c in range(dimension):
                color = colors[((r + c) % 2)]
                pygame.draw.rect(screen, color, pygame.Rect(
                    c * squareSize, r * squareSize, squareSize, squareSize))
    
    def drawPieces(screen, chess_board, squareSize):
        for r in range(8):
            for c in range(8):
                piece = chess_board.get_piece_at(r, c)
                if piece:
                    screen.blit(piece.get_image(), (c * squareSize, r * squareSize))

# Main Game Loop
class GameState:
    def main(width, height, squareSize):
        timer = pygame.time.Clock()
        chess_board = ChessBoard()
        fps = 60
        
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Chess Game")
        
        validMoves = chess_board.getValidMoves()
        moveMade = False
        squareSelected = ()
        playerClicks = []
        
        while True:
            timer.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    colClicked = location[0] // squareSize
                    rowClicked = location[1] // squareSize
                
                    if squareSelected == (rowClicked, colClicked):
                        squareSelected = ()  # deselect
                        playerClicks = []  # clear clicks
                    
                    else:
                        squareSelected = (rowClicked, colClicked)
                        playerClicks.append(squareSelected)
            
                # Check if it was a second click
                if len(playerClicks) == 2:
                    startSquare = playerClicks[0]
                    endSquare = playerClicks[1]
                    move = Move(startSquare, endSquare, chess_board.board)
                    
                    if chess_board.get_piece_at(startSquare[0], startSquare[1]):
                        if move in validMoves:
                            chess_board.MovePiece(move)
                            moveMade = True
                        
                    squareSelected = ()
                    playerClicks = []
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:  # Undo when 'z' is pressed
                        chess_board.undoMove()
                        moveMade = True
                        
            if moveMade:
                validMoves = chess_board.getValidMoves()  # regenerate valid moves
                moveMade = False
          
            Draw.drawBoard(screen, Draw.dimension, squareSize)
            Draw.drawPieces(screen, chess_board, squareSize)                       
            timer.tick(fps)
            pygame.display.flip()  # Update the screen

if __name__ == "__main__":
    GameState.main(Draw.width, Draw.height, Draw.squareSize)
