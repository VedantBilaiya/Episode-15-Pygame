# Importing and Intilizing Pygame , Importing Random , Importing Maths
import pygame
import random
import math

from pygame import mixer

pygame.init()

# Creating The Screen For Our Game
screen = pygame.display.set_mode((800, 600))

# Title
pygame.display.set_caption('Space Invander Game')

# Icon
icon = pygame.image.load('launch.png')
pygame.display.set_icon(icon)

# Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(100)
    enemyY.append(10)
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

# Scores
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

scoreX = 10
scoreY = 10

game_over = pygame.font.Font('freesansbold.ttf', 64)

def gameOver():
    game_over_text = font.render("GAME OVER",True, (255,255,255))
    screen.blit(game_over_text,(200, 250))

def show_score():
    score = font.render("Score : " + str(score_value),True, (255,255,255))
    screen.blit(score,(scoreX, scoreY))

def player():
    screen.blit(playerImg, (playerX, playerY))


def enemy():
    screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))


def fire_bullet(bulletX, bulletY):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (bulletX, bulletY))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.6
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.6
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound('gun.wav')
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Adding Boundries So that our player cannot go outside
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        
        # Enemy Movement
        enemyX[i] += enemyX_change[i]

        # Game Over
        if enemyY[i] > 300:
            for j in range(num_of_enemies):
                gameOver()
                enemyY[j] = 2000
                break

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            enemySound = mixer.Sound('enemy.wav')
            enemySound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 100)

        enemy()

    # Bullet Movement
    if bulletY < 0:
        bulletY = 480
        bullet_state = "ready"
    elif bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Calling The Functions
    player()
    show_score()
    pygame.display.update()
