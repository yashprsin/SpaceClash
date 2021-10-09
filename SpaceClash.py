import pygame
import math
import random
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Clash")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
Player_image = pygame.image.load("space-invaders.png")
Player_x = 370
Player_y = 480
Player_x_change = 0

# Enemy
Enemy_image = []
Enemy_x = []
Enemy_y = []
Enemy_x_change = []
Enemy_y_change = []
n_of_enemies = 6

for i in range(n_of_enemies):
    Enemy_image.append(pygame.image.load("alien.png"))
    Enemy_x.append(random.randint(0, 735))
    Enemy_y.append(random.randint(30, 160))
    Enemy_x_change.append(4)
    Enemy_y_change.append(40)

# Bullet

# Ready - you can't see the bullet on the screen
# Fire - The bullet is currently moving
Bullet_image = pygame.image.load("bullet.png")
Bullet_x = 0
Bullet_y = 480
Bullet_x_change = 0
Bullet_y_change = 10
Bullet_State = "ready"

# Font
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

Text_x = 10
Text_y = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(Player_image, (x, y))


def enemy(x, y, i):
    screen.blit(Enemy_image[i], (x, y))


def fire_bullet(x, y):
    global Bullet_State
    Bullet_State = "fire"
    screen.blit(Bullet_image, (x + 16, y + 10))


def isCollison(Enemy_x, Enemy_y, Bullet_x, Bullet_y):
    distance = math.sqrt((math.pow(Enemy_x - Bullet_x, 2)) + (math.pow(Enemy_y - Bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB - red, green, blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right and left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Player_x_change = - 5
            if event.key == pygame.K_RIGHT:
                Player_x_change = 5
            if event.key == pygame.K_SPACE:
                if Bullet_State == "ready":
                    Bullet_sound = mixer.Sound('laser.wav')
                    Bullet_sound.play()
                    # Get the current x coordinate of the spaceship
                    Bullet_x = Player_x
                    fire_bullet(Player_x, Player_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                Player_x_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    # checking for the boundaries of spaceship so it doesn't go out of bounds
    Player_x += Player_x_change

    if Player_x <= 0:
        Player_x = 0
    elif Player_x >= 736:
        Player_x = 736
    Player_x += Player_x_change

    # Enemy Movement
    for i in range(n_of_enemies):

        # Game Over
        if Enemy_y[i] > 440:
            for j in range(n_of_enemies):
                Enemy_y[j] = 2000
            game_over_text()
            break

        Enemy_x[i] += Enemy_x_change[i]

        if Enemy_x[i] <= 0:
            Enemy_x_change[i] = 4
            Enemy_y[i] += Enemy_y_change[i]
        elif Enemy_x[i] >= 736:
            Enemy_x_change[i] = - 4
            Enemy_y[i] += Enemy_y_change[i]

        # Collision
        collision = isCollison(Enemy_x[i], Enemy_y[i], Bullet_x, Bullet_y)
        if collision:
            Explosion_sound = mixer.Sound('explosion.wav')
            Explosion_sound.play()
            Bullet_y = 480
            Bullet_State = "ready"
            score_value += 1
            Enemy_x[i] = random.randint(0, 735)
            Enemy_y[i] = random.randint(30, 160)

        enemy(Enemy_x[i], Enemy_y[i], i)

    # Bullet Movement
    if Bullet_y <= 0:
        Bullet_y = 480
        Bullet_State = "ready"

    if Bullet_State == "fire":
        fire_bullet(Bullet_x, Bullet_y)
        Bullet_y -= Bullet_y_change

    player(Player_x, Player_y)
    show_score(Text_x, Text_y)
    pygame.display.update()
