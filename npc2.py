from constants import *
import pygame as pg


class Octi(pg.sprite.Sprite):
    def __init__(self, map_width, map_height, pos):
        self._layer = 2
        super(Octi, self).__init__()

        self.load_animations()
        self.current_animation = self.move_animation_right
        self.current_image = 0

        self.image = self.current_animation[self.current_image]

        self.rect = self.image.get_rect()
        self.rect.topleft = pos # Начальное положение персонажа
        self.left_edge = pos[0] - (16 * TILE_SCALE * 3)
        self.right_edge = pos[0] + (16 * TILE_SCALE * 3)


        self.phys_box = pg.Rect(0, 0, self.rect.w * 0.5, self.rect.h)

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 1
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
                self.current_animation = self.move_animation_left
        elif self.direction == "left":
            self.velocity_x = -5
            if self.rect.left <= self.left_edge:
                self.direction = "right"
                self.current_animation = self.move_animation_right


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
                self.direction = "left"

            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left = platform.rect.right
                self.direction = "right"

        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >=len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()

    def load_animations(self):
        tile_size = 16
        num_images = 2

        self.move_animation_left = []
        spriteshet = pg. image.load("sprites/Sprite Pack 2/3 - Octi/Idle_&_Movement (16 x 16).png")
        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spriteshet.subsurface(rect)
            image = pg.transform.scale_by(image, TILE_SCALE)
            self.move_animation_left.append(image)
        self.move_animation_right = [pg.transform.flip(image, True, False) for image in self.move_animation_left]
