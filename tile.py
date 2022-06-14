import pygame, json

class Tile(pygame.sprite.Sprite): # https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
    def __init__(self):
        super().__init__()
        self.clicked()

    def set_initial_nbs(self):
        file = open('nb_rules.json')
        data = json.load(file)
        self.nbs = data["data"]
        file.close()
        # for key, val in data["data"].items():
        #     if key == self.name:
        #         #self.nbs = (key, val)
        #         self.nbs = {key:val}

    def set_nbs(self, nbs):
        self.nbs = nbs

    def get_nbs(self) -> dict:
        return self.nbs
    
    def set_name(self, name):
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
        
        # all sides are free
        else:
            print("not corner/side")
            return nbs[self.name]
    
    def clicked(self) -> bool: # when set to true, user should not be able to click again
        self.clicked = True

    def set_coords(self, coords): # Tuple
        self.coords = coords

    def get_coords(self) -> tuple:
        return self.coords      