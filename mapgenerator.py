import pygame, sys, random, tile, json
from pygame.locals import *
from itertools import product
import numpy as np
IMG_SIZE = 16

class MapGenerator:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 640
        self.occupied_tiles = []


    def on_init(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.FPS = 30
        self.FramePerSec = pygame.time.Clock()
        self.running = True


    def on_event(self, event: pygame.event):
        if event.type == pygame.QUIT:
            self.running = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.initialize_wfc(pos)
            pygame.event.set_blocked(pygame.MOUSEBUTTONUP)


    def draw_tile(self, t: tile):
        self.display_surf.blit((pygame.image.load(f"tiles/{t.img_name}.png")), t.coords)
        pygame.display.update()
       

    def load_data(self) -> tuple:
        file = open('nb_rules.json')
        data = json.load(file)
        file.close()
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
        up, down, left, right = [], [], [], []
        for i in data:
            if i == name:
                up, down, left, right = list(data[i].values())

        return up, down, left, right


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


    def update_grid_around_tile(self, t: tile, x: int, y: int):
        """
            Changes the possible outcomes of tiles around the drawn tile.
        """
        step = 1
        UP, DOWN, LEFT, RIGHT = (x, y - step), (x, y + step), (x - step, y), (x + step, y)
        max = int((self.width / IMG_SIZE) - 1)

        if x == 0: # LEFT BORDER
            if y == 0: # CORNER L/U                    
                if len(self.grid[DOWN]) != 1: self.grid[DOWN] = t.valid_nbs_down
                if len(self.grid[RIGHT]) != 1: self.grid[RIGHT] = t.valid_nbs_right
            elif y == max: # CORNER L/D
                if len(self.grid[UP]) != 1: self.grid[UP] = t.valid_nbs_up    
                if len(self.grid[RIGHT]) != 1: self.grid[RIGHT] = t.valid_nbs_right
            else:
                if len(self.grid[UP]) != 1: self.grid[UP] = t.valid_nbs_up
                if len(self.grid[DOWN]) != 1: self.grid[DOWN] = t.valid_nbs_down
                if len(self.grid[RIGHT]) != 1: self.grid[RIGHT] = t.valid_nbs_right

        elif x == max: # RIGHT BORDER     
            if y == 0: # CORNER R/U
                if len(self.grid[DOWN]) != 1: self.grid[DOWN] = t.valid_nbs_down
                if len(self.grid[LEFT]) != 1: self.grid[LEFT] = t.valid_nbs_left
            elif y == max: # CORNER R/D
                if len(self.grid[UP]) != 1: self.grid[UP] = t.valid_nbs_up
                if len(self.grid[LEFT]) != 1: self.grid[LEFT] = t.valid_nbs_left
            else:
                if len(self.grid[UP]) != 1: self.grid[UP] = t.valid_nbs_up
                if len(self.grid[DOWN]) != 1: self.grid[DOWN] = t.valid_nbs_down
                if len(self.grid[LEFT]) != 1: self.grid[LEFT] = t.valid_nbs_left

        elif y == 0 and x != 0 and x != max: # UPPER BORDER
            if len(self.grid[DOWN]) != 1: self.grid[DOWN] = t.valid_nbs_down
            if len(self.grid[LEFT]) != 1: self.grid[LEFT] = t.valid_nbs_left
            if len(self.grid[RIGHT]) != 1: self.grid[RIGHT] = t.valid_nbs_right
        elif y == max and x != 0 and x != max: # BOTTOM BORDER
            if len(self.grid[UP]) != 1: self.grid[UP] = t.valid_nbs_up
            if len(self.grid[LEFT]) != 1: self.grid[LEFT] = t.valid_nbs_left
            if len(self.grid[RIGHT]) != 1: self.grid[RIGHT] = t.valid_nbs_right

        else: # ALL SIDES FREE
            if len(self.grid[UP]) != 1: self.grid[UP] = t.valid_nbs_up
            if len(self.grid[DOWN]) != 1: self.grid[DOWN] = t.valid_nbs_down
            if len(self.grid[LEFT]) != 1: self.grid[LEFT] = t.valid_nbs_left
            if len(self.grid[RIGHT]) != 1: self.grid[RIGHT] = t.valid_nbs_right

    
    def check_adjacency(self, x: int, y: int, data: dict) -> dict:
        """
            Checks if a tile is not on a border and checks if the coordinates already have neighbouring tiles. 
            If so, the function returns the respective neighbours of those existing tiles as a dict.
        """
        step = 1
        UP, DOWN, LEFT, RIGHT = (x, y - step), (x, y + step), (x - step, y), (x + step, y)
        min, max = 0, int((self.width / IMG_SIZE) - 1)
        all_nbs = {}

        if x == min:
            if y == min:
                if len(self.grid[DOWN]) == 1: all_nbs["down"] = self.get_valid_nbs(self.grid[DOWN][0], data)[0]
                if len(self.grid[RIGHT]) == 1: all_nbs["right"] = self.get_valid_nbs(self.grid[RIGHT][0], data)[2]

            elif y == max:
                if len(self.grid[UP]) == 1: all_nbs["up"] = self.get_valid_nbs(self.grid[UP][0], data)[1]
                if len(self.grid[RIGHT]) == 1: all_nbs["right"] = self.get_valid_nbs(self.grid[RIGHT][0], data)[2]

            else:
                if len(self.grid[UP]) == 1: all_nbs["up"] = self.get_valid_nbs(self.grid[UP][0], data)[1]
                if len(self.grid[DOWN]) == 1: all_nbs["down"] = self.get_valid_nbs(self.grid[DOWN][0], data)[0]
                if len(self.grid[RIGHT]) == 1: all_nbs["right"] = self.get_valid_nbs(self.grid[RIGHT][0], data)[2]

        elif x == max:
            if y == min:
                if len(self.grid[DOWN]) == 1: all_nbs["down"] = self.get_valid_nbs(self.grid[DOWN][0], data)[0]
                if len(self.grid[RIGHT]) == 1: all_nbs["right"] = self.get_valid_nbs(self.grid[RIGHT][0], data)[2]

            elif y == max:
                if len(self.grid[UP]) == 1: all_nbs["up"] = self.get_valid_nbs(self.grid[UP][0], data)[1]
                if len(self.grid[LEFT]) == 1: all_nbs["left"] = self.get_valid_nbs(self.grid[LEFT][0], data)[3]

            else:
                if len(self.grid[UP]) == 1: all_nbs["up"] = self.get_valid_nbs(self.grid[UP][0], data)[1]
                if len(self.grid[DOWN]) == 1: all_nbs["down"] = self.get_valid_nbs(self.grid[DOWN][0], data)[0]
                if len(self.grid[LEFT]) == 1: all_nbs["left"] = self.get_valid_nbs(self.grid[LEFT][0], data)[3]

        elif y == min:
            if len(self.grid[DOWN]) == 1: all_nbs["down"] = self.get_valid_nbs(self.grid[DOWN][0], data)[0]
            if len(self.grid[LEFT]) == 1: all_nbs["left"] = self.get_valid_nbs(self.grid[LEFT][0], data)[3]
            if len(self.grid[RIGHT]) == 1: all_nbs["right"] = self.get_valid_nbs(self.grid[RIGHT][0], data)[2]

        elif y == max:
            if len(self.grid[UP]) == 1: all_nbs["up"] = self.get_valid_nbs(self.grid[UP][0], data)[1]
            if len(self.grid[LEFT]) == 1: all_nbs["left"] = self.get_valid_nbs(self.grid[LEFT][0], data)[3]
            if len(self.grid[RIGHT]) == 1: all_nbs["right"] = self.get_valid_nbs(self.grid[RIGHT][0], data)[2]

        else:
            if len(self.grid[UP]) == 1: all_nbs["up"] = self.get_valid_nbs(self.grid[UP][0], data)[1]
            if len(self.grid[DOWN]) == 1: all_nbs["down"] = self.get_valid_nbs(self.grid[DOWN][0], data)[0]
            if len(self.grid[LEFT]) == 1: all_nbs["left"] = self.get_valid_nbs(self.grid[LEFT][0], data)[3]
            if len(self.grid[RIGHT]) == 1: all_nbs["right"] = self.get_valid_nbs(self.grid[RIGHT][0], data)[2]

        return all_nbs


    def get_min_entropy(self) -> tuple:
        """
            Looks for the cells in the grid with the lowest entropy (meaning the least possible options) and returns the coordinates with the possible tiles.
        """
        options, coords = [], []

        for i, row in enumerate(self.grid):
            for j, elem in enumerate(row):
                if len(elem) != 1 and len(elem) != 36:
                    options.append(elem)
                    coords.append((i, j))

        next = random.choice(options)
        index = options.index(next)
        self.grid[i][j] = next
        return next, coords[index]


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
        nbs_up, nbs_down, nbs_left, nbs_right = self.get_valid_nbs(name, data)
        first_tile = tile.Tile(name, IMG_SIZE, IMG_SIZE, nbs_up, nbs_down, nbs_left, nbs_right)
        self.set_pos_first_tile(first_tile, pos)
        self.draw_tile(first_tile)
        self.create_grid(img_names)
        x, y = self.update_grid(first_tile)
        self.update_grid_around_tile(first_tile, x, y)
        self.wave_function_collapse(data)


    def find_common_option(self, options: list, adjacent_options: dict) -> str:
        """
            Looks for the common option(s) between all the directions and chooses a random one if there's more than one.
            If not, it will return one or none.
        """
        all = [options]
        for dir in adjacent_options.values():
            all.append(dir)
    
        common = list(set.intersection(*[set(l) for l in all]))
        print(common) 
        if len(common) == 1:         
            return common[0] 
        elif common == []:
            return None
        return random.choice(common)
        

    def wave_function_collapse(self, data: dict):
        """
            Checks if not fully collapsed and then picks a new position based on the lowest entropy (least amount of tile options).
            Then a new tile object gets created and drawn in that spot.
            The grid gets updated and the process repeats until the wave is fully collapsed (the len of all options in the grid is equal to 1).
        """
        while not self.is_fully_collapsed():
            options, (x, y) = self.get_min_entropy()
            if (x, y) not in self.occupied_tiles:
                adjacent_options = self.check_adjacency(x, y, data)
                name = self.find_common_option(options, adjacent_options)
                if name != None:
                    up, down, left, right = self.get_valid_nbs(name, data)
                    next = tile.Tile(name, IMG_SIZE, IMG_SIZE, up, down, left, right)
                    next.set_coords((int(x * 16), int(y * 16)))
                    self.occupied_tiles.append((x, y))
                    self.draw_tile(next)
                    self.update_grid(next)
                    self.update_grid_around_tile(next, x, y)
                else:
                    #self.wave_function_collapse(data) # maximum recursion depth exceeded
                    pass
            print(len(self.occupied_tiles))

        
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
        if self.on_init() == False:
            self.running = False
        
        pygame.display.set_caption('MapGenerator')
        self.on_startup()
        while(self.running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.FramePerSec.tick(self.FPS)
        self.on_cleanup()