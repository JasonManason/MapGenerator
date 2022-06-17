import pygame, json, tile, pandas

class MapOfTiles(pygame.sprite.Group): # group of sprites: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group
    def __init__(self):
        super().__init__()
        self.size = self.width, self.height = 640, 640 # something that fits in eventual window and is some multiple of 16x16 from the tiles
        self.max_tiles = int((self.width / 16) * (self.height / 16))
        self.clicked = False
        self.occupied_tiles = []


    def set_grid(self):
        """Create a grid with numpy??? or even pandas!? so via cols and rows we can get: occupied, adjacent all sides, coords, image name"""
        n_cols, n_rows = int((self.size[0] / 16)), int((self.size[0] / 16))
        n_tiles = int(n_cols * n_rows)
        # USE: numpy.meshgrid!! creates grid of coordinates for plotting?
        pass


    def load_tileset(self) -> list[str]:
        file = open('nb_rules.json')
        data = json.load(file)
        file.close()
        self.tileset = [i for i in data["data"]]
        return self.tileset # eventually return different datatype to also get weights or maybe as different method?
    

    def get_tileset(self) -> list[str]:
        return self.tileset


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