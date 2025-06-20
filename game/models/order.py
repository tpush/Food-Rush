from dataclasses import dataclass
import random


@dataclass
class Order:
    """Простая структура для хранения данных о заказе."""
    name: str
    reward: int
    base_distance: int


class OrderManager:
    """Управляет созданием, выбором и параметрами заказов."""

    _POSSIBLE_ORDERS = [
        Order("Пицца 'Пепперони'", 100, 20000),
        Order("Набор 'Филадельфия'", 150, 25000),
        Order("Двойной чизбургер", 80, 18000),
        Order("Капучино на кокосовом", 50, 15000),
        Order("Шоколадный торт", 200, 30000),
        Order("Вок с курицей", 120, 22000),
    ]

    def __init__(self):
        self.available_orders = []
        self.selected_order = None
        self.selected_route_type = None
        self.generate_new_orders()

    def generate_new_orders(self, count=3):
        """Генерирует новый список доступных заказов."""
        self.available_orders = random.sample(
            self._POSSIBLE_ORDERS, min(count, len(self._POSSIBLE_ORDERS)))
        self.selected_order = None
        self.selected_route_type = None

    def select_order(self, order_index):
        if 0 <= order_index < len(self.available_orders):
            self.selected_order = self.available_orders[order_index]

    def select_route(self, route_type):
        if route_type in ['short', 'long']:
            self.selected_route_type = route_type

    def get_final_parameters(self):
        """Возвращает итоговые параметры заказа с учетом маршрута."""
        if not self.selected_order or not self.selected_route_type:
            return None

        if self.selected_route_type == 'long':
            distance = self.selected_order.base_distance * 1.5
            reward = self.selected_order.reward * 1.0
        else:
            distance = self.selected_order.base_distance * 0.7
            reward = self.selected_order.reward * 2.0

        return int(distance), int(reward)
