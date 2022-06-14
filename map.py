import tile, pygame, json, random

class Map(pygame.sprite.Group): # group of sprites: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group
    def __init__(self):
        self.size = self.width, self.height = 320, 320 # something that fits in eventual window and is some multiple of 16x16 from the tiles
        self.n_tiles = int((self.width / 16) * (self.height / 16))
        self.clicked = False

    def load_tileset(self):
        file = open('nb_rules.json')
        data = json.load(file)
        file.close()
        return [i for i in data["data"]] # eventually return different datatype to also get weights or maybe as different method?
        

    # def draw_map(self):
        
