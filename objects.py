import random

import pygame as pg
from settings import *

pg.init()
pg.font.init()


def clamp(v, low, high):
    return (low, True) if v < low else (high, True) if v > high else (v, False)


class Player:
    def __init__(self, x, y, speed=speed):
        self.x = float(x)
        self.y = float(y)
        self.speed = speed
        self.rect = pg.Rect((self.x, self.y, player_width, player_height))
        self.history_snake = []
        self.hit_wall = False

    # The v_X is an abbreviation for Velocity x
    def update(
        self,
        speed,
        dt,
        vx,
        vy,
    ):
        ancient = (self.x, self.y)
        self.v_x = dt * vx * speed
        self.v_y = dt * vy * speed

        self.x, hit_x = clamp(self.v_x + self.x, 0, (Windows_Width - player_width))
        self.y, hit_y = clamp(self.v_y + self.y, 70, (Windows_Height - player_height))
        self.hit_wall = hit_x or hit_y

        self.rect.topleft = (round(self.x), round(self.y))
        if (self.x, self.y) != ancient:
            self.history_snake.insert(0, (self.x, self.y))
            del self.history_snake[2000:]


class Segment:
    def __init__(self, index):
        self.index = index
        self.rect = pg.Rect((1000, 1000 / 2, player_width, player_height))
        self.visible = False

    def before(self, history, gap):
        i = (self.index + 1) * gap
        if i < len(history):
            x, y = history[i]
            self.rect.topleft = (round(x), round(y))
            self.visible = True


class Level_up:
    def __init__(self):
        x = random.randint(100, 600)
        y = random.randint(100, 550)
        self.rect = pg.Rect((x, y, level_up_width, level_up_height))

class Power_1:
    def __init__(self):
        x = random.randint(100, 600)
        y = random.randint(100, 550)
        self.rect = pg.Rect((x, y, power_1_size, power_1_size))
        self.be_live_time = pg.time.get_ticks()
    def expired(self):
        return pg.time.get_ticks() - self.be_live_time >= power_1_duration
    
class Power_2:
    def __init__(self):
        x = random.randint(100, 600)
        y = random.randint(100, 550)
        self.rect = pg.Rect((x, y, power_1_size, power_1_size))
        self.be_live_time = pg.time.get_ticks()
    def expired2(self):
        if shield == 0:
            return pg.time.get_ticks() - self.be_live_time >= power_1_duration
    
    