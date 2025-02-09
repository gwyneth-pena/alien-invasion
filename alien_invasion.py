import sys
from time import sleep
from button import Button
import pygame
from alien import Alien
from bullet import Bullet
from game_stats import GameStats
from settings import Settings
from ship import Ship

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.bg_color = self.settings.bg_color

        self.game_stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.game_active = False
        self.play_button = Button(self, "Play")
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._check_keydowns(event)
            if event.type == pygame.KEYUP:
                self._check_keyups(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if not self.game_active and button_clicked:
            self.game_active = True
            pygame.mouse.set_visible(False)
            self.game_stats.reset_stats()
            self.bullets.empty()
            self.aliens.empty()
            self.create_fleet()
            self.ship.center_ship()

    def _check_keydowns(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
            if event.key == pygame.K_SPACE:
                self.fire_bullets()
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                sys.exit()                   

    def _check_keyups(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.ship.moving_left = False
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False

    def fire_bullets(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()

        self._check_bullet_and_alien_collisions()

    def _check_bullet_and_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        self._check_aliens_hit_ship()
        self._check_aliens_hit_bottom()

    def _create_alien(self, pos_x, pos_y):
        new_alien = Alien(self)
        new_alien.x = pos_x
        new_alien.rect.x = pos_x
        new_alien.rect.y = pos_y
        self.aliens.add(new_alien)
        
    def create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < self.settings.screen_height - (alien_height*3):
            while current_x < self.settings.screen_width - (alien_width*2):
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width
            
            current_x = alien_width
            current_y += 2*alien_height

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _decrease_ship(self):
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self.game_active = True
            self.bullets.empty()
            self.aliens.empty()
            self.create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False

    def _check_aliens_hit_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._decrease_ship()
    
    def _check_aliens_hit_ship(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._decrease_ship()

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.ship.blitme()
        if not self.game_active:
            pygame.mouse.set_visible(True)
            self.play_button.draw_button()
        pygame.display.flip()

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()