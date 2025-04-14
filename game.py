import pygame
import random
from utils import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(
            center=(LANE_POSITIONS[1], SCREEN_HEIGHT - 150))
        self.lane = 1

    def move(self, direction):
        if direction == "left" and self.lane > 0:
            self.lane -= 1
        elif direction == "right" and self.lane < 2:
            self.lane += 1
        self.rect.centerx = LANE_POSITIONS[self.lane]


class Obstacle(pygame. sprite.Sprite):
    def __init__(self, obstacle_type):
        super().__init__()
        self.obstacle_type = obstacle_type
        self.image = pygame.Surface((OBSTACLE_SIZE, OBSTACLE_SIZE))
        self.image.fill(OBSTACLE_COLORS[obstacle_type])
        self.rect = self.image.get_rect(
            center=(random.choice(LANE_POSITIONS)-OBSTACLE_SIZE))

    def update(self):
        self.rect.y += OBSTACLE_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Городской курьер")
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1500)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move("left")
                elif event.key == pygame.K_RIGHT:
                    self.player.move("right")
            elif event.type == self.obstacle_timer:
                obstacle = Obstacle(random.choice(["manhole"], ["car"]))
                self.all_sprites.add(obstacle)
                self.obstacles.add(obstacle)

    def check_collisions(self):
        if pygame.sprite.spritecollide(self.player, self.obstacles, dokill=False):
            print("Игра закончена! Произошло столкновение с препятствием.")
            self.running = False

    def run(self):
        while self.running:
            self.handle_events()
            self.all_sprites.update()
            self.check_collisions()

            self.screen.fill(SKY_COLOR)
            pygame.draw.rect(self.screen, ROAD_COLOR,
                             (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
            self.all_sprites.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

