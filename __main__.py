import pygame
from program.Game import *

if __name__ == '__main__' :
    pygame.init()
    pygame.mixer.init()
    music = pygame.mixer.music.load("assets/music/Jeu_Yvan.ogg")
    pygame.mixer.music.play(-1, 0.0)

    game = Game()
    game.run()

