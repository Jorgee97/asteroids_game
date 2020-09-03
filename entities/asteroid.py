from typing import List
import os
import pygame
from random import choice, randrange


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = self.define_random_size()
        self.x = self.random_position()
        self.y = self.random_position(is_x=False)
        self.life = 100
        self.img = pygame.image.load(os.path.join('assets', 'asteroid.png')).convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.size[0], self.size[1]))
        self.mask = pygame.mask.from_surface(self.img)

        self.hit_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'hit.wav'))
        self.explosion_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'explosion.wav'))

        self.constant_x_movement = randrange(-2, 4)
        self.constant_y_movement = randrange(1, 4)

        self.rect: pygame.Rect = self.img.get_rect()
        self.rect.topleft = self.x, self.y

    @staticmethod
    def define_random_size() -> List:
        return choice([[40, 40], [50, 50], [60, 60], [70, 70], [80, 80], [90, 90]])

    def random_position(self, is_x=True) -> int:
        if is_x:
            return round(randrange(100, 600 - self.size[0]))
        else:
            return round(randrange(-250, 100 - self.size[0]))

    def draw(self, game_display):
        game_display.blit(self.img, (self.x, self.y))

    def explode(self):
        self.explosion_sound.play()
        self.kill()

    def move_on_collision(self, x, y):
        self.x += x
        self.y += y
        self.rect.topleft = self.x, self.y

    def move(self):
        self.x += self.constant_x_movement
        self.y += self.constant_y_movement
        self.rect.topleft = self.x, self.y

    def check_collision(self, bullets, spaceship, asteroids):
        for bullet in bullets:
            if pygame.sprite.collide_rect(self, bullet):
                if bullet.get_rect().top:
                    bullet.kill()
                    self.life -= 25
                    self.hit_sound.play()
                    if self.life <= 0:
                        spaceship.score += 10
                        self.explode()

        for asteroid in asteroids:
            if self != asteroid and pygame.sprite.collide_mask(self, asteroid):
                if asteroid.rect.left:
                    asteroid.constant_x_movement = -2
                    self.constant_x_movement = 2
                if asteroid.rect.right:
                    asteroid.constant_x_movement = 2
                    self.constant_x_movement = -2
                if asteroid.rect.bottom:
                    asteroid.constant_y_movement = -2
                    self.constant_y_movement = 2
                if asteroid.rect.top:
                    asteroid.constant_y_movement = 2
                    self.constant_y_movement = -2

        if self.x + self.size[0] > 600:
            self.constant_x_movement = -2
        if self.x < 0:
            self.constant_x_movement = 2

        if self.y < 0:
            self.constant_y_movement = randrange(1, 4)

    def get_rect(self):
        return self.rect

    def randomize_constant_movement_on_collision(self):
        self.constant_x_movement = randrange(-2, 5)
        self.constant_y_movement = randrange(2, 6)
