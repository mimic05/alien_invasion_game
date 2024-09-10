import pygame, sys, time
from game_stats import GameStats
from ship import Ship
from settings import Settings
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class Game():
    def __init__(self):
        pygame.init() # initialization pygame

        self.settings = Settings() # creating settings instance
        self.clock = pygame.time.Clock() # creating clock to contro fps

        self.win = pygame.display.set_mode((self.settings.win_width, self.settings.win_height)) # setting game window
        self.bg_color = self.settings.bg_color # background color
        pygame.display.set_caption("Alien shooter") # setting game name

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self) # creating ship instance

        self.bullets = pygame.sprite.Group() # creating sprite group to hold bullets
        self.aliens = pygame.sprite.Group() # creating sprite group to hold alien fleet

        self._create_fleet() # creating alien fleet using (_create_fleet() helper method)

        self.play_button = Button(self, "Play")

    def run_game(self):
        while True:
            self.clock.tick(self.settings.FPS)
            self._check_event() # checking every event in a for loop
            if self.stats.game_active:
                self.ship.update_ship_position() # update the ship position in every loop after a valid keypress
                self.bullets.update() # update the position of every bullet in the self.bullets group
                self._remove_bullets() # delete the bullet once they get past the screen
                self._update_alien() # update alien's x and y position
                self._update_screen() # update all the screen elements
            else:
                self._update_screen()

    def _check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active: # check if button has clicked and game is active
            self.settings._levelup_settings() # reset changing settings values when play button is clicked
            self.stats.reset_stats() # reset game stats
            self.stats.game_active = True # make game state active
            self.sb._prep_score() # prepare score image
            self.sb._prep_ship()

            self.aliens.empty() # removing all the remaining aliens
            self.bullets.empty() # removing all the remaining bullets

            self._create_fleet() # create new fleet
            self.ship.center_ship() # bring the alien ship to the center
            pygame.mouse.set_visible(False) # setting mouse visibility of once the button is clicked

    def _check_keydown(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet() # pressing space will triger _fire_bullet() helper method

    def _check_keyup(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed and self.stats.game_active: # if self.bullet group has lass than specefied number
            # of bullets, only then add new bullet
            new_bullet = Bullet(self) # creates instance of Bullet class
            self.bullets.add(new_bullet) # add that instance to self.bullets group

    def _remove_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._bullet_alien_collisions()

    def _bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions: # check if collision happed between ship and bullet
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_point * len(aliens) # if yes then increment schore
            self.sb._prep_score() # prep score image of that score
            self.sb.check_high_score() # checking if current score is new high score

        if  len(self.aliens) == 0: # check if all aliens has been shot donw //Basically we are entering a new level if all aliens are shot down
            self.bullets.empty() # if yes then empty the bullet group
            self._create_fleet() # create new alien fleet
            self.settings.increase_speed() # increase game speed
            self.stats.level += 1
            self.sb._prep_level()

    def _create_fleet(self):
        alien = Alien(self) # creating alien instance
        alien_width, alien_height = alien.rect.size # storing alien's width and height in two variable
        available_space_x = self.settings.win_width - (2 * alien_width) # checking available x space
        alien_number_x = available_space_x // (2 * alien_width) # checking number of alien that can fit in x space

        ship_height = self.ship.rect.height # accessing ship's height element
        available_space_y = self.settings.win_height - (3 * alien_height) - (ship_height + 60)# checking available y space ####### unstable change
        alien_number_y = available_space_y // (2 * alien_height) # checking number of alien that can fin in y space

        #creating the first row of alien
        for row_number in range(alien_number_y):
            for alien_number in range(alien_number_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self) # create alien instance
        alien_width, alien_height = alien.rect.size # storing alien's width in a variable
        alien.x = alien_width + (alien_number * 2 * alien_width)
        alien.rect.x = alien.x # setting rect's x position
        alien.rect.y = 15 + alien.rect.height + (2 * alien_height * row_number) # setting aliens y position ######### unstable change
        self.aliens.add(alien)

    def _update_alien(self):
        self._check_fleet_edges()
        self.aliens.update() # call update() medthod from alien class on self.aliens; sprite group
        if pygame.sprite.spritecollideany(self.ship, self.aliens): # check collistion between ship and alines
            self._ship_hit() # if collision happens; call _ship_hit() medthod
        self._bottom_hit() # check if any of the aliens has reached bottom

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites(): # loop through every alien instance in self.aliens group
            if alien.check_edge(): # call check_edge() medthod on every every alien instance
                self._change_fleet_direction() # call _change_fleet_direction() when condition is Ture
                break # break out of this loop once _change_fllet_direction() is called

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites(): # loop through every alien instance in self.aliens group
            alien.rect.y += self.settings.fleet_drop_speed # increase rect's y position
        self.settings.fleet_direction *= -1 # multiply fleet_directin with nagative one

    def _ship_hit(self):
        if self.stats.ship_left > 0:
            # decrement ship number
            self.stats.ship_left -= 1
            self.sb._prep_ship()

            # removing remaining ship and bullet
            self.aliens.empty()
            self.bullets.empty()

            # creating new fleet and centering ship
            self._create_fleet()
            self.ship.center_ship()
            # pause
            time.sleep(2)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _bottom_hit(self):
        screen_rect = self.win.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        self.win.fill(self.bg_color)
        self.ship.draw_ship() # fetching draw ship method from Ship class of ship module
        for bullet in self.bullets.sprites():
            bullet.draw_bullet() # draws every bullet instance present in self.bullets group

        self.aliens.draw(self.win) # draws every allien in self.alines group
        self.sb.draw_score() # draws score

        if not self.stats.game_active: # draw the play button when the game is inactive
            self.play_button.draw_button()
        pygame.display.update()

g = Game()
g.run_game()