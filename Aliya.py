""" Code By Ali Talabi """
import random
import pgzrun
import sys
import pygame

from pgzero import clock, music
from pgzero.keyboard import keyboard
from pgzero.actor import Actor
from ctypes import windll
from pgzero.loaders import sounds

WIDTH = 1000
HEIGHT = 500
mod = sys.modules['__main__']
hwnd = pygame.display.get_wm_info()['window']
windll.user32.MoveWindow(hwnd, 175, 100, WIDTH, HEIGHT, False)
TITLE = "Aliya"

bg1 = Actor("bg1")
bg2 = Actor("bg1")
hero = Actor("hero")
moving_spike1 = Actor("moving_spike")
moving_spike2 = Actor("moving_spike")
moving_spike3 = Actor("moving_spike")
moving_spike4 = Actor("moving_spike")
moving_spike5 = Actor("moving_spike")
moving_spike6 = Actor("moving_spike")
spike_wall1 = Actor("spike_wall")
play_but = Actor("play_but1")
show_health = Actor("health")
pause_but = Actor("pause_button1")
resume_but = Actor("resume_but1")
quit_but = Actor("quit_but1")
how_to_play_but = Actor("how_to_play_but1")
help_game = Actor("help_game1")
play_again_but = Actor("play_again_but1")
main_menu_but = Actor("main_menu_but1")
hero_hitbox = Actor("hero_hitbox")

laser_guns = []
lasers = []

for i in range(3):
    laser_gun = Actor("laser_gun")
    laser = Actor("laser")
    laser_gun.x = 1035
    laser_gun.y = 125 + (i * 125)
    laser_gun.angle = 90
    laser.x = 2 * WIDTH
    laser.y = 125 + (i * 125)
    laser_guns.append(laser_gun)
    lasers.append(laser)

bg1.pos = WIDTH // 2, HEIGHT // 2
bg2.pos = WIDTH + WIDTH // 2, HEIGHT // 2
hero.pos = 50, HEIGHT // 2
hero_hitbox.pos = hero.pos
show_health.pos = 900, 12.5
moving_spike1.pos = 957, random.randint(101, 399)
moving_spike2.pos = 1157, random.randint(101, 399)
moving_spike3.pos = 1357, random.randint(101, 399)
moving_spike4.pos = 1457, random.randint(101, 399)
moving_spike5.pos = 1557, random.randint(101, 399)
moving_spike6.pos = 1757, random.randint(101, 399)
spike_wall1.pos = 1141, random.randint(150, 350)
play_but.pos = WIDTH // 2, HEIGHT // 2 - 50
quit_but.pos = WIDTH // 2, HEIGHT // 2 + 162
how_to_play_but.pos = WIDTH // 2, HEIGHT // 2 + 56
pause_but.pos = 10000, 10000
resume_but.pos = 10000, 10000
help_game.pos = 10000, 10000
play_again_but.pos = 10000, 10000
main_menu_but.pos = 10000, 10000

bgs_speed = 4
hero_speed = 4
hero_turn_speed = 7
moving_spike_speed_y = 3
moving_spike_speed_x = 4
spike_wall_speed_x = 5
spike_wall_speed_y = 5
moving_spike_turn_speed = 10
music_form = 0
show_health_image_num = -1
change_music_form_time = 18
win_timer = 64
timer_in_screen = 0
laser_guns_come_time = 16
laser_shooting_time = 2
laser_off_time = 2.7

game_status = "starting_menu"
hero_status = "normal"

health_image_list = ["health_lose_1", "health_lose_2", "health_lose_3", "health_lose_4", "health_lose_5",
                     "health_lose_6", "health_lose_7", "health_lose_8"]

music_list = ["game_music_1", "game_music_2", "game_music_3"]
music_status = music_list[music_form]

random_move_list = []
for i in range(6):
    move_list = ["up", "down"]
    move = random.choice(move_list)
    random_move_list.append(move)

