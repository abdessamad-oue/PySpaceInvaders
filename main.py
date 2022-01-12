import random
import math
import pygame
from Explosion import Explosion
from pygame import mixer
import config

pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))

# title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("img/icon.png").convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
fps = 60

# backgound
bg = pygame.image.load('img/space_bg.png').convert_alpha()

# background sounds
# mixer.music.load('sounds/a_start_to_space.ogg')
# mixer.music.set_volume(0.4)
# mixer.music.play(-1)

# Player
playerImg = pygame.image.load("img/spaceship.png").convert_alpha()
playerX = 370
playerY = 500
playerX_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 20

enemies_png = ['img/enemy.png', 'img/enemy2.png', 'img/enemy3.png']
for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load(random.choice(enemies_png)).convert_alpha())
    enemyX.append(random.randint(50, 750))
    enemyY.append(random.randint(20, 100))
    enemyX_change.append(config.ENEMY_X_SPEED)
    enemyY_change.append(config.ENEMY_Y_SPEED)

# bullet
bulletImg = pygame.image.load("img/bullet.png").convert_alpha()
bulletX = 0
bulletY = 480
bulletY_change = config.BULLET_SPEED
# state for bullet (ready | fire )
bullet_state = "ready"

# score
score = 0

game_over = False


# Functions
def display_player(x, y):
    screen.blit(playerImg, (x, y))


def display_score(score_value):
    my_font = pygame.font.Font(config.FONT_FILE, 20)
    score_text = "Score : {}".format(score_value)
    text_surface = my_font.render(score_text, False, (0, 255, 0))
    screen.blit(text_surface, (10, 550))


def display_game_over():
    my_font = pygame.font.Font(config.FONT_FILE, 50)
    score_text = "GAME OVER"
    text_surface = my_font.render(score_text, False, (0, 255, 0))
    screen.blit(text_surface, (240, 280))


def display_enemy(x, y, index):
    screen.blit(enemyImg[index], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    return False


explosion_group = pygame.sprite.Group()

# game loop
# running = 1
while 1:
    clock.tick(fps)
    # Red, Green, Blue
    screen.fill((0, 0, 0))
    # bg image
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # keyboard event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -config.PLAYER_SPEED
            if event.key == pygame.K_RIGHT:
                playerX_change = config.PLAYER_SPEED
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound('sounds/LaserShot.wav')
                    bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries of spaceship
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 730:
        playerX = 730

    explosion_group.draw(screen)
    explosion_group.update()
    # Enemy movements
    for i in range(number_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = config.ENEMY_X_SPEED
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -config.ENEMY_X_SPEED
            enemyY[i] += enemyY_change[i]

        # Collision
        coll = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if coll:
            bulletY = 480
            bullet_state = "ready"
            bullet_sound = mixer.Sound('sounds/explosion.wav')
            bullet_sound.play()
            score += 100
            explosion = Explosion(enemyX[i], enemyY[i])
            explosion_group.add(explosion)
            enemyX[i] = random.randint(0, 780)
            enemyY[i] = random.randint(50, 100)

        collision_game_over = is_collision(enemyX[i], enemyY[i], playerX, playerY)
        if collision_game_over:
            bullet_sound = mixer.Sound('sounds/explosion.wav')
            bullet_sound.play()
            explosionPlayer = Explosion(playerX, playerY)
            playerX = playerY = 3000
            explosion_group.add(explosionPlayer)
            game_over = True
            break

        display_enemy(enemyX[i], enemyY[i], i)

    if bulletY < 20:
        bullet_state = "ready"
        bulletY = 480

    # bullet movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    display_player(playerX, playerY)
    display_score(score)

    # Check Game Over
    if score == config.SCORE_GAME_OVER or game_over:
        number_of_enemies = 0
        display_game_over()

    pygame.display.update()

print("Goodbye")
