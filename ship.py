import pygame
import os
from settings import Settings
from pygame.sprite import Sprite
#'C:/code/pygame_projects/image/ship2.png'

class Ship(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.win # accessing screen element from game and storing that in a variable
        self.settings = game.settings

        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'images', 'ship2.png')

        print(image_path)

        self.original_image = pygame.image.load(image_path) # loding image
        self.image = pygame.transform.scale(self.original_image, (25, 30)) # resizing image

        self.rect = self.image.get_rect() # making rectangle of image
        self.screen_rect = self.screen.get_rect() # making rectangle of screen

        self.rect.midbottom = self.screen_rect.midbottom # setting the position to draw the ship
        self.ship_speed = self.settings.ship_speed

        self.moving_right = False
        self.moving_left = False

    def update_ship_position(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.ship_speed

    def draw_ship(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.rect.midbottom
