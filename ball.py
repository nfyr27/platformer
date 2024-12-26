import pygame as pg

class Ball(pg.sprite.Sprite):
    def __init__(self, player_rect, direction):
        super(Ball, self).__init__()

        self.direction = direction
        self.speed = 10

        self.image = pg.image.load("Sprites/ball.png")
        self.image = pg.transform.scale(self.image, (30, 30))

        self.live = 500
        self.time = pg.time.get_ticks()

        self.rect = self.image.get_rect()

        if direction == "right":
            self.rect.x = player_rect.right
        else:
            self.rect.x = player_rect.left

        self.rect.y = player_rect.centery

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if self.time + self.live < pg.time.get_ticks():
            self.kill()
