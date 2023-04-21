import pygame
import sys

pygame.init()

# экран
screen_width = 800  # ширина экрана в пикселях
screen_height = 600  # высота экрана в пикселях
screen = pygame.display.set_mode((screen_width, screen_height))  # экран
pygame.display.set_caption("Моя программа")

# игрок
player_width = 50  # ширина игрока
player_height = 50  # высота игрока
player_x = screen_width // 2 - player_width // 2
player_y = screen_height // 2 - player_height // 2
player_color = (255, 255, 255)  # RGB
player = pygame.Rect((player_x, player_y, player_width, player_height))  # x, y, ширина, высота

while True:  # главный цикл

    # события
    for event in pygame.event.get():  # собираем события
        if event.type == pygame.QUIT:  # обработка события
            pygame.quit()  # выгрузили модули pygame из пямяти
            sys.exit()  # закрыли программу
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # нажатая клавиша
                pygame.quit()
                sys.exit()
    
    keys = pygame.key.get_pressed() # собираем нажатые клавиши
    if keys[pygame.K_UP]:  # обрабатываем нажатые клавиши 
        player.y -= 1
    if keys[pygame.K_DOWN]:
        player.y += 1
    if keys[pygame.K_LEFT]:
        player.x -= 1
    if keys[pygame.K_RIGHT]:
        player.x += 1

    # отрисовка
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, player_color, player)  # рисуем игрока
    pygame.display.flip()  # обновляем экран
