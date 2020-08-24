'''
This module contains resource loading functions
Also contains general tools which don't belong anywhere else
'''
# art made with https://www.piskelapp.com/
# sound made with https://www.bfxr.net/
from os import path
import pygame as pg
from settings import *


def text(screen, text, size, pos, color=WHITE):
    font = pg.font.Font(path.join(FONT_DIR, FONT_NAME), size)
    text_surface = font.render(text, False, color)
    text_rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, text_rect)


def style_numbers(int):
    string = str(int)
    if len(string) != 5:
        if len(string) == 1:
            string = '0000' + string
        if len(string) == 2:
            string = '000' + string
        if len(string) == 3:
            string = '00' + string
        if len(string) == 4:
            string = '0' + string
    return string


class SpriteSheet:
    '''Utility class for loading and parsing spritesheets.'''
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height, color):
        '''Change color and return a single image.'''
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        color_image = pg.Surface(image.get_size()).convert_alpha()
        color_image.fill(color)
        image.blit(color_image, (0,0), special_flags = pg.BLEND_RGBA_MIN)
        image.set_colorkey(BLACK)
        return image


class SoundController:
    '''Utility class for loading and controlling sounds.'''
    def __init__(self, sound_name_list):
        self.effects = {}
        for sound_name in sound_name_list:
            self.effects[sound_name] = pg.mixer.Sound(path.join(SOUND_DIR, sound_name+'.ogg'))
            self.effects[sound_name].set_volume(.5)

    def volume_up(self):
        for sound in self.effects.values():
            sound.set_volume(sound.get_volume() + .1)

    def volume_down(self):
        for sound in self.effects.values():
            sound.set_volume(sound.get_volume() - .1)
