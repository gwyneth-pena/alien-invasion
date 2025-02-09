import pygame.font

class Scoreboard:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.game_stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_img = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        self.level_img_rect = self.level_img.get_rect()
        self.level_img_rect.right = self.score_rect.right
        self.level_img_rect.top = self.score_rect.bottom + 10

    def prep_high_score(self):
        high_score = f"{self.stats.high_score:,}"
        self.high_score_img = self.font.render(high_score, True, self.text_color, self.settings.bg_color)
        self.high_score_img_rect = self.high_score_img.get_rect()
        self.high_score_img_rect.centerx = self.screen_rect.centerx
        self.high_score_img_rect.top = self.score_rect.top

    def prep_score(self):
        score_str = f"{self.stats.score:,}"
        self.score_img = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def draw_score(self):
        self.screen.blit(self.high_score_img, self.high_score_img_rect)
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.level_img, self.level_img_rect)
    
    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()