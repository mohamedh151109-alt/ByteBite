import math
import random
import time

import pygame as pg
from objects import Level_up, Player, Power_1, Power_2, Segment
from settings import *

pg.init()
pg.font.init()

######### Variables ##########

boost1 = None
boost1_until = 0
boost2 = None
shield = 0
defended_until = 0
next_boost = pg.time.get_ticks() + random.randint(6000, 14000)
screen = pg.display.set_mode((Windows_Width, Windows_Height))
running = True
snake_img = pg.transform.scale(
    pg.image.load("assests/Snake.png").convert_alpha(), (player_width, player_height)
)
head_images = {
    (0, -1): pg.transform.rotate(snake_img, 180),
    (0, 1): snake_img,
    (-1, 0): pg.transform.rotate(snake_img, -90),
    (1, 0): pg.transform.rotate(snake_img, 90),
    (0, 0): pg.transform.rotate(snake_img, 180),
}
body_img = pg.transform.scale(
    pg.image.load("assests/Snake_body.png").convert_alpha(),
    (player_width, player_height),
)
shield_img = pg.transform.scale(
    pg.image.load("assests/shield.png").convert_alpha(), (power_2_size, power_2_size)
)
apple_img = pg.transform.scale(
    pg.image.load("assests/Apple.png").convert_alpha(),
    (level_up_width, level_up_height),
)
x2_img = pg.transform.scale(
    pg.image.load("assests/2.png").convert_alpha(), (power_1_size, power_1_size)
)
pg.display.set_caption("Snake Game")
clock = pg.time.Clock()
player = Player(
    Windows_Width / 2 - player_width / 2, (Windows_Height / 2 - player_height / 2) + 35
)
vx = 0
vy = 0
level_up = Level_up()
segments = []
GAPS = 7

current_page = "menu"
your_score = 0

#############################


########### Fonts ###########

main_font = pg.font.Font("freesansbold.ttf", 50)
big_font = pg.font.SysFont(None, 80)
small_font = pg.font.SysFont(None, 35)
middle_font = pg.font.SysFont(None, 42)

#############################

######### Reset function ########


def new_game():
    player = Player(
        Windows_Width / 2 - player_width / 2,
        (Windows_Height / 2 - player_height / 2) + 35,
    )
    vx, vy = 0, 0
    last_x, last_y = 0, 0
    distance_since = player_width
    level_up = Level_up()
    segments = []
    player_score = 0
    return (
        player,
        vx,
        vy,
        last_x,
        last_y,
        distance_since,
        level_up,
        segments,
        player_score,
    )


#################################

####### drawing function ########

def drawing(text, font, color, x, y):
    new_text = font.render(text, True, color)
    screen.blit(new_text, new_text.get_rect(center=(x, y)))

################################


