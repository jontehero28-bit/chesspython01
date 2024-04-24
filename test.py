# Import Modules/Libraries
import pygame
import sys

# Initialize
pygame.init()

# Some initial variables were moved to other classes to free up main.py
#Now with additional change the main.py is completely empty. All it does is imports and initializes libraries and runs the code.


# ChessPiece class that has the main functionalities that all the chesspieces have. SUPERCLASS
class ChessPiece:
    def __init__(self, symbol, color, imageLoad):
        self.symbol = symbol
        self.color = color
        self.image_path = imageLoad
        self.image = pygame.image.load(imageLoad)
        self.position = None  # To track the piece's position

    def get_symbol(self):  # return all of the values cuz
        return self.symbol

    def get_color(self):
        return self.color

    def get_image(self):
        return self.image

    def set_position(self, position):
        self.position = position

class King(ChessPiece):  # subclass for all the chesspieces
    def __init__(self, color, image_path):
        super().__init__('K', color, image_path)
        self.position = None

    def get_moves(self, board):
        moves = []
        current_row, current_col = self.position

        # Define all possible directions for the King to move    #NOTE There is better way to do it. King move like a rook or a bishop but only one square at a time
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, 1), (1, -1), (-1, -1)]

        for dr, dc in directions:  # dr= direction row dc= direction column put this together with current row and current col. Put it for the targeted piece
            new_row, new_col = current_row + dr, current_col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                # get the position on the board. newRow and newCol
                targetPiece = board.get_piece_at(new_row, new_col)
                if not targetPiece or targetPiece.color != self.color:
                    moves.append((new_row, new_col))

        return moves
        pass  # TODO: Needs logic for the "castling" rule maybe wont do.


# NOTE there is better way to do it. Queen moves like a bishop or a rook so i could just paste rooks and bishops move there.
class Queen(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('Q', color, image_path)
        self.position = None

    # it should do it as long as it wants. NOTE maybe it does not work.
    def get_moves(self, board):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),  # vertical and horizontal movement
                      (1, 1), (-1, 1), (1, -1), (-1, -1)]  # diagonal movement

        current_row, current_col = self.position

        for dr, dc in directions:  # and so it should go all the way.  #dr= direction row dc= direction column put this together with current row and current col. Put it for the targeted piece
            for i in range(1, 8):  # Queen can move up to 7 squares in any direction
                new_row, new_col = current_row + i * dr, current_col + i * dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board.get_piece_at(new_row, new_col)
                    if not target_piece:
                        moves.append((new_row, new_col))
                    elif target_piece.color != self.color:
                        # exit this loop if condition is met. Fr
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return moves
        pass


# Rook similar to queen. Just copy queens move and change a little. NOTE later i can paste bishop and rook.
class Rook(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('R', color, image_path)
        self.position = None

    def get_moves(self, board):
        moves = []
        # vertical and horizontal movement
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        current_row, current_col = self.position

        for dr, dc in directions:
            for i in range(1, 8):  # Rook can move up to 7 squares in any direction
                new_row, new_col = current_row + i * dr, current_col + i * dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board.get_piece_at(new_row, new_col)
                    if not target_piece:
                        moves.append((new_row, new_col))
                    elif target_piece.color != self.color:
                        # exit this loop if condition is met. Fr
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return moves
        pass


class Bishop(ChessPiece):  # subclass for bishop
    def __init__(self, color, image_path):
        super().__init__('B', color, image_path)
        self.position = None

    def get_moves(self, board):
        moves = []
        # diagonal like moving
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

        current_row, current_col = self.position

        for dr, dc in directions:
            for i in range(1, 8):  # Bishop can move up to 7 squares in any direction
                new_row, new_col = current_row + i * dr, current_col + i * dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board.get_piece_at(
                        new_row, new_col)  # break that
                    if not target_piece:
                        moves.append((new_row, new_col))
                    elif target_piece.color != self.color:
                        # exit this loop if condition is met. Fr
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break

        return moves
        pass


class Knight(ChessPiece):  # subclass knight
    def __init__(self, color, image_path):
        super().__init__('N', color, image_path)
        self.position = None

    # moves in L form. https://stackoverflow.com/questions/19372622/how-do-i-generate-all-of-a-knights-moves
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


class Pawn(ChessPiece):  # subclass for pawns
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


# ChessBoard class 
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
        self.whiteTurnMove = True
        self.MoveLog = []
        self.initialize_pieces()  # initialize the pieces
        
    def MovePiece(self, move):
        self.board[move.startRow][move.startCol] = "" #square behind must be empty
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.MoveLog.append(move) #i can use the movelog to undo moves
        self.whiteTurnMove = not self.whiteTurnMove #swap player turn
        

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

                piece = piece_map[piece_symbol]
                piece.set_position((row, col))
                return piece
        return None

    def remove_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = ""  # remove piece from board
            
class Move():
    
    #making new map key values
    #key : value
    #new keyvalues are: In chess rows are called ranks
    #Columns are called files, So i will change my names and map key from programming language to chess language
    #example: instead of black rook that is on position row 0 col 0 (programming lng) it is on rank 8 file 8 (chess lng)
    #https://impythonist.wordpress.com/2017/01/01/modeling-a-chessboard-and-mechanics-of-its-pieces-in-python/
    #article above helped me alot
    
    rankToRow = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowToRank = {v: k for k, v in rankToRow.items()}          #for loop that reverses the values above other way around
    
    filesToCol = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
    colToFiles = {v: k for k, v in filesToCol.items()}
    
    def __init__(self, startSquare, endSquare, board):
        self.startRow = startSquare[0]               #keep track of the data
        self.startCol = startSquare[1]               #from this row, col
        self.endRow = endSquare[0]                   #to this row, col
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]     #move piece
        self.pieceCaptured = board[self.endRow][self.endCol]      #capture piece
        
    def getChessLikeNotation(self): #notation like in chess (first file then rank)
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol) #i dont understand why i need self here
        
    def getRankFile(self, r, c):
        return self.colToFiles[c] + self.rowToRank[r] #In chess you say first file then rank example a8, d2, f7 this is chess notation
            
