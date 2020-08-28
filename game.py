import os
import sys
from random import randrange

import pygame
from pygame.locals import *

from entities.entity import Movement
from entities.asteroid import Asteroid
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

        self.spaceship: SpaceShip = SpaceShip(x=self.width // 2, y=self.height - 20 * 2)
        self.ship_can_shoot = False
        self.total_asteroids = 5
        self.many_asteroids = 5

        self.asteroids = pygame.sprite.Group()
    
    def draw_asteroids(self):
        asteroids_list = []
        for _ in range(0, self.many_asteroids):
            asteroids_list.append(Asteroid())
            self.many_asteroids -= 1

        self.asteroids.add(asteroids_list)
        for asteroid in self.asteroids:
            asteroid.draw(self.game_display)

        if len(self.asteroids) < self.total_asteroids:
            self.asteroids.add(Asteroid())

    def move_asteroids(self):
        for asteroid in self.asteroids:
            asteroid.move(0, 1)

    def check_asteroid_collision(self):
        for asteroid in self.asteroids:
            asteroid.check_collision(self.spaceship.bullets, self.spaceship)

    def check_asteroid_boundaries(self):
        for asteroid in self.asteroids:
            if asteroid.y > self.height:
                self.asteroids.remove(asteroid)
                self.asteroids.add(Asteroid())

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
        self.spaceship.boundaries_check(self.width, self.height)
        self.shooting()
        print(self.spaceship.life)

        # Asteroids
        self.draw_asteroids()
        self.move_asteroids()
        self.check_asteroid_collision()
        self.check_asteroid_boundaries()

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
