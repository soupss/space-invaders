from random import randrange
import pygame as pg
from pygame.math import Vector2
from settings import *
from sprites.bullet import MobBullet as Bullet


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.game = game
        self.groups = self.game.sprites, self.game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.type = type
        self.load_images()
        self.frames = self.images[self.type - 1]
        self.frame = 0
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = Vector2(self.rect.topleft)
        self.dir = Vector2(1, 0)
        self.speed = Vector2(MOB_BASE_SPEED, MOB_BASE_SPEED)
        self.frame_rate = MOB_BASE_FRAMERATE
        self.last_updated = pg.time.get_ticks()

    def load_images(self):
        self.images = [
            [
                self.game.spritesheet.get_image(0, 128, 48, 32, WHITE),
                self.game.spritesheet.get_image(48, 128, 48, 32, WHITE)
            ],
            [
                self.game.spritesheet.get_image(0, 160, 44, 32, WHITE),
                self.game.spritesheet.get_image(48, 160, 44, 32, WHITE)
            ],
            [
                self.game.spritesheet.get_image(0, 192, 32, 32, WHITE),
                self.game.spritesheet.get_image(48, 192, 32, 32, WHITE)
            ],
        ]

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_updated > self.frame_rate:
            self.frame += 1
            if self.frame == len(self.frames):
                self.frame = 0
            self.last_updated = now
            self.image = self.frames[self.frame]
        self.mask = pg.mask.from_surface(self.image)

    def shoot(self):
        Bullet(self.game, self.rect.centerx, self.rect.bottom)

    def update(self):
        self.animate()
        self.pos += self.speed.elementwise() * self.dir.elementwise()
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

class MobGroup(pg.sprite.Group):
    '''Mob group class which handles collision, movement, scaling etc.'''
    def __init__(self, game):
        self.game = game
        pg.sprite.Group.__init__(self)
        self.mobs = self.sprites()
        self.cols = MOB_PACK_COLS
        self.rows = MOB_PACK_ROWS
        self.colgroups = []
        for _ in range(self.cols):
            self.colgroups.append(pg.sprite.Group())
        self.advance_frames = 0
        self.last_shot = pg.time.get_ticks()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > MOB_BASE_SHOOT_DELAY:
            valid_shooters = []
            for cg in self.colgroups:
                if not cg:
                    del cg
                    continue
                valid_shooters.append(cg.sprites()[-1])
            if valid_shooters:
                selected_shooter = valid_shooters[randrange(len(valid_shooters))]
                selected_shooter.shoot()
                self.last_shot = now

    def advance(self):
        if self.advance_frames > 0:
            for mob in self.mobs:
                mob.dir.y = 1
            self.advance_frames -= 1
        else:
            for mob in self.mobs:
                mob.dir.y = 0

    def scale(self):
        # increase mob speed and frame rate when mobs die
        max = self.cols * self.rows
        dead = max - len(self.mobs)
        speed = dead * MOB_SPEED_SCALE + MOB_BASE_SPEED
        frame_rate = dead * MOB_FRAMERATE_SCALE + MOB_BASE_FRAMERATE
        for mob in self.mobs:
            mob.speed.x = speed
            mob.speed.y = speed
            mob.frame_rate = frame_rate
        # music
        self.game.sound_controller.dundun_rate = frame_rate


    def update(self):
        self.mobs = self.sprites()
        self.scale()
        self.shoot()
        # edge hits
        for mob in self.mobs:
            if mob.rect.right >= WIDTH:
                self.advance_frames = MOB_ADVANCE_FRAMES
                for MOB in self.mobs:
                    MOB.dir.x = -1
            if mob.rect.left <= 0:
                self.advance_frames = MOB_ADVANCE_FRAMES
                for MOB in self.mobs:
                    MOB.dir.x = 1
        self.advance()
