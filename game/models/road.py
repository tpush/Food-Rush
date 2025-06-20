import pygame
import random
from .. import constants as C
from .obstacles import OncomingCar, Manhole


class DecorativeElement:
    """Класс для программно нарисованных декоративных элементов."""

    def __init__(self, type, x, y, draw_data):
        self.type = type
        self.x = x
        self.y = y
        self.draw_data = draw_data

    def update(self, dt, road_speed):
        # Декорации движутся только с дорогой
        self.y += road_speed * dt

    def draw(self, screen):
        if self.type == 'small_stone':
            stone_width = self.draw_data['stone_width']
            stone_height = self.draw_data['stone_height']
            stone_color = self.draw_data['stone_color']

            # Камень (эллипс)
            stone_rect = pygame.Rect(self.x - stone_width / 2,
                                     self.y,
                                     stone_width,
                                     stone_height)
            pygame.draw.ellipse(screen, stone_color, stone_rect)

            # Тень
            shadow_offset_x = random.randint(1, 3)
            shadow_offset_y = random.randint(1, 3)
            shadow_color = (max(0, stone_color[0] - 20),
                            max(0, stone_color[1] - 20),
                            max(0, stone_color[2] - 20))
            # Отрисовка меньшего эллипса со смещением
            pygame.draw.ellipse(
                screen, shadow_color,
                (stone_rect.x + shadow_offset_x,
                 stone_rect.y + shadow_offset_y,
                 stone_rect.width - shadow_offset_x,
                 stone_rect.height - shadow_offset_y)
            )


