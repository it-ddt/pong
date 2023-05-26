import pygame
import sys
from random import randint, choice
from math import radians, sin, cos

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 30


class Game:
    """
    игра
    звуки отскоков и голов
    меню: выбрать игру с человеком или с компом
    закручивание мяча при ударе о ракетку
    """
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
        self.player_1 = Paddle(
            self.screen_rect, 
            (self.screen_rect.width * 0.1, self.screen_rect.centery),
            keys=(pygame.K_w, pygame.K_s),
        )
        self.player_2 = Paddle(
            self.screen_rect, 
            (self.screen_rect.width * 0.9, self.screen_rect.centery),
            is_automatic=True,
        )
        self.ball = Ball(self.screen_rect)
        self.ball.throw_in()
        self.score_1 = Score(
            center=(self.screen_rect.width * 0.25, self.screen_rect.height * 0.05),
            size=50,
            player=self.player_1
        )
        self.score_2 = Score(
            center=(self.screen_rect.width * 0.75, self.screen_rect.height * 0.05),
            size=50,
            player=self.player_2
        )
        self.paddles = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.scores = pygame.sprite.Group()
        self.paddles.add(self.player_1)
        self.paddles.add(self.player_2)
        self.balls.add(self.ball)
        self.scores.add(self.score_1)
        self.scores.add(self.score_2)
        self.clock = pygame.time.Clock()
        self.main_loop()

    def check_goal(self):
        if self.ball.rect.right >= self.screen_rect.right:
            self.player_1.score += 1
            self.ball.throw_in()
        if self.ball.rect.left <= self.screen_rect.left:
            self.player_2.score += 1
            self.ball.throw_in()

    def main_loop(self):
        game = True
        while game:
            dt = self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                game = False

            self.paddles.update(self.ball, dt)
            self.balls.update(self.paddles)
            self.scores.update()
            self.check_goal()
            self.screen.fill(BLACK)
            self.paddles.draw(self.screen)
            self.balls.draw(self.screen)
            self.scores.draw(self.screen)
            pygame.draw.line(
                self.screen,
                WHITE,
                self.screen_rect.midtop,
                self.screen_rect.midbottom
            )
            pygame.display.flip()
            
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
        self.score = 0
        self.elapsed_time = 0

    def update(self, ball, dt):
        if not self.is_automatic:
            keys = pygame.key.get_pressed()
            if keys[self.keys[0]]:
                if self.rect.top > self.screen_rect.top:
                    self.rect.y -= self.speed
            if keys[self.keys[1]]:
                if self.rect.bottom < self.screen_rect.bottom:
                    self.rect.y += self.speed
        else:  # автоматика
            self.elapsed_time += dt
            if self.elapsed_time >= 100:  # TODO: пробросить ожидание в конструктор
                if self.rect.centery > ball.rect.centery:
                    if self.rect.top > self.screen_rect.top:
                        self.rect.y -= self.speed
                if self.rect.centery < ball.rect.centery:
                    if self.rect.bottom < self.screen_rect.bottom:
                        self.rect.y += self.speed
                self.elapsed_time = 0


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

    def update(self, paddles_group):
        self.move()
        self.wall_bounce()
        self.paddles_bounce(paddles_group)

    def move(self):
        """
        движение мяча по X и Y
        """
        self.vel_x = sin(radians(self.direction)) * self.speed
        self.vel_y = cos(radians(self.direction)) * self.speed * -1
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def throw_in(self):
        """
        вброс мяча: центрирование и поворт в сторону одни или других ворот
        """
        self.rect.center = self.screen_rect.center
        self.direction = choice((randint(45, 135), randint(225, 315)))

    def wall_bounce(self):
        """
        отскок от верхней и нижней границы экрана
        """
        if self.rect.top <= self.screen_rect.top:
            self.direction *= -1
            self.direction += 180
        elif self.rect.bottom >= self.screen_rect.bottom:
            self.direction *= -1
            self.direction += 180

    def paddles_bounce(self, paddles_group):
        """
        отскок мяча от ракеток
        """
        for paddle in paddles_group:
            if paddle.rect.colliderect(self.rect):
                self.direction *= -1


class Score(pygame.sprite.Sprite):
    """
    табло
    FIXME: счёт всех игроков не обновляется, остаеётся изначальным
    """
    def __init__(
            self,
            center=None,
            size=None,
            color=WHITE,
            player=None
    ):
        super().__init__()
        self.font = pygame.font.Font(None, size)
        self.player = player
        self.color = color
        self.image = self.font.render(str(self.player.score), True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.image = self.font.render(str(self.player.score), True, self.color)
        self.rect = self.image.get_rect(center=self.rect.center)


game = Game()
sys.exit()
