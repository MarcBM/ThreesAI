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
        # The tile's ord is randomly chosen
        # The values range from 1 to max_ord - 3
        if max_ord > 3:
            self.highest_possible_ord = max_ord - 3
            high_ord = random.randint(1, self.highest_possible_ord)
            self.tiles.append(Tile(high_ord))
        
        # Shuffle the tiles to randomize their order
        random.shuffle(self.tiles)

    def draw_tile(self, max_ord, row, col, renderer=None):
        t = self.tiles.pop()
        t.set_position(row, col)
        if renderer:
            renderer.newTile(t)
            renderer.add_to_render_queue(t)
        if len(self.tiles) == 0:
            self.refill(max_ord)
        return t
    
    def peek(self):        
        preview = []

        top_ord = self.tiles[-1].ord
        if top_ord > 0:
            lowPreview = random.randint(max(1, top_ord - 2), top_ord)
            currPreview = lowPreview
            while len(preview) < 3 and currPreview <= self.highest_possible_ord:
                preview.append(currPreview)
                currPreview += 1
            
            currPreview = lowPreview - 1
            while len(preview) < 3 and currPreview > 0:
                preview.append(currPreview)
                currPreview -= 1
        else:
            preview.append(top_ord)

        preview.sort()
        
        return preview

class Threes:
    def __init__ (self, board_size=4):
        # Initialize a 4x4 board with zeros
        self.board_size = board_size
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.highest_ord = 0
        # Initialize a bag of tiles
        self.tile_bag = TileBag(self.board_size)
        self.previewTiles = []
        self.allowed_moves = []
        self.game_over = False
        self.renderer = None
        self.controller = None
    
    def assign_renderer(self, renderer):
        self.renderer = renderer

    def assign_controller(self, controller):
        self.controller = controller

    def start_game(self):
        # Choose 9 random positions on the board to place starting tiles
        should_place = [True] * 9 + [False] * 7
        random.shuffle(should_place)
        index = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                if should_place[index]:
                    tile = self.tile_bag.draw_tile(self.highest_ord, row, col, self.renderer)
                    self.board[row][col] = tile
                index += 1

        self.allowed_moves = self.moves_allowed()
        self.generate_preview_tiles()
        
        if self.renderer:
            self.renderer.draw()

    def reset_game(self):
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.highest_ord = 0
        self.tile_bag = TileBag(self.board_size)
        self.game_over = False
        if self.renderer:
            self.renderer.clear_render_queue()

        self.start_game()

    def move(self, direction):
        if self.renderer:
            self.renderer.clear_render_queue()

        rowDelta, colDelta = direction

        # Moving Left or Right
        if rowDelta == 0:
            rowsMoved = set()
            for row in range(self.board_size):
                # Moving Left
                if colDelta < 0:
                    for col in range(self.board_size):
                        if self.move_tile(row, col, direction):
                            rowsMoved.add(row)
                    
                # Moving Right
                else:
                    for col in range(self.board_size - 1, -1, -1):
                        if self.move_tile(row, col, direction):
                            rowsMoved.add(row)

            if len(rowsMoved) > 0:
                newTileRow = random.choice(tuple(rowsMoved))
                # Moving Left
                if colDelta < 0:
                    self.board[newTileRow][-1] = self.tile_bag.draw_tile(self.highest_ord, newTileRow, self.board_size - 1, self.renderer)
                # Moving Right
                else:
                    self.board[newTileRow][0] = self.tile_bag.draw_tile(self.highest_ord, newTileRow, 0, self.renderer)
        # Moving Up or Down
        else:
            colsMoved = set()
            for col in range(self.board_size):
                # Moving Up
                if rowDelta < 0:
                    for row in range(self.board_size):
                        if self.move_tile(row, col, direction):
                            colsMoved.add(col)
                # Moving Down
                else:
                    for row in range(self.board_size - 1, -1, -1):
                        if self.move_tile(row, col, direction):
                            colsMoved.add(col)

            if len(colsMoved) > 0:
                newTileCol = random.choice(tuple(colsMoved))
                # Moving Up
                if rowDelta < 0:
                    self.board[-1][newTileCol] = self.tile_bag.draw_tile(self.highest_ord, self.board_size - 1, newTileCol, self.renderer)
                # Moving Down
                else:
                    self.board[0][newTileCol] = self.tile_bag.draw_tile(self.highest_ord, 0, newTileCol, self.renderer)

        self.generate_preview_tiles()

        self.allowed_moves = self.moves_allowed()

        if len(self.allowed_moves) == 0:
            self.game_over = True

        if self.renderer:
            self.renderer.draw()
        if self.controller:
            self.controller.unlock()

    def move_tile(self, row, col, direction):
        moved = False
        tile = self.board[row][col]
        if not tile:
            return moved
        rowDelta, colDelta = direction
        newRow = row + rowDelta
        newCol = col + colDelta

        if min(newRow, newCol) >= 0 and max(newRow, newCol) < self.board_size:
            if not self.board[newRow][newCol]:
                tile.set_position(newRow, newCol)
                self.board[newRow][newCol] = tile
                self.board[row][col] = None
                moved = True
            else:
                blockingTile = self.board[newRow][newCol]
                # Can merge
                if (tile.ord >= 0 and tile.ord == blockingTile.ord) or tile.ord + blockingTile.ord == -3:
                    newOrd = tile.ord + 1 if tile.ord >= 0 else 0
                    self.highest_ord = max(self.highest_ord, newOrd)
                    newTile = Tile(newOrd)
                    newTile.set_position(newRow, newCol)
                    self.board[newRow][newCol] = newTile
                    self.board[row][col] = None
                    tile = newTile
                    moved = True
                    if self.renderer:
                        self.renderer.newTile(newTile)
        
        if self.renderer:
            self.renderer.add_to_render_queue(tile)

        return moved
    
    def moves_allowed(self):
        allowed_moves = []

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for direction in directions:
            rowDelta, colDelta = direction
            move_possible = False

            for row in range(self.board_size):
                for col in range(self.board_size):
                    tile = self.board[row][col]
                    if not tile:
                        continue
                    newRow = row + rowDelta
                    newCol = col + colDelta

                    if min(newRow, newCol) >= 0 and max(newRow, newCol) < self.board_size:
                        blockingTile = self.board[newRow][newCol]
                        if not blockingTile:
                            move_possible = True
                        else:
                            if (tile.ord >= 0 and tile.ord == blockingTile.ord) or tile.ord + blockingTile.ord == -3:
                                move_possible = True

                    if move_possible:
                        break
                if move_possible:
                    break

            if move_possible:
                allowed_moves.append(direction)

        return allowed_moves

    def generate_preview_tiles(self):
        self.previewTiles = []
        for ord in self.tile_bag.peek():
            tile = Tile(ord)
            self.previewTiles.append(tile)
            if self.renderer:
                self.renderer.newPreviewTile(tile)

    def calculate_score(self):
        score = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                tile = self.board[row][col]
                if tile:
                    score += tile.get_score()
        return score