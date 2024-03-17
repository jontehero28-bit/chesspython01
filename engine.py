#Will contain input and information about current chess game. Determine valid moves (extra. keep a move log)

class GameState():
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
        self.whiteTurnMove = True
        self.moveLog = []
        
    def MovePiece(self, move):
        self.board[move.startRow][move.startCol] = "--" #square behind must be empty
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #i can use the movelog to undo moves
        self.whiteTurnMove = not self.whiteTurnMove #swap player turn
        
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