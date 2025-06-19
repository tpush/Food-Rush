import pygame
from game import constants as C
from .services.progress_manager import ProgressManager
from .services.asset_loader import AssetLoader
from .models.player import Player
from .models.road import Road
from .models.order import OrderManager
from .views.menu_view import MenuView
from .views.hud_view import HUDView
from .views.animation_view import DeliveryAnimationView
from .views.minigame.minigame_view import MinigameView


class GameManager:
    """Управляет общим состоянием игры."""

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.game_state = C.GameState.MENU

        # Инициализация сервисов
        self.progress_manager = ProgressManager()
        self.order_manager = OrderManager()

        road_width = C.WINDOW_WIDTH * C.ROAD_WIDTH_RATIO
        road_left = (C.WINDOW_WIDTH - road_width) / 2
        self.lane_centers = [
            road_left + road_width * C.LANE_1_POS_RATIO,
            road_left + road_width * C.LANE_2_POS_RATIO,
            road_left + road_width * C.LANE_3_POS_RATIO
        ]

        # Инициализация моделей
        self.player = Player(self.lane_centers)
        self.road = Road(self.lane_centers, None)

        # Инициализация представлений
        self.menu_view = MenuView(self.progress_manager, self.order_manager)
        self.hud_view = HUDView()
        self.animation_view = DeliveryAnimationView()
        self.minigame_view = MinigameView()

        self.current_order_distance = 0
        self.current_order_reward = 0

        self.revive_available = True

        AssetLoader.play_music(C.MSC_MENU)

    def run(self):
        """Основной игровой цикл."""
        while self.running:
            dt = self.clock.tick(C.FPS) / 1000.0

            self.handle_events()
            self.update(dt)
            self.draw(self.screen)

            pygame.display.flip()

    def handle_events(self):
        """Обрабатывает события игры."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.game_state == C.GameState.PLAYING:
                    self.game_state = C.GameState.PAUSED
                elif self.game_state == C.GameState.PAUSED:
                    self.game_state = C.GameState.PLAYING

            if self.game_state == C.GameState.MENU:
                action = self.menu_view.handle_event(event)
                if action == 'quit':
                    self.running = False
                elif action == 'start_game':
                    self.start_new_game()

            elif self.game_state == C.GameState.PLAYING:
                self.player.handle_input(event)

            elif self.game_state == C.GameState.REVIVE_MINIGAME:
                result = self.minigame_view.handle_event(event)
                if result == 'win':
                    self.player.revive()
                    self.game_state = C.GameState.PLAYING
                    AssetLoader.play_music(C.MSC_GAME)
                elif result == 'lose':
                    self.end_game(success=False)

            elif self.game_state == C.GameState.GAME_OVER_SCREEN:
                action = self.menu_view.handle_event(event)
                if action == 'start_minigame':
                    self.revive_available = False
                    self.minigame_view.start()
                    self.game_state = C.GameState.REVIVE_MINIGAME
                elif action == 'go_to_main':
                    self.game_state = C.GameState.MENU
                    self.menu_view._set_state('main')

    def update(self, dt):
        """Обновление логики игры в зависимости от состояния."""
        if self.game_state == C.GameState.PLAYING:
            self.player.update(dt)
            self.road.update(dt, self.player.speed)
            self._check_collisions()

            if self.road.distance_traveled >= self.current_order_distance:
                self.end_game(success=True)

        elif self.game_state == C.GameState.REVIVE_MINIGAME:
            self.minigame_view.update(dt)

        elif self.game_state == C.GameState.DELIVERY_ANIMATION:
            if self.animation_view.update(dt):
                self.game_state = C.GameState.MENU
                self.menu_view._set_state('main')
                AssetLoader.play_music(C.MSC_MENU)

    def _check_collisions(self):
        """Проверяет столкновения игрока с препятствиями."""
        collided_obstacle = pygame.sprite.spritecollideany(
            self.player, self.road.obstacles, pygame.sprite.collide_mask)
        if collided_obstacle:
            if hasattr(collided_obstacle, 'is_open') and \
               not collided_obstacle.is_open:
                return

            self.road.remove_obstacle(collided_obstacle)
            if not self.player.take_damage():
                AssetLoader.play_sound(C.SND_COLLISION)
                AssetLoader.play_music(C.MSC_MENU)

                if self.revive_available:
                    self.game_state = C.GameState.GAME_OVER_SCREEN
                    self.menu_view._set_state('game_over',
                                              revive_available=True)
                else:
                    self.end_game(success=False)

    def draw(self, screen):
        """Отрисовка всего на экране."""
        self.screen.fill(C.COLOR_GREEN_GRASS)

        if self.game_state == C.GameState.MENU:
            self.menu_view.draw(self.screen)

        elif self.game_state in [C.GameState.PLAYING, C.GameState.PAUSED]:
            self.road.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)
            self.hud_view.draw(self.screen, self.player,
                               self.current_order_distance -
                               self.road.distance_traveled,
                               self.current_order_reward,
                               self.progress_manager.coins)
            if self.game_state == C.GameState.PAUSED:
                self._draw_pause_overlay()

        elif self.game_state == C.GameState.REVIVE_MINIGAME:
            self.minigame_view.draw(self.screen)

        elif self.game_state == C.GameState.DELIVERY_ANIMATION:
            self.animation_view.draw(self.screen)

        elif self.game_state == C.GameState.GAME_OVER_SCREEN:
            self.menu_view.draw(self.screen)

    def start_new_game(self):
        """Создание нового заезда."""
        self.revive_available = True
        params = self.order_manager.get_final_parameters()
        if not params or params[0] is None:
            self.game_state = C.GameState.MENU
            return
        self.current_order_distance, self.current_order_reward = params

        self.road.reset(self.order_manager.selected_route_type)
        self.player.reset_stats(self.progress_manager.
                                get_current_vehicle_stats())

        self.game_state = C.GameState.PLAYING
        AssetLoader.play_music(C.MSC_GAME)

    def end_game(self, success):
        """Завершает игру, обрабатывая результат."""
        if success:
            self.progress_manager.add_coins(self.current_order_reward)
            AssetLoader.play_sound(C.SND_ORDER_COMPLETED)
            self.animation_view.start()
            self.game_state = C.GameState.DELIVERY_ANIMATION
        else:
            AssetLoader.play_sound(C.SND_ORDER_FAILED)
            self.game_state = C.GameState.GAME_OVER_SCREEN
            self.menu_view._set_state('game_over', revive_available=False)
            AssetLoader.play_music(C.MSC_MENU)

    def _draw_pause_overlay(self):
        """Отрисовка затемнения во время паузы."""
        overlay = pygame.Surface((C.WINDOW_WIDTH, C.WINDOW_HEIGHT),
                                 pygame.SRCALPHA)
        overlay.fill(C.PAUSE_OVERLAY_COLOR)
        self.screen.blit(overlay, (0, 0))

        font = AssetLoader.get_font(C.FONT_SIZE_TITLE)
        pause_text = font.render("ПАУЗА", True, C.COLOR_WHITE)
        text_rect = pause_text.get_rect(center=(C.WINDOW_WIDTH / 2,
                                                C.WINDOW_HEIGHT / 2))
        self.screen.blit(pause_text, text_rect)
