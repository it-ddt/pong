"""
TODO:
    крутить мяч при отскоке от ракетки:
        ракетка едет вниз - мяч закручивается вверх;
        ракетка едет вверх - мяч закручивается вниз;
    звуки: гол мне и противнику, отскок
    противник слишком сильный!
    выбрать режим игры: с компом или человеком
    уровень сложности
    ООП!!!
"""

import pygame
import sys
from degrees_to_velocity import degrees_to_velocity
from random import randint

pygame.init()  # инициализация модулей пайгейма

# константы
WHITE = (255, 255, 255)  # белый цвет
BLACK = (0, 0, 0)  # черный цвет
FPS = 60  # ограничение кадров в секунду

# экран
screen_info = pygame.display.Info()  # собираем инфу об экране
screen_width = screen_info.current_w  # ширина экрана в пикселях
screen_height = screen_info.current_h  # высота экрана в пикселях
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)  # экран
pygame.display.set_caption("Игра Понг")  # заголовок окна

def players_to_center():
    player1.x = screen_width * 0.1
    player1.y = screen_height // 2 - player1_height // 2
    player2.x = screen_width * 0.9 - player2_width
    player2.y = screen_height // 2 - player2_height // 2

# игрок 1
player1_width = 20  # ширина игрока
player1_height = 80  # высота игрока
player1_score = 0  # забитые голы
player1_speed = 10  # скорость игрока
player1 = pygame.Rect((0, 0, player1_width, player1_height))  # создаем игрока

# игрок 2
player2_width = 20  # ширина игрока
player2_height = 80  # высота игрока
player2_score = 0  # забитые голы
player2_speed = 10
player2 = pygame.Rect((0, 0, player2_width, player2_height))  # создаем игрока

players_to_center()

# мяч

def ball_to_center():
    ball.x = screen_width // 2 - ball_width // 2
    ball.y = screen_height // 2 - ball_height // 2

def rotate_ball() -> tuple:
    if randint(0, 1) == 0:
        direction = randint(225, 315)
    else:
        direction = randint(90, 135)
    velocity = degrees_to_velocity(direction, 10)
    return velocity

ball_width = 15
ball_height = 15

ball = pygame.Rect((0, 0, ball_width, ball_height))
ball_to_center()
velocity = rotate_ball()
ball_speed_x = velocity[0]
ball_speed_y = velocity[1]

clock = pygame.time.Clock()  # часы для контроя FPS

# табло
score_left = pygame.font.Font(None, 60)
score_right = pygame.font.Font(None, 60)

game = True  
while game:
    """ 
        Главный цикл игры
        Цикл должен обязательно закончится обновлением дисплея,
        если выйти по break, то игра зависнет!
        Контролируем, идет ли игра, переменной game
    """

    # события
    for event in pygame.event.get():  # проходим по всем событиям, которые происходят сейчас
        if event.type == pygame.QUIT:  # обработка события выхода
            game = False
        if event.type == pygame.KEYDOWN:  # нажатая клавиша (не зажатая!)
            if event.key == pygame.K_ESCAPE:  # клавиша Esc
                game = False

    keys = pygame.key.get_pressed() # собираем коды нажатых клавиш в список
    if keys[pygame.K_w]:  # клавиша w
        if player1.y > 0:
            player1.y -= player1_speed  # двигаем игрока1 вверх (в PG Y растет вниз)
    if keys[pygame.K_s]:  # клавиша s
        if player1.y < screen_height - player1_height:
            player1.y += player1_speed   # двигаем игрока1 вниз
    """
    if keys[pygame.K_UP]:  # клавиша стрелка вверх
        if player2.y > 0:
            player2.y -= player2_speed   # двигаем игрока2 вверх (в PG Y растет вниз)
    if keys[pygame.K_DOWN]:  # клавиша стрелка вниз
        if player2.y < screen_height - player2_height:
            player2.y += player2_speed   # двигаем игрока2 вниз
    """
    
    # логика
    ball.x += ball_speed_x  # мяч всегда движется со своей скоростью по x
    ball.y += ball_speed_y  # мяч всегда движется со своей скоростью по x

    # логика компьютерного противника
    if ball.centery < player2.centery:  # мяч выше ракетки
        player2.y -= player2_speed
    if ball.centery > player2.centery:  # мяч ниже ракетки
        player2.y += player2_speed
    
    # отскоки от бортов
    if ball.y < 0:  # вылет вверх
        ball_speed_y *= -1
    if ball.y > screen_height - ball_height:  # вылет вниз
        ball_speed_y *= -1

    # отскок от ракеток
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1
        ball.x += ball_speed_x
        ball.y += ball_speed_y

    # голы
    if ball.x < 0:
        player2_score += 1
        ball_to_center()
        players_to_center()
        velocity = rotate_ball()
        ball_speed_x = velocity[0]
        ball_speed_y = velocity[1]
        pygame.time.delay(1000)
    if ball.x > screen_width - ball_width:
        player1_score += 1
        ball_to_center()
        players_to_center()
        velocity = rotate_ball()
        ball_speed_x = velocity[0]
        ball_speed_y = velocity[1]
        pygame.time.delay(1000)

    # отрисовка
    screen.fill(BLACK)  # заливаем экран чёрным
    pygame.draw.rect(screen, WHITE, player1)  # рисуем игрока1
    pygame.draw.rect(screen, WHITE, player2)  # рисуем игрока2
    pygame.draw.rect(screen, WHITE, ball)  # рисуем мяч
    score_left_img = score_left.render(str(player1_score), True, WHITE)
    score_right_img = score_right.render(str(player2_score), True, WHITE)
    screen.blit(score_left_img, (screen_width * 0.25, 20))
    screen.blit(score_right_img, (screen_width * 0.75, 20))
    line = pygame.draw.line(
        screen,
        WHITE,
        [screen_width // 2, 0],
        [screen_width // 2, screen_height],
        1
    )
    pygame.display.flip()  # обновляем экран
    clock.tick(FPS)  # 1 / FPS = время ожидания

# после завершения главного цикла
pygame.quit()  # выгрузили модули pygame из пямяти
sys.exit()  # закрыли программу
