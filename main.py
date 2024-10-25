import pygame
import sys

# Game state variables
score = 0
level = 1
grid = [[0 for _ in range(10)] for _ in range(20)]  # 10 columns x 20 rows grid
current_piece = None
next_piece = None



# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")


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
    screen.fill((0, 0, 0))

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()
