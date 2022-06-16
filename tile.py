import pygame, json, mapoftiles, random

class Tile(pygame.sprite.Sprite): # https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
    def __init__(self):
        super().__init__()
        #self.active_nbs = {} #{0:"default"}

    def set_initial_nbs(self):
        file = open('nb_rules.json')
        data = json.load(file)
        self.nbs = data["data"]
        file.close()

    def set_nbs(self, nbs: dict):
        self.nbs = nbs

    def get_nbs(self) -> dict:
        return self.nbs
    
    def set_name(self, name: str):
        self.name = name
    
    def get_name(self) -> str:
        return self.name

    def get_usable_nbs(self, coords, m) -> dict:
        """
        Returns only the usable neigbours of a tile and leaves out the rest in case of a corner or side tile.
        Uses dict comprehension.
        """
        nbs = self.get_nbs()
        
        #Check vertical sides
        if coords[0] == 0:
            if coords[1] == 0: # CORNER LEFT UP
                return {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_down", "nb_right"]}
            elif coords[1] == (m.height - 16): # CORNER LEFT DOWN
                return {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_up", "nb_right"]}
            else: # no left nbs
                return {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_up", "nb_down", "nb_right"]}

        elif coords[0] == (m.width - 16):
            if coords[1] == 0: # CORNER RIGHT UP
                return {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_down", "nb_left"]}
            elif coords[1] == (m.height - 16): # CORNER RIGHT DOWN
                return {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_up", "nb_left"]}
            else: # no right nbs
                return {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_up", "nb_down", "nb_left"]}

        # Check horizontal sides
        elif coords[1] == 0: # no up nbs
            return {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_down", "nb_left", "nb_right"]}
        elif coords[1] == (m.height - 16): # no down nbs
            return {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_up", "nb_left", "nb_right"]}
              
        else: # all sides are free
            return nbs[self.name]

    def set_coords(self, coords: tuple):
        self.coords = coords

    # def set_next_coords(self, direction: str):
    #     coords_up = (self.get_coords()[0], self.get_coords()[1] - 16)
    #     coords_down = (self.get_coords()[0], self.get_coords()[1] + 16)
    #     coords_left = (self.get_coords()[0] - 16, self.get_coords()[1])
    #     coords_right = (self.get_coords()[0] + 16, self.get_coords()[1])

    #     if direction == "nb_up":
    #         new_coords = coords_up

    #     elif direction == "nb_down":
    #         new_coords = coords_down

    #     elif direction == "nb_left":
    #         new_coords = coords_left
    #     else: # nb_right
    #         new_coords = coords_right

    #     self.coords = new_coords

    def get_coords(self) -> tuple:
        return self.coords

    # def add_active_nb(self, direction: str, name: str) -> dict: # use to later check all nbs of tile (max 4 {str:str})
    #     self.active_nbs[direction] = name

    # def get_active_nbs(self) -> dict:
    #     return self.active_nbs

    def check_if_spot_taken(self, directions: dict, m: mapoftiles) -> list:
        print("\n\n", directions)
        #print(self.active_nbs, "\n\n")
        print("self.get_nbs():\t", self.get_nbs(), "\n\n")

    def get_new_direction(self, direction: str, usable_sides: dict) -> str: # returns new direction
        # usable_sides = dict{str:list}
        new_options = list(usable_sides.keys()).remove(direction)
        new_direction = random.choice(new_options)
        print(new_direction)
        return new_direction
