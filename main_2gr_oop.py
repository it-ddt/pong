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
        score_1 = Score(
            center=(self.rect.width * 0.25, self.rect.height * 0.10),
            paddle=player_1
        )
        score_2 = Score(
            center=(self.rect.width * 0.75, self.rect.height * 0.10),
            paddle=player_2
        )
        self.paddles = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.scores = pygame.sprite.Group()
        self.paddles.add(player_1)
        self.paddles.add(player_2)
        ball.throw_in()
        self.balls.add(ball)
        self.scores.add(score_1)
        self.scores.add(score_2)
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
            self.paddles.update()
            self.balls.update()
            self.paddles.draw(self.screen)
            self.balls.draw(self.screen)
            self.scores.draw(self.screen)
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
            score=0
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
        self.score = score

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
        self.screen_rect = screen_rect

    def update(self):
        self.move()
        self.bounce()
        self.check_goal()

    def move(self):
        self.velocity_x = sin(radians(self.direction)) * self.speed
        self.velocity_y = cos(radians(self.direction)) * self.speed * -1
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def bounce(self):
        """
        отскок мяча от верхней и нижней границы
        """
        if self.rect.top <= self.screen_rect.top:
            self.direction *= -1
            self.direction += 180
        if self.rect.bottom >= self.screen_rect.bottom:
            self.direction *= -1
            self.direction += 180

    def throw_in(self):
        """
        центририрует мяч и запускает в направлении ворот левого или правого игрока
        """
        self.rect.center = self.screen_rect.center
        if randint(0, 1):
           self.direction = randint(45, 135)
        else:
            self.direction = randint(225, 315)

    def check_goal(self):
        """
        TODO:
        гол
        засчитать очко одному или другому игроку
        вернуть мяч на цетр
        повернуть мяч в другом направлении
        """
        if self.rect.right >= self.screen_rect.right:
            print("гол правому")
            self.throw_in()
        if self.rect.left <= self.screen_rect.left:
            print("гол правому")
            self.throw_in()
    

class Score(pygame.sprite.Sprite):
    """
    табло
    TODO:
    метод update, где табло перерисовывает счёт
    """
    def __init__(
            self,
            color=WHITE,
            size=50,
            center=(0, 0),
            paddle=None,
    ):
        super().__init__()
        self.font = pygame.font.Font(None, size)
        self.image = self.font.render(str(paddle.score), True, color)
        self.rect = self.image.get_rect(center=center)
        self.paddle = paddle
        

game = Game()
sys.exit()
