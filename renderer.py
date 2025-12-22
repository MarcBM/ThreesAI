import pygame
from pygame.locals import *

# Global constants
WIDTH, HEIGHT = 550, 800
MARGIN = 0.05
BORDER_WIDTH = 0.02
HEADER_HEIGHT = 0.2
FOOTER_HEIGHT = 0.1

BORDER_RADIUS = 5
TILE_RADIUS = 2

# Color definitions
BACKGROUND_COLOR = (32, 48, 70)  # dark steel-blue base
BORDER_COLOR = (18, 28, 42)  # darkest
CELL_BACKGROUND_COLOR = (45, 65, 90)  # slightly lighter than background

# Tile foregrounds (matte/muted and light for dark text)
RED_COLOR = (220, 120, 112)
BLUE_COLOR = (120, 170, 210)
LIGHT_GREY_COLOR = (70, 90, 112)  # muted steel-grey accent

LIGHT_TEXT_COLOR = (232, 238, 245)  # for text on dark backgrounds
DARK_TEXT_COLOR = (20, 22, 26)  # for text on light tiles (red/blue)

def initialise_display(DISPLAYSURF):
  DISPLAYSURF.fill(BACKGROUND_COLOR)

def get_board_dimensions():
  board_width = WIDTH - (2 * MARGIN * WIDTH)
  board_height = HEIGHT - (2 * MARGIN * HEIGHT) - HEADER_HEIGHT - FOOTER_HEIGHT
  return board_width, board_height

def draw_board(DISPLAYSURF, game=None):
  pass

def board_coord_to_screen_rect(board_x, board_y):
  board_width, board_height = get_board_dimensions()
  cell_width = (board_width - (BORDER_WIDTH * 5) / 4)
  cell_height = (board_height - (BORDER_WIDTH * 5) / 4)
  screen_x = MARGIN * WIDTH + BORDER_WIDTH * (board_x + 1) + cell_width * board_x
  screen_y = MARGIN * HEIGHT + HEADER_HEIGHT + BORDER_WIDTH * (board_y + 1) + cell_height * board_y

  return pygame.Rect(screen_x, screen_y, cell_width, cell_height)
