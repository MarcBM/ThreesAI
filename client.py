import pygame
import sys
from pygame.locals import *

from gameState import Threes
from renderer import RendererManager
from playerController import PlayerController

pygame.init()

FramePerSec = pygame.time.Clock()
FPS = 60

game = Threes()

renderer = RendererManager(game)
controller = PlayerController(game)
game.assign_renderer(renderer)
game.assign_controller(controller)

game.start_game()


# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            controller.handle_key_press(event)

    if renderer.updating:
        renderer.draw()
    FramePerSec.tick(FPS)
