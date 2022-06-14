import pygame, json

class Tile(pygame.sprite.Sprite): # https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
    def __init__(self):
        super().__init__()
        # self.rect = self.image.get_rect()
        self.clicked()
    
    def set_sprite(self, new_img): # set image via string
        self.image = new_img

    def get_nbs(self):
        # get rest of info via string "name" and search in jsonfile, return a dict of nb info
        file = open('nb_rules.json')
        data = json.load(file)
        file.close()
        for key, val in data["data"].items():
            if key == self.image:
                print(key, val)
                self.nbs = (key, val)
                return(key, val) # dict{}
    
    def clicked(self): # when set to true, user should not be able to click again
        self.clicked = True

    def set_nbs(self, new_nbs):
        self.nbs = new_nbs


    # def get_coords(self): # return upper left coordinates of tiles?
    #     return self.coords

    # def is_clicked(self):
    #     return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

        