import pygame
import sys
from pygame.locals import *
from gameState import Threes
from renderer import RendererManager

pygame.init()

FramePerSec = pygame.time.Clock()
FPS = 60

game = Threes()

renderer = RendererManager(game)
game.assign_renderer(renderer)

game.start_game()


# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    renderer.draw()
    FramePerSec.tick(FPS)
