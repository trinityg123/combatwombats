# Imports
import pygame
pygame.init()
pygame.mixer.init()

import os
import random
from assets import *
from sprites import Cannon, Alien
from scenery import Ground, Mountains, Stars
from xbox360_controller import XBox360Controller

# Initialize game engine
pygame.init()

# Set window position
os.environ['SDL_VIDEO_WINDOW_POS'] = "15, 30:"

# Window settings
WIDTH = 1000
HEIGHT = 660
TITLE = "Combat Wombats"

# Make window
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)

# Make a Controller
controller = XBox360Controller(0)

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Data
score_file = "data/high_score.txt"

# Stages
START = 0
PLAYING = 1
PAUSED = 2
DELAY = 3
GAME_OVER = 4

delay_ticks = 45

# Settings
cannon_speed = 4
bullet_speed = 6
bomb_speed = 3
drop_amount = 12

initial_shot_limit = 5
initial_alien_speed = 2
initial_bomb_rate = 5

sound_on = True
default_high_score = 2000



def read_high_score():
    if os.path.exists(score_file):
        with open(score_file, 'r') as f:
            return max([int(f.read().strip()), default_high_score])
    else:
        return default_high_score

def save_high_score(score):
    if not os.path.exists('data'):
        os.mkdir('data')

    with open((score_file), 'w') as f:
        f.write(str(score))

def update_high_score():
    if not os.path.exists('data'):
        os.mkdir('data')

    with open((score_file), 'w') as f:
        f.write(str(high_score))

def restart():
    global cannon, alien_speed, bomb_rate, shot_limit, score, level, stage

    cannon = Cannon(480, 480)
    alien_speed = initial_alien_speed
    bomb_rate = initial_bomb_rate
    shot_limit = initial_shot_limit

    score = 0
    level = 1
    stage = START

def setup():
    global aliens, bombs, bullets, stage, ticks

    a1 = Alien(200, 50, alien_speed)
    a2 = Alien(400, 50, alien_speed)
    a3 = Alien(600, 50, alien_speed)
    a4 = Alien(800, 50, alien_speed)
    a5 = Alien(300, 90, alien_speed)
    a6 = Alien(500, 90, alien_speed)
    a7 = Alien(700, 90, alien_speed)
    a8 = Alien(200, 120, alien_speed)
    a9 = Alien(400, 120, alien_speed)
    a10 = Alien(600, 120, alien_speed)
    a11 = Alien(800, 120, alien_speed)
    aliens = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11]
    
    bombs = []
    bullets = []

    ticks = delay_ticks
    stage = DELAY

def advance():
    global level, alien_speed, bomb_rate

    level += 1
    alien_speed += 0.5
    bomb_rate += 1

    setup()

def end_game(win):
    global stage

    stage = GAME_OVER
    display_end_screen(screen, win)

