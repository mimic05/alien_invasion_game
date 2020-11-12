class Settings():
    def __init__(self):
        # window settings
        self.win_width = 600
        self.win_height = 550
        self.bg_color = (10, 10, 10)

        # clock settings
        self.FPS = 300

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = (199, 0, 57)
        # self.bullet_speed = 1
        self.bullet_allowed = 4

        # alien settings
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10 # controlls fleets downward speed
        self.fleet_direction = 1 # controlls fleets direction
        self.ship_limit = 3 # number of ship a player can use before loosing game

        # level control
        self.speedup_scale = 1.1 # how quickly the game speeds up
        self.score_scale = 1.5
        self._levelup_settings()

    def _levelup_settings(self):
        self.ship_speed = 2
        self.bullet_speed = 1
        self.alien_speed = 0.5
        self.fleet_direction = 1
        # scoring
        self.alien_point = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_point = int(self.alien_point * self.score_scale)

















