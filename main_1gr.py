import pygame
import sys
from degrees_to_velocity import degrees_to_velocity


pygame.init()  # инициализация модулей пайгейма

# константы
WHITE = (255, 255, 255)  # белый цвет
BLACK = (0, 0, 0)  # черный цвет
FPS = 30

# экран
screen_width = 1000  # ширина экрана в пикселях
screen_height = 600  # высота экрана в пикселях
screen = pygame.display.set_mode((screen_width, screen_height))  # экран

# часы
clock = pygame.time.Clock()

# игрок 1
player_1_width = 20  # ширина игрока
player_1_height = 70  # высота игрока
player_1_x = 100
player_1_y = screen_height // 2 - player_1_height // 2  # игрок в центре по высоте
player_1_speed = 10
player_1_score = 0
player_1 = pygame.Rect((player_1_x, player_1_y, player_1_width, player_1_height))  # создаем игрока

# игрок 2
player_2_width = 20  # ширина игрока
player_2_height = 70  # высота игрока
player_2_x = screen_width - 100 - player_2_width
player_2_y = screen_height // 2 - player_2_height // 2  # игрок в центре по высоте
player_2_speed = 10
player_2_score = 0
player_2 = pygame.Rect((player_2_x, player_2_y, player_2_width, player_2_height))  # создаем игрока

# мяч
def ball_to_center():
    ball.x = screen_width // 2 - ball_width // 2
    ball.y = screen_height // 2 - ball_height // 2

ball_width = 10
ball_height = 10
ball_direction = degrees_to_velocity(45, 10)
ball_speed_x = ball_direction[0]
ball_speed_y = ball_direction[1]
ball_x = screen_width // 2 - ball_width // 2
ball_y = screen_height // 2 - ball_height // 2
ball = pygame.Rect((ball_x, ball_y, ball_width, ball_height))  # TODO: get_rect от поверхности


# табло
score_left = pygame.font.Font(None, 60)
score_left_x = screen_width * 0.25
score_right = pygame.font.Font(None, 60)
score_right_x = screen_width * 0.75

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
    if keys[pygame.K_w]:  # клавиша стрелка вверх
        if player_1.y > 0:
            player_1.y -= player_1_speed  # двигаем игрока1 вверх (в PG Y растет вниз)
    if keys[pygame.K_s]:  # клавиша стрелка вниз
        if player_1.y < screen_height - player_1_height :
            player_1.y += player_1_speed  # двигаем игрока1 вниз
    if keys[pygame.K_UP]:
        if player_2.y > 0:
            player_2.y -= player_2_speed 
    if keys[pygame.K_DOWN]:
        if player_2.y < screen_height - player_2_height :
            player_2.y += player_2_speed 
    
    # логика
    ball.x += ball_speed_x 
    ball.y += ball_speed_y
    if ball.x < 0:  # гол
        player_2_score += 1
        ball_to_center()
    if ball.x > screen_width - ball_width:  # гол
        player_1_score += 1
        ball_to_center()
    if ball.y < 0:
        ball_speed_y *= -1
    if ball.y > screen_height - ball_height:
        ball_speed_y *= -1

    # отскок от ракетки
    if ball.colliderect(player_1) or ball.colliderect(player_2):
        ball_speed_x *= -1

    score_left_img = score_left.render(str(player_1_score), True, WHITE)
    score_right_img = score_right.render(str(player_2_score), True, WHITE)

    # отрисовка
    screen.fill(BLACK)  # заливаем экран чёрным
    pygame.draw.rect(screen, WHITE, player_1)  # рисуем игрока 1
    pygame.draw.rect(screen, WHITE, player_2)  # рисуем игрока 2
    pygame.draw.rect(screen, WHITE, ball)  # мяч
    
    screen.blit(score_left_img, (score_left_x, 10))
    screen.blit(score_right_img, (score_right_x, 10))

    pygame.display.flip()  # обновляем экран
    clock.tick(FPS)  # 1 сек / FPS = ожидание

# после завершения главного цикла
pygame.quit()
sys.exit()