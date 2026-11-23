import time

import pygame as pg
from objects import Level_up, Player, Segment
from settings import *

pg.init()

screen = pg.display.set_mode((Windows_Width, Windows_Height))
running = True
pg.display.set_caption("Snake Game")
clock = pg.time.Clock()
player = Player(Windows_Width / 2 - player_width, Windows_Height / 2 - player_height)
vx = 0
vy = 0
level_up = Level_up()

segments = []
GAPS = 8

while running:
    dt = clock.tick(FPS) / 1000.0
    screen.fill((0, 0, 0))
    key = pg.key.get_pressed()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT and (vx != -1 or len(segments) == 0):
                vx, vy = 1, 0
            elif event.key == pg.K_LEFT and (vx != 1 or len(segments) == 0):
                vx, vy = -1, 0
            elif event.key == pg.K_DOWN and (vy != -1 or len(segments) == 0):
                vy, vx = 1, 0
            elif event.key == pg.K_UP and (vy != 1 or len(segments) == 0):
                vy, vx = -1, 0

    player.update(speed, dt, vx, vy)

    for seg in segments:
        seg.before(player.history_snake, GAPS)

    for seg in segments:
        if seg.visible:
            pg.draw.rect(screen, (100, 255, 100), seg.rect, border_radius=10)

    hit_self = any(
        seg.visible and player.rect.colliderect(seg.rect) for seg in segments[1:]
    )

    if player.hit_wall or hit_self:
        time.sleep(0.225)
        player = Player(
            Windows_Width / 2 - player_width, Windows_Height / 2 - player_height
        )
        vx, vy = 0, 0
        level_up = Level_up()
        segments = []

    player_rect = pg.draw.rect(screen, (4, 82, 2), player.rect, border_radius=6)
    level_up_rect = pg.draw.rect(screen, (255, 0, 0), level_up.rect, border_radius=6)

    x_distance = player_rect.x - level_up_rect.x

    if player_rect.colliderect(level_up_rect):
        level_up = Level_up()
        segments.append(Segment(len(segments)))

    pg.display.flip()


pg.quit()

# * To do : 1- reset massage 2- mainmenu 3- player shapes 4- score 5- edits
