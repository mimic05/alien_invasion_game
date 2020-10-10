import pygame as pg
import sys, time
from settings import Settings
from ship import Ship
from bullet import Bullet


class AlienInvasion():
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.settings = Settings()
        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pg.sprite.Group()

    def run_game(self):
        while True:
            self.clock.tick(self.settings.FPS)
            self._check_event()
            self.ship.update()
            self.bullets.update()
            self._update_bullets()
            self._update_screen()

    def _check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
                
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = True

        elif event.key == pg.K_LEFT:
            self.ship.moving_left = True
            
        elif event.key == pg.K_SPACE:
            self._fire_bullet()

        elif event.key == pg.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = False

        elif event.key == pg.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_alloted:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        pg.display.flip()
        
            
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
