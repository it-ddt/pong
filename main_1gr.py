import pygame
import sys

pygame.init()  # инициализация модулей пайгейма

# константы
WHITE = (255, 255, 255)  # белый цвет
BLACK = (0, 0, 0)  # черный цвет

# экран
screen_width = 800  # ширина экрана в пикселях
screen_height = 600  # высота экрана в пикселях
screen = pygame.display.set_mode((screen_width, screen_height))  # экран

# игрок
player_width = 50  # ширина игрока
player_height = 50  # высота игрока
player_x = screen_width // 2 - player_width // 2  # игрок в центре по ширине
player_y = screen_height // 2 - player_height // 2  # игрок в центре по высоте
player = pygame.Rect((player_x, player_y, player_width, player_height))  # создаем игрока

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
    if keys[pygame.K_UP]:  # клавиша стрелка вверх
        player.y -= 1  # двигаем игрока вверх (в PG Y растет вниз)
    if keys[pygame.K_DOWN]:  # клавиша стрелка вниз
        player.y += 1  # двигаем игрока вниз
    if keys[pygame.K_LEFT]:  # клавиша стрелка влево
        player.x -= 1  # двигаем игрока влево
    if keys[pygame.K_RIGHT]:  # клавиша стрелка вправо
        player.x += 1  # двигаем игрока вправо

    # отрисовка
    screen.fill(BLACK)  # заливаем экран чёрным
    pygame.draw.rect(screen, WHITE, player)  # рисуем игрока
    pygame.display.flip()  # обновляем экран

# после завершения главного цикла
pygame.quit()  # выгрузили модули pygame из пямяти
sys.exit()  # закрыли программу
