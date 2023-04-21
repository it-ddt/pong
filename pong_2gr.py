import pygame
import sys
from degrees_to_velocity import degrees_to_velocity

pygame.init()  # инициализация модулей пайгейма

# константы
WHITE = (255, 255, 255)  # белый цвет
BLACK = (0, 0, 0)  # черный цвет
FPS = 60

# экран
screen_width = 800  # ширина экрана в пикселях
screen_height = 600  # высота экрана в пикселях
screen = pygame.display.set_mode((screen_width, screen_height))  # экран
pygame.display.set_caption("Игра Понг")

# игрок 1
player1_width = 20  # ширина игрока
player1_height = 80  # высота игрока
player1_x = 50  # игрок в центре по ширине
player1_score = 0  # забитые голы
player1_y = screen_height // 2 - player1_height // 2  # игрок в центре по высоте
player1 = pygame.Rect((player1_x, player1_y, player1_width, player1_height))  # создаем игрока

# игрок 2
player2_width = 20  # ширина игрока
player2_height = 80  # высота игрока
player2_x = screen_width - player2_width - 50  # игрок в центре по ширине
player2_score = 0  # забитые голы
player2_y = screen_height // 2 - player1_height // 2  # игрок в центре по высоте
player2 = pygame.Rect((player2_x, player2_y, player2_width, player2_height))  # создаем игрока

# мяч
ball_width = 15
ball_height = 15
ball_x = screen_width // 2 - ball_width // 2
ball_y = screen_height // 2 - ball_height // 2
velocity = degrees_to_velocity(60, 10)
ball_speed_x = velocity[0] 
ball_speed_y = velocity[1]
ball = pygame.Rect((ball_x, ball_y, ball_width, ball_height))

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
            player1.y -= 1  # двигаем игрока1 вверх (в PG Y растет вниз)
    if keys[pygame.K_s]:  # клавиша s
        if player1.y < screen_height - player1_height:
            player1.y += 1  # двигаем игрока1 вниз
    if keys[pygame.K_UP]:  # клавиша стрелка вверх
        if player2.y > 0:
            player2.y -= 1  # двигаем игрока2 вверх (в PG Y растет вниз)
    if keys[pygame.K_DOWN]:  # клавиша стрелка вниз
        if player2.y < screen_height - player2_height:
            player2.y += 1  # двигаем игрока2 вниз
    
    # логика
    ball.x += ball_speed_x  # мяч всегда движется со своей скоростью по x
    ball.y += ball_speed_y  # мяч всегда движется со своей скоростью по x
    if ball.x < 0:  # TODO: гол, засчитать балл, вернуть в центр
        ball_speed_x *= -1  # переворачиваем скорость (меняем знак)
    if ball.x > screen_width - ball_width:  # мяч вылетел вправо
        ball_speed_x *= -1
    if ball.y < 0:  # вылет вверх
        ball_speed_y *= -1
    if ball.y > screen_height - ball_height:  # вылет вниз
        ball_speed_y *= -1

    # отрисовка
    screen.fill(BLACK)  # заливаем экран чёрным
    pygame.draw.rect(screen, WHITE, player1)  # рисуем игрока1
    pygame.draw.rect(screen, WHITE, player2)  # рисуем игрока2
    pygame.draw.rect(screen, WHITE, ball)  # рисуем мяч
    score_left_img = score_left.render(str(player1_score), True, WHITE)
    score_right_img = score_right.render(str(player2_score), True, WHITE)
    screen.blit(score_left_img, (screen_width * 0.25, 20))
    screen.blit(score_right_img, (screen_width * 0.75, 20))

    pygame.display.flip()  # обновляем экран
    clock.tick(FPS)  # 1 / FPS = время ожидания

# после завершения главного цикла
pygame.quit()  # выгрузили модули pygame из пямяти
sys.exit()  # закрыли программу
