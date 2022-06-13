import tile, pygame, json, random

class Map:
    def __init__(self):
        self.size = self.width, self.height = 320, 320 # something that fits in eventual window and is some multiple of 16x16 from the tiles

    def load_tileset(self): #n_tiles is number of needed tiles to fill map
        file = open('nb_rules.json')
        data = json.load(file)
        file.close()
        return [i for i in data["data"]]



    # def draw_map(self):
        
