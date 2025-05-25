from dataclasses import dataclass
from math import *
from time import *
from random import *
import pygame

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