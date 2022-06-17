import pygame, sys, random, mapoftiles, tile
from pygame.locals import *
from itertools import product

class MapGenerator:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 640 # has to scale with user map size choice later


    def on_init(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.FPS = 30
        self.FramePerSec = pygame.time.Clock()
        self.running = True

 
    def on_event(self, event: pygame.event): # https://www.pygame.org/docs/ref/event.html
        if event.type == pygame.QUIT:
            self.running = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.start_collapse(pos)
            # first; check if first click was on a tile before blocking event
            pygame.event.set_blocked(pygame.MOUSEBUTTONUP) # disable mouseclick after first click to start collapse


    def draw_tile(self, tile: tile, coords: tuple):
        self.display_surf.blit((pygame.image.load(f"tiles/{tile}.png")), coords)
        pygame.display.update()
    

    def start_collapse(self, pos: tuple): # mouse click will start collapse of tiles
        """
        Has user click a space where the first random tile spawns.
        """
        m = mapoftiles.MapOfTiles()
        tiles = m.load_tileset()
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

        free_coords = [c for c in t.check_adjacency(t.coords, m)[0] if c not in m.get_occupied_tiles()]
        print("free_coords in initial tile:\t\t", free_coords)
        self.wave_collapse(m, t, free_coords) # test


    def wave_collapse(self, m: mapoftiles, t: tile, free_coords: list): # test
        """
        Recursively collapses the wave further from the first clicked tile.
        """
        adjacent_coords, usable_sides = t.check_adjacency(t.get_coords(), m)
        print("adjacent_coords: ", adjacent_coords, type(adjacent_coords))
        print("usable_sides: ", usable_sides)

        for i, c in enumerate(free_coords):
            next = "tile" + str(len(m.get_occupied_tiles()))
            next = tile.Tile()
            next.set_initial_nbs()
            next.set_coords(c)
            if adjacent_coords[i] == c:
                img_name = random.choice(list(usable_sides.values())[i])
            next.set_name(img_name)
            print("name:\t\t", next.name)
            self.draw_tile(next.name, next.coords)   
            m.add_occupied_tiles(next.coords)
            free_coords_next = [c for c in next.check_adjacency(next.coords, m)[0] if c not in m.get_occupied_tiles()]
        
        while (len(m.get_occupied_tiles())) < m.max_tiles:
            self.wave_collapse(m, next, free_coords_next)


    def on_startup(self): # called once when the program starts
        # draw grid => for loop with blocks 14x14ps and 1px line around them?
        # #instructions for user
        # buttons / dropdown to choose map size / slider for slowmo?
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


if __name__ == "__main__":
    MG = MapGenerator()
    MG.on_execute()