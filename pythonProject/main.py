# Distint Howie
# CSC 308 - Python
# Project - Pygame
# 3/25/2023

# Libraries
import pygame
import os
import random

# Import Files
import button

pygame.font.init()
pygame.mixer.init()
pygame.init()
# pygame.video.init()


# Constant variables
# Width and height for a new window
WIDTH, HEIGHT = 1500, 800
MONSIZE = [pygame.display.Info().current_w , pygame.display.Info().current_h]
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
POW_WIDTH, POW_HEIGHT = 20, 20
pygame.display.set_caption("Main menu")  # name of window(wasn't sure what to name it)
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)  # seperate sides for each user

RED_IMMUNE = 0
YELLOW_IMMUNE = 0
ENEMY_IMMUNE = 0

# Power up type list
ENEMY_TYPES = ["small", "big1", "big2", "boss1", "boss2"]
POWER_UP_TYPES = ["TRI-LASER", "BEAM", "SPEED-UP", "SHIELD"]
MOVEMENT_FLAGS = []
HIT_FLAGS = []
yellow_power = ""  # current power up held by player
red_power = ""
yellow_pow_time = 0  # time left on power up
red_pow_time = 0

# Text displays
HEALTH_FONT = pygame.font.SysFont('comicsand', 40)
WINNER_FONT = pygame.font.SysFont('comicsand', 100)

# fullScreen= False
SINGLEPLAYER = False
# Colors
WHITE = (255, 255, 255)  # RBG values for white
BLACK = (0, 0, 0)  # RBG for black
RED = (255, 0, 0)  # RBG for red
YELLOW = (255, 255, 0)  # RBG for yellow
TXT_COLORS = (255, 255, 255)

FPS = 60  # frames per second
VEL = 4  # velocity of spacechips
POWER_VEL = 2  # power up fall speed
BULLET_VEL = 8  # velocity of the bullets
MAX_BULLETS = 5  # max allowable bullets on screen for each user

# unique event ids to check for bullet collison
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
YELLOW_BEAM_HIT = pygame.USEREVENT + 3
RED_BEAM_HIT = pygame.USEREVENT + 4
ENEMY_HIT = pygame.USEREVENT + 5
ENEMY_BEAM_HIT = pygame.USEREVENT + 6

