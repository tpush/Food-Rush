import pygame
from .. import constants as C
from ..services.asset_loader import AssetLoader


class Player(pygame.sprite.Sprite):
    """Класс игрока. Управляет состоянием, движением и взаимодействием."""

    def __init__(self, lane_centers):
        super().__init__()

        self.image = AssetLoader.get_image(C.IMG_PLAYER,
                                           (C.PLAYER_WIDTH, C.PLAYER_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.lane_centers = lane_centers
        self.target_x = self.lane_centers[1]
        self.rect.centerx = self.target_x
        self.rect.bottom = C.WINDOW_HEIGHT - 20

        self._setup_initial_state()
        self.reset_stats()

    def _setup_initial_state(self):
        """Инициализирует состояние, не зависящее от транспорта."""
        self.current_lane_index = 1
        self.rect.centerx = self.lane_centers[self.current_lane_index]
        self.target_x = self.rect.centerx

        self.speed = 0.0
        self.energy = C.PLAYER_MAX_ENERGY
        self.is_boosting = False
        self.is_braking = False
        self.alive = True

    def reset_stats(self, vehicle_stats=C.VEHICLES['bicycle']):
        """Сбрасывает характеристики игрока на основе данных о транспорте."""
        self.base_speed = C.PLAYER_BASE_SPEED * \
            vehicle_stats['speed_multiplier']
        self.lives = vehicle_stats['lives']
        self.max_lives = vehicle_stats['lives']
        self._setup_initial_state()

    def handle_input(self, event):
        """Обрабатывает ввод, относящийся к игроку."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self._move_lane(-1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self._move_lane(1)

        keys = pygame.key.get_pressed()
        self.is_boosting = keys[pygame.K_UP] or keys[pygame.K_w]
        self.is_braking = keys[pygame.K_DOWN] or keys[pygame.K_s]

    def _move_lane(self, direction):
        """Логика смены полосы движения."""
        new_lane = self.current_lane_index + direction
        if 0 <= new_lane < len(self.lane_centers):
            self.current_lane_index = new_lane
            self.target_x = self.lane_centers[self.current_lane_index]
            AssetLoader.play_sound(C.SND_MOVE)

    def update(self, dt):
        """Обновляет состояние игрока."""
        if not self.alive:
            return

        self._update_speed(dt)
        self._update_energy(dt)
        self._update_horizontal_position(dt)

    def _update_speed(self, dt):
        """Плавное обновление скорости игрока."""
        target_speed = self.base_speed
        if self.is_boosting and self.energy > 0:
            target_speed = self.base_speed * C.PLAYER_BOOST_MULTIPLIER
        elif self.is_braking:
            target_speed = 0

        if self.speed < target_speed:
            self.speed = min(target_speed,
                             self.speed + C.PLAYER_ACCELERATION * 10 * dt)
        elif self.speed > target_speed:
            self.speed = max(target_speed,
                             self.speed - C.PLAYER_DECELERATION * 10 * dt)

    def _update_energy(self, dt):
        """Обновление энергии."""
        if self.is_boosting and self.energy > 0:
            self.energy = max(0,
                              self.energy - C.PLAYER_ENERGY_DRAIN_RATE * dt)
            if self.energy == 0:
                self.is_boosting = False
        else:
            self.energy = min(C.PLAYER_MAX_ENERGY,
                              self.energy + C.PLAYER_ENERGY_REGEN_RATE * dt)

    def _update_horizontal_position(self, dt):
        """Плавное перемещение между полосами."""
        move_speed = 800 * dt
        dx = self.target_x - self.rect.centerx
        if abs(dx) < move_speed:
            self.rect.centerx = self.target_x
        else:
            self.rect.centerx += move_speed * (1 if dx > 0 else -1)

    def take_damage(self):
        """Обработка получения урона."""
        self.lives -= 1
        self.speed *= 0.5
        AssetLoader.play_sound(C.SND_COLLISION)
        return self.lives > 0

    def die(self):
        self.alive = False

    def revive(self):
        """Восстанавливает игрока для мини-игры."""
        self.lives = 1
        self.alive = True
