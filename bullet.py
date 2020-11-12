import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, game):
        super().__init__()
        self.win = game.win
        self.settings = game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = game.ship.rect.midtop # setting the posittion of bullets

    def update(self):
        self.rect.y -= self.settings.bullet_speed # substracting the bullet speed from the bullet's y co-ordinate
        # so after the bullet is fired it's y position will change but the x position will remain same

    def draw_bullet(self):
        pygame.draw.rect(self.win, self.color, self.rect)