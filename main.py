# to run:
# pip install pygame
# python main.py

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
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.setCaption("Tetris")

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



def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, char in enumerate(row):
            if char == '0':
                positions.append((piece.x + j - 2, piece.y + i - 4))

    return positions

def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(GRID_WIDTH) if grid[y][x] == (0, 0, 0)] for y in range(GRID_HEIGHT)]
    accepted_positions = [pos for sublist in accepted_positions for pos in sublist]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions and pos[1] > -1:
            return False
    return True


def draw_window(surface, grid, score=0):
    surface.fill((0, 0, 0))
    # Draw title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', True, (255, 255, 255))
    surface.blit(label, (SCREEN_WIDTH / 2 - label.get_width() / 2, 30))
    
    # Draw score
    font = pygame.font.SysFont('comicsans', 30)
    score_label = font.render(f'Score: {score}', True, (255, 255, 255))
    surface.blit(score_label, (TOP_LEFT_X + GRID_WIDTH * BLOCK_SIZE + 20, TOP_LEFT_Y))
    
    # Draw grid and border
    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0),
                     (TOP_LEFT_X, TOP_LEFT_Y, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE), 5)



def draw_current_piece(surface, piece, grid):
    positions = convert_shape_format(piece)

    for pos in positions:
        x, y = pos
        if y > -1:
            pygame.draw.rect(surface, piece.color,
                             (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            

def clear_rows(grid, locked_positions):
    increment = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            increment += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked_positions[(j, i)]
                except:
                    continue
    if increment > 0:
        for key in sorted(list(locked_positions), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked_positions[newKey] = locked_positions.pop(key)
    return increment



clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.5  # Adjust to change speed


fall_time += clock.get_rawtime()
clock.tick()

# Piece falls every `fall_speed` seconds
if fall_time / 1000 >= fall_speed:
    fall_time = 0
    current_piece.y += 1
    if not valid_space(current_piece, grid) and current_piece.y > 0:
        current_piece.y -= 1
        change_piece = True


locked_positions = {}  # (x, y):(255,0,0)
change_piece = False
grid = create_grid(locked_positions)

def get_shape():
    return Piece(5, 0, random.choice(SHAPES))

# Initialize game variables
locked_positions = {}
grid = create_grid(locked_positions)
current_piece = get_shape()
next_piece = get_shape()
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.5
change_piece = False
running = True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

if change_piece:
    for pos in convert_shape_format(current_piece):
        p = (pos[0], pos[1])
        locked_positions[p] = current_piece.color
    current_piece = next_piece
    next_piece = get_shape()
    change_piece = False


# Initialize Pygame
pygame.init()

# Main loop
running = True
while running:
    fall_time += clock.get_rawtime()
    clock.tick()

    # Fall logic
    if fall_time / 1000 >= fall_speed:
        fall_time = 0
        current_piece.y += 1
        if not valid_space(current_piece, grid) and current_piece.y > 0:
            current_piece.y -= 1
            change_piece = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_piece.x -= 1
                if not valid_space(current_piece, grid):
                    current_piece.x += 1
            elif event.key == pygame.K_RIGHT:
                current_piece.x += 1
                if not valid_space(current_piece, grid):
                    current_piece.x -= 1
            elif event.key == pygame.K_DOWN:
                current_piece.y += 1
                if not valid_space(current_piece, grid):
                    current_piece.y -= 1
            elif event.key == pygame.K_UP:
                current_piece.rotation += 1
                if not valid_space(current_piece, grid):
                    current_piece.rotation -= 1

    if change_piece:
        for pos in convert_shape_format(current_piece):
            p = (pos[0], pos[1])
            locked_positions[p] = current_piece.color

        current_piece = next_piece
        next_piece = get_shape()
        change_piece = False


    grid = create_grid(locked_positions)
    cleared_rows = clear_rows(grid, locked_positions)
    if cleared_rows > 0:
        score += cleared_rows * 100
    draw_window(screen, grid, score)
    draw_current_piece(screen, current_piece, grid)
    pygame.display.update()

    if check_lost(locked_positions):
        running = False

pygame.quit()
sys.exit()