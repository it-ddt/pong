import pygame
import sys
from random import randint
from math import sin, cos, radians

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 30


class Game:
    def __init__(self):
        pygame.init()
        screen_info = pygame.display.Info()
        self.screen = pygame.display.set_mode(
            (screen_info.current_w, screen_info.current_h),
            pygame.FULLSCREEN
        )
        self.rect = self.screen.get_rect()
        player_1 = Paddle(
            screen_rect=self.rect,
            center=(self.rect.width * 0.1, self.rect.centery),
            size=(self.rect.width * 0.01, self.rect.height * 0.1),
            keys=(pygame.K_w, pygame.K_s)
        )
        player_2 = Paddle(
            screen_rect=self.rect,
            center=(self.rect.width * 0.9, self.rect.centery),
            size=(self.rect.width * 0.01, self.rect.height * 0.1),
            is_automatic=True
        )
        ball = Ball(
            self.rect,
            self.rect.center,
            (self.rect.width * 0.01, self.rect.width * 0.01)
        )
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(player_1)
        self.all_sprites.add(player_2)
        self.all_sprites.add(ball)
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

            self.screen.fill(BLACK)
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            pygame.draw.line(
                self.screen,
                WHITE,
                (self.rect.centerx, self.rect.bottom),
                (self.rect.centerx, self.rect.top)
            )
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()


class Paddle(pygame.sprite.Sprite):
    def __init__(
            self,
            screen_rect=None,
            center=(0, 0),
            size=(10, 100),
            color=WHITE,
            keys=(pygame.K_UP, pygame.K_DOWN),
            is_automatic=False,
            speed=10,
    ):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.keys = keys
        self.is_automatic = is_automatic
        self.speed = speed
        self.screen_rect = screen_rect

    def update(self):
        keys = pygame.key.get_pressed()
        if not self.is_automatic:
            if keys[self.keys[0]]:
                if self.rect.top >= self.screen_rect.top:
                    self.rect.y -= self.speed
            if keys[self.keys[1]]:
                if self.rect.bottom <= self.screen_rect.bottom:
                    self.rect.y += self.speed


class Ball(pygame.sprite.Sprite):
    """ мяч """
    def __init__(
            self,
            screen_rect=None,
            center=(0, 0),
            size=(10, 10),
            color=WHITE,
            speed=10,
            velocity_x=None,
            velocity_y=None,
            direction=90
    ) -> None:
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.direction = direction
        self.speed = speed

    def update(self):
        self.velocity_x = sin(radians(self.direction)) * self.speed
        self.velocity_y = cos(radians(self.direction)) * self.speed * -1
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def bounce(self):
        """
        TODO:
        отскок мяч от верхней и нижней границы:
        как поменять направление?
        """
        pass

    def goal(self):
        """
        TODO:
        гол
        засчитать очко одному или другому игроку
        вернуть мяч на цетр
        повернуть мяч в другом направлении
        """
        pass
    

class Score:
    """ табло """
    pass


game = Game()
sys.exit()
