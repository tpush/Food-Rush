import pygame
from .. import constants as C
from ..services.asset_loader import AssetLoader


class Button:
    """Простой UI-элемент."""

    def __init__(self, rect, text, font, action=None, disabled=False):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.action = action
        self.disabled = disabled
        self.is_hovered = False

    def draw(self, screen):
        color = (C.BUTTON_DISABLED_COLOR if self.disabled else
                 (C.BUTTON_HOVER_COLOR if self.is_hovered else C.BUTTON_COLOR))
        pygame.draw.rect(screen, color, self.rect, border_radius=10)

        text_surf = self.font.render(self.text, True, C.COLOR_WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        """Обработка событий для кнопки."""
        if self.disabled:
            return None
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and \
           event.button == 1 and self.is_hovered:
            AssetLoader.play_sound('click.wav')
            return self.action
        return None


class MenuView:
    """Обработка отображения различных меню игры."""

    def __init__(self, progress_manager, order_manager):
        self.progress = progress_manager
        self.orders = order_manager
        self.state = 'main'
        self.background = AssetLoader.get_image(C.IMG_BACKGROUND,
                                                (C.WINDOW_WIDTH,
                                                 C.WINDOW_HEIGHT))

        self.font_title = AssetLoader.get_font(C.FONT_SIZE_TITLE)
        self.font_reg = AssetLoader.get_font(C.FONT_SIZE_LARGE)
        self.font_med = AssetLoader.get_font(C.FONT_SIZE_MEDIUM)
        self.font_small = AssetLoader.get_font(C.FONT_SIZE_SMALL)

        self.ui_elements = {}
        self.game_over_text = None
        self._set_state('main')

    def _set_state(self, new_state, revive_available=False):
        """Установка текущего состояния меню и генерация его элементов."""
        self.state = new_state
        self.ui_elements.clear()

        if self.state == 'main':
            self._create_main_menu()
        elif self.state == 'shop':
            self._create_shop_menu()
        elif self.state == 'orders':
            self._create_orders_menu()
        elif self.state == 'route':
            self._create_route_menu()
        elif self.state == 'game_over':
            self._create_game_over_menu(revive_available)

    def _create_main_menu(self):
        """Создание кнопок для главного меню."""
        self.ui_elements['btn_start'] = Button(
            (C.WINDOW_WIDTH/2 - 150, 300, 300, 70), "Начать",
            self.font_reg, 'go_to_orders')
        self.ui_elements['btn_shop'] = Button(
            (C.WINDOW_WIDTH/2 - 150, 400, 300, 70), "Магазин",
            self.font_reg, 'go_to_shop')
        self.ui_elements['btn_quit'] = Button(
            (C.WINDOW_WIDTH/2 - 150, 500, 300, 70), "Выход",
            self.font_reg, 'quit')

    def _create_shop_menu(self):
        """Создание кнопок для магазина транспорта."""
        start_x = C.WINDOW_WIDTH/2 - (len(C.VEHICLES) * 300 - 50) / 2
        for i, (key, data) in enumerate(C.VEHICLES.items()):
            is_owned = self.progress.vehicles.get(key, False)
            is_current = self.progress.current_vehicle == key

            btn_text = ("Выбрано" if is_current else
                        ("Выбрать" if is_owned else f"Купить ({data['price']})"))
            disabled = is_current or \
                (not is_owned and self.progress.coins < data['price'])

            self.ui_elements[f'btn_veh_{key}'] = Button(
                (start_x + i*300, 450, 250, 60), btn_text,
                self.font_med, f"select_{key}", disabled)

        self.ui_elements['btn_back'] = Button(
            (C.WINDOW_WIDTH/2-125, 600, 250, 60), "Назад",
            self.font_reg, 'go_to_main')

    def _create_orders_menu(self):
        """Создание кнопок для выбора заказов."""
        for i, order in enumerate(self.orders.available_orders):
            self.ui_elements[f'btn_order_{i}'] = Button(
                (C.WINDOW_WIDTH/2-250, 250 + i*100, 500, 80),
                order.name, self.font_med, f"order_{i}")
        self.ui_elements['btn_back'] = Button(
            (C.WINDOW_WIDTH/2-125, 600, 250, 60), "Назад",
            self.font_reg, 'go_to_main')

    def _create_route_menu(self):
        """Создание кнопок для выбора маршрута."""
        if self.orders.selected_order:
            base_distance = self.orders.selected_order.base_distance
            base_reward = self.orders.selected_order.reward

            route_button_width = 450
            route_button_height = 120

            dist_short = int(base_distance * 0.7)
            reward_short = int(base_reward * 2.0)

            dist_long = int(base_distance * 1.5)
            reward_long = int(base_reward * 1.0)

            self.ui_elements['btn_short'] = Button(
                (C.WINDOW_WIDTH/2 - route_button_width - 20,
                 350, route_button_width, route_button_height),
                f"Короткий: {dist_short/1000:.1f}км, {reward_short} монет",
                self.font_med, 'route_short'
            )
            self.ui_elements['btn_long'] = Button(
                (C.WINDOW_WIDTH/2 + 20, 350,
                 route_button_width, route_button_height),
                f"Длинный: {dist_long/1000:.1f}км, {reward_long} монет",
                self.font_med, 'route_long'
            )
        else:
            self._set_state('orders')
            return

        self.ui_elements['btn_back'] = Button(
            (C.WINDOW_WIDTH/2-125, 600, 250, 60), "К заказам",
            self.font_reg, 'go_to_orders')

    def _create_game_over_menu(self, revive_available):
        """Создание кнопок для экрана 'Игра окончена'."""
        self.game_over_text = self.font_title.render("ЗАКАЗ ПРОВАЛЕН!",
                                                     True, C.COLOR_RED)

        button_width = 450
        button_height = 90

        revive_btn_y = C.WINDOW_HEIGHT/2 - 50
        self.ui_elements['btn_revive'] = Button(
            (C.WINDOW_WIDTH/2 - button_width/2, revive_btn_y,
             button_width, button_height),
            "Возродиться (мини-игра)",
            self.font_reg,
            'start_minigame',
            disabled=not revive_available
        )

        menu_btn_y = C.WINDOW_HEIGHT/2 + 50
        self.ui_elements['btn_go_to_main'] = Button(
            (C.WINDOW_WIDTH/2 - button_width/2, menu_btn_y,
             button_width, button_height),
            "Меню",
            self.font_reg,
            'go_to_main'
        )

    def handle_event(self, event):
        """Обработка ввода пользователя в меню."""
        action = None
        for element in self.ui_elements.values():
            if isinstance(element, Button):
                result = element.handle_event(event)
                if result:
                    action = result
                    break

        if not action:
            return None

        if action == 'quit':
            return 'quit'
        if action == 'go_to_main':
            self._set_state('main')
            return action
        if action == 'go_to_shop':
            self._set_state('shop')
        if action == 'go_to_orders':
            self._set_state('orders')

        if action.startswith('select_'):
            key = action.split('_')[1]
            if not self.progress.vehicles.get(key, False):
                self.progress.buy_vehicle(key)
            else:
                self.progress.current_vehicle = key
            self.progress.save()
            self._set_state('shop')

        if action.startswith('order_'):
            idx = int(action.split('_')[1])
            self.orders.select_order(idx)
            self._set_state('route')

        if action.startswith('route_'):
            route_type = action.split('_')[1]
            self.orders.select_route(route_type)
            return 'start_game'

        if action == 'start_minigame':
            return action

        return None

    def draw(self, screen):
        """Отрисовка текущего меню на экране."""
        screen.blit(self.background, (0, 0))

        if self.state not in ['game_over']:
            title_surf = self.font_title.render(C.GAME_TITLE,
                                                True, C.COLOR_WHITE)
            screen.blit(title_surf,
                        title_surf.get_rect(centerx=C.WINDOW_WIDTH/2, y=50))

            coins_surf = self.font_reg.render(f"Монеты: {self.progress.coins}",
                                              True, C.COLOR_GOLD)
            screen.blit(coins_surf,
                        coins_surf.get_rect(right=C.WINDOW_WIDTH-20, top=20))

        if self.state == 'shop':
            self._draw_shop_details(screen)
        elif self.state == 'orders':
            order_title_surf = self.font_reg.render("Выберите заказ:",
                                                    True, C.COLOR_WHITE)
            screen.blit(order_title_surf,
                        order_title_surf.get_rect(centerx=C.WINDOW_WIDTH/2,
                                                  y=180))
        elif self.state == 'route':
            self._draw_route_details(screen)
        elif self.state == 'game_over':
            if self.game_over_text:
                text_rect = self.game_over_text.get_rect(
                    center=(C.WINDOW_WIDTH/2, C.WINDOW_HEIGHT/2 - 150))
                screen.blit(self.game_over_text, text_rect)

            coins_surf = self.font_reg.render(
                f"Итого монет: {self.progress.coins}", True, C.COLOR_GOLD)
            screen.blit(coins_surf,
                        coins_surf.get_rect(centerx=C.WINDOW_WIDTH/2,
                                            y=C.WINDOW_HEIGHT/2 - 100))

        for element in self.ui_elements.values():
            if isinstance(element, Button):
                element.draw(screen)

    def _draw_shop_details(self, screen):
        """Отрисовка деталей магазина."""
        start_x = C.WINDOW_WIDTH/2 - (len(C.VEHICLES) * 300 - 50) / 2
        for i, (key, data) in enumerate(C.VEHICLES.items()):
            name_surf = self.font_med.render(data['name'], True, C.COLOR_WHITE)
            screen.blit(name_surf,
                        name_surf.get_rect(centerx=start_x + i*300 + 125,
                                           y=300))

    def _draw_route_details(self, screen):
        """Отрисовка деталей выбора маршрута."""
        if self.orders.selected_order:
            order_name = self.orders.selected_order.name
            title = self.font_reg.render(f"Заказ: {order_name}", True,
                                         C.COLOR_WHITE)
            screen.blit(title,
                        title.get_rect(centerx=C.WINDOW_WIDTH/2, y=200))
