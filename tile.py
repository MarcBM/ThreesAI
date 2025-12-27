# Explanation of Tiles and Ordinal Values:
# Tile ordinals:
# -2 : Tile with value 2
# -1 : Tile with value 1
#  0 : Tile with value 3
#  1 : Tile with value 6
# Generally, for ord >= 0, tile value = 3 * (2 ** ord)
# This is useful because it allows us to easily handle game logic and scoring. Since the ordinal number is used for
# these calculations, using the ordinal value as the primary representation of tiles simplifies the implementation.
# The visual representation (the actual number on the tile) is purely for display purposes, and can be derived from the
# ordinal value as needed.
# As a general rule, tiles with the same ordinal value can be merged together. Tiles with ordinals -1 and -2 can only
# be merged with each other.
# The ordinal value of the tile is specifically useful for generating the random high-value tile when refilling the
# tile bag.
# Scoring:
# Tiles with ordinals -1 and -2 do not contribute to the score.
# For tiles with ord >= 0, score = 3 ** (ord + 1)

class Tile:
    def __init__(self, ord):
        self.ord = ord # Tile's ordinal value
        self.value = self.compute_value()
        self.position = (-1,-1)
    
    def compute_value(self):
        if self.ord == -2:
            return 2
        elif self.ord == -1:
            return 1
        else:
            return 3 * (2 ** self.ord)
        
    def get_score(self):
        if self.ord < 0:
            return 0
        else:
            return 3 ** (self.ord + 1)
        
    def set_position(self, row, col):
        self.position = (row, col)