# Main game loop
class GameState:
    
    def main(width, height, squareSize):
        timer = pygame.time.Clock()
        ch = ChessBoard()
        
        fps = 60
        selected_piece = None
        
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Chess Game")
        
        squareSelected = ()
        playerClicks = []
        
    
        # Initialize ChessBoard
        
        while True:
            timer.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:                #elif = if previous condition were not true, try this condition
                    location = pygame.mouse.get_pos()                     #(x, y) location for the mouse.
                    colClicked = location[0]//squareSize                  #so that it would know where player clicked.
                    rowClicked = location[1]//squareSize                  #problem: it can store only one position where the player clicked. If the player clicks on another piece it will run out of variable space.
                
                    if squareSelected == (rowClicked, colClicked):                #user clicked on the same square twice (NOT VALID MOVE)
                        squareSelected = ()                         #deselect
                        playerClicks = ()                           #clear
                    
                    else:
                        squareSelected = (rowClicked, colClicked)   #store information about row and col
                        playerClicks.append(squareSelected)         #Both for 1st and 2nd click .append adds a element to the list. In this case data about where player clicked. 
                    
                
                    
                #now check if this was players 2nd click
                if len(playerClicks) == 2: #len = length. if after second click
                    if ch.board[playerClicks[0][0]][playerClicks[0][1]] == "":
                        squareSelected = ()  # Reset the squareSelected value.
                        playerClicks = []  # Reset the playerClicks list.
                    #if player did 2nd click  change the piece position:
                    move = Move(playerClicks[0], playerClicks[1], ch.board) 
                    print(move.getChessLikeNotation())
                    ch.MovePiece(move)
                    squareSelected = () #remove information about which square was selected.
                    playerClicks = []   #so it would not be bigger than 2
                     
                            
                                     
                Draw.drawBoard(screen, Draw.dimension, squareSize)
                Draw.drawPieces(screen, ch, squareSize)                       
                timer.tick(fps)
                pygame.display.flip()  # Update the screen


class Draw:
    width, height = 512, 512
    dimension = 8
    squareSize = width // dimension
    
    def drawBoard(screen, dimension, squareSize):
    # Draw the chessboard
     colors = [pygame.Color("beige"), pygame.Color("dark green")]
     for r in range(dimension):  # for 8 rows (dimension = 8)
         for c in range(dimension):  # for 8 columns
            # chatGPT hepled me here, (from chatGPT) color = BOARD_COLOR_1 if (row + col) % 2 == 0 else BOARD_COLOR_2v
            color = colors[((r+c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(
                c*squareSize, r*squareSize, squareSize, squareSize))
    def drawPieces(screen, ch, squareSize):
    # Draw the pieces
     for row in range(8):
         for col in range(8):
            piece = ch.get_piece_at(row, col)
            if piece:
                screen.blit(piece.get_image(),
                            (col * squareSize, row * squareSize))

if __name__ == "__main__":
    GameState.main(Draw.width, Draw.height, Draw.squareSize)
