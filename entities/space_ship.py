import pygame
import os
from random import randrange
from entities.entity import Entity, Movement


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, size=10):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.rect: pygame.Rect = self.get_rect()
        self.rect.topleft = self.x, self.y

    def draw(self, game_display):
        pygame.draw.rect(game_display, (0, 0, 255), self.get_rect())

    def move(self, x, y):
        self.x += x
        self.y += y
        self.rect.topleft = self.x, self.y

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 5, 10)


class SpaceShip(Entity, pygame.sprite.Sprite):
    def __init__(self, x, y, size=64):
        Entity.__init__(self, x, y, size)
        pygame.sprite.Sprite.__init__(self)

        self.img = pygame.image.load(os.path.join('assets', 'ship.png')).convert_alpha()
        self.img = pygame.transform.scale(self.img, (64, 64))
        self.health = 100
        self.score = 0
        self.mask = pygame.mask.from_surface(self.img)
        self.bullets = pygame.sprite.Group()
        self.rect: pygame.Rect = self.img.get_rect()
        self.rect.topleft = self.x, self.y

        self.shoot_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'shoot.wav'))
        self.shoot_sound.set_volume(0.2)

    def draw(self, game_display):
        game_display.blit(self.img, (self.x, self.y))

    def draw_health(self, game_display):
        text = pygame.font.SysFont(None, 24)
        text_render = text.render(f"Health: {self.health}", True, (255, 255, 255))
        game_display.blit(text_render, (20, 20))

    def draw_score(self, game_display, x_max):
        text = pygame.font.SysFont(None, 24)
        text_render = text.render(f"Score: {self.score}", True, (255, 255, 255))
        game_display.blit(text_render, (x_max - 100, 20))

    def shoot(self, game_display):
        self.bullets.add(Bullet(self.x + (self.size // 2) - 2, self.y))
        self.shoot_sound.play()

        for bullet in self.bullets:
            pygame.draw.rect(game_display, (255, 255, 255), bullet.get_rect())

    def track_bullets(self, game_display):
        for bullet in self.bullets:
            bullet.move(0, -10)
            pygame.draw.rect(game_display, (255, 255, 255), bullet.get_rect())

            if bullet.y < 0:
                bullet.kill()

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
        self.rect.topleft = self.x, self.y

    def check_collisions(self, asteroids):
        if hit := pygame.sprite.spritecollide(self, asteroids, False, collided=pygame.sprite.collide_mask):
            self.health -= 10
            for h in hit:
                h.constant_x_movement = randrange(-2, 5)
                h.constant_y_movement = -2
