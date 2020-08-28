import pygame
from enum import Enum


class Movement(Enum):
    UP = [0, -5]
    DOWN = [0, 5]
    LEFT = [-5, 0]
    RIGHT = [5, 0]


class Entity:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def move(self, x, y):
        self.x += x
        self.y += y

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.size, self.size)
