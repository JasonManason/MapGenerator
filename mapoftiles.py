import pygame, json, tile

class MapOfTiles(pygame.sprite.Group): # group of sprites: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group
    def __init__(self):
        super().__init__()
        self.size = self.width, self.height = 640, 640 # something that fits in eventual window and is some multiple of 16x16 from the tiles
        self.max_tiles = int((self.width / 16) * (self.height / 16))
        self.clicked = False
        self.occupied_tiles = []
        self.free_tiles = []

    def load_tileset(self) -> list[str]:
        file = open('nb_rules.json')
        data = json.load(file)
        file.close()
        return [i for i in data["data"]] # eventually return different datatype to also get weights or maybe as different method?
    
    def get_max_tiles(self) -> int:
        return self.max_tiles

    def set_size(self, size: tuple):
        self.size = size # give user choice for S, M, L sized map!

    def add_occupied_tiles(self, tile: tuple):
        """
        Add the coordinates of a placed tile to the list of occupied tiles.
        """
        self.occupied_tiles.append(tile)

    def get_occupied_tiles(self) -> list:
        return self.occupied_tiles

    def check_if_taken(self, direction: str, t:tile, all_coords: list) -> bool:
        if direction == "nb_up":
            if tuple(map(lambda a, b: a + b, t.get_coords(), all_coords[0])) in self.get_occupied_tiles():
                print("up is taken")
                return True
            
        elif direction == "nb_down":
            if tuple(map(lambda a, b: a + b, t.get_coords(), all_coords[1])) in self.get_occupied_tiles():
                print("down is taken")
                return True

        elif direction == "nb_left":
            if tuple(map(lambda a, b: a + b, t.get_coords(), all_coords[2])) in self.get_occupied_tiles():
                print("left is taken")
                return True

        elif direction == "nb_right":
            if tuple(map(lambda a, b: a + b, t.get_coords(), all_coords[3])) in self.get_occupied_tiles():
                print("right is taken")
                return True
        else:
            print("spot is free")
            return False