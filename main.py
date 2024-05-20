import pygame
import random
import math

# Initialize the pygame features
pygame.init()

FPS = 60
WIDTH, HEIGHT = 800, 800
ROWS = 4
COLS = 4

# How large a tile is going to be.
RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

FONT = pygame.font.SysFont("comicsans", 60, bold=True)
# Speed at which the tiles will move (move velocity).
MOVE_VEL = 20

# Create a pygame window.
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)
    
    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)
    
    # Draw window border.
    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

def draw(window):
    # Paint the window the background color.
    window.fill(BACKGROUND_COLOR)
    
    draw_grid(window)
    
    pygame.display.update()

def main(window):
    clock = pygame.time.Clock()
    run = True
    
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        draw(window)
    
    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)