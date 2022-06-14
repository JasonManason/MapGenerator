import pygame, json

class Map(pygame.sprite.Group): # group of sprites: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group
    def __init__(self):
        super().__init__()
        self.size = self.width, self.height = 320, 320 # something that fits in eventual window and is some multiple of 16x16 from the tiles
        self.max_tiles = int((self.width / 16) * (self.height / 16))
        self.clicked = False

    def load_tileset(self) -> list[str]:
        file = open('nb_rules.json')
        data = json.load(file)
        file.close()
        return [i for i in data["data"]] # eventually return different datatype to also get weights or maybe as different method?
    
    def get_max_tiles(self) -> int:
        return self.max_tiles

    def set_size(self, size): # Tuple (width, height)
        self.size = size # give user choice for S, M, L sized map!