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
fps = 60
            
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
    
    #Size for game screen and name
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chess")
    timer = pygame.time.Clock()
    
    gs = engine.GameState()  #gs = gamestate
    loadImages()
    drawGameState(screen, gs)
    
    #GameRunning /press x to quit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            timer.tick(fps)
            pygame.display.flip()     
    
#Graphics and drawing.
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)
 
#draw squares *Remember chess board top left square always white, down left square always black. White squares are odd numbers and blacks are squares.
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