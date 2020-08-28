import pygame
from entities.entity import Entity


class Asteroid(Entity):
    def __init__(self, x, y, size, img=None):
        super().__init__(x, y, size)
        self.img = img

    def draw(self, game_display):
        pygame.draw.rect(game_display, (255, 0, 0), self.get_rect())
