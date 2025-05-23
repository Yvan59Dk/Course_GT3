from dataclasses import dataclass
from math import *
from time import *
from random import *
import pygame
import pytmx
import pyscroll
reso = 1

class Chrono():
    def __init__(self, time):
        self.time = time
        self.image = self.get_chrono()

    def get_chrono(self):
        image = gmtime(time() - self.time)
        image = strftime("%X", image)
        font = pygame.font.SysFont('', 50)
        image = font.render(image, True, (255, 255, 255))
        return image

    def update(self):
        self.image = self.get_chrono()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sound1 = pygame.mixer.Sound('music/pneu1.ogg')
        self.sound1.set_volume(0.3)
        self.sound2 = pygame.mixer.Sound('music/pneu2.ogg')
        self.sound2.set_volume(0.3)
        self.sprite_sheet = pygame.image.load("sprites/player_x1.png")
        self.item_sheet = pygame.image.load("sprites/item.png")
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

@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str

@dataclass
class Map:
    name: str
    walls: list
    sable : list
    herbe : list
    verf_S : list
    verf_N : list
    verf_O : list
    verf_E : list
    test_tour : list
    pitLane : list
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap

class MapManager:

    def __init__(self, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.wrong_way_V = False
        self.chrono_V = False
        self.current_map = "world"
        #self.win = False

        self.register_map("world")
        """
        self.register_map("house", portals=[
            Portal(from_world="house", origin_point="exit_house", target_world="world", teleport_point="enter_house_exit")
        ])"""

    def check_objet(self):
        # portails
        """
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)"""

        # collision
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()
            if sprite.feet.collidelist(self.get_sable()) > -1:
                self.player.change_vitesse( [-0.35, -0.35, -0.35, -0.35] )
            elif sprite.feet.collidelist(self.get_herbe()) > -1:
                self.player.change_vitesse( [-0.07, -0.07, -0.07, -0.07] )
            if sprite.feet.collidelist(self.get_verf_N()) > -1:
                if self.player.speed[0] > 2 :
                    self.wrong_way_V = True
            if sprite.feet.collidelist(self.get_verf_S()) > -1:
                if self.player.speed[1] > 2 :
                    self.wrong_way_V = True
            if sprite.feet.collidelist(self.get_verf_E()) > -1:
                if self.player.speed[3] > 2 :
                    self.wrong_way_V = True
            if sprite.feet.collidelist(self.get_verf_O()) > -1:
                if self.player.speed[2] > 2 :
                    self.wrong_way_V = True
            if sprite.feet.collidelist(self.get_test_tour()) > -1:
                self.chrono_V = True
            if sprite.feet.collidelist(self.get_pitLane()) > -1:
                for i in range(len(self.player.speed)):
                    if self.player.speed[i] > 3 :
                        self.player.speed[i] = 3


    def teleport_player(self,x,y):
        self.player.position[0] = x
        self.player.position[1] = y
        self.player.save_location()

    def register_map(self, name):
        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame(f"map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.7

        # liste collision
        walls = []
        sable = []
        herbe = []
        verf_N = []
        verf_S = []
        verf_E = []
        verf_O = []
        test_tour = []
        pitLane = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "sable":
                sable.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "herbe":
                herbe.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "verf_N":
                verf_N.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "verf_S":
                verf_S.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "verf_E":
                verf_E.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "verf_O":
                verf_O.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "test_tour":
                test_tour.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "pitLane":
                pitLane.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


        # dessiner groupe calque
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        group.add(self.player)

        # save map
        self.maps[name] = Map(name, walls, sable, herbe, verf_N, verf_S, verf_E, verf_O, test_tour, pitLane, group, tmx_data)

    def get_map(self): return self.maps[self.current_map]
    def get_group(self): return self.get_map().group
    def get_walls(self): return self.get_map().walls
    def get_sable(self): return self.get_map().sable
    def get_herbe(self): return self.get_map().herbe
    def get_verf_S(self): return self.get_map().verf_S
    def get_verf_N(self): return self.get_map().verf_N
    def get_verf_O(self): return self.get_map().verf_O
    def get_verf_E(self): return self.get_map().verf_E
    def get_test_tour(self): return self.get_map().test_tour
    def get_pitLane(self): return self.get_map().pitLane
    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def draw(self):
        groups = self.get_group()
        groups.draw(self.screen)
        groups.center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_objet()

class Game:

    def __init__(self):

        # Fenêtre
        self.screen = pygame.display.set_mode((1000, 800))
        self.rect = self.screen.get_rect()
        pygame.display.set_caption("Course GT3")

        # Gérerer le chrono
        self.chrono = Chrono(time())

        # Génerer un joueur
        self.player = Player(1611.33, 333.67)
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
        self.player.change_animation()

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

if __name__ == '__main__' :
    pygame.init()
    pygame.mixer.init()
    music = pygame.mixer.music.load("music/Jeu_Yvan.ogg")
    pygame.mixer.music.play(-1, 0.0)

    game = Game()
    game.run()

