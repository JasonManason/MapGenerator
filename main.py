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

    def draw_tile(self, tile: tile, coords: tuple): # move to tile class?
        self.display_surf.blit((pygame.image.load(f"tiles/{tile}.png")), coords)
        pygame.display.update()
    
    def start_collapse(self, pos: tuple): # mouse click will start collapse of tiles
        """
        Has user click a space where the first random tile spawns.
        """
        print(pos)
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
        
        self.collapse_further(m, t)

    def collapse_further(self, m: mapoftiles, t: tile):
        """
        Draws new tiles based on options from the original tile until the map is filled.
        """
        coords = t.get_coords()
        m.add_occupied_tiles(coords)
        usable_sides = t.get_usable_nbs(coords, m)
        direction = random.choice(list(usable_sides))
        next_tile = random.choice(usable_sides[direction]) # random for now, will be based on weights
        next = tile.Tile()
        next.set_name(next_tile)
        next.set_initial_nbs()
        coords_up = (coords[0], coords[1] - 16)
        coords_down = (coords[0], coords[1] + 16)
        coords_left = (coords[0] - 16, coords[1])
        coords_right = (coords[0] + 16, coords[1])
        all_coords = [coords_up, coords_down, coords_left, coords_right]
        #print("usable_sides:\t\t", usable_sides)

        while m.check_if_taken(direction, t, all_coords): # True // While??
            direction = t.get_new_direction(direction, usable_sides) # takes in current direction and picks a new one from usable sides?
            # if there's no more usable sides, pick random free tile?
            print("picking new direction")



        """PLAN for checking if next tile free/taken"""
        # function takes in (direction), returns bool
        # while taken == true: call function that takes in (usable_sides, direction) and returns new usable_sides
        # pick random direction from new_usable_sides (later based on weights)
        # function takes in (direction), returns bool, if true repeat while loop, if false continue with current direction

        # set coords based on direction // ADD next tile as active_nb to current tile!
        #this can be a seperate function/ method??
        if direction == "nb_up":
            next.set_coords(coords_up)

        elif direction == "nb_down":
            next.set_coords(coords_down)

        elif direction == "nb_left":
            next.set_coords(coords_left)

        else: # nb_right
            next.set_coords(coords_right)
        
        while len(m.get_occupied_tiles()) < m.get_max_tiles():
            m.add_occupied_tiles(next.coords)
            self.draw_tile(next.name, next.coords)
            self.collapse_further(m, next)

    def on_startup(self): # called once when the program starts
        # draw grid, instructions for user
        # buttons / dropdown to choose map size / slider for slowmo?
        pass

    def on_cleanup(self): # close window
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