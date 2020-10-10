import pygame as pg

class Ship():
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.original_image = pg.image.load('image/ship.png')
        self.image = pg.transform.scale(self.original_image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom # position
        self.x = float(self.rect.x)
        # self.y = float(self.rect.y)

        self.moving_right = False
        self.moving_left = False
        # self.moving_up = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)