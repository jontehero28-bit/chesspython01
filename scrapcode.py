 '''
    Problem here is to make "real" chess i need to make a method that checks for checks (as in king is in danger)
    so my method needs to check if move puts king in danger. If it does i should not allow this move.
    https://stackoverflow.com/questions/64825821/boolean-function-to-determine-if-white-king-is-in-check-given-positions-on-a-che 
    https://www.geeksforgeeks.org/check-if-any-king-is-unsafe-on-the-chessboard-or-not/
    also my rules do not work so in future commits i will change them unfortunately
    So to sumarize i need to destinguish all "valid" moves from all the "possible" moves.
    jag hatar schack
    '''
    
    def getValidMoves(self):     #All moves considering checks (king in danger)
        return self.getAllPossibleMoves()
    
    def getAllPossibleMoves(self): #all moves
        
        moves = [Move((6, 4), (4, 4), self.board)]
        for r in range(len(self.board)):  #number of rows =
            for c in range(len(self.board[r])):  #number of col in rows that exist = 8
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteTurnMove) or (turn == "b" and not self.whiteTurnMove):
                    place = self.board[r][c][1]
                    if piece == "P":
                        self.getPawnMoves(r, c, moves)
                    elif piece == "R":
                        self.getRookMoves(r, c, moves)
        return
                        
    #now get all the pawn and rook moves for the pawn located at row, col and add to the moves list. (later move to pawn  and rook subclass)
    
    def getPawnMoves(self, r, c, moves):
        pass
                
    def getRookMoves(self, r, c, moves):
        pass
    # Main game loop
class GameState:
    
    def main(width, height, squareSize):
        timer = pygame.time.Clock()
        ch = ChessBoard()
        fps = 60
        
        validMoves = ch.getValidMoves()     #so gamestate can see if the move that player made is in the list of valid moves that i generate.
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Chess Game")
        moveMade = False    #when move is made use this.
        
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
                    
                    if move in validMoves:
                        ch.MovePiece(move)
                        moveMade = True
                    squareSelected = () #remove information about which square was selected.
                    playerClicks = []   #so it would not be bigger than 2
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z: #undo when z is pressed NOTE pygame key presses are weird af
                        ch.undoMove()
                        moveMade = True
            if moveMade:
                validMoves = ch.getValidMoves()
                moveMade = False
                     
                            
                                     
            Draw.drawBoard(screen, Draw.dimension, squareSize)
            Draw.drawPieces(screen, ch)                       
            timer.tick(fps)
            pygame.display.flip()  # Update the screen