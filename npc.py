from constants import *
import pygame as pg


class Crab(pg.sprite.Sprite):
    def __init__(self, map_width, map_height, pos):
        self._layer = 2
        super(Crab, self).__init__()

        self.load_animations()
        self.current_animation = self.animation
        self.current_image = 0

        self.image = self.current_animation[self.current_image]

        self.rect = self.image.get_rect()
        self.rect.topleft = pos  # Начальное положение персонажа
        self.left_edge = pos[0] - (16 * TILE_SCALE * 2)
        self.right_edge = pos[0] + (16 * TILE_SCALE * 2)


        self.phys_box = pg.Rect(0, 0, self.rect.w * 0.5, self.rect.h)

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 1.5
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE
        self.timer = pg.time.get_ticks()
        self.interval = 200

        self.direction = "right"

    def update(self, platforms):

        if self.direction == "right":
            self.velocity_x = 5
            if self.rect.right >= self.right_edge:
                self.direction = "left"

        elif self.direction == "left":
            self.velocity_x = -5
            if self.rect.left <= self.left_edge:
                self.direction = "right"

        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0

            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0

            if platform.rect.collidepoint(self.rect.midright):
                self.rect.right = platform.rect.left

            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left = platform.rect.right

        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >=len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()

    def load_animations(self):
        tile_size = 32

        self.animation = []
        image = pg.image.load(
            "sprites/Sprite Pack 2/9 - Snip Snap Crab/Movement_(Flip_image_back_and_forth) (32 x 32).png")
        image = pg.transform.scale_by(image, TILE_SCALE)
        self.animation.append(image)
        self.animation.append(pg.transform.flip(image, True, False))