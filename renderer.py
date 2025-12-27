import pygame
from pygame.locals import *

# Global constants
WIDTH, HEIGHT = 550, 900

MARGIN_PCT = 0.05
BORDER_WIDTH_PCT = 0.02
HEADER_HEIGHT_PCT = 0.2
FOOTER_HEIGHT_PCT = 0.1
PREVIEW_TILE_SIZE_PCT = 0.7

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

PREVIEW_WIDTH = CELL_WIDTH * PREVIEW_TILE_SIZE_PCT
PREVIEW_HEIGHT = CELL_HEIGHT * PREVIEW_TILE_SIZE_PCT

PREVIEW_Y = MARGIN + HEADER_HEIGHT - PREVIEW_HEIGHT - BORDER_WIDTH

TOP_LEFTS = []
PREVIEW_TOP_LEFTS = []

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
LIGHT_YELLOW_TEXT_COLOR = (255, 230, 120)  # vibrant light yellow for contrast on LIGHT_GREY_COLOR

# Text settings
TILE_FONTS = {}
PREVIEW_FONTS = {}
SCORE_FONT = None

# Animation settings
ANIMATION_FRAMES = 20  # frames per animation

def start_renderer(board_size):
  # Pre-generate fonts for tile labels
  fontSize = int(CELL_HEIGHT) // 2
  for numDigits in range(1, 6):
    if numDigits > 2:
      fontSize = int(fontSize * 0.8)
    TILE_FONTS[numDigits] = pygame.font.SysFont('Arial', fontSize, bold=True)
    PREVIEW_FONTS[numDigits] = pygame.font.SysFont('Arial', int(fontSize * PREVIEW_TILE_SIZE_PCT), bold=True)
    
  global SCORE_FONT
  SCORE_FONT = pygame.font.SysFont('Arial', int(HEADER_HEIGHT * 0.4), bold=True)
  
  # Pre-calculate top-left positions for each cell
  for i in range(board_size):
    row = []
    for j in range(board_size):
        x = BOARD_X + BORDER_WIDTH * (j + 1) + CELL_WIDTH * j
        y = BOARD_Y + BORDER_WIDTH * (i + 1) + CELL_HEIGHT * i
        row.append((x, y))
    TOP_LEFTS.append(row)

  for j in range(3):
    row = []
    widthOfFullPreview = PREVIEW_WIDTH * (j + 1) + BORDER_WIDTH * (j)
    startX = WIDTH / 2 - widthOfFullPreview / 2
    for i in range(j + 1):
        x = startX + (PREVIEW_WIDTH + BORDER_WIDTH) * i
        y = PREVIEW_Y
        row.append((x, y))
    PREVIEW_TOP_LEFTS.append(row)
    
  DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption('Threes!')
  return DISPLAYSURF

def draw_screen(DISPLAYSURF, game=None):
  DISPLAYSURF.fill(BACKGROUND_COLOR)
  
  draw_board(DISPLAYSURF, game)

def draw_board(DISPLAYSURF, game=None):
  pygame.draw.rect(DISPLAYSURF, BORDER_COLOR, (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT), border_radius=BORDER_RADIUS)
  
  for row in range(game.board_size):
      for col in range(game.board_size):
          draw_tile(DISPLAYSURF, row, col)
  
def draw_tile(DISPLAYSURF, row, col, tile=None, highest_ord=0):
  x, y = TOP_LEFTS[row][col]
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
    text = tile.high_text if tile.ord >= 1 and tile.ord == highest_ord else tile.text
    text_x = x + CELL_WIDTH / 2 - text.get_width() / 2
    text_y = y + CELL_HEIGHT / 2 - text.get_height() / 2
    DISPLAYSURF.blit(text, (text_x, text_y))

def draw_preview_tiles(DISPLAYSURF, previewTiles):
  for i, tile in enumerate(previewTiles):
    x, y = PREVIEW_TOP_LEFTS[len(previewTiles) - 1][i]
    rect = pygame.Rect(x, y, PREVIEW_WIDTH, PREVIEW_HEIGHT)
    if tile.ord == -1:
        color = BLUE_COLOR
    elif tile.ord == -2:
        color = RED_COLOR
    else:
        color = LIGHT_GREY_COLOR
    
    pygame.draw.rect(DISPLAYSURF, color, rect, border_radius=TILE_RADIUS)
    if tile and tile.ord >= 1:
      text_x = x + PREVIEW_WIDTH / 2 - tile.text.get_width() / 2
      text_y = y + PREVIEW_HEIGHT / 2 - tile.text.get_height() / 2
      DISPLAYSURF.blit(tile.text, (text_x, text_y))

def draw_score(DISPLAYSURF, score):
  score_text = SCORE_FONT.render(f'{score}', True, LIGHT_TEXT_COLOR)
  text_x = WIDTH / 2 - score_text.get_width() / 2
  text_y = MARGIN + HEADER_HEIGHT / 2 - score_text.get_height() / 2
  DISPLAYSURF.blit(score_text, (text_x, text_y))
    
class RendererManager:
  def __init__(self, game):
    self.game = game
    self.surface = start_renderer(game.board_size)
    self.updating = False
    self.animation_time = ANIMATION_FRAMES # frames per animation
    self.current_frame = 0
    self.render_queue = []
    
  def draw(self):
    draw_screen(self.surface, self.game)
    for tile in self.render_queue:
       row, col = tile.position
       draw_tile(self.surface, row, col, tile, self.game.highest_ord)
    if self.game.game_over:
       draw_score(self.surface, self.game.calculate_score())
    else:
        draw_preview_tiles(self.surface, self.game.previewTiles)
    pygame.display.update()
    
  def newTile(self, tile):
    label = str(tile.value)
    numDigits = len(label)
    font = TILE_FONTS[numDigits]
    tile.text = font.render(label, True, DARK_TEXT_COLOR)
    tile.high_text = font.render(label, True, LIGHT_YELLOW_TEXT_COLOR)
    
    tile.offset = (0, 0)
    tile.moving = False

  def newPreviewTile(self, tile):
    if tile.ord >= 1:
      label = str(tile.value)
      numDigits = len(label)
      font = PREVIEW_FONTS[numDigits]
      tile.text = font.render(label, True, DARK_TEXT_COLOR)

  def add_to_render_queue(self, tile):
     self.render_queue.append(tile)

  def clear_render_queue(self):
     self.render_queue = []