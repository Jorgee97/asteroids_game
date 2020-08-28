from typing import List
import pygame
from random import randrange

from entities.entity import Movement


class Asteroid:
    def __init__(self, img=None):
        self.x = self.random_position()
        self.y = self.random_position()
        self.life = 100
        self.size = self.define_random_size()
        self.img = img

    @staticmethod
    def define_random_size() -> List:
        return [round(randrange(10, 50)), round(randrange(10, 50))]

    @staticmethod
    def random_position() -> int:
        return round(randrange(0, 400))

    def draw(self, game_display):
        pygame.draw.rect(game_display, (0, 0, 255), self.get_rect())

    def explode(self):
        self.x = 0
        self.y = 850

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

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size[0], self.size[1])
