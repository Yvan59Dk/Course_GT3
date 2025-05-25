from dataclasses import dataclass
from math import *
from time import *
from random import *
import pygame
import pytmx
import pyscroll

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
    verf_sortieSud : list
    verf_sortieNord : list
    verf_sortieOuest : list
    verf_sortieEst : list
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
        self.current_map = "map_test"
        #self.win = False

        self.register_map("map_test")
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
            if sprite.feet.collidelist(self.get_verf_sortieNord()) > -1:
                if self.player.speed[0] > 2 :
                    self.wrong_way_V = True
            if sprite.feet.collidelist(self.get_verf_sortieSud()) > -1:
                if self.player.speed[1] > 2 :
                    self.wrong_way_V = True
            if sprite.feet.collidelist(self.get_verf_sortieEst()) > -1:
                if self.player.speed[3] > 2 :
                    self.wrong_way_V = True
            if sprite.feet.collidelist(self.get_verf_sortieOuest()) > -1:
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
        tmx_data = pytmx.util_pygame.load_pygame(f"./assets/map/circuit_test/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        # liste collision
        walls = []
        sable = []
        herbe = []
        verf_sortieNord = []
        verf_sortieSud = []
        verf_sortieEst = []
        verf_sortieOuest = []
        test_tour = []
        pitLane = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "sable":
                sable.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "herbe":
                herbe.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "verf_sortieNord":
                verf_sortieNord.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "verf_sortieSud":
                verf_sortieSud.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "verf_sortieEst":
                verf_sortieEst.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "verf_sortieOuest":
                verf_sortieOuest.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "test_tour":
                test_tour.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "pitLane":
                pitLane.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


        # dessiner groupe calque
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        group.add(self.player)

        # save map
        self.maps[name] = Map(name, walls, sable, herbe, verf_sortieNord, verf_sortieSud, verf_sortieEst, verf_sortieOuest, test_tour, pitLane, group, tmx_data)

    def get_map(self): return self.maps[self.current_map]
    def get_group(self): return self.get_map().group
    def get_walls(self): return self.get_map().walls
    def get_sable(self): return self.get_map().sable
    def get_herbe(self): return self.get_map().herbe
    def get_verf_sortieSud(self): return self.get_map().verf_sortieSud
    def get_verf_sortieNord(self): return self.get_map().verf_sortieNord
    def get_verf_sortieOuest(self): return self.get_map().verf_sortieOuest
    def get_verf_sortieEst(self): return self.get_map().verf_sortieEst
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