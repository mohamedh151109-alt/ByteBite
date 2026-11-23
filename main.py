import pygame as pg
from settings import *
from snake import Player

pg.init()

screen = pg.display.set_mode((Windows_Width, Windows_Height))
running = True
pg.display.set_caption("Snake Game")
clock = pg.time.Clock()

player = Player(100, 100)

vx = 0
vy = 0

while running:
    dt = clock.tick(FPS) / 1000.0
    screen.fill((0, 0, 0))

    key = pg.key.get_pressed()

    for event in pg.event.get():
        
        if event.type == pg.QUIT:
                    running = False
        
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                vx, vy = 1, 0
            elif event.key == pg.K_LEFT:
                vx, vy = -1, 0
            elif event.key == pg.K_DOWN:
                vy, vx = 1, 0 
            elif event.key == pg.K_UP:
                vy, vx = -1, 0 
                

    player.update(speed, dt, vx, vy)

    pg.draw.rect(screen, (255, 0, 0), player.rect)
    pg.display.flip()


pg.quit()
