import pygame
from pygame.locals import *

from controller import Controller

MOVEMENT_KEYS = (K_LEFT, K_RIGHT, K_UP, K_DOWN)

class PlayerController(Controller):
    
    def handle_key_press(self, event):
        if not self.locked:
            if event.key in MOVEMENT_KEYS:
                self.lock()
                self.handle_movement_input(event.key)
            if event.key == K_r:
                self.game.reset_game()

    def handle_movement_input(self, key):
        direction = (0, 0)
        if key == K_UP:
            direction = (-1, 0)
        elif key == K_DOWN:
            direction = (1, 0)
        elif key == K_LEFT:
            direction = (0, -1)
        elif key == K_RIGHT:
            direction = (0, 1)
        if direction in self.game.allowed_moves:
            self.game.move(direction)
        else:
            self.unlock()