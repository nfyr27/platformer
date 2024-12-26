from constants import *
import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        self._layer = 2
        super(Player, self).__init__()

        self.load_animations()
        self.current_animation = self.idle_animation_right
        self.current_image = 0

        self.image = self.current_animation[self.current_image]

        self.rect = self.image.get_rect()
        self.rect.center = (200, map_height - 500)  # Начальное положение персонажа

        self.phys_box = pg.Rect(0, 0, self.rect.w * 0.5, self.rect.h)

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE
        self.timer = pg.time.get_ticks()
        self.interval = 200
        self.hp = 10
        self.damage_timer = pg.time.get_ticks()
        self.damage_interval = 1000

    def update(self, platforms):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and not self.is_jumping:
            self.jump()
        if keys[pg.K_a]:
            if self.current_animation != self.run_animation_left:
                self.current_animation = self.run_animation_left
                self.current_image = 0

            self.velocity_x = - 10
        elif keys[pg.K_d]:
            if self.current_animation != self.run_animation_right:
                self.current_animation = self.run_animation_right
                self.current_image = 0

            self.velocity_x = 10
        else:
            if self.current_animation not in (self.idle_animation_right, self.idle_animation_left):
                if self.current_animation == self.run_animation_right:
                    self.current_animation = self.idle_animation_right
                elif self.current_animation == self.run_animation_left:
                    self.current_animation = self.idle_animation_left
                else:
                    self.current_animation = self.idle_animation_right

            self.velocity_x = 0


        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x

        self.velocity_y += self.gravity

        # if self.velocity_y >= 16 * TILE_SCALE:
        #     self.velocity_y = 16 * TILE_SCALE - 1

        self.rect.y += self.velocity_y

        self.phys_box.midbottom = self.rect.midbottom

        for platform in platforms:
            if platform.rect.collidepoint(self.phys_box.midbottom):
                self.phys_box.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False

            if platform.rect.collidepoint(self.phys_box.midtop):
                self.phys_box.top = platform.rect.bottom
                self.velocity_y = 0

            if platform.rect.collidepoint(self.phys_box.midright):
                self.phys_box.right = platform.rect.left

            if platform.rect.collidepoint(self.phys_box.midleft):
                self.phys_box.left = platform.rect.right

        self.rect.midbottom = self.phys_box.midbottom

        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >=len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()


    def jump(self):
        self.velocity_y = -TILE_SCALE * 8
        self.is_jumping = True

    def get_damage(self):
        if pg.time.get_ticks() - self.damage_timer > self.damage_interval:
            self.hp -= 1
            self.damage_timer = pg.time.get_ticks()


    def load_animations(self):
        tile_size = 32

        self.idle_animation_right = []
        num_images = 4
        spriteshet = pg.image.load("sprites/Sprite Pack 3/4 - Tommy/Idle_Poses (32 x 32).png")
        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spriteshet.subsurface(rect)
            image = pg.transform.scale_by(image, TILE_SCALE)
            self.idle_animation_right.append(image)
        self.idle_animation_left = [pg.transform.flip(image, True, False) for image in self.idle_animation_right]

        self.run_animation_right = []
        num_images = 8
        spriteshet = pg.image.load("sprites/Sprite Pack 3/4 - Tommy/Running (32 x 32).png")
        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spriteshet.subsurface(rect)
            image = pg.transform.scale_by(image, TILE_SCALE)
            self.run_animation_right.append(image)
        self.run_animation_left = [pg.transform.flip(image, True, False) for image in self.run_animation_right]