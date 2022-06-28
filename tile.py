import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, img_name, width, height, valid_nbs_up, valid_nbs_down, valid_nbs_left, valid_nbs_right, \
        valid_nbs_lu, valid_nbs_ru, valid_nbs_ld, valid_nbs_rd):
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


    def get_img_name(self) -> str:
        return self.img_name


    def set_nbs(self):
        self.nbs = [self.valid_nbs_up, self.valid_nbs_down, self.valid_nbs_left, self.valid_nbs_right, \
            self.valid_nbs_lu, self.valid_nbs_ru, self.valid_nbs_ld, self.valid_nbs_rd]


    def get_nbs(self) -> list:
        return self.nbs


    def set_coords(self, coords: tuple):
        self.coords = coords


    def get_coords(self) -> tuple:
        return self.coords