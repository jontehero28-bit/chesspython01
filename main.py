#Main class. Will contain user input and displaying CurrentGame object.
#p.g.a det är min första stor projekt i python många anteckningar och kommentarer kommer vara förklaringar och markeringar för mig själv

#Import Modules/Libraries
import pygame

#Import Classes
import engine

#Initialize Modules/Libraries
pygame.init()

#Some initial variables
width = height = 512 #squares 64px64p
dimension = 8 #Board size 8x8
squareSize =  height// dimension #Math/ 8x8 = 64 512/8 = 64. squareSize 64x64 pixels.
images = {} #will use as a dictionary of images. images are taken from here https://drive.google.com/drive/folders/1qH7IQj5lj7o3MQIb5TAZhsDr_5f9p8aq

            
#----------------------------------------------------------------------------------------------------
#I use this way instead of using 
#images["wP] = pygame.image.load("images/wp.png) to save time and space. Found this here:
#https://stackoverflow.com/questions/65431717/efficient-way-to-load-mass-amounts-of-images-in-pygame

#Chess piece images
def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR", "bP", "bR", "bN", "bB", "bK", "bQ", "bB", "bN", "bR"]
    for piece in pieces:    
        images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (squareSize, squareSize))  #scale images to square size
        #write "images[wP]" to acess picture from the library.
#----------------------------------------------------------------------------------------------------
#handle user input and graphics
def main():
    
    #Size for game screen and name and timer
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chess")
    fps = 30
    time = pygame.time.Clock()
    
    squareSelected = () #no square selected in the begining of the game (keeps track of tuple for row and col)
    playerClicks = []   #track two tuples (two positions for row and col) example [(6,4), (4,4)]
    #first click is the square where is the piece that you want to move. Second click is where you want it to move. (Pawn)
    #tuple in python is like a list but they cannot be changed once they have been created. Which means they can be used to store data that will NOT be modified.
    
    gs = engine.GameState()  #gs = gamestate
    loadImages()
    drawGameState(screen, gs)
    
    #GameRunning /press x to quit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:          #elif = if previous condition were not true, try this condition
                location = pygame.mouse.get_pos()                     #(x, y) location for the mouse.
                colClicked = location[0]//squareSize            #so that it would know where player clicked.
                rowClicked = location[1]//squareSize            #problem: it can store only one position where the player clicked. If the player clicks on another piece it will run out of variable space.
                
                if squareSelected == (rowClicked, colClicked):                #user clicked on the same square twice (NOT VALID MOVE)
                    squareSelected = ()                         #deselect
                    playerClicks = ()                           #clear
                    
                else:
                    squareSelected = (rowClicked, colClicked)   #store information about row and col
                    playerClicks.append(squareSelected)         #Both for 1st and 2nd click .append adds a element to the list. In this case data about where player clicked. 
                    
                #now check if this was players 2nd click
                if len(playerClicks) == 2: #len = length. if after second click
                    #if player did 2nd click  change the piece position:
                    move = engine.Move(playerClicks[0], playerClicks[1], gs.board) 
                    print(move.getChessLikeNotation())
                    gs.MovePiece(move)
                    squareSelected = () #remove information about which square was selected.
                    playerClicks = []   #so it would not be bigger than 2
                    
                          
            time.tick(fps)
            pygame.display.flip()     
    
#Graphics and drawing.
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)
 
#d White squares are odd numbers and blacks are squares.
#https://stackoverflow.com/questions/45945254/make-a-88-chessboard-in-pygame-with-python partly followed this
def drawBoard(screen):
    colors = [pygame.Color("beige"), pygame.Color("dark green")]      
    for r in range(dimension): #for 8 rows (dimension = 8)
        for c in range(dimension): #for 8 columns
            color = colors[((r+c)%2)]  #chatGPT hepled me here, (from chatGPT) color = BOARD_COLOR_1 if (row + col) % 2 == 0 else BOARD_COLOR_2v
            pygame.draw.rect(screen, color, pygame.Rect(c*squareSize, r*squareSize, squareSize, squareSize))  #(ChatGPT) pygame.draw.rect(screen, color, pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

#draw pieces  
def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], pygame.Rect(c*squareSize, r*squareSize, squareSize, squareSize))
    
#if __main__ == "__main__":
main()