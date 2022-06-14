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
        """Now collapse from there, first check if all sides are free, then recursive collapse??"""

    def collapse_further(self, m, t):
        count = 0

        while count < m.get_max_tiles():
            coords = t.get_coords() # upper left (x, y) of tile
            usable_sides = t.get_usable_nbs(coords, m)
            print("usable_sides\n\n", usable_sides, "\n\n")



            # tile = current tile
            # check corner/side
            # choose random direction for now (-directionss if corner/side)
            # remember placement upper/left corner for this tile
            # choose random nb for now
            # draw in place # draw_tile(<Tile Class>, (x, y))
            # new tile = current tile
            # count += 1
            # repeat 

            count += 1 # only count after nb is placed!!
            pass
        pass

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