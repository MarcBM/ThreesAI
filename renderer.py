import pygame
from pygame.locals import *

from gameState import BOARD_SIZE

# Global constants
WIDTH, HEIGHT = 550, 800

MARGIN_PCT = 0.05
BORDER_WIDTH_PCT = 0.02
HEADER_HEIGHT_PCT = 0.2
FOOTER_HEIGHT_PCT = 0.1

MARGIN = MARGIN_PCT * WIDTH
BORDER_WIDTH = BORDER_WIDTH_PCT * WIDTH
HEADER_HEIGHT = HEADER_HEIGHT_PCT * HEIGHT
FOOTER_HEIGHT = FOOTER_HEIGHT_PCT * HEIGHT

BORDER_RADIUS = 20
TILE_RADIUS = 10

# Color definitions
BACKGROUND_COLOR = (15, 20, 30)  # much darker steel-blue base
BORDER_COLOR = (8, 10, 15)  # much darker
CELL_BACKGROUND_COLOR = (20, 28, 40)  # much darker background

# Tile foregrounds (matte/muted and light for dark text)
RED_COLOR = (220, 100, 90)
BLUE_COLOR = (80, 140, 200)
LIGHT_GREY_COLOR = (140, 150, 160)  # more grey, less white

LIGHT_TEXT_COLOR = (232, 238, 245)  # for text on dark backgrounds
DARK_TEXT_COLOR = (20, 22, 26)  # for text on light tiles (red/blue)

def draw_screen(DISPLAYSURF, game=None):
  DISPLAYSURF.fill(BACKGROUND_COLOR)
  
  draw_board(DISPLAYSURF, game)

def get_board_dimensions():
  board_width = WIDTH - (2 * MARGIN)
  board_height = HEIGHT - (2 * MARGIN) - HEADER_HEIGHT - FOOTER_HEIGHT
  return board_width, board_height

def draw_board(DISPLAYSURF, game=None):
  x = MARGIN
  y = MARGIN + HEADER_HEIGHT
  board_width, board_height = get_board_dimensions()
  pygame.draw.rect(DISPLAYSURF, BORDER_COLOR, (x, y, board_width, board_height), border_radius=BORDER_RADIUS)
  
  for i in range(BOARD_SIZE):
      for j in range(BOARD_SIZE):
          tile_ord = -3  # Default empty tile
          if game is not None:
              tile = game.board[j][i]
              tile_ord = tile.ord if tile else -3
          draw_tile(DISPLAYSURF, i, j, tile_ord)
  
def draw_tile(DISPLAYSURF, board_x, board_y, tile_ord):
  rect = board_coord_to_screen_rect(board_x, board_y)
  color = CELL_BACKGROUND_COLOR
  if tile_ord == -1:
      color = RED_COLOR
  elif tile_ord == -2:
      color = BLUE_COLOR
  elif tile_ord >= 0:
      color = LIGHT_GREY_COLOR
  
  pygame.draw.rect(DISPLAYSURF, color, rect, border_radius=TILE_RADIUS)

def board_coord_to_screen_rect(board_x, board_y):
  board_width, board_height = get_board_dimensions()
  cell_width = (board_width - (BORDER_WIDTH * 5)) / 4
  cell_height = (board_height - (BORDER_WIDTH * 5)) / 4
  screen_x = MARGIN + BORDER_WIDTH * (board_x + 1) + cell_width * board_x
  screen_y = MARGIN + HEADER_HEIGHT + BORDER_WIDTH * (board_y + 1) + cell_height * board_y

  return pygame.Rect(screen_x, screen_y, cell_width, cell_height)
