import sys
import pygame
from alien import Alien
from bullet import Bullet
from settings import Settings
from ship import Ship

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.bg_color = self.settings.bg_color
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.create_fleet()
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        while True:
            self._check_events()
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

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

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

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.ship.blitme()
        pygame.display.flip()

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()