import pygame
from random import randrange, choice


class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = randrange(0, 600)
        self.y = randrange(-200, 800)
        self.size = randrange(2, 10)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, game_display):
        pygame.draw.ellipse(game_display, choice([pygame.color.THECOLORS['white'], pygame.color.THECOLORS['yellow']]), self.rect)
        self.update()

    def update(self, *args, **kwargs):
        self.y += 1
        self.rect.x = self.x
        self.rect.y = self.y

    def boundaries_check(self, max_y, stars):
        if self.y > max_y - self.size:
            stars.remove(self)
