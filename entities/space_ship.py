import pygame
from entities.entity import Entity, Movement


class Bullet(Entity):
    def __init__(self, x, y, size=10):
        super().__init__(x, y, size)

    def draw(self, game_display):
        pygame.draw.rect(game_display, (0, 0, 255), self.get_rect())

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 5, 10)


class SpaceShip(Entity):
    def __init__(self, x, y, size, img=None):
        super().__init__(x, y, size)
        self.img = img
        self.life = 100
        self.bullets = []

    def draw(self, game_display):
        pygame.draw.rect(game_display, (255, 0, 0), self.get_rect())

    def shoot(self, game_display):
        self.bullets.append(Bullet(self.x, self.y - self.size))
        self.bullets.append(Bullet(self.x + self.size - 7, self.y - self.size))

        for bullet in self.bullets:
            pygame.draw.rect(game_display, (255, 255, 255), bullet.get_rect())

    def track_bullets(self, game_display):
        for bullet in self.bullets:
            bullet.move(0, -10)
            pygame.draw.rect(game_display, (255, 255, 255), bullet.get_rect())

            if bullet.y < 0:
                self.bullets.remove(bullet)

    def boundaries_check(self, max_x, max_y):
        if self.x > max_x - self.size:
            self.x = max_x - self.size
        if self.x < 0:
            self.x = 0

        if self.y < 0:
            self.y = 0
        if self.y > max_y - self.size:
            self.y = max_y - self.size

    def move_ship(self, movement: Movement):
        self.x += movement.value[0]
        self.y += movement.value[1]
