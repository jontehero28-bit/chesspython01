'''
I know it would be more proper to move all the getPieceMove to designated Chesspiece subclasses but i dont have time to change this right now.
I can komplettera later
also i showed that my rules can be in subclasses in previous commits.
my class diagram will show how it looks right now, today.
'''

# Import Modules/Libraries
import pygame
import sys

# Initialize
pygame.init()

# Some initial variables were moved to other classes to free up main.py
#Now with additional change the main.py is completely empty. All it does is imports and initializes libraries and runs the code.

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
        
piece = ChessPiece("P", "white", "images/wP.png")  # White pawn define for further use

class King(ChessPiece):  # subclass for all the chesspieces
    def __init__(self, color, image_path):
        super().__init__('K', color, image_path)
        self.position = None
        
class Queen(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('Q', color, image_path)
        self.position = None
        
class Rook(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('R', color, image_path)
        self.position = None
        
class Bishop(ChessPiece):  # subclass for bishop
    def __init__(self, color, image_path):
        super().__init__('B', color, image_path)
        self.position = None

class Knight(ChessPiece):  # subclass knight
    def __init__(self, color, image_path):
        super().__init__('N', color, image_path)
        self.position = None
        
class Pawn(ChessPiece):  # subclass for pawns
    # Previous move coordinates
    previous_move = None

    def __init__(self, color, image_path):
        super().__init__('P', color, image_path)
        self.position = None
        self.starting_row = None  # Define position and starting row
        
class ChessBoard():
    
    images = {}
    
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR",],   
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR",]]
        
        self.moveFunctions = {"P": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves, 
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self. getKingMoves}   #kind of a dictionarie
        self.whiteTurnMove = True
        self.moveLog = []
        
    def MovePiece(self, move):
        self.board[move.startRow][move.startCol] = "--" #square behind must be empty
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #i can use the movelog to undo moves
        self.whiteTurnMove = not self.whiteTurnMove #swap player turn after moved piece
    
    def undoMove(self):
        if len(self.moveLog) != 0: #Check that move log is not 0
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved #reset the movved piece.
            self.board[move.endRow][move.endCol] = move.pieceCaptured #reset the captured piece
            self.whiteTurnMove = not self.whiteTurnMove#switch the turn back
    def get_piece_at(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            piece_symbol = self.board[row][col]
            if piece_symbol == "--":  # Check if it's an empty square
                return None  # Return None if the square is empty
            
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
            
            # If the piece symbol is in the map, return the corresponding piece
            if piece_symbol in piece_map:
                piece = piece_map[piece_symbol]
                piece.set_position((row, col))
                return piece
            
        return None
    
    '''
    Problem here is to make "real" chess i need to make a method that checks for checks (as in king is in danger)
    so my method needs to check if move puts king in danger. If it does i should not allow this move.
    https://stackoverflow.com/questions/64825821/boolean-function-to-determine-if-white-king-is-in-check-given-positions-on-a-che 
    https://www.geeksforgeeks.org/check-if-any-king-is-unsafe-on-the-chessboard-or-not/
    also my rules do not work so in future commits i will change them unfortunately
    So to sumarize i need to destinguish all "valid" moves from all the "possible" moves.
    jag hatar schack YOLO
    '''
    
    def getValidMoves(self, piece):     #All moves considering checks (king in danger)
        return self.getAllPossibleMoves(piece)
    
    def getAllPossibleMoves(self, piece): #all moves
        
        moves = []
        for r in range(len(self.board)):  #number of rows =
            for c in range(len(self.board[r])):  #number of col in rows that exist = 8
                turn = self.board[r][c][0]                      #crazy lifehack NOTE [0] is for the first letter in the board.
                if (turn == "w" and self.whiteTurnMove) or (turn == "b" and not self.whiteTurnMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves
            
    #now get all the pawn and rook moves for the pawn located at row, col and add to the moves list. (later move to pawn  and rook subclass)
    def getPawnMoves(self, r, c, moves): #Pawns are the hardest to make because bP and wP move differently and they have the most special rules for them
        
        if self.whiteTurnMove: #if it is white pawns turn i print out possible moves for pawns
            
            if self.board[r-1][c] == "--": #1square pawn move = check if square is empty NOTE adds to moves list
                moves.append(Move((r, c), (r-1, c), self.board)) #(Move((startSquare), (endSquare), board))
                
                if r == 6 and self.board[r-2][c] == "--":   #2square pawn move r == 6 startrow for all whiteP
                    moves.append(Move((r, c), (r-2, c), self.board))    #adds to moves list
            
            if c-1 >= 0:    #check so piece would not go outside of the board if it wants to capture NOTE captures to the left
                if self.board[r-1][c-1][0] == "b":   #check if enemy piece is there. [0] = "b"
                    moves.append(Move((r, c), (r-1, c-1), self.board))    #adds to moves list
            
            if c+1 < 7:  #captures to the right
                if self.board[r-1][c+1][0] == "b":  #enemy piece
                    moves.append(Move((r, c), (r-1, c+1), self.board))    #adds to moves list
                    
            else: #black pawn moves very similar
                if self.board[r+1][c] == "--": #1square pawn move = check if square is empty NOTE adds to moves list
                    moves.append(Move((r, c), (r+1, c), self.board)) #(Move((startSquare), (endSquare), board))
                
                if r == 1 and self.board[r+2][c] == "--":   #2square pawn move r == 1 startrow for all blackP
                    moves.append(Move((r, c), (r-2, c), self.board))    #adds to moves list
            
            if c-1 >= 0:    #check so piece would not go outside of the board if it wants to capture NOTE captures to the left
                if self.board[r+1][c-1][0] == "w":   #check if enemy piece is there. [0] = "2"
                    moves.append(Move((r, c), (r+1, c-1), self.board))    #adds to moves list
            
            if c+1 <= 7:  #captures to the right
                if self.board[r+1][c+1][0] == "w":  #enemy piece white
                    moves.append(Move((r, c), (r+1, c+1), self.board))    #adds to moves list
                    
        #add pawn promotions later NOTE i dont have time to do this before this project is due.
                    
                
    def getRookMoves(self, r, c, moves):   #pretty similar to my old rule set
        directions = ((-1, 0,), (0, -1), (1, 0), (0, 1)) #up, left, down, right
        enemyColor = "b" if self.whiteTurnMove else "w"
        
        for d in directions:
            for i in range (1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #piece is on board
                    endPiece = self.board[endRow][endRow]
                    if endPiece == "--":     #empty space
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:   #enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:   #friendly piece valid
                        break
                else:  #piece off board
                    break
    
    #NOTE https://impythonist.wordpress.com/2017/01/01/modeling-a-chessboard-and-mechanics-of-its-pieces-in-python/
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteTurnMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:   #not an ally piece
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    
    def getBishopMoves(self, r, c, moves):   #also similar to rook and my old rule scheme and thanks to that i save a lot of time.
        directions = ((-1, -1,), (-1, 1), (1, -1), (1, 1)) #diagonals, X
        enemyColor = "b" if self.whiteTurnMove else "w"
        for d in directions:
            for i in range (1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty
                        moves.append(Move(r, c), (endRow, endCol), self.board)
                    elif endPiece[0] == enemyColor:    #enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #friendly piece yo
                       break
                else:   #off board yo
                    break
    
    def getQueenMoves(self, r, c, moves):  #rook + bishop = queen. fw wit dat
        self.getRookMoves(r, c, moves)     
        self.getBishopMoves(r, c, moves)
    
    def getKingMoves(self, r, c, moves): #kinda ish simillar to knight moves
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteTurnMove else "b"
        for i in range(8):
            endRow = r + kingMoves [i][0]
            endCol = c + kingMoves [i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #empty or enemypiece
                    moves.append(Move((r, c), (endRow, endCol), self.board))
        
        
    
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
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol #Check note
        
    '''
    Explaining moveID: by debugging this i create a bunch of zeroes that have id for diffrent moves
    NOTE: Move a black pawn from A7 to A6. moveID will be 1020. 1 is startrow 0 is startcolumn and 2 is endrow and 0 is end col
    
    If i understand correctly i need to override equals cuz i use class and methods system.
    If i used string or int i would not have to do that. https://www.geeksforgeeks.org/method-overriding-in-python/ 
    '''
    def __eq__(self, other):    #compare an object to another object
        if isinstance (other, Move):         #return if object is an instance of a class (or subclass)
            return self.moveID == other.moveID
        return False
        
    def getChessLikeNotation(self): #notation like in chess (first file then rank)
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol) #i dont understand why i need self here
        
    def getRankFile(self, r, c):
        return self.colToFiles[c] + self.rowToRank[r] #In chess you say first file then rank example a8, d2, f7 this is chess notation

# Main game loop
class GameState:
    
    def main(width, height, squareSize, piece):
        timer = pygame.time.Clock()
        ch = ChessBoard()
        fps = 60
        
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Chess Game")
        
        validMoves = ch.getValidMoves(piece) #gamestate can see if the move that player made is in the list of valid moves that i generate.
        moveMade = False                #when move is made use this. Use this just so i regenerate the function above when i need to and not every frame /ps smart code is boring
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
                    if ch.board[playerClicks[0][0]][playerClicks[0][1]] == "--":
                        squareSelected = ()  # Reset the squareSelected value.
                        playerClicks = []  # Reset the playerClicks list.
                    #if player did 2nd click  change the piece position:
                    move = Move(playerClicks[0], playerClicks[1], ch.board) 
                    print(move.getChessLikeNotation())   
                    if move in validMoves:    #checka att det finns i validmoves
                        ch.MovePiece(move)
                        print("White turn move:", ch.whiteTurnMove)  # print the current turn
                        moveMade = True
                        
                    squareSelected = () #remove information about which square was selected.
                    playerClicks = []   #so it would not be bigger than 2
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z: #undo when z is pressed NOTE pygame key presses are weird af
                        ch.undoMove()
                        moveMade = True
                        
            if moveMade:
                validMoves = ch.getValidMoves(piece)  #if move was made generate new set of valid moves.
                moveMade = False
          
            Draw.drawBoard(screen, Draw.dimension, squareSize)
            Draw.drawPieces(screen, ch, squareSize)                       
            timer.tick(fps)
            pygame.display.flip()  # Update the screen
            
class Draw:   #Responsible for all drawing
    width, height = 512, 512
    dimension = 8
    squareSize = width // dimension
    images = {}
     
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

    GameState.main(Draw.width, Draw.height, Draw.squareSize, piece)
                