# Load in assets used for the game
BACKROUND_MUSIC = pygame.mixer.Sound(os.path.join('Assets', 'cyber-war-126419.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
SHIELD_BLOCK_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'shield-block.mp3'))
BEAM_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'beam.mp3'))
PICKUP_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'pickup.mp3'))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,
                                                                  (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,
                                                               (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SMALL_ENEMY1_IMAGE = pygame.image.load(os.path.join('Assets', 'SMALL_ENEMY1_IMAGE.png'))
SMALL_ENEMY1_IMAGE = pygame.transform.rotate(pygame.transform.scale(SMALL_ENEMY1_IMAGE,
                                                                    (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

BIG_ENEMY1_IMAGE = pygame.image.load(os.path.join('Assets', 'big_eme1.png'))
BIG_ENEMY1_IMAGE = pygame.transform.rotate(pygame.transform.scale(BIG_ENEMY1_IMAGE,
                                                                  (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

BIG_ENEMY2_IMAGE = pygame.image.load(os.path.join('Assets', 'big_eme_2.png'))
BIG_ENEMY2_IMAGE = pygame.transform.rotate(pygame.transform.scale(BIG_ENEMY2_IMAGE,
                                                                  (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
BOSS1_IMAGE = pygame.image.load(os.path.join('Assets', 'boss1.png'))
BOSS1_IMAGE = pygame.transform.rotate(pygame.transform.scale(BOSS1_IMAGE,
                                                             (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
BOSS2_IMAGE = pygame.image.load(os.path.join('Assets', 'boss2.png'))
BOSS2_IMAGE = pygame.transform.rotate(pygame.transform.scale(BOSS2_IMAGE,
                                                             (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# power up assets
TRILASER_POW_IMAGE = pygame.image.load(os.path.join('Assets', 'tri-laser.png'))
TRILASER_POW_IMAGE = pygame.transform.scale(TRILASER_POW_IMAGE, (POW_WIDTH, POW_HEIGHT))
BEAM_POW_IMAGE = pygame.image.load(os.path.join('Assets', 'beam.png'))
BEAM_POW_IMAGE = pygame.transform.scale(BEAM_POW_IMAGE, (POW_WIDTH, POW_HEIGHT))
SPEED_UP_IMAGE = pygame.image.load(os.path.join('Assets', 'speed-up.png'))
SPEED_UP_IMAGE = pygame.transform.scale(SPEED_UP_IMAGE, (POW_WIDTH, POW_HEIGHT))
SHIELD_IMAGE = pygame.image.load(os.path.join('Assets', 'shield.png'))
SHIELD_IMAGE = pygame.transform.scale(SHIELD_IMAGE, (POW_WIDTH, POW_HEIGHT))

# get images
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))
SINGLE_PLAYER_IMG = pygame.image.load(os.path.join('Assets', 'singleplayer.png')).convert_alpha()
MULTIPLAYER_IMG = pygame.image.load(os.path.join('Assets', 'multiplayer.png')).convert_alpha()
EXIT_IMG = pygame.image.load(os.path.join('Assets', 'exit.png')).convert_alpha()

# create buttons
singlePlayerButton = button.Button(550, 135, SINGLE_PLAYER_IMG, .8)
multiplayerButton = button.Button(550, 250, MULTIPLAYER_IMG, .8)
exitButton = button.Button(550, 350, EXIT_IMG, .8)


def draw_main_menu():
    run = True
    selection = False
    while selection == False:
        BACKROUND_MUSIC.play(-1)
        while run:
            # draw backround

            WIN.blit(SPACE, (0, 0))
            # draw border
            pygame.draw.rect(WIN, BLACK, BORDER)

            # add buttons with handlers
            # go to single player
            if singlePlayerButton.draw(WIN):
                selection = True
                pygame.display.set_caption("SinglePlayer")
                singleplayer()

            # go to multiplayer
            if multiplayerButton.draw(WIN):
                selection = True
                pygame.display.set_caption("MulitPlayer")
                main()

            # exit the game
            if exitButton.draw(WIN):
                pygame.QUIT()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
            # upadate the display
            pygame.display.update()


def singleplayer():
    # draw_main_menu()
    # pygame.init()
    fullScreen = False
    # Starting position of spaceships
    red = pygame.Rect(1200, 310, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    # yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    fire_time = 0
    enemyTimer = 1
    enemy_ship = []
    enemy_ship_type = []
    enemy_health = []
    enemy_bullets = []
    HIGHSCORE = 0

    # keep track of bullets in list
    red_bullets = []
    yellow_bullets = []

    # keep track of power up locations
    yellow_power_ups = []  # falling power up rectangle
    red_power_ups = []
    yellow_pow_types = []  # falling power up type
    red_pow_types = []
    powerUpTimer = 0  # timer until next power up falls
    global red_power, yellow_power, red_pow_time, yellow_pow_time

    # other power up info
    yellow_beam_start = False  # trigger beam to fire
    red_beam_start = False
    yellow_beam_time = 60 * 0.75  # delay to fire beam
    red_beam_time = 60 * 0.75
    yellow_beams = []  # holds beam rectangle
    red_beams = []
    yellow_beam_whither = 0  # how long beam lasts for
    red_beam_whither = 0
    yellow_beam_warnings = []  # warning flash for beam
    red_beam_warnings = []

    # Starting health for users
    red_health = 10
    yellow_health = 10
    sHealth = 1
    bigHealth = 2
    bossHealth = 3
    global RED_IMMUNE, YELLOW_IMMUNE
    j = 0

    clock = pygame.time.Clock()  # FPS
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            # check to see if user closed the window
            if event.type == pygame.QUIT:
                # update run
                run = False
                pygame.quit()

            # fire bullets
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and red_power == "BEAM":
                    red_beam_start = True
                elif event.key == pygame.K_SPACE and (
                        len(red_bullets) < 15 or (red_power == "TRI-LASER" and len(red_bullets) < 3 * 15)):
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    if red_power == "TRI-LASER":  # create tri lasers if you have that power up
                        bullet = pygame.Rect(
                            red.x, red.y + 1, 10, 5)
                        red_bullets.append(bullet)
                        bullet = pygame.Rect(
                            red.x, red.y + red.height - 1, 10, 5)
                        red_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

            # lose health if bullets hit
            if event.type == RED_HIT:
                if red_power != "SHIELD":
                    red_health -= 1
                    BULLET_HIT_SOUND.play()
                else:
                    SHIELD_BLOCK_SOUND.play()

            if event.type == ENEMY_HIT:
                for i in range(len(enemy_health)):
                    if HIT_FLAGS[i] == True:
                        enemy_health[i] -= 1
                        BULLET_HIT_SOUND.play()
                        HIT_FLAGS[i] = False

            # lose health if beams hit
            if event.type == ENEMY_BEAM_HIT:
                for i in range(len(enemy_health)):
                    if HIT_FLAGS[i] == True:
                        enemy_health[i] -= 1
                        BULLET_HIT_SOUND.play()

        # decrement i frames
        if YELLOW_IMMUNE > 0:
            YELLOW_IMMUNE -= 1
        if RED_IMMUNE > 0:
            RED_IMMUNE -= 1

        # for resizing the screen

        pygame.display.update()

        high_score = ''
        if red_health <= 0:
            high_score = 'HIGHSCORE:' + str(HIGHSCORE)

        if high_score != "":
            draw_HighScore(high_score)

        # get keys pressed by users
        keys_pressed = pygame.key.get_pressed()
        # spawn a enemy
        enemyTimer += 1
        if enemyTimer >= ((60 * 5) // ((HIGHSCORE) / 1000 + 1)):
            # reset the timer
            enemyTimer = 0
            enemy_ship.append(pygame.Rect(random.randrange(0, BORDER.x - 40), 0, SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
            enemy_ship_type.append(ENEMY_TYPES[random.randrange(len(ENEMY_TYPES))])
            if enemy_ship_type[0 + j] == 'small':
                enemyTimer += 60 * 3  # spawn reduce spawn cooldown on smaller enemies
                enemy_health.append(sHealth)
            elif enemy_ship_type[0 + j] == 'big1' or enemy_ship_type[0 + j] == 'big2':
                enemyTimer += 60 * 1.5
                enemy_health.append(bigHealth)
            else:
                enemyTimer += 0
                enemy_health.append(bossHealth)
            j += 1
            MOVEMENT_FLAGS.append(True)
            HIT_FLAGS.append(False)

        # to make enemies fire
        fire_time += 1
        if len(enemy_ship) == 0:
            fire_time = 0
        if fire_time == 60 * 3 and (len(enemy_ship) > 0):
            for i in range(len(enemy_ship)):
                ene = enemy_ship[i]
                # regular enemies shoot normal lasers
                if enemy_ship_type[i] == 'small' or enemy_ship_type[i] == 'big1' or enemy_ship_type[i] == 'boss2':
                    bullet = pygame.Rect(ene.x, ene.y + ene.height // 2 - 2, 10, 5)
                    enemy_bullets.append(bullet)
                # boss 1 shoots tri-lasers
                elif enemy_ship_type[i] == 'boss1':
                    bullet = pygame.Rect(ene.x, ene.y + ene.height // 2 - 2, 10, 5)
                    enemy_bullets.append(bullet)
                    bullet = pygame.Rect(ene.x, ene.y + ene.height, 10, 5)
                    enemy_bullets.append(bullet)
                    bullet = pygame.Rect(ene.x, ene.y, 10, 5)
                    enemy_bullets.append(bullet)

                BULLET_FIRE_SOUND.play()
                fire_time = 0
        # boss 2 shoots minigun
        elif fire_time == 60 * 2 and (len(enemy_ship) > 0) and (
                'boss2' in enemy_ship_type or 'big2' in enemy_ship_type):
            for i in range(len(enemy_ship)):
                ene = enemy_ship[i]
                if enemy_ship_type[i] == 'boss2' or enemy_ship_type[
                    i] == 'big2':  # big2 shoots at a different time than normal wave
                    bullet = pygame.Rect(ene.x, ene.y + ene.height // 2 - 2, 10, 5)
                    enemy_bullets.append(bullet)
                BULLET_FIRE_SOUND.play()
        elif fire_time == 60 * 1 and (len(enemy_ship) > 0) and 'boss2' in enemy_ship_type:
            for i in range(len(enemy_ship)):
                ene = enemy_ship[i]
                if enemy_ship_type[i] == 'boss2':
                    bullet = pygame.Rect(ene.x, ene.y + ene.height // 2 - 2, 10, 5)
                    enemy_bullets.append(bullet)
                BULLET_FIRE_SOUND.play()

        # removing enemies from the screen and increasing the highscore
        for i in range(len(enemy_health)):
            if enemy_health[i] <= 0:
                if enemy_ship_type[i] == 'small':
                    HIGHSCORE += 5
                elif enemy_ship_type[i] == 'big1' or enemy_ship_type[i] == 'big2':
                    HIGHSCORE += 15
                else:
                    HIGHSCORE += 25
                enemy_health.pop(i)
                enemy_ship_type.pop(i)
                enemy_ship.pop(i)
                MOVEMENT_FLAGS.pop(i)
                HIT_FLAGS.pop(i)
                j -= 1
                break

        # powerups
        powerUpTimer += 1
        if powerUpTimer == 60 * 15:  # spawn powerup every 15 seconds
            red_power_ups.append(pygame.Rect(random.randrange(BORDER.x + BORDER.width, WIDTH - 20), 0, 20, 20))
            red_pow_types.append(POWER_UP_TYPES[random.randrange(len(POWER_UP_TYPES))])
            powerUpTimer = 0

        # lose power up after a set amount of time

        if red_pow_time > 0:
            red_pow_time -= 1
        else:
            red_power = ""

        # create beams
        if red_beam_start:
            red_beam_time -= 1
            if red_beam_time < 0:
                BEAM_SOUND.play()
                red_beam_warnings = []
                red_beams.append(pygame.Rect(0, red.y + red.height // 2 - 4, red.x, 7))
                red_beam_start = False
                red_beam_time = 60 * 0.75
                red_beam_whither = 60 * 0.25

        # create beam warning
        if red_beam_start and red_beam_time > 0:
            red_beam_warnings = []
            red_beam_warnings.append((red.x, red.y + red.height // 2 - 4))

        # linger time for beams
        if red_beam_whither > 0:
            red_beam_whither -= 1
            if red_beam_whither == 0:
                red_beams = []

        # Movement functions
        # yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        # Bullet movement and collison
        # handle_bullets(yellow_bullets, red_bullets, yellow, red , enemy_ship)
        handle_singleplayer_bullets(red_bullets, enemy_ship, red, enemy_bullets, enemy_health)

        # handle beam collision
        # handle_beams(yellow_beams, red_beams, yellow, red)
        handle_singleplayer_beams(red_beams, enemy_ship)

        # handle power ups
        # handle_power_ups(yellow_power_ups, red_power_ups, yellow_pow_types, red_pow_types, yellow, red)
        handle_singleplayer_powerups(red_power_ups, red_pow_types, red)

        handle_enemy_ships(enemy_ship, enemy_ship_type)

        # Create window with game elements
        draw_singlepayer(red, yellow_bullets, red_bullets, enemy_bullets, red_health, red_power_ups, red_pow_types,
                         red_beams, yellow_beam_warnings, red_beam_warnings, enemy_ship, enemy_ship_type)

    # rerun application after each game until user quits
    singleplayer()


def draw_singlepayer(red, yellow_bullets, red_bullets, enemy_bullets, red_health, red_power_ups, red_pow_types,
                     red_beams, yellow_beam_warnings, red_beam_warnings, ships, shiptypes):
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    # blit is how you update the screen with images/text
    # fill the screen with space image
    WIN.blit(SPACE, (0, 0))
    # draw border
    pygame.draw.rect(WIN, BLACK, BORDER)

    enemy_beam_start_flags = []

    # render text and display in set positions
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    # render in spaceship to screen

    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # draw bullets for both spaceships
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bullet in enemy_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for beamWarning in red_beam_warnings:
        pygame.draw.circle(WIN, RED, beamWarning, 7)
        pygame.draw.circle(WIN, WHITE, beamWarning, 6)

    for beam in red_beams:
        pygame.draw.rect(WIN, RED, beam)
        innerBeam = pygame.Rect(beam.x, beam.y + 1, beam.width, 5)
        pygame.draw.rect(WIN, WHITE, innerBeam)

    if red_power == "SHIELD":
        R, B, G = RED
        transRED = (R, B, G, 100)
        pygame.draw.circle(surface, transRED, (red.x + red.width // 2, red.y + red.height // 2 + 4), 33)
    WIN.blit(surface, (0, 0))

    for i in range(len(red_power_ups)):
        powerUp = red_power_ups[i]
        pygame.draw.rect(WIN, RED, powerUp)
        if red_pow_types[i] == "TRI-LASER":
            WIN.blit(TRILASER_POW_IMAGE, (powerUp.x, powerUp.y))
        elif red_pow_types[i] == "BEAM":
            WIN.blit(BEAM_POW_IMAGE, (powerUp.x, powerUp.y))
        elif red_pow_types[i] == "SPEED-UP":
            WIN.blit(SPEED_UP_IMAGE, (powerUp.x, powerUp.y))
        elif red_pow_types[i] == "SHIELD":
            WIN.blit(SHIELD_IMAGE, (powerUp.x, powerUp.y))
        # to draw approaite ship tp the screen
    for i in range(len(ships)):
        ship = ships[i]
        if shiptypes[i] == "small":
            WIN.blit(SMALL_ENEMY1_IMAGE, (ship.x, ship.y))
        elif shiptypes[i] == "big1":
            WIN.blit(BIG_ENEMY1_IMAGE, (ship.x, ship.y))
        elif shiptypes[i] == "big2":
            WIN.blit(BIG_ENEMY2_IMAGE, (ship.x, ship.y))
        elif shiptypes[i] == "boss1":
            WIN.blit(BOSS1_IMAGE, (ship.x, ship.y))
        elif shiptypes[i] == "boss2":
            WIN.blit(BOSS2_IMAGE, (ship.x, ship.y))

    # update display
    pygame.display.update()


def handle_singleplayer_bullets(red_bullets, ship, red, e_bullet, health):
    # for hitting enemy ships in singleplayer
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        for i in range(len(ship)):
            if ship[i].colliderect(bullet):
                pygame.event.post(pygame.event.Event(ENEMY_HIT))
                if bullet in red_bullets:
                    red_bullets.remove(bullet)
                HIT_FLAGS[i] = True
                BULLET_HIT_SOUND.play()
            # going of screen
        if bullet.x < 0:
            red_bullets.remove(bullet)

    # for the enemies hitting the  red ship
    for bullet in e_bullet:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            e_bullet.remove(bullet)
            # going off screen
        if bullet.x > WIDTH:
            e_bullet.remove(bullet)


def handle_singleplayer_powerups(red_power_ups, red_pow_types, red):
    global red_power, red_pow_time
    for i in range(len(red_power_ups)):
        powerup = red_power_ups[i]
        powerup.y += POWER_VEL  # move powerup down
        if red.colliderect(powerup):
            red_power_ups.remove(powerup)  # player picked up a power up
            red_power = red_pow_types[i]
            red_pow_types.pop(i)
            red_pow_time = 10 * 60
            if red_power == "SHIELD":
                red_pow_time = red_pow_time / 2
            PICKUP_SOUND.play()
        elif powerup.y > HEIGHT:
            red_power_ups.remove(powerup)  # powerup off screen
            red_pow_types.pop(i)


def handle_singleplayer_beams(red_beams, eme):
    for beam in red_beams:
        for i in range(len(eme)):
            if eme[i].colliderect(beam):
                pygame.event.post(pygame.event.Event(ENEMY_BEAM_HIT))
                HIT_FLAGS[i] = True


def draw_HighScore(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()  # update display to show text
    pygame.time.delay(5000)  # 5sec delay
    exit()


############## MULTIPLAYER


def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health, yellow_power_ups, red_power_ups,
                yellow_pow_types, red_pow_types,
                yellow_beams, red_beams, yellow_beam_warnings, red_beam_warnings):
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    # blit is how you update the screen with images/text
    # fill the screen with space image
    WIN.blit(SPACE, (0, 0))
    # draw border
    pygame.draw.rect(WIN, BLACK, BORDER)

    # render text and display in set positions
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)

    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    # WIN.blit(yellow_health_text, (10,10))

    # render in spaceships to screen

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    # WIN.blit(SMALL_ENEMY1_IMAGE,)

    # draw bullets for both spaceships
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # draw beam warnings
    for beamWarning in yellow_beam_warnings:
        pygame.draw.circle(WIN, YELLOW, beamWarning, 7)
        pygame.draw.circle(WIN, WHITE, beamWarning, 6)
    for beamWarning in red_beam_warnings:
        pygame.draw.circle(WIN, RED, beamWarning, 7)
        pygame.draw.circle(WIN, WHITE, beamWarning, 6)

    # draw beams
    for beam in yellow_beams:
        pygame.draw.rect(WIN, YELLOW, beam)
        innerBeam = pygame.Rect(beam.x, beam.y + 1, beam.width, 5)
        pygame.draw.rect(WIN, WHITE, innerBeam)

    for beam in red_beams:
        pygame.draw.rect(WIN, RED, beam)
        innerBeam = pygame.Rect(beam.x, beam.y + 1, beam.width, 5)
        pygame.draw.rect(WIN, WHITE, innerBeam)

    # draw shields
    if yellow_power == "SHIELD":
        # points = ((yellow.x + yellow.width//2, yellow.y + yellow.height//2), (yellow.x + yellow.width + yellow.height
        R, B, G = YELLOW
        transYELLOW = (R, B, G, 100)
        pygame.draw.circle(surface, transYELLOW, (yellow.x + yellow.width // 2, yellow.y + yellow.height // 2 + 4), 33)
    if red_power == "SHIELD":
        R, B, G = RED
        transRED = (R, B, G, 100)
        pygame.draw.circle(surface, transRED, (red.x + red.width // 2, red.y + red.height // 2 + 4), 33)
    WIN.blit(surface, (0, 0))

    # draw power ups
    for i in range(len(yellow_power_ups)):
        powerUp = yellow_power_ups[i]
        pygame.draw.rect(WIN, YELLOW, powerUp)
        if yellow_pow_types[i] == "TRI-LASER":
            WIN.blit(TRILASER_POW_IMAGE, (powerUp.x, powerUp.y))
        elif yellow_pow_types[i] == "BEAM":
            WIN.blit(BEAM_POW_IMAGE, (powerUp.x, powerUp.y))
        elif yellow_pow_types[i] == "SPEED-UP":
            WIN.blit(SPEED_UP_IMAGE, (powerUp.x, powerUp.y))
        elif yellow_pow_types[i] == "SHIELD":
            WIN.blit(SHIELD_IMAGE, (powerUp.x, powerUp.y))

    for i in range(len(red_power_ups)):
        powerUp = red_power_ups[i]
        pygame.draw.rect(WIN, RED, powerUp)
        if red_pow_types[i] == "TRI-LASER":
            WIN.blit(TRILASER_POW_IMAGE, (powerUp.x, powerUp.y))
        elif red_pow_types[i] == "BEAM":
            WIN.blit(BEAM_POW_IMAGE, (powerUp.x, powerUp.y))
        elif red_pow_types[i] == "SPEED-UP":
            WIN.blit(SPEED_UP_IMAGE, (powerUp.x, powerUp.y))
        elif red_pow_types[i] == "SHIELD":
            WIN.blit(SHIELD_IMAGE, (powerUp.x, powerUp.y))

    # update display
    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    # handle keys being pressed and off screen
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # if left player, left key is being pressed
        yellow.x -= VEL
        if yellow_power == "SPEED-UP":
            yellow.x -= VEL // 2
    if keys_pressed[
        pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # if left player, right key is being pressed
        yellow.x += VEL
        if yellow_power == "SPEED-UP":
            yellow.x += VEL // 2
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # if left player, up key is being pressed
        yellow.y -= VEL
        if yellow_power == "SPEED-UP":
            yellow.y -= VEL // 2
    if keys_pressed[
        pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 10:  # if left player, down key is being pressed
        yellow.y += VEL
        if yellow_power == "SPEED-UP":
            yellow.y += VEL // 2


def red_handle_movement(keys_pressed, red):
    # handle keys being pressed and off screen
    if keys_pressed[
        pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # if right player, left key is being pressed
        red.x -= VEL
        if red_power == "SPEED-UP":
            red.x -= VEL // 2
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # if right player, right key is being pressed
        red.x += VEL
        if red_power == "SPEED-UP":
            red.x += VEL // 2
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # if right player, up key is being pressed
        red.y -= VEL
        if red_power == "SPEED-UP":
            red.y -= VEL // 2
    if keys_pressed[
        pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 10:  # if right player, down key is being pressed
        red.y += VEL
        if red_power == "SPEED-UP":
            red.y += VEL // 2


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL  # move bullets on screen for yellow player
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))  # event if red player was hit
            yellow_bullets.remove(bullet)  # remove bullet
        elif bullet.x > WIDTH:  # else check if it hit the end of window
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL  # move bullets on screen for red player
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))  # event if red player was hit
            red_bullets.remove(bullet)  # remove bullet
        elif bullet.x < 0:  # else check if it hit the end of window
            red_bullets.remove(bullet)


# detects if beam hit a ship
def handle_beams(yellow_beams, red_beams, yellow, red):
    for beam in yellow_beams:
        if red.colliderect(beam):
            pygame.event.post(pygame.event.Event(RED_BEAM_HIT))
    for beam in red_beams:
        if yellow.colliderect(beam):
            pygame.event.post(pygame.event.Event(YELLOW_BEAM_HIT))


def handle_power_ups(yellow_power_ups, red_power_ups, yellow_pow_types, red_pow_types, yellow, red):
    global yellow_power, red_power, red_pow_time, yellow_pow_time

    for i in range(len(yellow_power_ups)):
        powerup = yellow_power_ups[i]
        powerup.y += POWER_VEL  # move powerup down
        if yellow.colliderect(powerup):
            yellow_power_ups.remove(powerup)  # player picked up a power up
            yellow_power = yellow_pow_types[i]
            yellow_pow_types.pop(i)
            yellow_pow_time = 10 * 60
            if yellow_power == "SHIELD":
                yellow_pow_time = yellow_pow_time / 2
            PICKUP_SOUND.play()
        elif powerup.y > HEIGHT:
            yellow_power_ups.remove(powerup)  # powerup off screen
            yellow_pow_types.pop(i)

    for i in range(len(red_power_ups)):
        powerup = red_power_ups[i]
        powerup.y += POWER_VEL  # move powerup down
        if red.colliderect(powerup):
            red_power_ups.remove(powerup)  # player picked up a power up
            red_power = red_pow_types[i]
            red_pow_types.pop(i)
            red_pow_time = 10 * 60
            if red_power == "SHIELD":
                red_pow_time = red_pow_time / 2
            PICKUP_SOUND.play()
        elif powerup.y > HEIGHT:
            red_power_ups.remove(powerup)  # powerup off screen
            red_pow_types.pop(i)


def handle_enemy_ships(enemy_ship, enemy_ship_type):
    for i in range(len(enemy_ship)):
        ene = enemy_ship[i]
        if MOVEMENT_FLAGS[i]:
            ene.y += 2
        if ene.y > HEIGHT - 50:
            MOVEMENT_FLAGS[i] = False

        if not MOVEMENT_FLAGS[i]:
            ene.y -= 2
            if ene.y < 0:
                MOVEMENT_FLAGS[i] = True


def draw_winner(text):
    # Winning message
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()  # update display to show text
    pygame.time.delay(5000)  # 5sec delay


def main():
    # draw_main_menu()
    # pygame.init()
    fullScreen = False
    # Starting position of spaceships
    red = pygame.Rect(1200, 310, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # keep track of bullets in list
    red_bullets = []
    yellow_bullets = []

    # keep track of power up locations
    yellow_power_ups = []  # falling power up rectangle
    red_power_ups = []
    yellow_pow_types = []  # falling power up type
    red_pow_types = []
    powerUpTimer = 0  # timer until next power up falls
    global red_power, yellow_power, red_pow_time, yellow_pow_time

    # other power up info
    yellow_beam_start = False  # trigger beam to fire
    red_beam_start = False
    yellow_beam_time = 60 * 0.75  # delay to fire beam
    red_beam_time = 60 * 0.75
    yellow_beams = []  # holds beam rectangle
    red_beams = []
    yellow_beam_whither = 0  # how long beam lasts for
    red_beam_whither = 0
    yellow_beam_warnings = []  # warning flash for beam
    red_beam_warnings = []

    # Starting health for users
    red_health = 10
    yellow_health = 10
    global RED_IMMUNE, YELLOW_IMMUNE

    clock = pygame.time.Clock()  # FPS
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            # check to see if user closed the window
            if event.type == pygame.QUIT:
                # update run
                run = False
                pygame.quit()

            # fire bullets
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and yellow_power == "BEAM":
                    yellow_beam_start = True
                elif event.key == pygame.K_SPACE and (len(yellow_bullets) < MAX_BULLETS or (
                        yellow_power == "TRI-LASER" and len(yellow_bullets) < 3 * MAX_BULLETS)):
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    if yellow_power == "TRI-LASER":  # create tri lasers if you have that power up
                        bullet = pygame.Rect(
                            yellow.x + yellow.width, yellow.y + 1, 10, 5)
                        yellow_bullets.append(bullet)
                        bullet = pygame.Rect(
                            yellow.x + yellow.width, yellow.y + yellow.height - 1, 10, 5)
                        yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and red_power == "BEAM":
                    red_beam_start = True
                elif event.key == pygame.K_RSHIFT and (len(red_bullets) < MAX_BULLETS or (
                        red_power == "TRI-LASER" and len(red_bullets) < 3 * MAX_BULLETS)):
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    if red_power == "TRI-LASER":  # create tri lasers if you have that power up
                        bullet = pygame.Rect(
                            red.x, red.y + 1, 10, 5)
                        red_bullets.append(bullet)
                        bullet = pygame.Rect(
                            red.x, red.y + red.height - 1, 10, 5)
                        red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # lose health if beam hits
            if event.type == RED_BEAM_HIT and red_power != "SHIELD":
                if RED_IMMUNE <= 0:
                    RED_IMMUNE = 60 * 0.1
                    if red_power != "SHIELD":
                        red_health -= 1
                        BULLET_HIT_SOUND.play()
                    else:
                        SHIELD_BLOCK_SOUND.play()

            if event.type == YELLOW_BEAM_HIT and yellow_power != "SHIELD":
                if YELLOW_IMMUNE <= 0:
                    YELLOW_IMMUNE = 60 * 0.1
                    if yellow_power != "SHIELD":
                        yellow_health -= 1
                        BULLET_HIT_SOUND.play()
                    else:
                        SHIELD_BLOCK_SOUND.play()

            # lose health if bullets hit
            if event.type == YELLOW_HIT and yellow_power != "SHIELD":
                if yellow_power != "SHIELD":
                    yellow_health -= 1
                    BULLET_HIT_SOUND.play()
                else:
                    SHIELD_BLOCK_SOUND.play()
            if event.type == RED_HIT:
                if red_power != "SHIELD":
                    red_health -= 1
                    BULLET_HIT_SOUND.play()
                else:
                    SHIELD_BLOCK_SOUND.play()

            # decrement i frames
            if YELLOW_IMMUNE > 0:
                YELLOW_IMMUNE -= 1
            if RED_IMMUNE > 0:
                RED_IMMUNE -= 1

            # for resizing the screen
            if event.type == pygame.VIDEORESIZE:
                if not fullScreen:
                    WIN = pygame.display.set_mode((event.w, event.h),
                                                  pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
                    WIN.blit(pygame.transform.scale(SPACE, event.dict['size']), (0, 0))
                    pygame.display.update()
            if event.type == pygame.K_f:
                fullScreen = not fullScreen
                if fullScreen:
                    WIN = pygame.display.set_mode((MONSIZE), pygame.FULLSCREEN)
                else:
                    WIN = pygame.display.set_mode((WIN.get_width(), WIN.get_height()), pygame.RESIZABLE)
        pygame.display.update()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        # get keys pressed by users
        keys_pressed = pygame.key.get_pressed()

        # powerups
        powerUpTimer += 1
        if powerUpTimer == 60 * 15:  # spawn powerup every 15 seconds
            yellow_power_ups.append(pygame.Rect(random.randrange(0, BORDER.x - 20), 0, 20, 20))
            red_power_ups.append(pygame.Rect(random.randrange(BORDER.x + BORDER.width, WIDTH - 20), 0, 20, 20))

            yellow_pow_types.append(POWER_UP_TYPES[random.randrange(len(POWER_UP_TYPES))])
            red_pow_types.append(POWER_UP_TYPES[random.randrange(len(POWER_UP_TYPES))])

            powerUpTimer = 0

        # lose power up after a set amount of time
        if yellow_pow_time > 0:
            yellow_pow_time -= 1
        else:
            yellow_power = ""

        if red_pow_time > 0:
            red_pow_time -= 1
        else:
            red_power = ""

        # create beams
        if yellow_beam_start:
            yellow_beam_time -= 1
            if yellow_beam_time < 0:
                BEAM_SOUND.play()
                yellow_beam_warnings = []
                yellow_beams.append(
                    pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 4, WIDTH - yellow.x, 7))
                yellow_beam_start = False
                yellow_beam_time = 60 * 0.75
                yellow_beam_whither = 60 * 0.25
        if red_beam_start:
            red_beam_time -= 1
            if red_beam_time < 0:
                BEAM_SOUND.play()
                red_beam_warnings = []
                red_beams.append(pygame.Rect(0, red.y + red.height // 2 - 4, red.x, 7))
                red_beam_start = False
                red_beam_time = 60 * 0.75
                red_beam_whither = 60 * 0.25

        # create beam warning
        if yellow_beam_start and yellow_beam_time > 0:
            yellow_beam_warnings = []
            yellow_beam_warnings.append((yellow.x + yellow.width, yellow.y + yellow.height // 2 - 4))
        if red_beam_start and red_beam_time > 0:
            red_beam_warnings = []
            red_beam_warnings.append((red.x, red.y + red.height // 2 - 4))

        # linger time for beams
        if yellow_beam_whither > 0:
            yellow_beam_whither -= 1
            if yellow_beam_whither == 0:
                yellow_beams = []
        if red_beam_whither > 0:
            red_beam_whither -= 1
            if red_beam_whither == 0:
                red_beams = []

        # Movement functions
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        # Bullet movement and collison
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # handle beam collision
        handle_beams(yellow_beams, red_beams, yellow, red)

        # handle power ups
        handle_power_ups(yellow_power_ups, red_power_ups, yellow_pow_types, red_pow_types, yellow, red)

        # Create window with game elements
        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health, yellow_power_ups,
                    red_power_ups, yellow_pow_types, red_pow_types,
                    yellow_beams, red_beams, yellow_beam_warnings, red_beam_warnings)

    # rerun application after each game until user quits
    main()


draw_main_menu()

