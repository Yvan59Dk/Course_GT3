from dataclasses import dataclass
from math import *
from time import *
from random import *
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
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
        self.anime:list = [0, 0]
        self.position:list[int] = [0, 0]
        self.images = {
            'down' : self.get_image(self.sprite_sheet, 0, 0),
            'left': self.get_image(self.sprite_sheet, 0, 64),
            'right': self.get_image(self.sprite_sheet, 0, 64*2),
            'up': self.get_image(self.sprite_sheet, 0, 64*3)
        }
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.5, 32)
        self.old_position = self.position.copy()
        self.speed:list[float] = [0, 0, 0, 0]

    def save_location(self): 
        """ Sauvegarde la position précédente de la voiture """
        self.old_position = self.position.copy()

    def load_sprite(self):
        """ Fonction servant à charger le sprite de la voiture """
        self.image = self.get_image(self.sprite_sheet, floor(self.anime[0])*32, self.anime[1]*32)
        self.image.set_colorkey([255, 0, 255])

    def change_hitbox(self):
        """
            Fonction permettant de changer dynamiquement la hitbox de la voiture en fonction de son sens.
            Elle se base sur la liste "anime" pour pouvoir savoir quel est le sens de la voiture.
        """
        if self.anime[1] == 0 or self.anime[1] == 3 :
            self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.5, 32)
        elif self.anime[1] == 1 or self.anime[1] == 2 :
            self.hitbox = pygame.Rect(0, 0, 32, self.rect.width * 0.5)

    def change_speed(self, speed_change:list[float]):
        """
            Fonction qui prend en paramétre un liste de 4 éléments de type float. Chacun de ces élements modifira la vitesse de la voiture. 
            La vitesse évolue en fonction du signe de l'élément et de sa taille.

            **Format : change_speed(['haut','bas','gauche','droite'])**
        """
        assert len(speed_change) == 4
        for i in range(len(self.speed)):
            vit = self.speed[i]+speed_change[i]
            if 0 <= vit :
                if vit <= 6:
                    self.speed[i] = vit
            else:
                self.speed[i] = 0

    def move_anime(self):
        """
            Fonction permettant de changer le sprite souhaité en fonction de la vitesse. 
             - En dessous d'une vitesse de 1, le sprite sera celui de base.
             - Au dessus d'une vitesse de 1, le sprite va basculer entre son sprite d'animation 1 et 2.
        """
        vit = 0.15
        if self.anime[0] + vit >= 3:
            self.anime[0] = 1
        elif self.speed[0] < 1 and self.speed[1] < 1 and self.speed[2] < 1 and self.speed[3] < 1 :
            self.anime[0] = 0
        else:
            self.anime[0] += vit

    def move(self):
        """
            **Fonction sensé être exécuter toute les frames** : *c'est un groupement des fonctions.*

            Elle exécute un changement de vitesse constant, met à jour la position,
            met en valeur par défaut l'animation et s'occupe des bruitages.
        """
        self.change_speed( [-0.15, -0.15, -0.15, -0.15] )
        self.position[1] += -self.speed[0] + self.speed[1]
        self.position[0] += -self.speed[2] + self.speed[3]
        if self.speed[0] < 1 and self.speed[1] < 1 and self.speed[2] < 1 and self.speed[3] < 1 :
            self.anime[0] = 0
        if sum(self.speed) > 9 :
            if randint(0,1) == 0 and pygame.mixer.get_busy() == False :
                self.sound1.play()
            elif randint(0,1) == 1 and pygame.mixer.get_busy() == False :
                self.sound2.play()


    def move_right(self): self.change_speed( [0, 0, 0, 0.3] )
    def move_left(self): self.change_speed( [0, 0, 0.3, 0] )
    def move_up(self): self.change_speed( [0.3, 0, 0, 0] )
    def move_down(self): self.change_speed( [0, 0.3, 0, 0] )

    def update(self):
        """ Fonction qui met à jour les données de position de la voiture. """
        self.change_hitbox()
        self.rect.topleft = self.position
        self.hitbox.midbottom = self.rect.midbottom

    def move_back(self):
        """ Fonction qui permet à la voiture de rebondir en arriére. """
        self.position = self.old_position
        self.rect.topleft = self.position
        self.hitbox.midbottom = self.rect.midbottom
        self.speed = [self.speed[1]/2,self.speed[0]/2,self.speed[3]/2,self.speed[2]/2]

    def get_image(self, sheet, x:int, y:int) -> pygame.Surface:
        """
            Fonction prenant en paramétre un fichier et des coordonnées x et y.
            Elle retourne un carré de 32*32 depuis ce fichier.

            **Format : get_image(fichier, coordonnées X, coordonnées Y)**
        """
        image = pygame.Surface([32,32])
        image.blit(sheet, (0, 0), (x, y, 32, 32))
        return image

    def get_wrong_way(self)  -> pygame.Surface:
        """ Fonction retournant l'image de contre sens. """
        image = self.get_image(self.item_sheet, 0, 0)
        image.set_colorkey([255, 0, 255])
        return image

    def update_wrong_way(self):
        """ Fonction mettant à jour les données relatives au contre-sens. """
        self.image = self.get_wrong_way()