from typing import List
import os
import pygame
from random import randrange


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = self.define_random_size()
        self.x = self.random_position()
        self.y = self.random_position(is_x=False)
        self.life = 100
        self.img = pygame.image.load(os.path.join('assets', 'asteroid.png'))
        self.img = pygame.transform.scale(self.img, (self.size[0], self.size[1]))

        self.rect = self.get_rect()

    @staticmethod
    def define_random_size() -> List:
        return [round(randrange(20, 100)), round(randrange(20, 100))]

    def random_position(self, is_x=True) -> int:
        if is_x:
            return round(randrange(100, 600 - self.size[0]))
        else:
            return round(randrange(-250, 100 - self.size[0]))

    def draw(self, game_display):
        game_display.blit(self.img, (self.x, self.y))

    def explode(self):
        self.kill()

    def move(self, x, y):
        self.x += x
        self.y += y

    def check_collision(self, bullets, spaceship):
        for bullet in bullets[:]:
            if self.get_rect().colliderect(bullet.get_rect()):
                if bullet.get_rect().top:
                    bullets.remove(bullet)
                    self.life -= 25
                    if self.life == 0:
                        self.explode()

        if self.get_rect().colliderect(spaceship.get_rect()):
            if spaceship.get_rect().top and self.get_rect().bottom:
                spaceship.life -= 10
                # TODO: find better way to handle the life decreasing of the ship
                spaceship.move(0, 10)
                return
        
        if self.x > 600:
            self.move(-10, 0)
        if self.x < 0:
            self.move(1, 1)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size[0], self.size[1])
