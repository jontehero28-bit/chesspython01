import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for the board
BOARD_SIZE = 8
SQUARE_SIZE = 64  # size of the squares in pixels
BOARD_COLOR_1 = (238, 238, 210)  # light color (cream)
BOARD_COLOR_2 = (118, 150, 86)   # dark color (green)

# Set up the display
screen_size = (BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Chess Board")

# Function to draw the board
def draw_board(screen):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = BOARD_COLOR_1 if (row + col) % 2 == 0 else BOARD_COLOR_2
            pygame.draw.rect(screen, color, pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_board(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
