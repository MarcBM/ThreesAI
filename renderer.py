import pygame
from pygame.locals import *

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
TILE_FONTS = {}

# Animation settings
ANIMATION_FRAMES = 20  # frames per animation

def start_renderer(board_size):
  # Pre-generate fonts for tile labels
  fontSize = int(CELL_HEIGHT) // 2
  for numDigits in range(1, 6):
    if numDigits > 2:
      fontSize = int(fontSize * 0.8)
    TILE_FONTS[numDigits] = pygame.font.SysFont('Arial', fontSize, bold=True)
    
  # Pre-calculate top-left positions for each cell
  for i in range(board_size):
    row = []
    for j in range(board_size):
        x = BOARD_X + BORDER_WIDTH * (j + 1) + CELL_WIDTH * j
        y = BOARD_Y + BORDER_WIDTH * (i + 1) + CELL_HEIGHT * i
        row.append((x, y))
    TOP_LEFTS.append(row)
    
  DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption('Threes!')
  return DISPLAYSURF

def draw_screen(DISPLAYSURF, game=None):
  DISPLAYSURF.fill(BACKGROUND_COLOR)
  
  draw_board(DISPLAYSURF, game)

def draw_board(DISPLAYSURF, game=None):
  pygame.draw.rect(DISPLAYSURF, BORDER_COLOR, (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT), border_radius=BORDER_RADIUS)
  
  for i in range(game.board_size):
      for j in range(game.board_size):
          draw_tile(DISPLAYSURF, i, j)
          if game is not None:
              tile = game.board[j][i]
              if tile:
                 draw_tile(DISPLAYSURF, i, j, tile)
  
def draw_tile(DISPLAYSURF, board_x, board_y, tile=None):
  x, y = TOP_LEFTS[board_y][board_x]
  color = CELL_BACKGROUND_COLOR
  
  if tile:
    x += tile.offset[0] * (CELL_WIDTH + BORDER_WIDTH)
    y += tile.offset[1] * (CELL_HEIGHT + BORDER_WIDTH)
    if tile.ord == -1:
        color = BLUE_COLOR
    elif tile.ord == -2:
        color = RED_COLOR
    elif tile.ord >= 0:
        color = LIGHT_GREY_COLOR
      
  rect = pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)
  
  pygame.draw.rect(DISPLAYSURF, color, rect, border_radius=TILE_RADIUS)
  if tile:    
    DISPLAYSURF.blit(tile.text, (x + CELL_WIDTH / 2 - tile.text.get_width() / 2, y + CELL_HEIGHT / 2 - tile.text.get_height() / 2))
    
class RendererManager:
  def __init__(self, game):
    self.game = game
    self.surface = start_renderer(game.board_size)
    self.animation_time = ANIMATION_FRAMES # frames per animation
    self.current_frame = 0
    self.tiles_in_motion = []
    
  def draw(self):
    draw_screen(self.surface, self.game)
    pygame.display.update()
    
  def newTile(self, tile):
    label = str(tile.value)
    numDigits = len(label)
    font = TILE_FONTS[numDigits]
    tile.text = font.render(label, True, DARK_TEXT_COLOR)
    
    tile.offset = (0, 0)
    tile.moving = False