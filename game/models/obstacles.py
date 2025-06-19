import pygame
import random
from abc import ABC, abstractmethod
from .. import constants as C
from ..services.asset_loader import AssetLoader


class Obstacle(pygame.sprite.Sprite, ABC):
    """Абстрактный базовый класс для всех препятствий."""

    def __init__(self, lane_x):
        super().__init__()
        self.lane_x = lane_x

    @abstractmethod
    def update(self, dt, road_speed):
        """Обновляет позицию и состояние препятствия."""
        self.rect.y += road_speed * dt
        if self.rect.top > C.WINDOW_HEIGHT:
            self.kill()


class OncomingCar(Obstacle):
    """Препятствие - встречная машина."""
    BODY_COLORS = [
        (220, 50, 50),
        (50, 50, 220),
        (50, 200, 50),
        (220, 220, 50),
        (150, 150, 150),
        (200, 100, 0),
        (100, 50, 150),
        (0, 150, 150),
        (255, 165, 0)
    ]

    def __init__(self, lane_x):
        super().__init__(lane_x)

        self.image = pygame.Surface((C.CAR_WIDTH + 20, C.CAR_HEIGHT + 20),
                                    pygame.SRCALPHA)

        car_body_color = random.choice(self.BODY_COLORS)

        # Отрисовка кузова
        main_body_rect = pygame.Rect(10, 10, C.CAR_WIDTH, C.CAR_HEIGHT)
        pygame.draw.rect(self.image, car_body_color, main_body_rect,
                         border_radius=8)

        pygame.draw.rect(
            self.image,
            (max(0, car_body_color[0]-30),
             max(0, car_body_color[1]-30),
             max(0, car_body_color[2]-30)),
            (10, C.CAR_HEIGHT * 0.3 + 10, C.CAR_WIDTH, C.CAR_HEIGHT * 0.4),
            border_radius=5
        )

        # Колеса
        wheel_width = int(C.CAR_WIDTH * 0.3)
        wheel_height = int(C.CAR_HEIGHT * 0.15)

        pygame.draw.rect(self.image, C.COLOR_BLACK,
                         (10 + int(C.CAR_WIDTH * 0.05),
                          C.CAR_HEIGHT - wheel_height + 10,
                          wheel_width, wheel_height),
                         border_radius=3)
        pygame.draw.rect(self.image, C.COLOR_BLACK,
                         (10 + C.CAR_WIDTH - wheel_width -
                          int(C.CAR_WIDTH * 0.05),
                          C.CAR_HEIGHT - wheel_height + 10,
                          wheel_width, wheel_height),
                         border_radius=3)

        # Диски
        rim_width = int(wheel_width * 0.6)
        rim_height = int(wheel_height * 0.6)

        pygame.draw.rect(
            self.image, (180, 180, 180),
            (10 + int(C.CAR_WIDTH * 0.05) + (wheel_width - rim_width)/2,
             C.CAR_HEIGHT - wheel_height + 10 + (wheel_height - rim_height)/2,
             rim_width, rim_height),
            border_radius=2
        )
        pygame.draw.rect(
            self.image, (180, 180, 180),
            (10 + C.CAR_WIDTH - wheel_width - int(C.CAR_WIDTH * 0.05) +
             (wheel_width - rim_width)/2,
             C.CAR_HEIGHT - wheel_height + 10 + (wheel_height - rim_height)/2,
             rim_width, rim_height),
            border_radius=2
        )

        # Окна
        window_main_width = int(C.CAR_WIDTH * 0.7)
        window_main_height = int(C.CAR_HEIGHT * 0.3)
        window_main_x = (C.CAR_WIDTH - window_main_width) / 2 + 10
        window_main_y = int(C.CAR_HEIGHT * 0.2) + 10
        pygame.draw.rect(self.image, C.COLOR_BLUE_SKY,
                         (window_main_x, window_main_y,
                          window_main_width, window_main_height),
                         border_radius=5)

        side_window_width = int(C.CAR_WIDTH * 0.2)
        side_window_height = int(C.CAR_HEIGHT * 0.25)
        pygame.draw.rect(self.image, C.COLOR_BLUE_SKY,
                         (10 + int(C.CAR_WIDTH * 0.05),
                          window_main_y + 5,
                          side_window_width, side_window_height),
                         border_radius=3)
        pygame.draw.rect(self.image, C.COLOR_BLUE_SKY,
                         (10 + C.CAR_WIDTH - side_window_width -
                          int(C.CAR_WIDTH * 0.05),
                          window_main_y + 5,
                          side_window_width, side_window_height),
                         border_radius=3)

        # Фары (передние)
        light_width = int(C.CAR_WIDTH * 0.15)
        light_height = int(C.CAR_HEIGHT * 0.08)
        light_offset = int(C.CAR_WIDTH * 0.08)

        pygame.draw.rect(self.image, C.COLOR_GOLD,
                         (10 + light_offset,
                          C.CAR_HEIGHT + 10 - light_height - 5,
                          light_width, light_height),
                         border_radius=2)
        pygame.draw.rect(self.image, C.COLOR_GOLD,
                         (10 + C.CAR_WIDTH - light_offset - light_width,
                          C.CAR_HEIGHT + 10 - light_height - 5,
                          light_width, light_height),
                         border_radius=2)

        self.rect = pygame.Rect(0, 0, C.CAR_WIDTH, C.CAR_HEIGHT)
        self.rect.centerx = lane_x
        self.rect.bottom = 0

        self.image_offset_x = (self.image.get_width() - self.rect.width) / 2
        self.image_offset_y = (self.image.get_height() - self.rect.height) / 2

        self.mask = pygame.mask.from_surface(self.image)
        self.speed = random.uniform(100, 200)

    def update(self, dt, road_speed):
        """Обновляет позицию машины."""
        effective_speed = road_speed + self.speed
        self.rect.y += effective_speed * dt
        if self.rect.top > C.WINDOW_HEIGHT:
            self.kill()

    def draw(self, screen):
        """Отрисовывает машину с учетом смещения изображения."""
        screen.blit(self.image, (self.rect.x - self.image_offset_x,
                                 self.rect.y - self.image_offset_y))


