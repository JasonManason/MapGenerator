import pygame

class Tile(pygame.sprite.Sprite):
    """
    A tile object to be placed on the grid of the map generator.
    """
    def __init__(self, img_name, width, height, valid_nbs_up, valid_nbs_down, valid_nbs_left, valid_nbs_right, \
        valid_nbs_lu, valid_nbs_ru, valid_nbs_ld, valid_nbs_rd):
        """
        Constructor for the tile object.
        """
        super().__init__()
        self.img_name = img_name
        self.width = width
        self.height = height
        self.valid_nbs_up = valid_nbs_up
        self.valid_nbs_down = valid_nbs_down
        self.valid_nbs_left = valid_nbs_left
        self.valid_nbs_right = valid_nbs_right
        self.valid_nbs_lu = valid_nbs_lu # left up
        self.valid_nbs_ru = valid_nbs_ru # right up
        self.valid_nbs_ld = valid_nbs_ld # left down
        self.valid_nbs_rd = valid_nbs_rd # right down


    def set_img_name(self, img_name: str):
        self.img_name = img_name


    def set_coords(self, coords: tuple):
        self.coords = coords