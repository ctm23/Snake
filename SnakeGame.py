import pygame
import sys
import random


# Defining static variables
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
SPEED = 15
BLOCK = 25
DIS_W, DIS_H = 1000, 800

# Setting up the game
pygame.init()
dis = pygame.display.set_mode(size=(DIS_W, DIS_H))
pygame.display.set_caption('SNAKE!')
clock = pygame.time.Clock()
font_style = pygame.font.SysFont('calibri', 30)
saved_high_score = open('highscore.txt', 'r')
high_score = int(saved_high_score.read())
saved_high_score.close()

def message(msg, color, x, y):
    # Displays a game message
    rend_msg = font_style.render(msg, True, color)
    dis.blit(rend_msg, [x, y])


def draw_snake(snake_list):
    # Renders the snake
    for x in snake_list:
        pygame.draw.rect(dis, BLUE, [x[0], x[1], BLOCK, BLOCK])


def play_game():
    # Setting initial variables
    global high_score
    score = 0
    x, y = DIS_W/2, DIS_H/2
    x_delta, y_delta = 0, 0
    snake_list = []
    game_over = False
    pause_game = False
    food_x = round(random.randrange(0, DIS_W - BLOCK) / BLOCK) * BLOCK
    food_y = round(random.randrange(0, DIS_H - BLOCK) / BLOCK) * BLOCK

    # Game While Loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_game = True
                if event.key == pygame.K_c:
                    pause_game = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x_delta, y_delta = -BLOCK, 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x_delta, y_delta = BLOCK, 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    x_delta, y_delta = 0, -BLOCK
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    x_delta, y_delta = 0, BLOCK

        if pause_game:
            message("Game Paused - press C to continue", WHITE, DIS_W/4, DIS_H/4)
            pygame.display.update()
            continue

        x += x_delta
        y += y_delta
        snake_list.append((x, y))
        if len(snake_list) > score+1:
            del snake_list[0]

        if len(snake_list) != len(set(snake_list)):
            game_over = True

        if x == food_x and y == food_y:
            score += 1
            food_x = round(random.randrange(0, DIS_W - BLOCK) / BLOCK) * BLOCK
            food_y = round(random.randrange(0, DIS_H - BLOCK) / BLOCK) * BLOCK

        dis.fill(BLACK)
        draw_snake(snake_list)
        pygame.draw.rect(dis, RED, [food_x, food_y, BLOCK, BLOCK])
        color = GREEN if score > high_score else WHITE
        message(f"Current Score: {score}", color, 0, 0)
        pygame.display.update()
        clock.tick(SPEED)

        if not (0 < x < DIS_W) or not (0 < y < DIS_H):
            game_over = True

    while True:
        pygame.display.update()
        message("GAME OVER -- Press C to play again", RED, DIS_W/4, DIS_H/4)
        if score > high_score:
            message(f"You got {score} -- New High Score!", GREEN, DIS_W/4, DIS_H/3)
            high_score = score

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                play_game()
            if event.type == pygame.QUIT:
                new_high_score = open('highscore.txt', 'w')
                new_high_score.write(str(high_score))
                new_high_score.close()
                pygame.quit()
                sys.exit()


play_game()
