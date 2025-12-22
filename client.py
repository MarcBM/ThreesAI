import pygame
import sys
from pygame.locals import *

pygame.init()

FramePerSec = pygame.time.Clock()
FPS = 60

BACKGROUND_COLOR = (32, 48, 70)        # dark steel-blue base
BORDER_COLOR = (18, 28, 42)            # darkest
CELL_BACKGROUND_COLOR = (45, 65, 90)   # slightly lighter than background

# Tile foregrounds (matte/muted and light for dark text)
RED_COLOR = (220, 120, 112)
BLUE_COLOR = (120, 170, 210)
LIGHT_GREY_COLOR = (70, 90, 112)       # muted steel-grey accent

LIGHT_TEXT_COLOR = (232, 238, 245)     # for text on dark backgrounds
DARK_TEXT_COLOR = (20, 22, 26)         # for text on light tiles (red/blue)

# Set up display
WIDTH, HEIGHT = 550, 800
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(BACKGROUND_COLOR)
pygame.display.set_caption('Threes!')

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)