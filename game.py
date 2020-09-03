import sys

import pygame
from pygame.locals import *

from entities.entity import Movement
from entities.asteroid import Asteroid
from entities.space_ship import SpaceShip
from entities.star import Star


class GameManager:
    def __init__(self, player: SpaceShip):
        self.player = player
        self.level = 1
        self.total_asteroids = 5
        self.many_asteroids = 5
        self.increment_asteroid_per_level = 1
        self.increment_after_score_gt_than = 100

    def increment_level(self):
        if self.player.score > self.increment_after_score_gt_than:
            self.increment_after_score_gt_than += 100
            self.level = 2
            self.total_asteroids += 1
            self.player.health += round(self.player.health * 0.1)

    def game_over(self) -> bool:
        return self.player.health <= 0


class Game:
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    def __init__(self, width, height):
        # picture = pygame.image.load(os.path.join('img', 'bg_space.jpg'))
        # self.bg = pygame.transform.scale(picture, (width, height))

        self.width = width
        self.height = height
        self.game_display = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Asteroids')

        self.spaceship: SpaceShip = SpaceShip(x=self.width // 2, y=self.height - 20 * 2)
        self.ship_can_shoot = False

        self.game_manager = GameManager(self.spaceship)

        # Initialize game components
        self.asteroids = pygame.sprite.Group()
        self.asteroids.add([Asteroid() for _ in range(self.game_manager.many_asteroids)])
        self.stars = pygame.sprite.Group()
        self.stars.add([Star() for _ in range(100)])

    def draw_asteroids(self):
        for asteroid in self.asteroids:
            asteroid.draw(self.game_display)

        if len(self.asteroids) < self.game_manager.total_asteroids:
            self.asteroids.add(Asteroid())

    def move_asteroids(self):
        for asteroid in self.asteroids:
            asteroid.move()

    def check_asteroid_collision(self):
        for asteroid in self.asteroids:
            asteroid.check_collision(self.spaceship.bullets, self.spaceship, self.asteroids)

    def check_asteroid_boundaries(self):
        for asteroid in self.asteroids:
            if asteroid.y > self.height:
                self.asteroids.remove(asteroid)
                self.asteroids.add(Asteroid())

    def draw_bg_stars(self):
        for start in self.stars:
            start.draw(self.game_display)

    def check_stars_boundaries(self):
        for star in self.stars:
            star.boundaries_check(self.height, self.stars)
        if len(self.stars) < 100:
            self.stars.add([Star() for _ in range(20)])

    def clear_display(self):
        self.game_display.fill((0, 0, 0))

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
        # Background
        self.draw_bg_stars()
        self.check_stars_boundaries()

        self.spaceship.draw(self.game_display)
        self.spaceship.track_bullets(self.game_display)
        self.spaceship.draw_health(self.game_display)
        self.spaceship.draw_score(self.game_display, self.width)
        self.spaceship.check_collisions(self.asteroids)
        self.movement(pygame.key.get_pressed())
        self.spaceship.boundaries_check(self.width, self.height)
        self.shooting()

        # Asteroids
        self.draw_asteroids()
        self.move_asteroids()
        self.check_asteroid_collision()
        self.check_asteroid_boundaries()

        # Level Checking and Increment
        self.game_manager.increment_level()

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
            # TODO: validate user's health and if game_over proceed to pause game and ask for restart
            self.clear_display()
            self.render()
            clock.tick(fps)


if __name__ == "__main__":
    display_width = 600
    display_height = 800
    game = Game(display_width, display_height)
    game.game_loop()
