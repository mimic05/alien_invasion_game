import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, game):
        super().__init__()
        self.win = game.win # accessing game window
        self.settings = game.settings
        self.original_image = pygame.image.load("C:/CODE/pygame_projects/image/alien_ship.png") # loading image
        self.image = pygame.transform.scale(self.original_image, (35, 40)) # scaling down image

        self.screen_rect = self.win.get_rect()
        self.rect = self.image.get_rect() # getting rect of image

        self.rect.x = 20 # setting x postion of rect
        self.rect.y = self.rect.height # setting y position of rect

    def update(self):
        self.x += (self.settings.alien_speed *  self.settings.fleet_direction)
        self.rect.x = self.x # seeting rect's x position to current self.x value

    def check_edge(self):
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True
