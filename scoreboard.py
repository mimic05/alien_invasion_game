import pygame.font
import os
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    def __init__(self, game):
        self.win = game.win
        self.settings = game.settings
        self.stats = game.stats
        self.game = game

        self.screen_rect = self.win.get_rect()

        # font settings -->
        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 18)

        # prepairing the score image
        self._prep_score()
        self._prep_high_score()
        self._prep_level()
        self._prep_ship()

    def _prep_score(self):
        rounded_score = round(self.stats.score, -1) # rounding number nearest to 10
        score_str = "{:,}".format(rounded_score) # text to be rendered
        self.score_sticker = f"Score: {score_str}"

        self.score_image = self.font.render(self.score_sticker, True, self.text_color, self.settings.bg_color) # making text with background
        self.score_rect = self.score_image.get_rect() # making rect of text

        self.score_rect.right = self.screen_rect.right - 20 # setting rect position
        self.score_rect.top = 10 # setting rect position 20 px down from top edge

    def _prep_high_score(self):
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'highest_score.txt')

        # Print the file path for debugging
        print(f"File path: {file_path}")

        try:
            with open(file_path, "r") as f:
                self.high_score = int(f.read().strip())
        except FileNotFoundError:
            self.high_score = 0
            print(f"File not found: {file_path}. Initializing high score to 0.")
        except ValueError:
            self.high_score = 0
            print(f"Invalid data in file: {file_path}. Initializing high score to 0.")
        except Exception as e:
            self.high_score = 0
            print(f"An error occurred while reading the file: {e}. Initializing high score to 0.")

        self.hs_str =  f"Highest Score: {self.high_score}"
        self.high_score_image = self.font.render(self.hs_str, True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def draw_score(self):
        self.win.blit(self.score_image, self.score_rect)
        self.win.blit(self.high_score_image, self.high_score_rect)
        self.win.blit(self.level_image, self.level_rect)
        self.ships.draw(self.win)

    def check_high_score(self):
        if self.stats.score > int(self.high_score):
            with open("highest_score.txt", "w") as f:
                f.write(str(self.stats.score))
            self._prep_high_score()

    def _prep_level(self):
        self.str =  str(self.stats.level)
        self.level_str = f"Level: {self.str}"
        self.level_image = self.font.render(self.level_str, True, self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()

        self.level_rect.left = (10)
        self.level_rect.top = 10

    def _prep_ship(self):
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.game)
            ship.rect.x = 5 + ship_number * ship.rect.width
            ship.rect.y = 25
            self.ships.add(ship)


