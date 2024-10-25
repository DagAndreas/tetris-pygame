import pygame
import sys

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
    
    # Optional: Fill the screen with black
    screen.fill((0, 0, 0))

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()
