

import pygame


class Settings:
    def __init__(self):
        if pygame.FULLSCREEN:
            info = pygame.display.Info()
            self.screen_width = info.current_w
            self.screen_height = info.current_h
        else:
            self.screen_width = 1200
            self.screen_height = 800
        self.ship_speed = 3
        self.bullet_speed = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullets_allowed = 10
        self.fleet_drop_speed = 10
        self.alien_speed = 4
        self.fleet_direction = 1
        self.bullet_color = (60, 60, 60)
        self.bg_color = (230, 230, 230)