import os
import sys

import pygame
from pygame.locals import *

from entities.entity import Movement
from entities.space_ship import SpaceShip


class Game:
    pygame.init()

    def __init__(self, width, height):
        picture = pygame.image.load(os.path.join('img', 'bg_space.jpg'))
        self.bg = pygame.transform.scale(picture, (width, height))

        self.width = width
        self.height = height
        self.game_display = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Asteroids')

        self.spaceship: SpaceShip = SpaceShip(x=self.width // 2, y=self.height - 20 * 2, size=20, img=None)
        self.ship_can_shoot = False

    def clear_display(self):
        self.game_display.fill((255, 255, 255))
        self.game_display.blit(self.bg, (0, 0))

    def movement(self, key_pressed):
        if key_pressed[ord('w')]:
            self.spaceship.move_ship(Movement.UP)
        if key_pressed[ord('s')]:
            self.spaceship.move_ship(Movement.DOWN)
        if key_pressed[ord('a')]:
            self.spaceship.move_ship(Movement.LEFT)
        if key_pressed[ord('d')]:
            self.spaceship.move_ship(Movement.RIGHT)

    def shooting(self):
        if self.ship_can_shoot:
            self.spaceship.shoot(self.game_display)
            self.ship_can_shoot = False

    def render(self):
        self.spaceship.draw(self.game_display)
        self.spaceship.track_bullets(self.game_display)
        self.movement(pygame.key.get_pressed())
        self.shooting()
        pygame.display.update()

    def game_loop(self):
        fps = 60
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ship_can_shoot = True
                if event.type == KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.ship_can_shoot = False

            self.clear_display()
            self.render()
            clock.tick(fps)


if __name__ == "__main__":
    display_width = 600
    display_height = 800
    game = Game(display_width, display_height)
    game.game_loop()
