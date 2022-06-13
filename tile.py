import pygame
 
# file = open('nb_rules.json')
# data = json.load(file)

# for i in data["data"]:
#     print(i)

# file.close()

class Tile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("tiles/grass0") # test image for now, will be variable
        self.rect = self.image.get_rect()
        #self.image = pygame.image.load(tiles/<image var here>)

    # def is_clicked(self):
    #     return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

        