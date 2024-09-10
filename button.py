import pygame.font

class Button():
    def __init__(self, game, msg):

        self.win = game.win # accessing game window
        self.screen_rect = self.win.get_rect() # making rect of window

        self.width, self.height = 150, 50 # setting weidth and height
        self.button_color = (230, 230, 230) # settting button color
        self.text_color = (255, 0, 0) # setting text color
        self.font = pygame.font.SysFont(None, 40) # setting font attribute; none = defauls font, 48 text size

        self.rect = pygame.Rect(0, 0, self.width, self.height) # setting rect
        self.rect.center = self.screen_rect.center # aligning rect

        self._prep_msg(msg) # helper method

    def _prep_msg(self, msg):
        # arguments of self.font.render -->
        # 1. Text to be rendered  2. Boolean value determines the smoothening of the edge of the text
        # 3. Color of text  4. Color of text background
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_rect = self.msg_image.get_rect()

        self.msg_rect.center = self.screen_rect.center

    def draw_button(self):
        self.win.fill(self.button_color, self.rect)
        self.win.blit(self.msg_image, self.msg_rect)