import pygame
import sys
import random
from pygame import mixer

pygame.init()

# variables of sounds
#pygame.mixer.music.load("Powerful-Trap-.mp3")
#mixer.music.play(-1)

# variables of screen size:
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
SURFACE = screen
BACKGROUND_IMAGE = pygame.image.load("Desert.png")
BLACK_COLOR = (0, 0, 0)  # for the score

# variables of the player 
current_image = pygame.image.load("player.png")
currents_image = pygame.transform.scale(current_image, (55,55))
player_size = 50
player_position = [WIDTH / 2, HEIGHT - 2 * player_size]
player_images = {
    pygame.K_LEFT: pygame.image.load("player_left.png"),
    pygame.K_RIGHT: pygame.image.load("player_right.png"),
    pygame.K_UP: pygame.image.load("player.png"),
    pygame.K_DOWN: pygame.image.load("player.png")
}
pygame.key.set_repeat(100, 75) # to set the ket presses to be continuous

# variables of the enemy
enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (55,55))
enemy_size = 50
enemy_position = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_position]
SPEED = 3

game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

def set_level(score, SPEED):
    if score < 20:
        SPEED = 3
    elif score < 40:
        SPEED = 5
    elif score < 60:
        SPEED = 7
    elif score < 90:
        SPEED = 10
    elif score < 110:
        SPEED = 15
    elif score < 130:
        SPEED = 20
    else:
        SPEED = 25

    return SPEED


def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_position = random.randint(0, WIDTH - enemy_size)
        y_position = 0
        new_enemy = [x_position, y_position]
        enemy_list.append(new_enemy)


def draw_enemies(enemy_list):
    for enemy_position in enemy_list:
        #pygame.draw.rect(SURFACE, WHITE_COLOR, (enemy_position[0], enemy_position[1], enemy_size, enemy_size))
        screen.blit(enemy_image, (enemy_position[0], enemy_position[1]))



def update_enemy_position(enemy_list, score):
    for idx, enemy_position in enumerate(enemy_list):
        if enemy_position[1] >= 0 and enemy_position[1] < HEIGHT:
            enemy_position[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score


def collision_check(enemy_list, player_position):
    for enemy_position in enemy_list:
        if detect_collision(player_position, enemy_position):
            return True
    return False


def detect_collision(player_position, enemy_position):
    p_x = player_position[0]
    p_y = player_position[1]

    e_x = enemy_position[0]
    e_y = enemy_position[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < e_x + enemy_size):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_position[0]
            y = player_position[1]

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                x -= player_size / 2
                current_image = player_images[pygame.K_LEFT]

            elif keys[pygame.K_RIGHT]:
                x += player_size / 2
                current_image = player_images[pygame.K_RIGHT]

            elif keys[pygame.K_UP]:
                y -= player_size / 2
                current_image = player_images[pygame.K_UP]

            elif keys[pygame.K_DOWN]:
                y += player_size / 2
                current_image = player_images[pygame.K_DOWN]

            player_position = [x, y]

    # making the last position of the player disappear (color black)
    screen.blit(BACKGROUND_IMAGE, (0,0))

    drop_enemies(enemy_list)
    SPEED = set_level(score, SPEED)
    score = update_enemy_position(enemy_list, score)
    text = "Score:" + str(score)
    label = myFont.render(text, 1, BLACK_COLOR)
    screen.blit(label, (WIDTH - 200, HEIGHT - 40))

    if collision_check(enemy_list, player_position):
        game_over = True
        break

    draw_enemies(enemy_list)

    screen.blit(current_image, (player_position[0], player_position[1]))
    screen.blit(enemy_image, (enemy_position[0], enemy_position[1]))

    #pygame.draw.rect(SURFACE, BLACK_COLOR, (player_position[0], player_position[1], player_size, player_size))
    #pygame.draw.rect(SURFACE, WHITE_COLOR, (enemy_position[0], enemy_position[1], enemy_size, enemy_size))
    clock.tick(40)

    pygame.display.update()
