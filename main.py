import pygame, sys, random
from pygame.locals import *
import map, tile
from itertools import product

class MapGenerator:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 320, 320 # has to scale with user map size choice later

    def on_init(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.FPS = 30
        self.FramePerSec = pygame.time.Clock()
        self.running = True
 
    def on_event(self, event): # https://www.pygame.org/docs/ref/event.html
        if event.type == pygame.QUIT:
            self.running = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.start_collapse(pos)
            # first check if first click was on a tile before blocking event
            pygame.event.set_blocked(pygame.MOUSEBUTTONUP) # disable mouseclick after first click to start collapse

    def draw_tile(self, tile, coords):
        self.display_surf.blit((pygame.image.load(f"tiles/{tile}.png")), coords)
        pygame.display.update()
    
    def start_collapse(self, pos): # mouse click will start collapse of tiles
        """
        Has user click a space where the first random tile spawns.
        """
        print(pos)
        m = map.Map()
        tiles = m.load_tileset() # list of tiles as strings
        coords = [c for c in range(self.width) if c % 16 == 0]
        coordinates = list(product(coords, coords))
        first_tile = random.choice(tiles) # first tile stays random?
        t = tile.Tile()
        t.set_name(first_tile)
        t.set_initial_nbs()

        #Check to see where the first tile needs to be placed:
        for x_y in coordinates:
            rect_x_y = pygame.Rect(x_y, (16, 16))
            if rect_x_y.collidepoint(pos):
                t.set_coords(x_y)
                self.draw_tile(first_tile, x_y)
        
        self.collapse_further(m, t) # t = first tile
    
    def collapse_further(self, m, t):
        """
        Draws new tiles based on options from the original tile until the map is filled.
        """
        count = 0
        coords = t.get_coords() # upper left (x, y) of tile
        usable_sides = t.get_usable_nbs(coords, m)
        print("usable_sides\n\n", usable_sides, "\n\n")
        direction = random.choice(list(usable_sides)) # random for now, will be based on weights
        next_tile = random.choice(usable_sides[direction]) # random for now, will be based on weights
        next = tile.Tile()
        next.set_name(next_tile)
        next.set_initial_nbs()

        # set coords based on direction
        if direction == "nb_up":
            next.set_coords((coords[0], coords[1] - 16))
        elif direction == "nb_down":
            next.set_coords((coords[0], coords[1] + 16))
        elif direction == "nb_left":
            next.set_coords((coords[0] - 16, coords[1]))
        else: # right
            next.set_coords((coords[0] + 16, coords[1]))
        
        while count < m.get_max_tiles():
            self.draw_tile(next.name, next.coords)
            self.collapse_further(m, next)
            count += 1


    def on_startup(self): # called once when the program starts
        # draw grid, explanation for user
        # buttons / dropdown to choose map size
        pass

    def on_cleanup(self): # close game
        pygame.quit()
        sys.exit()
 
    def on_execute(self): # initialize pygame and enter main loop
        if self.on_init() == False:
            self.running = False
        
        pygame.display.set_caption('MapGenerator')
        self.on_startup()
        while(self.running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.FramePerSec.tick(self.FPS)
        self.on_cleanup()


if __name__ == "__main__":
    MG = MapGenerator()
    MG.on_execute()