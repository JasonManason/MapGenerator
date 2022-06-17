from numpy import tile
import pygame, json, mapoftiles, random

class Tile(pygame.sprite.Sprite): # https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
    def __init__(self):
        super().__init__()


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


    def check_adjacency(self, coords: tuple, m: mapoftiles) -> tuple(list, dict):
        """
        Returns only the coordinates of the free adjacent tiles.
        """
        nbs = self.get_nbs()
        coords_up = (coords[0], coords[1] - 16)
        coords_down = (coords[0], coords[1] + 16)
        coords_left = (coords[0] - 16, coords[1])
        coords_right = (coords[0] + 16, coords[1])
        
        #Check vertical sides
        if coords[0] == 0:
            if coords[1] == 0: # CORNER LEFT UP
                return [coords_down, coords_right], {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_down", "nb_right"]}
            elif coords[1] == (m.height - 16): # CORNER LEFT DOWN
                return [coords_up, coords_right], {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_up", "nb_right"]}
            else: # no left nbs
                return [coords_up, coords_down, coords_right], {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_up", "nb_down", "nb_right"]}

        elif coords[0] == (m.width - 16):
            if coords[1] == 0: # CORNER RIGHT UP
                return [coords_down, coords_left], {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_down", "nb_left"]}
            elif coords[1] == (m.height - 16): # CORNER RIGHT DOWN
                return [coords_up, coords_left], {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_up", "nb_left"]}
            else: # no right nbs
                return [coords_up, coords_down, coords_left], {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_up", "nb_down", "nb_left"]}

        # Check horizontal sides
        elif coords[1] == 0: # no up nbs
            return [coords_down, coords_left, coords_right], {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_down", "nb_left", "nb_right"]}
        elif coords[1] == (m.height - 16): # no down nbs
            return [coords_up, coords_left, coords_right], {n: nbs[self.name][n] for n in nbs[self.name].keys() & ["nb_up", "nb_left", "nb_right"]}
              
        else: # all sides are free
            return [coords_up, coords_down, coords_left, coords_right], nbs[self.name]


    def set_coords(self, coords: tuple):
        self.coords = coords


    def get_coords(self) -> tuple:
        return self.coords