def display_start_screen():
    screen.blit(startscreen_img, [0,0]) 
    
    title_text = FONT_XL.render(TITLE, True, WHITE)
    sample_text = FONT_SM.render("Press Space to Play", True, WHITE)
    high_score_text = FONT_SM.render("Current High Score:", True, WHITE)
    the_high_score = FONT_SM.render(str(high_score), True, WHITE)

    screen.blit(title_text, [WIDTH // 2 - title_text.get_rect().width // 2 , 700])
    screen.blit(sample_text, [WIDTH // 2 - sample_text.get_rect().width // 2 , 500])
    screen.blit(high_score_text, [WIDTH // 2 - high_score_text.get_rect().width // 2 , 550])
    screen.blit(the_high_score, [WIDTH //2 - the_high_score.get_rect().width // 2, 600])

def display_pause_screen(screen):
    screen.blit(pause_img, [0, 0])

def display_end_screen(screen, win):
    if win == True:
        screen.blit(wonendscreen_img, [0,0])
    else:
        screen.blit(loseendscreen_img, [0,0])

def display_stats(screen, score, level, high_score, shield):
    score_text = FONT_SM.render(("Score: " + str(score)), True, WHITE)
    screen.blit(score_text, [WIDTH // 2.5 - score_text.get_rect().width// 2, 5])

    high_score_text =  FONT_SM.render(("High Score: " + str(high_score)), True, WHITE)
    screen.blit(high_score_text, [WIDTH // 13 - score_text.get_rect().width// 2, 5])

    level_text = FONT_SM.render(("Level: " + str(level)), True, WHITE)
    screen.blit(level_text, [WIDTH -350 - level_text.get_rect().width, 5])

    shield_text = FONT_SM.render(("Shield: "), True, WHITE)
    screen.blit(shield_text, [WIDTH -150 - shield_text.get_rect().width, 5])
    screen.blit(shield_img, [825, 10])
    pygame.draw.rect(screen, GREY, [(825 + shield), 12, (100 - shield), 28])
    pygame.draw.rect(screen, GREY, [925, 20, 5, 10])
    pygame.draw.rect(screen, GREY, [825, 10, 100, 30], 5)
    

def toggle_sound(can_mute):
    if pygame.mixer.get_busy() and can_mute == True:
        pygame.mixer.pause()
        print("muted")
    elif can_mute == False:
        pygame.mixer.unpause()
        print("unmuted")

# hide mouse cursor over screen
pygame.mouse.set_visible(0)

# Make scenery objects
ground = Ground(0, 560, 1000, 500)
mountains = Mountains(0, 480, 1000, 80, 9)
stars = Stars(0, 0, 1000, 560, 125)

# Get high score
high_score = read_high_score()

# Game loop
done = False
can_shoot = True
can_mute = True
can_flip_sound = True
cheatMode = False
cheatCheck = True
restart()
pygame.mixer.Sound.play(THEME)

while not done:
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # joystick stuff
    back = controller.back()
    start = controller.start()
    lt_stick = controller.left_stick_axes()
    aButton = controller.a()
    back = controller.back()
    dPad = controller.hat()
    lb = controller.left_bumper()
    rb = controller.right_bumper()



    # game logic
    if stage == START:
        if start == 1:
            stage = PLAYING
            setup()
    else:
        if dPad[0] == 1:
            stage = PAUSED

    if PLAYING:
        cannon.move(int(lt_stick[0] * 10))
        if not cheatMode:
            if aButton > 0 and len(bullets) < shot_limit and can_shoot == True:
                cannon.shoot(bullets, -bullet_speed)
                can_shoot = False
            elif aButton == 0:
                can_shoot = True
        if cheatMode:
            if aButton > 0:
                cannon.shoot(bullets, -bullet_speed)
            
        if back and can_flip_sound:
            toggle_sound(can_mute)
            can_flip_sound = False
            can_mute = not can_mute
            
        elif not back:
            can_flip_sound = True
        if cheatCheck:
            if lb == 1 and rb == 1:
                cheatMode = True
                cheatCheck = False
                print("cheat mode activated")
       
        
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = DELAY

            elif stage == PLAYING:
                if event.key == pygame.K_SPACE and len(bullets) < shot_limit:
                    cannon.shoot(bullets, -bullet_speed)
                    score -= 1

                elif event.key == pygame.K_p:
                    stage = PAUSED

            elif stage == PAUSED:
                if event.key == pygame.K_p:
                    stage = PLAYING

            elif stage == GAME_OVER:
                if event.key == pygame.K_r:
                    reset()

    if stage == PLAYING:
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT]:
            cannon.move(cannon_speed)
        elif key[pygame.K_LEFT]:
            cannon.move(-cannon_speed)
        elif key[pygame.K_s]:
            toggle_sound(can_mute)


    # Game logic
    if stage == DELAY:
        if delay_ticks > 0:
            delay_ticks -= 1
        else:
            stage = PLAYING

    if stage == PAUSED:
        display_pause_screen(screen)
        pygame.mixer.pause()
        if start == 1:
            stage = PLAYING
            pygame.mixer.unpause()

    if stage == PLAYING:
        # process scenery
        stars.update()
        
        # process cannon
        cannon.update()

        # process enemies
        fleet_hits_edge = False

        for a in aliens:
            a.update()

            r = random.randint(0, 1000)
            if r < bomb_rate:
                a.drop_bomb(bombs, bomb_speed)

            if a.x <= 0 or a.x + a.w >= WIDTH:
                fleet_hits_edge = True

        if fleet_hits_edge:
            for a in aliens:
                a.reverse_and_drop(drop_amount)

        # process bombs
        for b in bombs:
            b.update(ground)

            if b.intersects(cannon):
                b.kill()
                cannon.apply_damage(20)
                pygame.mixer.Sound.play(HIT)
            elif b.intersects(ground):
                b.kill()

        # process bullets
        for b in bullets:
            b.update()

            for a in aliens:
                if b.intersects(a):
                    b.kill()
                    a.kill()
                    score += a.value
                    pygame.mixer.Sound.play(HIT)


        # update score
        for a in aliens:
            if not a.alive:
                score += a.value

        # check game status
        if cannon.alive == False:
            end_game(False)
        elif len(aliens) == 0:
            advance()
        elif level > 10:
            end_game(True)
        for a in aliens:
            if a.intersects(ground):
                end_game(False)

        if score > high_score:
            high_score = score

    if stage == GAME_OVER:
        if score > high_score:
            high_score == score
            update_high_score()
            save_high_score(score)
            print(score)
        if start == 1:
            restart()


   # Drawing code
    screen.blit(background_img, [0,0])

    if stage == START:
        display_start_screen()

    elif stage in [PLAYING, PAUSED, DELAY, GAME_OVER]:
        stars.draw(screen)
        mountains.draw(screen)
        ground.draw(screen)

        cannon.draw(screen)

        for a in aliens:
            a.draw(screen)

        for b in bullets:
            b.draw(screen)

        for b in bombs:
            b.draw(screen)

        if stage == PAUSED:
            display_pause_screen(screen)
        if stage == GAME_OVER:
            if level > 10:
                display_end_screen(screen, True)
            else:
                display_end_screen(screen, False)

        display_stats(screen, score, level, high_score, cannon.shield)


    # Update screen
    pygame.display.flip()
    clock.tick(refresh_rate)


    # Remove killed objects
    if stage != START:
        aliens = [a for a in aliens if a.alive]
        bullets = [b for b in bullets if b.alive]
        bombs = [b for b in bombs if b.alive]


# Close window on quit
pygame.mixer.quit()
pygame.quit()
