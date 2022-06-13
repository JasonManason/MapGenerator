import pygame, sys, json
from pygame.locals import *
import map, tile


class MapGenerator:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 400, 400
        
    def on_execute(self):
        pass

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.FPS = 30
        self.FramePerSec = pygame.time.Clock()
        self._running = True
 
    def on_event(self, event): #check if an event has occured
        if event.type == pygame.QUIT:
            self._running = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.start_collapse(pos)
    
    def start_collapse(self, pos): # mouse click will start collapse of tiles
        print(pos)
        # clicked_tile = [t for t in tiles if t.rect.collidepoint(pos)]
        pass

    def on_loop(self): # gameplay loop
        pass

    def on_render(self): # render to pygame window
        pass

    def on_cleanup(self): # close game
        pygame.quit()
        sys.exit()
 
    def on_execute(self): # initialize pygame and enter main loop
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render() 
            self.FramePerSec.tick(self.FPS)
        self.on_cleanup()


if __name__ == "__main__":
    MG = MapGenerator()
    MG.on_execute()