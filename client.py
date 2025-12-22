import pygame
import sys
from pygame.locals import *
from gameState import Threes
from renderer import WIDTH, HEIGHT, draw_screen

pygame.init()

FramePerSec = pygame.time.Clock()
FPS = 60

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Threes!')

game = Threes()
game.start_game()

draw_screen(DISPLAYSURF, game)


# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    draw_screen(DISPLAYSURF, game)

    pygame.display.update()
    FramePerSec.tick(FPS)
