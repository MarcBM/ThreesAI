import pygame
import sys
from pygame.locals import *
from gameState import Threes
from renderer import WIDTH, HEIGHT, initialise_display

pygame.init()

FramePerSec = pygame.time.Clock()
FPS = 60

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
initialise_display(DISPLAYSURF)
pygame.display.set_caption('Threes!')

game = Threes()


# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