status_moving_spike1 = random_move_list[0]
status_moving_spike2 = random_move_list[1]
status_moving_spike3 = random_move_list[2]
status_moving_spike4 = random_move_list[3]
status_moving_spike5 = random_move_list[4]
status_moving_spike6 = random_move_list[5]

laser_gun_stop = False
laser_gun_back_bool = False
music_play = True
help_screen_come_bool = False
laser_gun_come_3 = True
change_music_form_bool = True

spike_wall1.angle = 90


def change_help_screen_come_bool():
    """ This function brings up the help page . """
    global help_screen_come_bool
    help_screen_come_bool = True


def laser_gun_back():
    """ This function calls the laser gun again . """
    global laser_gun_back_bool
    if laser_gun_back_bool and game_status != "pause":
        if music_status != music_list[2]:
            for laser_gun_item in laser_guns:
                laser_gun_item.x += 2
                if laser_gun_item.x >= 1036:
                    laser_gun_item.pos = 10000, 10000
                    laser_gun_back_bool = False

        if music_status == music_list[2]:
            laser_guns[0].x += 2
            if laser_guns[0].x >= 1036:
                laser_guns[0].pos = 10000, 10000
                laser_gun_back_bool = False


def laser_off():
    """ This function returns the laser gun after shooting the laser . """
    global laser_gun_back_bool
    laser_gun_back_bool = True
    if music_status != music_list[2]:
        for laser_item in lasers:
            laser_item.x = 2 * WIDTH

    if music_status == music_list[2]:
        lasers[0].x = 2 * WIDTH
    clock.schedule_interval(laser_gun_back, 1 / 60)


def laser_shooting():
    """ This function shoots the laser . """
    if music_status != music_list[2]:
        for laser_item in lasers:
            laser_item.x = WIDTH // 2
            sounds.laser_shoot.play()

    if music_status == music_list[2]:
        lasers[0].y = laser_guns[0].y
        lasers[0].x = WIDTH // 2
        sounds.laser_shoot.play()


def spike_wall_call():
    """ This function calls the spike wall . """
    spike_wall1.x = 1141
    spike_wall1.y = random.randint(150, 350)


def music_change_form():
    """ This function changes music form . """
    global music_status, music_form
    music_status = music_list[music_form + 1]
    music_form += 1


def image_change_normal():
    """ This function changes a hero to normal status . """
    global hero_status
    if hero_status == "invincible":
        hero.image = "hero"
        hero_status = "normal"


def correct_actors_motion(actor):
    """ This function, when something is removed from the page,
        re-enters it from the opposite side . """
    if actor.x < -actor.width // 2:
        actor.x = WIDTH + actor.width // 2


def correct_moving_spikes_motion(actor):
    """ This function will insert moving spikes from the opposite side with
        a random height position when they leave the page . """
    if actor.x < -actor.width // 2:
        actor.x = WIDTH + actor.width // 2
        actor.y = random.randint(100, 400)


