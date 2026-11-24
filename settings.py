# the Constants in our project to the project organized
import pygame as pg

pg.init()
pg.font.init()

# the windows screen dimensions
power_1_size = 40
power_1_life = 7000
power_1_duration = 7000
power_2_size = 40
power_2_life = 10000
power_2_duration = 7000
Windows_Width = 650
Windows_Height = 650
FPS = 60
player_width = 40
player_height = 40
level_up_width = 40
level_up_height = 40
speed_choices = [("SLOW", 200), ("MIDDLE", 350), ("FAST", 520)]
current_speed_index = 1
speed = speed_choices[current_speed_index][1]
font_x = 10
font_y = 20
player_score = 0
shield = 0
