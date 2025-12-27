class Controller:
    def __init__(self, game):
        self.game = game
        self.locked = False

    def lock(self):
        self.locked = True
    
    def unlock(self):
        self.locked = False