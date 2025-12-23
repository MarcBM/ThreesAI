import pygame
from pygame.locals import *

from gameState import BOARD_SIZE

# Global constants
WIDTH, HEIGHT = 550, 900

MARGIN_PCT = 0.05
BORDER_WIDTH_PCT = 0.02
HEADER_HEIGHT_PCT = 0.2
FOOTER_HEIGHT_PCT = 0.1

MARGIN = MARGIN_PCT * WIDTH
BORDER_WIDTH = BORDER_WIDTH_PCT * WIDTH
HEADER_HEIGHT = HEADER_HEIGHT_PCT * HEIGHT
FOOTER_HEIGHT = FOOTER_HEIGHT_PCT * HEIGHT

BOARD_X = MARGIN
BOARD_Y = MARGIN + HEADER_HEIGHT
BOARD_WIDTH = WIDTH - (2 * MARGIN)
BOARD_HEIGHT = HEIGHT - (2 * MARGIN) - HEADER_HEIGHT - FOOTER_HEIGHT

CELL_WIDTH = (BOARD_WIDTH - (BORDER_WIDTH * 5)) / 4
CELL_HEIGHT = (BOARD_HEIGHT - (BORDER_WIDTH * 5)) / 4

TOP_LEFTS = []
for i in range(BOARD_SIZE):
    row = []
    for j in range(BOARD_SIZE):
        x = BOARD_X + BORDER_WIDTH * (j + 1) + CELL_WIDTH * j
        y = BOARD_Y + BORDER_WIDTH * (i + 1) + CELL_HEIGHT * i
        row.append((x, y))
    TOP_LEFTS.append(row)

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

# Text settings
TILE_FONT_SIZE = 24
TILE_FONT = None
TILE_LABELS = {}

def start_renderer(DISPLAYSURF, game=None):
  global TILE_FONT
  TILE_FONT = pygame.font.SysFont('Arial', TILE_FONT_SIZE)
  for ord in range(-2, 20):
      if ord == -1:
          label = '1'
      elif ord == -2:
          label = '2'
      else:
          label = str(3 * (2 ** ord))
      TILE_LABELS[ord] = TILE_FONT.render(label, True, DARK_TEXT_COLOR)
  draw_board(DISPLAYSURF, game)

def draw_screen(DISPLAYSURF, game=None):
  DISPLAYSURF.fill(BACKGROUND_COLOR)
  
  draw_board(DISPLAYSURF, game)

def draw_board(DISPLAYSURF, game=None):
  pygame.draw.rect(DISPLAYSURF, BORDER_COLOR, (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT), border_radius=BORDER_RADIUS)
  
  for i in range(BOARD_SIZE):
      for j in range(BOARD_SIZE):
          offset = (0, 0)
          draw_tile(DISPLAYSURF, i, j, offset, -3)
          if game is not None:
              tile = game.board[j][i]
              if tile:
                 offset = tile.offset
                 draw_tile(DISPLAYSURF, i, j, offset, tile.ord)
  
def draw_tile(DISPLAYSURF, board_x, board_y, offset, tile_ord):
  x, y = TOP_LEFTS[board_y][board_x]
  x += offset[0] * (CELL_WIDTH + BORDER_WIDTH)
  y += offset[1] * (CELL_HEIGHT + BORDER_WIDTH)
  rect = pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)
  color = CELL_BACKGROUND_COLOR
  if tile_ord == -1:
      color = RED_COLOR
  elif tile_ord == -2:
      color = BLUE_COLOR
  elif tile_ord >= 0:
      color = LIGHT_GREY_COLOR
  
  pygame.draw.rect(DISPLAYSURF, color, rect, border_radius=TILE_RADIUS)
  if tile_ord != -3:
    DISPLAYSURF.blit(TILE_LABELS[tile_ord + 2], (x + CELL_WIDTH / 2 - TILE_LABELS[tile_ord].get_width() / 2,
                                            y + CELL_HEIGHT / 2 - TILE_LABELS[tile_ord].get_height() / 2))