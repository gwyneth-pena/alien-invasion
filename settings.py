

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
        self.ship_limit = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullets_allowed = 10
        self.fleet_drop_speed = 10
        
        self.speed_up_scale = 1.1
        self.score_scale =1.5
        self.bullet_color = (60, 60, 60)
        self.bg_color = (230, 230, 230)

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 8
        self.bullet_speed = 3
        self.alien_speed = 4
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.bullet_speed *= self.speed_up_scale
        self.alien_speed  *= self.speed_up_scale
        self.alien_points = int(self.score_scale*self.alien_points)