import pygame as pg
from constants import  *


class Platform(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        super(Platform, self).__init__()

        self.image = pg.transform.scale_by(image, TILE_SCALE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE


class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        super(Coin, self).__init__()

        self.load_animation()
        self.current_image = 0
        self.image = self.animation[self.current_image]

        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE

        self.timer = pg.time.get_ticks()
        self.interval = 200

    def load_animation(self):
        tile_size = 16
        num_images = 5

        self.animation = []
        spriteshet = pg.image.load("Sprites/Coin_Gems/MonedaD.png")
        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spriteshet.subsurface(rect)
            image = pg.transform.scale_by(image, TILE_SCALE)
            self.animation.append(image)

    def update(self):
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >=len(self.animation):
                self.current_image = 0
            self.image = self.animation[self.current_image]
            self.timer = pg.time.get_ticks()

class Portal(pg.sprite.Sprite):
    def __init__(self, x, y):
        super(Portal, self).__init__()

        self.load_animation()
        self.current_image = 0
        self.image = self.animation[self.current_image]

        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE

        self.timer = pg.time.get_ticks()
        self.interval = 200

    def load_animation(self):
        tile_size = 64
        num_images = 8

        self.animation = []
        spriteshet = pg.image.load("Sprites/Purple Portal Sprite Sheet.png")
        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spriteshet.subsurface(rect)
            image = pg.transform.scale_by(image, TILE_SCALE)
            self.animation.append(image)

    def update(self):
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >=len(self.animation):
                self.current_image = 0
            self.image = self.animation[self.current_image]
            self.timer = pg.time.get_ticks()