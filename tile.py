import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, img_name, width, height, valid_nbs_up, valid_nbs_down, valid_nbs_left, valid_nbs_right): #, weight):
        super().__init__()
        self.img_name = img_name
        self.width = width
        self.height = height
        self.valid_nbs_up = valid_nbs_up
        self.valid_nbs_down = valid_nbs_down
        self.valid_nbs_left = valid_nbs_left
        self.valid_nbs_right = valid_nbs_right
        #self.weight = weight


    def set_img_name(self, img_name: str):
        self.img_name = img_name


    def get_img_name(self) -> str:
        return self.img_name


    def set_nbs(self):
        self.nbs = [self.valid_nbs_up, self.valid_nbs_down, self.valid_nbs_left, self.valid_nbs_right]


    def get_nbs(self) -> list:
        return self.nbs


    def set_coords(self, coords: tuple):
        self.coords = coords


    def get_coords(self) -> tuple:
        return self.coords