######### Draw Menu ############
def draw_menu():
    drawing("SNAKE GAME", big_font, (100, 255, 100), Windows_Width // 2, 120)
    if your_score != 0:
        drawing(
            f"GAME OVER - SCORE: {your_score}",
            small_font,
            (255, 80, 80),
            Windows_Width // 2,
            180,
        )
    for i, (label, value) in enumerate(speed_choices):
        if i == current_speed_index:
            color = (255, 255, 0)
            text = "<---" + label
        else:
            color = (200, 200, 200)
            text = label
        drawing(text, main_font, color, Windows_Width // 2, 260 + i * 60)
        drawing(
            "Move UP/DOWN to change speed, Enter to start",
            small_font,
            (150, 150, 150),
            Windows_Width // 2,
            Windows_Height - 40,
        )

############################


########### Score ##############

def score_f():
    sub_title = middle_font.render("SNAKE GAME", True, (100, 255, 100))
    screen.blit(sub_title, (450, font_y + 20))
    # drawing("SNAKE GAME", small_font, (100, 255, 100), 500, font_y)
    score_text = main_font.render(f"Your Score: {player_score}", True, (255, 255, 255))
    screen.blit(score_text, (font_x, font_y))
    pg.draw.line(screen, (200, 200, 200), (0, 70), (Windows_Width, 70), 3)


# * to do: 1- main menu 2-
player, vx, vy, last_x, last_y, distance_since, level_up, segments, player_score = (
    new_game()
)
##############################


############ The loop of the window ############

while running:
    dt = clock.tick(FPS) / 1000.0
    screen.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN:
            if current_page == "menu":
                if event.key == pg.K_UP:
                    current_speed_index = (current_speed_index - 1) % len(speed_choices)
                elif event.key == pg.K_DOWN:
                    current_speed_index = (current_speed_index + 1) % len(speed_choices)
                elif event.key == pg.K_RETURN:  # K_return == Enter
                    speed = speed_choices[current_speed_index][1]
                    (
                        player,
                        vx,
                        vy,
                        last_x,
                        last_y,
                        distance_since,
                        level_up,
                        segments,
                        player_score,
                    ) = new_game()
                    current_page = "play"
                    GAPS = math.ceil((player_width) / (speed / FPS))
                    boost1 = None
                    boost1_until = 0
                    boost2 = None
                    shield = 0
                    defended_until = 0
                    next_boost = pg.time.get_ticks() + random.randint(7000, 14000)

            elif current_page == "play":
                can_turn = distance_since >= player_width or len(segments) == 0
                if event.key == pg.K_ESCAPE:
                    current_page = "menu"
                elif (
                    event.key == pg.K_RIGHT
                    and can_turn
                    and (last_x != -1 or len(segments) == 0)
                ):
                    if (vx, vy) != (1, 0):
                        vx, vy = 1, 0
                        distance_since = 0
                elif (
                    event.key == pg.K_LEFT
                    and can_turn
                    and (last_x != 1 or len(segments) == 0)
                ):
                    if (vx, vy) != (-1, 0):
                        vx, vy = -1, 0
                        distance_since = 0
                elif (
                    event.key == pg.K_DOWN
                    and can_turn
                    and (last_y != -1 or len(segments) == 0)
                ):
                    if (vx, vy) != (0, 1):
                        vy, vx = 1, 0
                        distance_since = 0
                elif (
                    event.key == pg.K_UP
                    and can_turn
                    and (last_y != 1 or len(segments) == 0)
                ) and (vx, vy) != (0, -1):
                    vy, vx = -1, 0
                    distance_since = 0
    if current_page == "menu":
        draw_menu()
    ########################### Playing #############################

    elif current_page == "play":
        now = pg.time.get_ticks()
        player.update(speed, dt, vx, vy)
        last_x, last_y = vx, vy
        distance_since += speed * dt
        for seg in segments:
            seg.before(player.history_snake, GAPS)

        for seg in segments:
            if seg.visible:
                screen.blit(body_img, seg.rect)

        hit_self = any(
            seg.visible and player.rect.colliderect(seg.rect) for seg in segments[1:]
        )

        if (player.hit_wall or hit_self) and now >= defended_until:
            if shield == 0:
                time.sleep(0.225)
                your_score = player_score
                current_page = "menu"
                (
                    player,
                    vx,
                    vy,
                    last_x,
                    last_y,
                    distance_since,
                    level_up,
                    segments,
                    player_score,
                ) = new_game()
                boost1 = None
                boost1_until = 0
                shield = 0
                boost2 = None
                defended_until = 0
                next_boost = pg.time.get_ticks() + random.randint(7000, 14000)
                continue
            else:
                defended_until = now + 1000
                next_boost = now + random.randint(7000, 14000)
                shield = 0
        if boost1 is None and boost2 is None and now >= next_boost:
            if shield == 1 or random.random() > 0.5:
                boost1 = Power_1()
            else:
                boost2 = Power_2()

        if boost1 is not None:
            if boost1.expired():
                boost1 = None
                next_boost = now + random.randint(7000, 14000)
            else:
                screen.blit(x2_img, boost1.rect)
                if player.rect.colliderect(boost1.rect):
                    boost1_until = now + power_1_duration
                    boost1 = None
                    next_boost = now + random.randint(7000, 14000)
        if boost2 is not None:
            if boost2.expired2():
                boost2 = None
                next_boost = now + random.randint(7000, 14000)
            else:
                screen.blit(shield_img, boost2.rect)
                if player.rect.colliderect(boost2.rect):
                    shield = 1
                    boost2 = None
                    next_boost = now + random.randint(7000, 14000)
        head = head_images[(vx, vy)]
        player.rect = screen.blit(head, player.rect)
        level_up_rect = screen.blit(apple_img, level_up.rect)

        x_distance = player.rect.x - level_up_rect.x

        if player.rect.colliderect(level_up_rect):
            level_up = Level_up()
            segments.append(Segment(len(segments)))
            if now < boost1_until:
                player_score += 2
                segments.append(Segment(len(segments)))
            else:
                player_score += 1

        if now < boost1_until:
            left_seconds = (boost1_until - now) / 1000
            drawing(
                f"x2 SCORE {int(left_seconds)} SECONDS left",
                small_font,
                (0, 200, 255),
                220,
                90,
            )
        if shield == 1:
            drawing(
                "You have 1 shield",
                small_font,
                (255, 100, 100),
                Windows_Width // 2 + 200,
                90,
            )

        score_f()
    ######################################################################

    pg.display.flip()
##################################
pg.quit()
