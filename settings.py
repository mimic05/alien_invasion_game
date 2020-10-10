class Settings():
    def __init__(self):
        # game window settings--
        self.FPS = 300
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # ship settings--
        self.ship_speed = 1.5

        # bullet setting--
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_alloted = 4