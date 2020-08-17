import pygame
from player import Bullet


class Explosion:
    def __init__(self, x, y):
        self.display = pygame.display.get_surface()
        self.x = x
        self.y = y
        self.img = pygame.image.load('assets/sprites/explosion.png')
        self.exploded_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if not current_time - self.exploded_time > 150:
            self.display.blit(self.img, (self.x, self.y))


class Enemy:
    def __init__(self, pos, type):
        self.display = pygame.display.get_surface()
        self.x = pos[0]
        self.y = pos[1]
        self.type = type
        self.base_speed = 1
        self.speed = self.base_speed
        self.dir = 1  # 1 = right, -1 = left
        self.img = pygame.image.load(f'assets/sprites/alien{self.type}.png')
        self.rect = self.img.get_rect(x=self.x, y=self.y)
        self.bullets = []

    def left(self):
        self.dir = -1

    def right(self):
        self.dir = 1

    def advance(self):
        self.y += abs(self.speed)

    def shoot(self):
        bulletx = self.x + self.img.get_width() / 2 - 2
        self.bullets.append(Bullet((bulletx, self.y + 36), False))

    def update(self):
        self.x += self.speed * self.dir
        self.rect = self.display.blit(self.img, (self.x, self.y))
        for i, b in enumerate(self.bullets):
            b.update()
            if b.y > self.display.get_height():
                del self.bullets[i]