class Road:
    """Управляет дорогой, препятствиями и декорациями."""

    def __init__(self, lane_centers, current_route_type):
        self.lane_centers = lane_centers
        self.obstacles = pygame.sprite.Group()
        self.decorations = []
        self.distance_traveled = 0
        self.current_route_type = current_route_type

        # Для разметки
        self.line_y_positions = [
            y for y in range(
                -C.WINDOW_HEIGHT,
                C.WINDOW_HEIGHT,
                C.ROAD_LINE_LENGTH + C.ROAD_LINE_GAP
            )
        ]

        # Геометрия дороги
        self.road_width = C.WINDOW_WIDTH * C.ROAD_WIDTH_RATIO
        self.road_x = (C.WINDOW_WIDTH - self.road_width) / 2
        self.road_rect = pygame.Rect(self.road_x, 0,
                                     self.road_width, C.WINDOW_HEIGHT)
        self.left_border = self.road_x
        self.right_border = self.road_x + self.road_width

        # Для появления препятствий
        self.obstacle_spawn_timer = 0.0
        # Для появления декораций
        self.decoration_spawn_timer = 0.0

        self._initial_spawn_decorations()

    def reset(self, current_route_type):
        """Сброс состояния дороги для новой игры."""
        self.obstacles.empty()
        self.decorations.clear()
        self.distance_traveled = 0
        self.obstacle_spawn_timer = 1.0 / C.OBSTACLE_SPAWN_RATE
        self.decoration_spawn_timer = 0.0
        self.current_route_type = current_route_type
        self._initial_spawn_decorations()

    def _initial_spawn_decorations(self):
        """Создает начальный набор декораций для заполнения экрана."""
        y_step = C.DECORATION_INITIAL_SPAWN_INTERVAL
        start_y = C.WINDOW_HEIGHT + 200

        current_y = start_y
        while current_y > C.DECORATION_MIN_Y_SPAWN - 200:
            num_decorations_at_y = random.randint(5, 10)
            for _ in range(num_decorations_at_y):
                # Небольшая случайность по Y
                self._spawn_decoration(current_y +
                                       random.uniform(-y_step/2, y_step/2))
            current_y -= y_step

    def update(self, dt, player_speed):
        """Обновление состояния дороги, препятствий и декораций."""
        self.distance_traveled += player_speed * dt
        self._update_road_lines(dt, player_speed)
        self._update_obstacle_spawning(dt)
        self._update_decoration_spawning(dt, player_speed)

        self.obstacles.update(dt, player_speed)

        # Обновление и удаление декораций
        for decor in list(self.decorations):
            decor.update(dt, player_speed)
            # Максимальная высота маленького камня
            max_decor_height = (max(C.SMALL_STONE_SIZE_RANGE) *
                                C.SMALL_STONE_ASPECT_RATIO_VARIATION[1])
            if decor.y > C.WINDOW_HEIGHT + max_decor_height:
                self.decorations.remove(decor)

    def _update_road_lines(self, dt, player_speed):
        """Движение дорожной разметки."""
        for i in range(len(self.line_y_positions)):
            self.line_y_positions[i] += player_speed * dt
            if self.line_y_positions[i] > C.WINDOW_HEIGHT:
                # Перемещение линии вверх
                self.line_y_positions[i] -= (C.WINDOW_HEIGHT +
                                             C.ROAD_LINE_LENGTH +
                                             C.ROAD_LINE_GAP)

    def _update_obstacle_spawning(self, dt):
        """Логика появления новых препятствий."""
        self.obstacle_spawn_timer -= dt
        if self.obstacle_spawn_timer <= 0:
            self.obstacle_spawn_timer = 1.0 / C.OBSTACLE_SPAWN_RATE
            self._spawn_obstacle()

    def _spawn_obstacle(self):
        """Создает и добавляет новое препятствие на случайную полосу."""
        lane_x = random.choice(self.lane_centers)

        # Если маршрут "long", появляются только люки
        if self.current_route_type == 'long':
            obstacle = Manhole(lane_x)
        else:
            if random.random() < C.CAR_SPAWN_CHANCE:
                obstacle = OncomingCar(lane_x)
            else:
                obstacle = Manhole(lane_x)

        for existing_obstacle in self.obstacles:
            if abs(existing_obstacle.rect.bottom - obstacle.rect.bottom) < 200:
                return

        self.obstacles.add(obstacle)

    def _update_decoration_spawning(self, dt, player_speed):
        """Логика появления новых декоративных элементов на газоне."""
        if random.random() < C.DECORATION_SPAWN_CHANCE_PER_FRAME:
            self._spawn_decoration()

    def _spawn_decoration(self, spawn_y=None):
        """Создает и добавляет новый декоративный элемент на газон."""
        decor_type = 'small_stone'

        side = random.randint(0, 1)

        # Определяем диапазон X-координат для спавна на газоне
        if side == 0:  # Левый газон
            x_min = C.WINDOW_WIDTH * C.DECORATION_SIDE_MARGIN_PERCENT
            x_max = (self.left_border -
                     C.WINDOW_WIDTH * C.DECORATION_SIDE_MARGIN_PERCENT)
        else:  # Правый газон
            x_min = (self.right_border +
                     C.WINDOW_WIDTH * C.DECORATION_SIDE_MARGIN_PERCENT)
            x_max = (C.WINDOW_WIDTH -
                     C.WINDOW_WIDTH * C.DECORATION_SIDE_MARGIN_PERCENT)

        x = random.uniform(x_min, x_max)
        y = (spawn_y if spawn_y is not None else
             random.uniform(C.DECORATION_MIN_Y_SPAWN, 0))

        draw_data = {}
        # Логика для 'small_stone'
        if decor_type == 'small_stone':
            base_size = random.randint(C.SMALL_STONE_SIZE_RANGE[0],
                                       C.SMALL_STONE_SIZE_RANGE[1])
            aspect_ratio = random.uniform(
                C.SMALL_STONE_ASPECT_RATIO_VARIATION[0],
                C.SMALL_STONE_ASPECT_RATIO_VARIATION[1])

            # Случайно выбираем, будет ли камень шире или выше
            if random.random() < 0.5:
                draw_data['stone_width'] = base_size
                draw_data['stone_height'] = int(base_size * aspect_ratio)
            else:
                draw_data['stone_width'] = int(base_size * aspect_ratio)
                draw_data['stone_height'] = base_size

            draw_data['stone_color'] = random.choice(C.SMALL_STONE_COLORS)
            new_decoration = DecorativeElement('small_stone', x, y, draw_data)

        self.decorations.append(new_decoration)

    def remove_obstacle(self, obstacle):
        self.obstacles.remove(obstacle)

    def draw(self, screen):
        """Отрисовка дороги, разметки, препятствий и декораций."""
        # Фон (трава)
        screen.fill(C.COLOR_GREEN_GRASS)

        # Отрисовка декораций
        for decor in sorted(self.decorations, key=lambda d: d.y):
            # Максимальная высота маленького камня для корректного
            # удаления/появления
            max_decor_height = (max(C.SMALL_STONE_SIZE_RANGE) *
                                C.SMALL_STONE_ASPECT_RATIO_VARIATION[1])
            if (decor.y < C.WINDOW_HEIGHT + max_decor_height and
                    decor.y > C.DECORATION_MIN_Y_SPAWN - max_decor_height):
                decor.draw(screen)

        # Дорога
        pygame.draw.rect(screen, C.COLOR_GRAY_ROAD, self.road_rect)

        # Разметка
        line_x1 = self.left_border + self.road_width / 3
        line_x2 = self.left_border + self.road_width * 2 / 3

        for y_pos in self.line_y_positions:
            start_pos1 = (line_x1, y_pos)
            end_pos1 = (line_x1, y_pos + C.ROAD_LINE_LENGTH)
            pygame.draw.line(screen, C.COLOR_WHITE, start_pos1, end_pos1,
                             C.ROAD_LINE_WIDTH)

            start_pos2 = (line_x2, y_pos)
            end_pos2 = (line_x2, y_pos + C.ROAD_LINE_LENGTH)
            pygame.draw.line(screen, C.COLOR_WHITE, start_pos2, end_pos2,
                             C.ROAD_LINE_WIDTH)

        # Препятствия
        self.obstacles.draw(screen)