class Manhole(Obstacle):
    """Препятствие - канализационный люк."""

    def __init__(self, lane_x):
        super().__init__(lane_x)

        self.original_cover_image = AssetLoader.get_image(
            C.IMG_MANHOLE, (C.MANHOLE_SIZE, C.MANHOLE_SIZE)
        )

        max_vertical_offset = (C.MANHOLE_SIZE *
                               C.MANHOLE_DIAGONAL_OFFSET_FACTOR)
        image_height = int(C.MANHOLE_SIZE + max_vertical_offset * 2)
        if image_height < C.MANHOLE_SIZE:
            image_height = C.MANHOLE_SIZE

        self.image = pygame.Surface((C.MANHOLE_SIZE * 2, image_height),
                                    pygame.SRCALPHA)

        self.initial_cover_y_on_image = (image_height - C.MANHOLE_SIZE) / 2
        self.initial_cover_x_on_image = (self.image.get_width() / 2 -
                                         C.MANHOLE_SIZE / 2)

        self.image.blit(self.original_cover_image,
                        (self.initial_cover_x_on_image,
                         self.initial_cover_y_on_image))

        self.rect = self.image.get_rect()
        self.rect.centerx = lane_x
        self.rect.bottom = 0

        self.mask = pygame.mask.from_surface(self.image)

        self.is_open = False
        self.open_progress = 0.0
        self.is_transitioning = False

        self.open_direction = random.choice([-1, 1])

    def update(self, dt, road_speed):
        """Обновляет люк, включая логику открытия."""
        super().update(dt, road_speed)

        if (not self.is_transitioning and
                self.rect.y > C.WINDOW_HEIGHT * C.MANHOLE_OPEN_Y_THRESHOLD_RATIO):
            self.is_transitioning = True

        if self.is_transitioning and self.open_progress < 1.0:
            self.open_progress = min(1.0,
                                     self.open_progress +
                                     C.MANHOLE_TRANSITION_SPEED * dt)
            self._animate_opening()

            if self.open_progress >= 1.0:
                self.is_open = True
                self.mask = pygame.mask.from_surface(self.image)

    def _animate_opening(self):
        """
        Перерисовывает изображение люка, анимируя сдвиг крышки
        в случайную сторону по диагонали.
        """
        self.image.fill((0, 0, 0, 0))

        hole_center_x_on_image = self.initial_cover_x_on_image + \
            C.MANHOLE_SIZE / 2
        hole_center_y_on_image = self.initial_cover_y_on_image + \
            C.MANHOLE_SIZE / 2
        pygame.draw.circle(self.image, C.COLOR_BLACK,
                           (int(hole_center_x_on_image),
                            int(hole_center_y_on_image)),
                           int(C.MANHOLE_SIZE / 2 * 0.8))

        horizontal_displacement = (self.open_progress * C.MANHOLE_SIZE *
                                   C.MANHOLE_OPEN_OFFSET_MULTIPLIER)

        vertical_displacement = (self.open_progress * C.MANHOLE_SIZE *
                                 C.MANHOLE_DIAGONAL_OFFSET_FACTOR)

        current_cover_x = (self.initial_cover_x_on_image +
                           (horizontal_displacement * self.open_direction))
        current_cover_y = self.initial_cover_y_on_image + \
            vertical_displacement

        self.image.blit(self.original_cover_image,
                        (int(current_cover_x), int(current_cover_y)))

        self.mask = pygame.mask.from_surface(self.image)
