import pygame
import sys
from random import randint, choice
from math import radians, sin, cos

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 30


class Game:
    """ игра """
    def __init__(self):
        pygame.init()
        screen_info = pygame.display.Info()
        self.W = screen_info.current_w
        self.H = screen_info.current_h
        self.screen = pygame.display.set_mode(
            (self.W, self.H),
            pygame.FULLSCREEN
        )
        self.screen_rect = self.screen.get_rect()
        player_1 = Paddle(
            self.screen_rect, 
            (self.screen_rect.width * 0.1, self.screen_rect.centery),
            keys=(pygame.K_w, pygame.K_s),
        )
        player_2 = Paddle(
            self.screen_rect, 
            (self.screen_rect.width * 0.9, self.screen_rect.centery),
            is_automatic=True,
        )
        ball = Ball(self.screen_rect)
        ball.throw_in()
        self.paddles = pygame.sprite.Group()
        self.ball = pygame.sprite.Group()
        self.paddles.add(player_1)
        self.paddles.add(player_2)
        self.ball.add(ball)
        self.clock = pygame.time.Clock()
        self.main_loop()
        
    def main_loop(self):
        game = True
        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                game = False

            self.paddles.update()
            self.ball.update()
            self.screen.fill(BLACK)
            self.paddles.draw(self.screen)
            self.ball.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()


class Paddle(pygame.sprite.Sprite):
    """
    ракетка

    TODO:
    поведение автоматической ракетки - она движется относительно Y мяча
    """
    def __init__(
            self,
            screen_rect=None,
            center=(0, 0),
            color=WHITE,
            size=None,
            speed=10,
            keys=(pygame.K_UP, pygame.K_DOWN),
            is_automatic=False,
    ):
        super().__init__()
        self.screen_rect = screen_rect
        if not size:
            size = (self.screen_rect.width * 0.01, self.screen_rect.height * 0.10)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = speed
        self.keys = keys
        self.is_automatic = is_automatic

    def update(self):
        if not self.is_automatic:
            keys = pygame.key.get_pressed()
            if keys[self.keys[0]]:
                if self.rect.top > self.screen_rect.top:
                    self.rect.y -= self.speed
            if keys[self.keys[1]]:
                if self.rect.bottom < self.screen_rect.bottom:
                    self.rect.y += self.speed


class Ball(pygame.sprite.Sprite):
    """
    мяч
    отскок от бортов (верхнего и нижнего)
    отскок от ракеток
    """
    def __init__(
            self,
            screen_rect=None,
            center=None,
            color=WHITE,
            size=None,
            speed=10,
            direction=90,
            vel_x=0,
            vel_y=0,
    ):
        super().__init__()
        self.screen_rect = screen_rect
        if not size:
            size = (self.screen_rect.width * 0.01, self.screen_rect.width * 0.01)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        if not center:
            self.rect.center = screen_rect.center
        self.speed = speed
        self.direction = direction
        self.vel_x = vel_x
        self.vel_y = vel_y

    def update(self):
        self.vel_x = sin(radians(self.direction)) * self.speed
        self.vel_y = cos(radians(self.direction)) * self.speed * -1
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.bounce()

    def throw_in(self):
        self.rect.center = self.screen_rect.center
        self.direction = choice((randint(45, 135), randint(225, 315)))

    def bounce(self):
        if self.rect.top <= self.screen_rect.top:
            self.direction *= -1
            self.direction += 180
        elif self.rect.bottom >= self.screen_rect.bottom:
            self.direction *= -1
            self.direction += 180


class Score:
    """ табло """
    pass


game = Game()
sys.exit()
