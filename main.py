import pygame as pg
import pytmx

from constants import *
from tiles import Platform, Coin, Portal
from player import Player
from npc import Crab
from npc2 import Octi
from ball import Ball

pg.init()


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Платформер")
        self.level = 1
        self.setup()

    # noinspection PyAttributeOutsideInit
    def setup(self):
        self.mode = "game"
        self.clock = pg.time.Clock()
        self.is_running = False

        self.tmx_map = pytmx.load_pygame(f"maps/level {self.level}.tmx")
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.portals = pg.sprite.GroupSingle()

        self.map_pixel_width = self.tmx_map.tilewidth * self.tmx_map.width * TILE_SCALE
        self.map_pixel_height = self.tmx_map.tileheight * self.tmx_map.height * TILE_SCALE

        self.player = Player(self.map_pixel_width, self.map_pixel_height)
        self.all_sprites.add(self.player)
        self.background = pg.image.load("background.jpg")
        self.background = pg.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.collected_coins = 0

        for layer in self.tmx_map:
            for x, y, gid, in layer:
                tile = self.tmx_map.get_tile_image_by_gid(gid)
                if tile:
                    platform = Platform(tile, x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight)

                    if layer.name == "ground":
                        self.all_sprites.add(platform)
                        self.platforms.add(platform)
                    elif layer.name == "crab":
                        pos = (x * self.tmx_map.tilewidth * TILE_SCALE, y * self.tmx_map.tileheight)
                        crab = Crab(self.map_pixel_width, self.map_pixel_height, pos)
                        self.all_sprites.add(crab)
                        self.enemies.add(crab)
                    elif layer.name == "octi":
                        pos = (x * self.tmx_map.tilewidth * TILE_SCALE, y * self.tmx_map.tileheight)
                        octi = Octi(self.map_pixel_width, self.map_pixel_height, pos)
                        self.all_sprites.add(octi)
                        self.enemies.add(octi)
                    elif layer.name == "coins":
                        coin = Coin(x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight)
                        self.all_sprites.add(coin)
                        self.coins.add(coin)
                        self.coins_amount = len(self.coins.sprites())
                    elif layer.name == "portal":
                        portal = Portal(x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight)
                        self.all_sprites.add(portal)
                        self.portals.add(portal)

                    else:
                        self.all_sprites.add(platform)
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 4

        self.run()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pg.quit()
        quit()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            if self.mode == "game over":
                if event.type == pg.KEYDOWN:
                    self.setup()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if self.player.current_animation in (
                            self.player.idle_animation_right, self.player.run_animation_right):
                        direction = "right"
                    else:
                        direction = "left"

                    ball = Ball(self.player.rect, direction)
                    self.all_sprites.add(ball)
                    self.balls.add(ball)

        #keys = pg.key.get_pressed()
        #
        # if keys[pg.K_LEFT]:
        #     self.camera_x += self.camera_speed
        # if keys[pg.K_RIGHT]:
        #     self.camera_x -= self.camera_speed
        # if keys[pg.K_UP]:
        #     self.camera_y += self.camera_speed
        # if keys[pg.K_DOWN]:
        #     self.camera_y -= self.camera_speed

    def update(self):
        if self.player.hp <= 0:
            self.mode = "game over"
            return

        hits = pg.sprite.spritecollide(self.player, self.coins, True)
        for hit in hits:
            self.collected_coins += 1
            print(self.collected_coins)
            print(self.coins_amount)

        for enemy in self.enemies.sprites():
            enemy.update(self.platforms)
            if pg.sprite.collide_mask(self.player, enemy):
                self.player.get_damage()
        self.player.update(self.platforms)
        self.balls.update()
        self.coins.update()
        self.portals.update()

        pg.sprite.groupcollide(self.balls, self.enemies, True, True)
        pg.sprite.groupcollide(self.balls, self.platforms, True, False)
        hits = pg.sprite.spritecollide(self.player, self.portals, False, pg.sprite.collide_mask)
        if self.collected_coins > self.coins_amount / 2:
            for hit in hits:
                self.level += 1
                if self.level == 3:
                    quit()
                self.setup()


        self.camera_x = self.player.rect.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.rect.y - SCREEN_HEIGHT // 2

        self.camera_x = max(0, min(self.camera_x, self.map_pixel_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.map_pixel_height - SCREEN_HEIGHT))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, -self.camera_y))
        # pg.draw.rect(self.screen, (100, 100, 255), self.player.rect.move(-self.camera_x, -self.camera_y), width=2)
        # pg.draw.rect(self.screen, (255, 0, 0), self.player.phys_box.move(-self.camera_x, -self.camera_y), width=2)
        pg.draw.rect(self.screen, pg.Color("red"), (10, 10, self.player.hp * 10, 10))
        pg.draw.rect(self.screen, pg.Color("black"), (10, 10, 100, 10), 1)

        if self.mode == "game over":
            text = font.render("Вы проиграли", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
        pg.display.flip()


if __name__ == "__main__":
    game = Game()
