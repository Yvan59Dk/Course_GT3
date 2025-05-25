from dataclasses import dataclass
from math import *
from time import *
from random import *
import pygame
reso = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sound1 = pygame.mixer.Sound('./assets/music/pneu1.ogg')
        self.sound1.set_volume(0.3)
        self.sound2 = pygame.mixer.Sound('./assets/music/pneu2.ogg')
        self.sound2.set_volume(0.3)
        self.sprite_sheet = pygame.image.load("./assets/sprites/player.png")
        self.item_sheet = pygame.image.load("./assets/sprites/item.png")
        self.image = self.get_image(self.sprite_sheet, 0, 0)
        self.image.set_colorkey([255, 0, 255])
        self.rect = self.image.get_rect()
        self.anime = [0, 0]
        self.position = [x, y]
        self.images = {
            'down' : self.get_image(self.sprite_sheet, 0, 0),
            'left': self.get_image(self.sprite_sheet, 0, 64*reso),
            'right': self.get_image(self.sprite_sheet, 0, 64*reso*2),
            'up': self.get_image(self.sprite_sheet, 0, 64*reso*3)
        }
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.speed = [0, 0, 0, 0]

    def save_location(self): self.old_position = self.position.copy()

    def change_animation(self):
        self.image = self.get_image(self.sprite_sheet, floor(self.anime[0])*32, floor(self.anime[1])*32)
        self.image.set_colorkey([255, 0, 255])

    def change_vitesse(self, L):
        for i in range (len(self.speed)):
            vit = self.speed[i]+L[i]
            if 0 <= vit :
                if vit <= 6:
                    self.speed[i] = vit
            else:
                self.speed[i] = 0

    def move_anime(self):
        vit = 0.15
        if self.anime[0] + vit >= 3:
            self.anime[0] = 1
        elif self.speed[0] < 1 and self.speed[1] < 1 and self.speed[2] < 1 and self.speed[3] < 1 :
            self.anime[0] = 0
        else:
            self.anime[0] += vit

    def move(self):
        self.change_vitesse( [-0.15, -0.15, -0.15, -0.15] )
        self.position[1] += -self.speed[0] + self.speed[1]
        self.position[0] += -self.speed[2] + self.speed[3]
        if self.speed[0] < 1 and self.speed[1] < 1 and self.speed[2] < 1 and self.speed[3] < 1 :
            self.anime[0] = 0
        if sum(self.speed) > 9 :
            if randint(0,1) == 0 and pygame.mixer.get_busy() == False :
                self.sound1.play()
            elif randint(0,1) == 1 and pygame.mixer.get_busy() == False :
                self.sound2.play()


    def move_right(self): self.change_vitesse( [0, 0, 0, 0.3] )
    def move_left(self): self.change_vitesse( [0, 0, 0.3, 0] )
    def move_up(self): self.change_vitesse( [0.3, 0, 0, 0] )
    def move_down(self): self.change_vitesse( [0, 0.3, 0, 0] )

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.speed = [self.speed[1]/2,self.speed[0]/2,self.speed[3]/2,self.speed[2]/2]

    def get_image(self, sheet, x, y):
        image = pygame.Surface([32*reso,32*reso])
        image.blit(sheet, (0, 0), (x, y, 32*reso, 32*reso))
        return image

    def get_wrong_way(self):
        image = self.get_image(self.item_sheet, 0, 0)
        image.set_colorkey([255, 0, 255])
        return image

    def update_wrong_way(self):
        self.image = self.get_wrong_way()