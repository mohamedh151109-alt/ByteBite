import pygame as pg
from settings import *


def clamp(v, low, high):
    return low if v < low else min(v, high)


class Player:
    def __init__(self, x, y, speed=speed):
        self.x = float(x)
        self.y = float(y)
        self.speed = speed
        self.rect = pg.Rect((100, 100, player_width, player_height))
# The v_X is abbreviate for Velocity x
    def update(self, speed, dt, vx, vy,):
        self.v_x = dt * vx * speed
        self.v_y = dt * vy * speed

        self.x = clamp(self.v_x + self.x, 0, Windows_Width - player_width)
        self.y = clamp(self.v_y + self.y, 0, Windows_Height - (player_height))

        self.rect.topleft = (round(self.x), round(self.y))
