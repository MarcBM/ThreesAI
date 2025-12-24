import random

from tile import Tile

class TileBag:
    def __init__(self, board_size):
        self.board_size = board_size
        self.tiles = []
        self.highest_possible_ord = 0
        self.refill()

    def refill(self, max_ord = 0):
        # Fill the bag with 12 tiles, 4 of each type (1s, 2s, and 3s)
        self.tiles = []
        for _ in range(self.board_size):
            self.tiles.append(Tile(-1))  # Tile with ord -1 (value 1)
            self.tiles.append(Tile(-2))  # Tile with ord -2 (value 2)
            self.tiles.append(Tile(0))    # Tile with ord 0 (value 3)
        # If max_ord > 3, add 1 tile of a higher ord than 0.
        # The tile's ord is randomly chosen between a maximum of 3 values
        # The values range from max_ord - 3 to max(1, max_ord - 5)
        if max_ord > 3:
            self.highest_possible_ord = max_ord - 3
            high_ord = random.randint(max(1, max_ord - 5), max_ord - 3)
            self.tiles.append(Tile(high_ord))
        
        # Shuffle the tiles to randomize their order
        random.shuffle(self.tiles)

    def draw_tile(self, max_ord):
        t = self.tiles.pop()
        if len(self.tiles) == 0:
            self.refill(max_ord)
        return t
    
    def peek(self):        
        preview = []

        top_ord = self.tiles[-1].ord
        if top_ord > 0:
            for i in range(max(1, self.highest_possible_ord - 2), self.highest_possible_ord + 1):
                preview.append(i)
        else:
            preview.append(top_ord)
        
        return preview



class Threes:
    def __init__ (self, board_size=4):
        # Initialize a 4x4 board with zeros
        self.board_size = board_size
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.highest_ord = 0
        # Initialize a bag of tiles
        self.tile_bag = TileBag(self.board_size)
        self.renderer = None
    
    def assign_renderer(self, renderer):
        self.renderer = renderer

    def start_game(self):
        # Choose 9 random positions on the board to place starting tiles
        should_place = [True] * 9 + [False] * 7
        random.shuffle(should_place)
        index = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if should_place[index]:
                    new_tile = self.tile_bag.draw_tile(self.highest_ord)
                    self.board[i][j] = new_tile
                    if self.renderer:
                        self.renderer.newTile(new_tile)
                index += 1