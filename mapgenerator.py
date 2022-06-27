import pygame, sys, random, tile, json, numpy as np
from pygame.locals import *
from itertools import product

IMG_SIZE = 16

class MapGenerator:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 640
        self.occupied_tiles = []


    def on_init(self):
        """
            Gets called once at the start of the program to initialize the display surface, the FPS and sets the program to a running state.
        """
        pygame.init()
        self.display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.FPS = 30
        self.FramePerSec = pygame.time.Clock()
        self.running = True


    def on_event(self, event: pygame.event):
        """
            Checks for the occurence of events.
            If the window closed, the program stops running.
            If the user clicked somewhere in the frame, the wave function collapse starts, then the event gets blocked.
        """
        if event.type == pygame.QUIT:
            self.running = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.initialize_wfc(pos)
            pygame.event.set_blocked(pygame.MOUSEBUTTONUP)


    def draw_tile(self, t: tile):
        """
            Takes in a tile object and draws its image at its given coordinates.
        """
        self.display_surf.blit((pygame.image.load(f"tiles/{t.img_name}.png")), t.coords)
        pygame.display.update()
       

    def load_data(self) -> tuple:
        """
            Loads in a json file with tilenames and their adjacency rules.
            Then it returns a tuple with the names as a list and the entire json file as a dict.
        """
        file = open('nb_rules.json')
        data = json.load(file)
        file.close()
        self.data_len = len(data["data"])
        return data["data"], [i for i in data["data"]]


    def set_pos_first_tile(self, t: tile, pos: tuple):
        """
            Sets the coordinates of the first tile to the correct position on the grid.
        """
        coords = [c for c in range(self.width) if c % 16 == 0]
        coordinates = list(product(coords, coords))

        for x_y in coordinates:
            rect_x_y = pygame.Rect(x_y, (16, 16))
            if rect_x_y.collidepoint(pos):
                t.set_coords(x_y)
                self.occupied_tiles.append(x_y)


    def get_valid_nbs(self, name: str, data: dict) -> list:
        """
            Returns a nested list of all valid neighbours of a given tile.
        """
        up, down, left, right, diag_lu, diag_ru, diag_ld, diag_rd = [], [], [], [], [], [], [], []
        for i in data:
            if i == name:
                up, down, left, right, diag_lu, diag_ru, diag_ld, diag_rd = list(data[i].values())

        return up, down, left, right, diag_lu, diag_ru, diag_ld, diag_rd


    def create_grid(self, img_names: list):
        """
            Creates a grid and fills every position with all possible tiles.
        """
        self.grid = np.ndarray((int(self.width / IMG_SIZE), int(self.height / IMG_SIZE)), dtype=list)
        self.grid.fill(img_names)


    def update_grid(self, t: tile) -> tuple:
        """
            Changes the spot on the grid to the drawn tile and returns the indexes of the grid as a tuple.
        """
        x, y = t.coords
        step = IMG_SIZE
        if x != 0 and y != 0:
            self.grid[int(x / step)][int(y / step)] = [t.img_name]
            return (int(x / step), int(y / step))
        elif x == 0 and y != 0:
            self.grid[0][int(y / step)] = [t.img_name]
            return (0, int(y / step))
        elif y == 0:
            self.grid[int(x / step)][0] = [t.img_name]
            return (int(x / step), 0)
        else:
            self.grid[0][0] = [t.img_name]
            return (0, 0)

    def common_nb(self, old: list, new: list) -> list:
        """
            Finds the common element between two lists of possible neighbours in order to remove the impossible tile options.
        """
        return list(set(old).intersection(new))


    def update_grid_around_tile(self, t: tile, x: int, y: int):
        """
            Checks if a given tile is not in a corner or bottom spot and changes the possible neighbours accordingly,
            unless a neighbouring tile is already collapsed.
        """
        step = 1
        UP, DOWN, LEFT, RIGHT = (x, y - step), (x, y + step), (x - step, y), (x + step, y)
        LU, RU, LD, RD, = (x - step, y - step), (x + step, y - step), (x - step, y + step), (x + step, y + step)
        max = int((self.width / IMG_SIZE) - 1)

        if x == 0: # LEFT BORDER
            if y == 0: # CORNER L/U              
                if len(self.grid[DOWN]) == self.data_len: self.grid[DOWN] = t.valid_nbs_down
                elif len(self.grid[DOWN]) != 1 and len(self.grid[DOWN]) != self.data_len: self.grid[DOWN] = self.common_nb(self.grid[DOWN], t.valid_nbs_down) # first one rewritten
                if len(self.grid[RIGHT]) != 1: self.grid[RIGHT] = t.valid_nbs_right
                elif len(self.grid[RIGHT]) != 1 and len(self.grid[RIGHT]) != self.data_len: self.grid[RIGHT] = self.common_nb(self.grid[RIGHT], t.valid_nbs_right) 
                if len(self.grid[RD]) == self.data_len: self.grid[RD] = t.valid_nbs_rd
                elif len(self.grid[RD]) != 1 and len(self.grid[RD]) != self.data_len: self.grid[RD] = self.common_nb(self.grid[RD], t.valid_nbs_rd)

            elif y == max or y == max + 1: # CORNER L/D
                if len(self.grid[UP]) != 1: self.grid[UP] = t.valid_nbs_up
                elif len(self.grid[UP]) != 1 and len(self.grid[UP]) != self.data_len: self.grid[UP] = self.common_nb(self.grid[UP], t.valid_nbs_up) 
                if len(self.grid[RIGHT]) != 1: self.grid[RIGHT] = t.valid_nbs_right
                elif len(self.grid[RIGHT]) != 1 and len(self.grid[RIGHT]) != self.data_len: self.grid[RIGHT] = self.common_nb(self.grid[RIGHT], t.valid_nbs_right)
                if len(self.grid[RU]) == self.data_len: self.grid[RU] = t.valid_nbs_ru
                elif len(self.grid[RU]) != 1 and len(self.grid[RU]) != self.data_len: self.grid[RU] = self.common_nb(self.grid[RU], t.valid_nbs_ru)

            else:
                if len(self.grid[UP]) != 1: self.grid[UP] = t.valid_nbs_up
                elif len(self.grid[UP]) != 1 and len(self.grid[UP]) != self.data_len: self.grid[UP] = self.common_nb(self.grid[UP], t.valid_nbs_up)   
                if len(self.grid[DOWN]) != 1: self.grid[DOWN] = t.valid_nbs_down
                elif len(self.grid[DOWN]) != 1 and len(self.grid[DOWN]) != self.data_len: self.grid[DOWN] = self.common_nb(self.grid[DOWN], t.valid_nbs_down)
                if len(self.grid[RIGHT]) != 1: self.grid[RIGHT] = t.valid_nbs_right
                elif len(self.grid[RIGHT]) != 1 and len(self.grid[RIGHT]) != self.data_len: self.grid[RIGHT] = self.common_nb(self.grid[RIGHT], t.valid_nbs_right)
                if len(self.grid[RU]) == self.data_len: self.grid[RU] = t.valid_nbs_ru
                elif len(self.grid[RU]) != 1 and len(self.grid[RU]) != self.data_len: self.grid[RU] = self.common_nb(self.grid[RU], t.valid_nbs_ru)              
                if len(self.grid[RD]) == self.data_len: self.grid[RD] = t.valid_nbs_rd
                elif len(self.grid[RD]) != 1 and len(self.grid[RD]) != self.data_len: self.grid[RD] = self.common_nb(self.grid[RD], t.valid_nbs_rd)

        elif x == max: # RIGHT BORDER
            if y == 0: # CORNER R/U
                if len(self.grid[DOWN]) != 1: self.grid[DOWN] = t.valid_nbs_down
                elif len(self.grid[DOWN]) != 1 and len(self.grid[DOWN]) != self.data_len: self.grid[DOWN] = self.common_nb(self.grid[DOWN], t.valid_nbs_down)
                if len(self.grid[LEFT]) != 1: self.grid[LEFT] = t.valid_nbs_left
                elif len(self.grid[LEFT]) != 1 and len(self.grid[LEFT]) != self.data_len: self.grid[LEFT] = self.common_nb(self.grid[LEFT], t.valid_nbs_left) 
                if len(self.grid[LD]) == self.data_len: self.grid[LD] = t.valid_nbs_ld
                elif len(self.grid[LD]) != 1 and len(self.grid[LD]) != self.data_len: self.grid[LD] = self.common_nb(self.grid[LD], t.valid_nbs_ld)
            elif y == max or y == max + 1: # CORNER R/D
                if len(self.grid[UP]) != 1: self.grid[UP] = t.valid_nbs_up
                elif len(self.grid[UP]) != 1 and len(self.grid[UP]) != self.data_len: self.grid[UP] = self.common_nb(self.grid[UP], t.valid_nbs_up) 
                if len(self.grid[LEFT]) != 1: self.grid[LEFT] = t.valid_nbs_left
                elif len(self.grid[LEFT]) != 1 and len(self.grid[LEFT]) != self.data_len: self.grid[LEFT] = self.common_nb(self.grid[LEFT], t.valid_nbs_left) 
                if len(self.grid[LU]) == self.data_len: self.grid[LU] = t.valid_nbs_lu
                elif len(self.grid[LU]) != 1 and len(self.grid[LU]) != self.data_len: self.grid[LU] = self.common_nb(self.grid[LU], t.valid_nbs_lu)
            else:
                if len(self.grid[UP]) != 1: self.grid[UP] = t.valid_nbs_up
                elif len(self.grid[UP]) != 1 and len(self.grid[UP]) != self.data_len: self.grid[UP] = self.common_nb(self.grid[UP], t.valid_nbs_up) 
                if len(self.grid[DOWN]) != 1: self.grid[DOWN] = t.valid_nbs_down
                elif len(self.grid[DOWN]) != 1 and len(self.grid[DOWN]) != self.data_len: self.grid[DOWN] = self.common_nb(self.grid[DOWN], t.valid_nbs_down)
                if len(self.grid[LEFT]) != 1: self.grid[LEFT] = t.valid_nbs_left
                elif len(self.grid[LEFT]) != 1 and len(self.grid[LEFT]) != self.data_len: self.grid[LEFT] = self.common_nb(self.grid[LEFT], t.valid_nbs_left) 
                if len(self.grid[LU]) == self.data_len: self.grid[LU] = t.valid_nbs_lu
                elif len(self.grid[LU]) != 1 and len(self.grid[LU]) != self.data_len: self.grid[LU] = self.common_nb(self.grid[LU], t.valid_nbs_lu)
                if len(self.grid[LD]) == self.data_len: self.grid[LD] = t.valid_nbs_ld
                elif len(self.grid[LD]) != 1 and len(self.grid[LD]) != self.data_len: self.grid[LD] = self.common_nb(self.grid[LD], t.valid_nbs_ld)

        elif y == 0: # UPPER BORDER
            if len(self.grid[DOWN]) != 1: self.grid[DOWN] = t.valid_nbs_down
            elif len(self.grid[DOWN]) != 1 and len(self.grid[DOWN]) != self.data_len: self.grid[DOWN] = self.common_nb(self.grid[DOWN], t.valid_nbs_down)
            if len(self.grid[LEFT]) != 1: self.grid[LEFT] = t.valid_nbs_left
            elif len(self.grid[LEFT]) != 1 and len(self.grid[LEFT]) != self.data_len: self.grid[LEFT] = self.common_nb(self.grid[LEFT], t.valid_nbs_left) 
            if len(self.grid[RIGHT]) != 1: self.grid[RIGHT] = t.valid_nbs_right
            elif len(self.grid[RIGHT]) != 1 and len(self.grid[RIGHT]) != self.data_len: self.grid[RIGHT] = self.common_nb(self.grid[RIGHT], t.valid_nbs_right)
            if len(self.grid[LD]) == self.data_len: self.grid[LD] = t.valid_nbs_ld
            elif len(self.grid[LD]) != 1 and len(self.grid[LD]) != self.data_len: self.grid[LD] = self.common_nb(self.grid[LD], t.valid_nbs_ld)
            if len(self.grid[RD]) == self.data_len: self.grid[RD] = t.valid_nbs_rd
            elif len(self.grid[RD]) != 1 and len(self.grid[RD]) != self.data_len: self.grid[RD] = self.common_nb(self.grid[RD], t.valid_nbs_rd)

        elif y == max or y == max + 1: # BOTTOM BORDER
            if len(self.grid[UP]) != 1: self.grid[UP] = t.valid_nbs_up
            elif len(self.grid[UP]) != 1 and len(self.grid[UP]) != self.data_len: self.grid[UP] = self.common_nb(self.grid[UP], t.valid_nbs_up) 
            if len(self.grid[LEFT]) != 1: self.grid[LEFT] = t.valid_nbs_left
            elif len(self.grid[LEFT]) != 1 and len(self.grid[LEFT]) != self.data_len: self.grid[LEFT] = self.common_nb(self.grid[LEFT], t.valid_nbs_left) 
            if len(self.grid[RIGHT]) != 1: self.grid[RIGHT] = t.valid_nbs_right
            elif len(self.grid[RIGHT]) != 1 and len(self.grid[RIGHT]) != self.data_len: self.grid[RIGHT] = self.common_nb(self.grid[RIGHT], t.valid_nbs_right)
            if len(self.grid[LU]) == self.data_len: self.grid[LU] = t.valid_nbs_lu
            elif len(self.grid[LU]) != 1 and len(self.grid[LU]) != self.data_len: self.grid[LU] = self.common_nb(self.grid[LU], t.valid_nbs_lu)
            if len(self.grid[RU]) == self.data_len: self.grid[RU] = t.valid_nbs_ru
            elif len(self.grid[RU]) != 1 and len(self.grid[RU]) != self.data_len: self.grid[RU] = self.common_nb(self.grid[RU], t.valid_nbs_ru)

        else: # ALL SIDES ARE FREE
            if len(self.grid[UP]) != 1: self.grid[UP] = t.valid_nbs_up
            elif len(self.grid[UP]) != 1 and len(self.grid[UP]) != self.data_len: self.grid[UP] = self.common_nb(self.grid[UP], t.valid_nbs_up) 
            if len(self.grid[DOWN]) != 1: self.grid[DOWN] = t.valid_nbs_down
            elif len(self.grid[DOWN]) != 1 and len(self.grid[DOWN]) != self.data_len: self.grid[DOWN] = self.common_nb(self.grid[DOWN], t.valid_nbs_down)
            if len(self.grid[LEFT]) != 1: self.grid[LEFT] = t.valid_nbs_left
            elif len(self.grid[LEFT]) != 1 and len(self.grid[LEFT]) != self.data_len: self.grid[LEFT] = self.common_nb(self.grid[LEFT], t.valid_nbs_left) 
            if len(self.grid[RIGHT]) != 1: self.grid[RIGHT] = t.valid_nbs_right
            elif len(self.grid[RIGHT]) != 1 and len(self.grid[RIGHT]) != self.data_len: self.grid[RIGHT] = self.common_nb(self.grid[RIGHT], t.valid_nbs_right)
            if len(self.grid[LU]) == self.data_len: self.grid[LU] = t.valid_nbs_lu
            elif len(self.grid[LU]) != 1 and len(self.grid[LU]) != self.data_len: self.grid[LU] = self.common_nb(self.grid[LU], t.valid_nbs_lu)
            if len(self.grid[RU]) == self.data_len: self.grid[RU] = t.valid_nbs_ru
            elif len(self.grid[RU]) != 1 and len(self.grid[RU]) != self.data_len: self.grid[RU] = self.common_nb(self.grid[RU], t.valid_nbs_ru)
            if len(self.grid[LD]) == self.data_len: self.grid[LD] = t.valid_nbs_ld
            elif len(self.grid[LD]) != 1 and len(self.grid[LD]) != self.data_len: self.grid[LD] = self.common_nb(self.grid[LD], t.valid_nbs_ld)
            if len(self.grid[RD]) == self.data_len: self.grid[RD] = t.valid_nbs_rd
            elif len(self.grid[RD]) != 1 and len(self.grid[RD]) != self.data_len: self.grid[RD] = self.common_nb(self.grid[RD], t.valid_nbs_rd)

    
    def check_adjacency(self, x: int, y: int, data: dict) -> dict:
        """
            Checks if a tile is not on a border and checks if the coordinates already have neighbouring tiles. 
            If so, the function returns the respective neighbours of those existing tiles as a dict.
            So if a tile on the left is collapsed, the left tile returns its possible right neighbours.
        """
        step = 1
        UP, DOWN, LEFT, RIGHT = (x, y - step), (x, y + step), (x - step, y), (x + step, y)
        LU, RU, LD, RD, = (x - step, y - step), (x + step, y - step), (x - step, y + step), (x + step, y + step)
        min, max = 0, int((self.width / IMG_SIZE) - 1)
        all_nbs = {}

        if x == min:
            if y == min: # CORNER L/U
                if len(self.grid[DOWN]) == 1: all_nbs["down"] = self.get_valid_nbs(self.grid[DOWN][0], data)[0]
                if len(self.grid[RIGHT]) == 1: all_nbs["right"] = self.get_valid_nbs(self.grid[RIGHT][0], data)[2]
                if len(self.grid[RD]) == 1: all_nbs["rd"] = self.get_valid_nbs(self.grid[RD][0], data)[4]

            elif y == max or y == max + 1: # CORNER L/D
                if len(self.grid[UP]) == 1: all_nbs["up"] = self.get_valid_nbs(self.grid[UP][0], data)[1]
                if len(self.grid[RIGHT]) == 1: all_nbs["right"] = self.get_valid_nbs(self.grid[RIGHT][0], data)[2]
                if len(self.grid[RU]) == 1: all_nbs["ru"] = self.get_valid_nbs(self.grid[RU][0], data)[6]

            else: # LEFT BORDER
                if len(self.grid[UP]) == 1: all_nbs["up"] = self.get_valid_nbs(self.grid[UP][0], data)[1]
                if len(self.grid[DOWN]) == 1: all_nbs["down"] = self.get_valid_nbs(self.grid[DOWN][0], data)[0]
                if len(self.grid[RIGHT]) == 1: all_nbs["right"] = self.get_valid_nbs(self.grid[RIGHT][0], data)[2]
                if len(self.grid[RD]) == 1: all_nbs["rd"] = self.get_valid_nbs(self.grid[RD][0], data)[4]
                if len(self.grid[RU]) == 1: all_nbs["ru"] = self.get_valid_nbs(self.grid[RU][0], data)[6]

        elif x == max:
            if y == min: # CORNER R/U
                if len(self.grid[DOWN]) == 1: all_nbs["down"] = self.get_valid_nbs(self.grid[DOWN][0], data)[0]
                if len(self.grid[LEFT]) == 1: all_nbs["left"] = self.get_valid_nbs(self.grid[LEFT][0], data)[3]
                if len(self.grid[LD]) == 1: all_nbs["ld"] = self.get_valid_nbs(self.grid[LD][0], data)[5]

            elif y == max or y == max + 1: # CORNER R/D
                if len(self.grid[UP]) == 1: all_nbs["up"] = self.get_valid_nbs(self.grid[UP][0], data)[1]
                if len(self.grid[LEFT]) == 1: all_nbs["left"] = self.get_valid_nbs(self.grid[LEFT][0], data)[3]
                if len(self.grid[LU]) == 1: all_nbs["lu"] = self.get_valid_nbs(self.grid[LU][0], data)[7]

            else: # RIGHT BORDER
                if len(self.grid[UP]) == 1: all_nbs["up"] = self.get_valid_nbs(self.grid[UP][0], data)[1]
                if len(self.grid[DOWN]) == 1: all_nbs["down"] = self.get_valid_nbs(self.grid[DOWN][0], data)[0]
                if len(self.grid[LEFT]) == 1: all_nbs["left"] = self.get_valid_nbs(self.grid[LEFT][0], data)[3]
                if len(self.grid[LD]) == 1: all_nbs["ld"] = self.get_valid_nbs(self.grid[LD][0], data)[5]
                if len(self.grid[LU]) == 1: all_nbs["lu"] = self.get_valid_nbs(self.grid[LU][0], data)[7]

        elif y == min: # UPPER BORDER
            if len(self.grid[DOWN]) == 1: all_nbs["down"] = self.get_valid_nbs(self.grid[DOWN][0], data)[0]
            if len(self.grid[LEFT]) == 1: all_nbs["left"] = self.get_valid_nbs(self.grid[LEFT][0], data)[3]
            if len(self.grid[RIGHT]) == 1: all_nbs["right"] = self.get_valid_nbs(self.grid[RIGHT][0], data)[2]
            if len(self.grid[LD]) == 1: all_nbs["ld"] = self.get_valid_nbs(self.grid[LD][0], data)[5]
            if len(self.grid[RD]) == 1: all_nbs["rd"] = self.get_valid_nbs(self.grid[RD][0], data)[4]

        elif y == max or y == max + 1: # BOTTOM BORDER
            if len(self.grid[UP]) == 1: all_nbs["up"] = self.get_valid_nbs(self.grid[UP][0], data)[1]
            if len(self.grid[LEFT]) == 1: all_nbs["left"] = self.get_valid_nbs(self.grid[LEFT][0], data)[3]
            if len(self.grid[RIGHT]) == 1: all_nbs["right"] = self.get_valid_nbs(self.grid[RIGHT][0], data)[2]
            if len(self.grid[LU]) == 1: all_nbs["lu"] = self.get_valid_nbs(self.grid[LU][0], data)[7]
            if len(self.grid[RU]) == 1: all_nbs["ru"] = self.get_valid_nbs(self.grid[RU][0], data)[6]

        else: # ALL SIDES ARE FREE
            if len(self.grid[UP]) == 1: all_nbs["up"] = self.get_valid_nbs(self.grid[UP][0], data)[1]
            if len(self.grid[DOWN]) == 1: all_nbs["down"] = self.get_valid_nbs(self.grid[DOWN][0], data)[0]
            if len(self.grid[LEFT]) == 1: all_nbs["left"] = self.get_valid_nbs(self.grid[LEFT][0], data)[3]
            if len(self.grid[RIGHT]) == 1: all_nbs["right"] = self.get_valid_nbs(self.grid[RIGHT][0], data)[2]
            if len(self.grid[LU]) == 1: all_nbs["lu"] = self.get_valid_nbs(self.grid[LU][0], data)[7]
            if len(self.grid[RU]) == 1: all_nbs["ru"] = self.get_valid_nbs(self.grid[RU][0], data)[6]
            if len(self.grid[LU]) == 1: all_nbs["lu"] = self.get_valid_nbs(self.grid[LU][0], data)[7]
            if len(self.grid[RU]) == 1: all_nbs["ru"] = self.get_valid_nbs(self.grid[RU][0], data)[6]

        return all_nbs


    def get_min_entropy(self) -> tuple:
        """
            Looks for the cells in the grid with the lowest entropy (meaning the least possible options) and returns the coordinates with the possible tiles.
        """
        options, coords = [], []

        for i, row in enumerate(self.grid):
            for j, elem in enumerate(row):
                if len(elem) != 1 and len(elem) != self.data_len:
                    options.append(elem)
                    coords.append((i, j))

        next = random.choice(options)
        index = options.index(next)
        self.grid[i][j] = next
        return next, coords[index]


    def find_common_option(self, options: list, adjacent_options: dict) -> str:
        """
            Looks for the common option(s) between all the directions and chooses a random one if there's more than one.
            If not, it will return one or none.
        """
        common = []
        all = [list(dir) for dir in adjacent_options.values()]      
        flattened = [l for ll in all for l in ll]

        for elem in flattened:
            if flattened.count(elem) == len(all) and elem not in common:
                common.append(elem)

        if len(common) == 1: return common[0] 
        elif common == []: return None
        return random.choice(common)


    def is_fully_collapsed(self) -> bool:
        """
            Checks if the wfc is fully collapsed by checking if any of the cells in the grid have more than 1 options.
        """
        for row in self.grid:
            for elem in row:
                if(len(elem) > 1):
                    return False
        return True


    def initialize_wfc(self, pos: tuple):
        """
            Creates a tile object and draws its sprite in the clicked spot of the grid.
            The spots around the first tile get uodated based on the tiles possible neighbours.
            After this the rest of the wave function collapse gets called.
        """
        data, img_names = self.load_data()
        name = random.choice(img_names)
        self.get_valid_nbs(name, data)
        up, down, left, right, lu, ru, ld, rd = self.get_valid_nbs(name, data)
        first_tile = tile.Tile(name, IMG_SIZE, IMG_SIZE, up, down, left, right, lu, ru, ld, rd)
        self.set_pos_first_tile(first_tile, pos)
        self.draw_tile(first_tile)
        self.create_grid(img_names)
        x, y = self.update_grid(first_tile)
        self.update_grid_around_tile(first_tile, x, y)
        self.wave_function_collapse(data)
        

    def wave_function_collapse(self, data: dict):
        """
            Checks if not fully collapsed and then picks a new position based on the lowest entropy (least amount of tile options).
            Then a new tile object gets created and drawn in that spot.
            The grid gets updated and the process repeats until the wave is fully collapsed (the len of all options in the grid is equal to 1).
        """
        while not self.is_fully_collapsed():
        #for i in range(100):
            options, (x, y) = self.get_min_entropy()
            if (x, y) not in self.occupied_tiles:         
                adjacent_options = self.check_adjacency(x, y, data)
                name = self.find_common_option(options, adjacent_options)
                if name != None:
                    up, down, left, right, lu, ru, ld, rd = self.get_valid_nbs(name, data)
                    next = tile.Tile(name, IMG_SIZE, IMG_SIZE, up, down, left, right, lu, ru, ld, rd)
                    next.set_coords((int(x * 16), int(y * 16)))
                    self.occupied_tiles.append((x, y))
                    self.draw_tile(next)
                    self.update_grid(next)
                    self.update_grid_around_tile(next, x, y)
                else:
                    # backtrack?
                    #self.wave_function_collapse(data) # maximum recursion depth exceeded
                    pass

        
    def on_startup(self):
        # EXTRA: draw a blended image of all options for every spot in grid?
        pass
    

    def update_blend(self):
        # EXTRA: change the blended image to options left for every spot in grid?
        pass


    def on_cleanup(self):
        pygame.quit()
        sys.exit()
 

    def on_execute(self):
        """
            Gets called after creation of the MapGenerator object to run the program.
            Repeatedly checks if the program is still running and if so, it repeatedly checks for events once per frame.
        """
        if self.on_init() == False:
            self.running = False
        
        pygame.display.set_caption('MapGenerator')
        self.on_startup()
        while(self.running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.FramePerSec.tick(self.FPS)
        self.on_cleanup()