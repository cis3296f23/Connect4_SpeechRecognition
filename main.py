# main.py
import sys
import pygame
import pygame_gui
import math
import numpy as np
from pygame.locals import *
from gui import Connect4GUI
from logic import Connect4Game

def main():
    pygame.init()

    # Set up the game
    game = Connect4Game()
    gui = Connect4GUI(game)

    # Set up the screen
    screen_number = 1
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Connect 4")

    while True:
        if screen_number == 1:
            screen_number = gui.screen1()
        elif screen_number == 2:
            screen_number = gui.screen2()
        elif screen_number == 3:
            screen_number = gui.screen3()

        pygame.display.flip()

if __name__ == "__main__":
    main()
