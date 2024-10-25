import pygame
import sys

# Game state variables
score = 0
level = 1
grid = [[0 for _ in range(10)] for _ in range(20)]  # 10 columns x 20 rows grid
current_piece = None
next_piece = None

import random

# Tetromino shapes represented as multi-dimensional arrays
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# List of shapes and their respective colors
SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [
    (0, 255, 0),    # S - Green
    (255, 0, 0),    # Z - Red
    (0, 255, 255),  # I - Cyan
    (255, 255, 0),  # O - Yellow
    (0, 0, 255),    # J - Blue
    (255, 165, 0),  # L - Orange
    (128, 0, 128)   # T - Purple
]

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x  # X position on the grid
        self.y = y  # Y position on the grid
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0  # Current rotation index

# Set up the display
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Grid dimensions and block size
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

# Top-left position of the play area
TOP_LEFT_X = (SCREEN_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - GRID_HEIGHT * BLOCK_SIZE - 20

def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid


def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x],
                             (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # Draw grid lines
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128),
                         (TOP_LEFT_X, TOP_LEFT_Y + i * BLOCK_SIZE),
                         (TOP_LEFT_X + GRID_WIDTH * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE))
    for j in range(GRID_WIDTH + 1):
        pygame.draw.line(surface, (128, 128, 128),
                         (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y),
                         (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + GRID_HEIGHT * BLOCK_SIZE))



# Initialize Pygame
pygame.init()



# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle key presses
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("Left key pressed")
            elif event.key == pygame.K_RIGHT:
                print("Right key pressed")
            elif event.key == pygame.K_DOWN:
                print("Down key pressed")
            elif event.key == pygame.K_UP:
                print("Up key pressed")
    
    # Optional: Fill the screen with black
    # screen.fill((0, 0, 0))

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()
