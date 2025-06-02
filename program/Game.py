from dataclasses import dataclass
from math import *
from time import *
from random import *

from program.Player import *
from program.map import *
from program.Chrono import *

import pygame

class Game:
    def __init__(self):

        # Fenêtre
        self.screen = pygame.display.set_mode((1000, 800))
        self.rect = self.screen.get_rect()
        pygame.display.set_caption("Course GT3")

        # Gérere le chrono
        self.chrono = Chrono(time())

        # Génere un joueur
        # PS : le faire directement avec les données de .tmx
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)

    def handle_imput(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.anime[1] = 3
            self.player.move_anime()
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.anime[1] = 0
            self.player.move_anime()
        if pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.anime[1] = 1
            self.player.move_anime()
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.anime[1] = 2
            self.player.move_anime()
        self.player.load_sprite()

    def draw(self):
        self.map_manager.draw()
        self.screen.blit(self.chrono.image, [0, 0])

    def update(self):
        self.map_manager.update()
        if self.map_manager.chrono_V == True:
            self.chrono.time = time()
            self.map_manager.chrono_V = False
        else:
            self.chrono.update()
        if self.map_manager.wrong_way_V == True :
            self.player.update_wrong_way()
            self.map_manager.wrong_way_V = False


    def run(self):
        clock = pygame.time.Clock()
        self.map_manager.teleport_player(self.map_manager.get_spawn()[0][0],self.map_manager.get_spawn()[0][1])

        # Boucle du jeu
        running = True

        while running:
            self.player.save_location()
            self.handle_imput()
            self.player.move()
            self.update()
            self.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()