def draw():
    global game_status

    if game_status == "starting_menu":
        mod.screen.blit("bg_first", (0, 0))
        play_but.draw()
        quit_but.draw()
        how_to_play_but.draw()
        help_game.draw()

    if game_status != "starting_menu" and game_status != "close_screen":
        bg1.draw()
        bg2.draw()
        moving_spike1.draw()
        moving_spike2.draw()
        moving_spike3.draw()
        moving_spike4.draw()
        moving_spike5.draw()
        moving_spike6.draw()
        spike_wall1.draw()
        show_health.draw()
        hero.draw()
        hero_hitbox.draw()
        pause_but.draw()
        resume_but.draw()
        pause_but.pos = 25, 25
        show_health.draw()
        main_menu_but.draw()

        if game_status == "pause":
            quit_but.draw()

        for laser_item in lasers:
            laser_item.draw()

        play_again_but.draw()

        for laser_gun_item in laser_guns:
            laser_gun_item.draw()

        mod.screen.draw.text("Time : " + str(timer_in_screen), center=(WIDTH // 2, 30), color="gold2", fontsize=30)

        if game_status == "win":
            mod.screen.draw.text("YOU WIN !", center=(WIDTH // 2, (HEIGHT // 2 - 100)), color="gold2", fontsize=100)

        if game_status == "lose":
            mod.screen.draw.text("GAME OVER", center=(WIDTH // 2, (HEIGHT // 2) - 100), color="red", fontsize=100)
            music.stop()

    if game_status == "quit":
        mod.screen.blit("bg_end", (0, 0))
        clock.schedule_unique(quit, 3)
        game_status = "close_screen"


def update():
    global game_status, hero_status, laser_gun_stop, status_moving_spike1, status_moving_spike2, status_moving_spike3, \
        status_moving_spike4, status_moving_spike5, status_moving_spike6, hero_turn_speed, spike_wall_speed_x, \
        spike_wall_speed_y, moving_spike_speed_x, moving_spike_speed_y, show_health_image_num, bgs_speed, \
        music_play, change_music_form_time, laser_guns_come_time, laser_off_time, \
        laser_shooting_time, laser_gun_come_3, change_music_form_bool, win_timer, timer_in_screen

    hero_hitbox.pos = hero.pos

    if game_status == "play":
        bg1.x -= bgs_speed
        bg2.x -= bgs_speed
        correct_actors_motion(bg1)
        correct_actors_motion(bg2)
        spike_wall1.x -= spike_wall_speed_x

        win_timer -= 1 / 60
        timer_in_screen = int(win_timer)

        quit_but.pos = 10000, 10000
        play_but.pos = 10000, 10000

        if music_play:
            music.play("game_music")
            music_play = False

        if moving_spike1.y < 100 and status_moving_spike1 == "up":
            status_moving_spike1 = "down"

        if moving_spike1.y > 400 and status_moving_spike1 == "down":
            status_moving_spike1 = "up"

        if status_moving_spike1 == "up":
            moving_spike1.y -= moving_spike_speed_y

        if status_moving_spike1 == "down":
            moving_spike1.y += moving_spike_speed_y

        if moving_spike1.x <= 300:
            correct_moving_spikes_motion(moving_spike1)

        moving_spike1.x -= moving_spike_speed_x
        moving_spike1.angle += moving_spike_turn_speed

        if moving_spike2.y < 100 and status_moving_spike2 == "up":
            status_moving_spike2 = "down"

        if moving_spike2.y > 400 and status_moving_spike2 == "down":
            status_moving_spike2 = "up"

        if status_moving_spike2 == "up":
            moving_spike2.y -= moving_spike_speed_y

        if status_moving_spike2 == "down":
            moving_spike2.y += moving_spike_speed_y

        if moving_spike2.x <= 300:
            correct_moving_spikes_motion(moving_spike2)

        moving_spike2.x -= moving_spike_speed_x
        moving_spike2.angle += moving_spike_turn_speed

        if moving_spike3.y < 100 and status_moving_spike3 == "up":
            status_moving_spike3 = "down"

        if moving_spike3.y > 400 and status_moving_spike3 == "down":
            status_moving_spike3 = "up"

        if status_moving_spike3 == "up":
            moving_spike3.y -= moving_spike_speed_y

        if status_moving_spike3 == "down":
            moving_spike3.y += moving_spike_speed_y

        if moving_spike3.x <= 300:
            correct_moving_spikes_motion(moving_spike3)

        moving_spike3.x -= moving_spike_speed_x
        moving_spike3.angle += moving_spike_turn_speed

        if moving_spike4.y < 100 and status_moving_spike4 == "up":
            status_moving_spike4 = "down"

        if moving_spike4.y > 400 and status_moving_spike4 == "down":
            status_moving_spike4 = "up"

        if status_moving_spike4 == "up":
            moving_spike4.y -= moving_spike_speed_y

        if status_moving_spike4 == "down":
            moving_spike4.y += moving_spike_speed_y

        if moving_spike4.x <= 300:
            correct_moving_spikes_motion(moving_spike4)

        moving_spike4.x -= moving_spike_speed_x
        moving_spike4.angle += moving_spike_turn_speed

        if moving_spike5.y < 100 and status_moving_spike5 == "up":
            status_moving_spike5 = "down"

        if moving_spike5.y > 400 and status_moving_spike5 == "down":
            status_moving_spike5 = "up"

        if status_moving_spike5 == "up":
            moving_spike5.y -= moving_spike_speed_y

        if status_moving_spike5 == "down":
            moving_spike5.y += moving_spike_speed_y

        if moving_spike5.x <= 300:
            correct_moving_spikes_motion(moving_spike5)

        moving_spike5.x -= moving_spike_speed_x
        moving_spike5.angle += moving_spike_turn_speed

        if moving_spike6.y < 100 and status_moving_spike6 == "up":
            status_moving_spike6 = "down"

        if moving_spike6.y > 400 and status_moving_spike6 == "down":
            status_moving_spike6 = "up"

        if status_moving_spike6 == "up":
            moving_spike6.y -= moving_spike_speed_y

        if status_moving_spike6 == "down":
            moving_spike6.y += moving_spike_speed_y

        if moving_spike6.x <= 300:
            correct_moving_spikes_motion(moving_spike6)

        moving_spike6.x -= moving_spike_speed_x
        moving_spike6.angle += moving_spike_turn_speed

        hero.angle -= hero_turn_speed

        if keyboard.left and hero.x > 30:
            hero_turn_speed = -7
            hero.x -= hero_speed

        if keyboard.right and hero.x < 970:
            hero_turn_speed = 7
            hero.x += hero_speed

        if keyboard.up and hero.y > 30:
            hero.y -= hero_speed

        if keyboard.down and hero.y < 470:
            hero.y += hero_speed

        if game_status == "play":
            change_music_form_time -= 1 / 60
            laser_guns_come_time -= 1 / 60

        if spike_wall1.x <= -80 and music_status == music_list[0]:
            clock.schedule(spike_wall_call, 1.5)

        if change_music_form_time <= 0 and change_music_form_bool:
            music_change_form()
            change_music_form_time = 18

        if laser_guns_come_time <= 0:
            if not laser_gun_stop and game_status != "pause":
                for laser_gun_item in laser_guns:
                    laser_gun_item.x -= 1

        if music_status == music_list[1]:
            moving_spike_speed_x = 5
            moving_spike_speed_y = 4
            bgs_speed = 5
            bg1.image = "bg2"
            bg2.image = "bg2(2)"

        if music_status == music_list[2]:
            moving_spike_speed_x = 3
            moving_spike_speed_y = 5
            bgs_speed = 4
            bg1.image = "bg3"
            bg2.image = "bg3"
            change_music_form_bool = False

        if music_status == music_list[2] and laser_gun_come_3:
            laser_guns_come_time = 24
            laser_gun_come_3 = False

        if (20 > laser_guns_come_time > 19) and not laser_gun_come_3:
            laser_guns[0].y = random.randint(140, 360)
            laser_guns[0].x = 1035
            laser_guns[0].angle = 90
            laser_shooting_time = 2
            laser_off_time = 2.7

        if (16 > laser_guns_come_time > 15) and not laser_gun_come_3:
            laser_guns[0].y = random.randint(140, 360)
            laser_guns[0].x = 1035
            laser_guns[0].angle = 90
            laser_shooting_time = 2
            laser_off_time = 2.7

        if (12 > laser_guns_come_time > 11) and not laser_gun_come_3:
            laser_guns[0].y = random.randint(140, 360)
            laser_guns[0].x = 1035
            laser_guns[0].angle = 90
            laser_shooting_time = 2
            laser_off_time = 2.7

        if (8 > laser_guns_come_time > 7) and not laser_gun_come_3:
            laser_guns[0].y = random.randint(140, 360)
            laser_guns[0].x = 1035
            laser_guns[0].angle = 90
            laser_shooting_time = 2
            laser_off_time = 2.7

        if (4 > laser_guns_come_time > 3) and not laser_gun_come_3:
            laser_guns[0].y = random.randint(140, 360)
            laser_guns[0].x = 1035
            laser_guns[0].angle = 90
            laser_shooting_time = 2
            laser_off_time = 2.7

        if music_status == music_list[2] and laser_guns[0].x <= 1035 and laser_gun_stop:
            if laser_guns[0].x > 965:
                laser_guns[0].x -= 1
            if laser_guns[0].x == 965:
                laser_off_time -= 1 / 60
                laser_shooting_time -= 1 / 60
                laser_gun_stop = True

        for laser_gun_item in laser_guns:
            if laser_gun_item.x == 965:
                laser_off_time -= 1 / 60
                laser_shooting_time -= 1 / 60
                laser_gun_stop = True

        if laser_shooting_time <= 0:
            laser_shooting()
            laser_shooting_time = 2000

        if laser_off_time <= 0:
            laser_off()
            laser_off_time = 2000

        if hero_status == "normal":
            if hero_hitbox.colliderect(moving_spike1) or hero_hitbox.colliderect(moving_spike2) or hero_hitbox.colliderect(moving_spike3) \
                    or hero_hitbox.colliderect(moving_spike4) or hero_hitbox.colliderect(moving_spike5) \
                    or hero_hitbox.colliderect(moving_spike6) or hero_hitbox.colliderect(spike_wall1) \
                    or hero_hitbox.collidelist(lasers) != -1 or hero_hitbox.y <= 100 or hero_hitbox.y >= 400:
                hero_status = "invincible"
                hero.image = "hero_damage"
                clock.schedule(image_change_normal, 2.5)

                show_health_image_num += 1
                show_health.image = health_image_list[show_health_image_num]
                if show_health_image_num == 7:
                    play_again_but.pos = WIDTH // 2, HEIGHT // 2
                    main_menu_but.pos = WIDTH // 2, HEIGHT // 2 + 108
                    game_status = "lose"

        if timer_in_screen == 0:
            game_status = "win"
            play_again_but.pos = WIDTH // 2, HEIGHT // 2
            main_menu_but.pos = WIDTH // 2, HEIGHT // 2 + 108
            music.stop()


def on_mouse_down(pos):
    global game_status
    if play_but.collidepoint(pos) and game_status == "starting_menu":
        play_but.image = "play_but2"

    if pause_but.collidepoint(pos) and play_again_but.pos != (WIDTH // 2, HEIGHT // 2):
        pause_but.image = "pause_button2"

    if resume_but.collidepoint(pos):
        resume_but.image = "resume_but2"

    if quit_but.collidepoint(pos):
        quit_but.image = "quit_but2"

    if how_to_play_but.collidepoint(pos):
        how_to_play_but.image = "how_to_play_but2"

    if help_game.collidepoint(pos):
        help_game.image = "help_game2"

    if play_again_but.collidepoint(pos):
        play_again_but.image = "play_again_but2"

    if main_menu_but.collidepoint(pos):
        main_menu_but.image = "main_menu_but2"


def on_mouse_up(pos):
    global game_status, help_screen_come_bool, bgs_speed, hero_speed, hero_turn_speed, moving_spike_speed_y, \
        moving_spike_speed_x, spike_wall_speed_y, spike_wall_speed_x, moving_spike_turn_speed, music_form, \
        show_health_image_num, change_music_form_time, laser_guns_come_time, laser_off_time, laser_shooting_time, \
        hero_status, status_moving_spike1, status_moving_spike2, status_moving_spike3, status_moving_spike4, \
        status_moving_spike5, status_moving_spike6, laser_gun_stop, laser_gun_back_bool, music_play, \
        change_music_form_bool, laser_gun_come_3, music_status, win_timer, timer_in_screen
    if play_but.collidepoint(pos) and game_status == "starting_menu":
        play_but.image = "play_but1"
        play_but.pos = 10000, 10000
        game_status = "play"

    if pause_but.collidepoint(pos) and play_again_but.pos != (WIDTH // 2, HEIGHT // 2):
        pause_but.image = "pause_button1"
        resume_but.pos = WIDTH // 2, HEIGHT // 2 - 108
        quit_but.pos = WIDTH // 2, HEIGHT // 2 + 108
        main_menu_but.pos = WIDTH // 2, HEIGHT // 2
        music.pause()
        game_status = "pause"

    if resume_but.collidepoint(pos):
        resume_but.image = "resume_but1"
        music.unpause()
        resume_but.pos = 10000, 10000
        main_menu_but.pos = 10000, 10000
        game_status = "play"

    if quit_but.collidepoint(pos):
        quit_but.image = "quit_but1"
        game_status = "quit"

    if how_to_play_but.collidepoint(pos):
        help_game.pos = WIDTH // 2, HEIGHT // 2
        clock.schedule(change_help_screen_come_bool, 0.1)
        play_but.pos = 10000, 10000
        quit_but.pos = 10000, 10000
        how_to_play_but.pos = 10000, 10000
        how_to_play_but.image = "how_to_play_but1"

    if help_game.collidepoint(pos) and help_screen_come_bool:
        help_game.pos = 10000, 10000
        play_but.pos = WIDTH // 2, HEIGHT // 2 - 50
        quit_but.pos = WIDTH // 2, HEIGHT // 2 + 162
        how_to_play_but.pos = WIDTH // 2, HEIGHT // 2 + 56
        help_screen_come_bool = False
        help_game.image = "help_game1"

    if play_again_but.collidepoint(pos):
        play_again_but.image = "play_again_but1"
        game_status = "play"
        bg1.pos = WIDTH // 2, HEIGHT // 2
        bg2.pos = WIDTH + WIDTH // 2, HEIGHT // 2
        hero.pos = 50, HEIGHT // 2
        hero_hitbox.pos = hero.pos
        show_health.pos = 900, 12.5
        moving_spike1.x = 957
        moving_spike2.x = 1157
        moving_spike3.x = 1357
        moving_spike4.x = 1457
        moving_spike5.x = 1557
        moving_spike6.x = 1757
        spike_wall1.x = 1141
        play_but.pos = WIDTH // 2, HEIGHT // 2 - 50
        quit_but.pos = WIDTH // 2, HEIGHT // 2 + 162
        how_to_play_but.pos = WIDTH // 2, HEIGHT // 2 + 56
        pause_but.pos = 10000, 10000
        resume_but.pos = 10000, 10000
        help_game.pos = 10000, 10000
        play_again_but.pos = 10000, 10000
        main_menu_but.pos = 10000, 10000

        bgs_speed = 4
        hero_speed = 4
        hero_turn_speed = 7
        moving_spike_speed_y = 3
        moving_spike_speed_x = 4
        spike_wall_speed_x = 5
        spike_wall_speed_y = 5
        moving_spike_turn_speed = 10
        music_form = 0
        show_health_image_num = -1
        change_music_form_time = 18
        laser_guns_come_time = 16
        laser_shooting_time = 2
        laser_off_time = 2.7
        win_timer = 64
        timer_in_screen = 0

        game_status = "play"
        hero_status = "normal"
        show_health.image = "health"
        hero.image = "hero"

        music.play("game_music")

        random_move_list = []
        for i in range(6):
            move_list = ["up", "down"]
            move = random.choice(move_list)
            random_move_list.append(move)

        status_moving_spike1 = random_move_list[0]
        status_moving_spike2 = random_move_list[1]
        status_moving_spike3 = random_move_list[2]
        status_moving_spike4 = random_move_list[3]
        status_moving_spike5 = random_move_list[4]
        status_moving_spike6 = random_move_list[5]

        laser_gun_stop = False
        laser_gun_back_bool = False
        music_play = True
        help_screen_come_bool = False
        laser_gun_come_3 = True
        change_music_form_bool = True

        spike_wall1.angle = 90

        bg1.image = "bg1"
        bg2.image = "bg1"

        music_status = music_list[music_form]

        laser_guns[0].x = 1035
        laser_guns[1].x = 1035
        laser_guns[2].x = 1035
        laser_guns[0].y = 125
        laser_guns[1].y = 250
        laser_guns[2].y = 375
        laser_guns[0].angle = 90
        laser_guns[1].angle = 90
        laser_guns[2].angle = 90
        lasers[0].x = 2 * WIDTH
        lasers[1].x = 2 * WIDTH
        lasers[2].x = 2 * WIDTH
        lasers[0].y = 125
        lasers[1].y = 250
        lasers[2].y = 375

    if main_menu_but.collidepoint(pos):
        main_menu_but.image = "main_menu_but1"
        bg1.pos = WIDTH // 2, HEIGHT // 2
        bg2.pos = WIDTH + WIDTH // 2, HEIGHT // 2
        hero.pos = 50, HEIGHT // 2
        hero_hitbox.pos = hero.pos
        show_health.pos = 900, 12.5
        moving_spike1.pos = 957, random.randint(101, 399)
        moving_spike2.pos = 1157, random.randint(101, 399)
        moving_spike3.pos = 1357, random.randint(101, 399)
        moving_spike4.pos = 1457, random.randint(101, 399)
        moving_spike5.pos = 1557, random.randint(101, 399)
        moving_spike6.pos = 1757, random.randint(101, 399)
        spike_wall1.pos = 1141, random.randint(150, 350)
        play_but.pos = WIDTH // 2, HEIGHT // 2 - 50
        quit_but.pos = WIDTH // 2, HEIGHT // 2 + 162
        how_to_play_but.pos = WIDTH // 2, HEIGHT // 2 + 56
        pause_but.pos = 10000, 10000
        resume_but.pos = 10000, 10000
        help_game.pos = 10000, 10000
        play_again_but.pos = 10000, 10000
        main_menu_but.pos = 10000, 10000

        bgs_speed = 4
        hero_speed = 4
        hero_turn_speed = 7
        moving_spike_speed_y = 3
        moving_spike_speed_x = 4
        spike_wall_speed_x = 5
        spike_wall_speed_y = 5
        moving_spike_turn_speed = 10
        music_form = 0
        show_health_image_num = -1
        change_music_form_time = 18
        laser_guns_come_time = 16
        laser_shooting_time = 2
        laser_off_time = 2.7
        win_timer = 64
        timer_in_screen = 0

        game_status = "starting_menu"
        hero_status = "normal"
        show_health.image = "health"
        hero.image = "hero"

        random_move_list = []
        for i in range(6):
            move_list = ["up", "down"]
            move = random.choice(move_list)
            random_move_list.append(move)

        status_moving_spike1 = random_move_list[0]
        status_moving_spike2 = random_move_list[1]
        status_moving_spike3 = random_move_list[2]
        status_moving_spike4 = random_move_list[3]
        status_moving_spike5 = random_move_list[4]
        status_moving_spike6 = random_move_list[5]

        laser_gun_stop = False
        laser_gun_back_bool = False
        music_play = True
        help_screen_come_bool = False
        laser_gun_come_3 = True
        change_music_form_bool = True

        spike_wall1.angle = 90

        bg1.image = "bg1"
        bg2.image = "bg1"

        music_status = music_list[music_form]

        laser_guns[0].x = 1035
        laser_guns[1].x = 1035
        laser_guns[2].x = 1035
        laser_guns[0].y = 125
        laser_guns[1].y = 250
        laser_guns[2].y = 375
        laser_guns[0].angle = 90
        laser_guns[1].angle = 90
        laser_guns[2].angle = 90
        lasers[0].x = 2 * WIDTH
        lasers[1].x = 2 * WIDTH
        lasers[2].x = 2 * WIDTH
        lasers[0].y = 125
        lasers[1].y = 250
        lasers[2].y = 375


pgzrun.go()
