import pygame, sys, json, random
from pygame.locals import *
import map, tile
from itertools import product


class MapGenerator:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 320, 320
        
    def on_execute(self):
        pass

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

    
    def start_collapse(self, pos): # mouse click will start collapse of tiles
        print(pos)
        m = map.Map()
        tiles = m.load_tileset() # list of tiles as strings
        coords = [c for c in range(self.width) if c % 16 == 0]
        coordinates = list(product(coords, coords))
        first_tile = random.choice(tiles)
        t0 = tile.Tile()
        t0.set_sprite(first_tile)
        t0.get_nbs()

        #Check to see where the first tile needs to be placed:
        for x_y in coordinates:
            rect_x_y = pygame.Rect(x_y, (16, 16))
            if rect_x_y.collidepoint(pos):
                self.display_surf.blit((pygame.image.load(f"tiles/{first_tile}.png")), x_y)        
        pygame.display.update()
        
        """Now collapse from there, first check if all sides are free, then recursive collapse??"""


    def on_loop(self): # gameplay loop
        pass

    def on_startup(self): # called once when the program starts
        # draw grid?
        pass

    def on_cleanup(self): # close game
        pygame.quit()
        sys.exit()
 
    def on_execute(self): # initialize pygame and enter main loop
        if self.on_init() == False:
            self.running = False
        
        pygame.display.set_caption('MapGenerator')
        self.on_startup()
        while( self.running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.FramePerSec.tick(self.FPS)
        self.on_cleanup()


if __name__ == "__main__":
    MG = MapGenerator()
    MG.on_execute()