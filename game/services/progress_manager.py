import json
import os
from .. import constants as C


class ProgressManager:
    """Управляет сохранением и загрузкой игрового прогресса."""

    def __init__(self):
        self.filepath = os.path.join(C.SAVES_DIR, C.PROGRESS_FILE)
        self.coins = 0
        self.vehicles = {key: data['price'] == 0
                         for key, data in C.VEHICLES.items()}
        self.current_vehicle = 'bicycle'
        self._ensure_saves_dir()
        self.load()

    def _ensure_saves_dir(self):
        """Убеждается, что директория для сохранений существует."""
        if not os.path.exists(C.SAVES_DIR):
            os.makedirs(C.SAVES_DIR)

    def load(self):
        """Загружает прогресс из JSON-файла."""
        if not os.path.exists(self.filepath):
            self.save()
            return

        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                self.coins = data.get('coins', 0)
                loaded_vehicles = data.get('vehicles', {})
                for key in C.VEHICLES:
                    self.vehicles[key] = loaded_vehicles.get(
                        key, C.VEHICLES[key]['price'] == 0)
                self.current_vehicle = data.get('current_vehicle', 'bicycle')
        except (json.JSONDecodeError, IOError, TypeError) as e:
            print(f"Ошибка загрузки прогресса '{self.filepath}': {e}. "
                  "Создается новый файл.")
            self.reset_and_save()

    def save(self):
        """Сохраняет текущий прогресс в JSON-файл."""
        data = {
            'coins': self.coins,
            'vehicles': self.vehicles,
            'current_vehicle': self.current_vehicle
        }
        try:
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Ошибка сохранения прогресса '{self.filepath}': {e}")

    def reset_and_save(self):
        """Сбрасывает прогресс к значениям по умолчанию и сохраняет."""
        self.coins = 0
        self.vehicles = {key: data['price'] == 0
                         for key, data in C.VEHICLES.items()}
        self.current_vehicle = 'bicycle'
        self.save()

    def add_coins(self, amount):
        """Добавляет монеты к прогрессу игрока."""
        if amount > 0:
            self.coins += amount
            self.save()

    def spend_coins(self, amount):
        """Тратит монеты игрока."""
        if self.coins >= amount:
            self.coins -= amount
            self.save()
            return True
        return False

    def buy_vehicle(self, vehicle_key):
        """Покупает транспортное средство, если у игрока достаточно монет."""
        if vehicle_key not in C.VEHICLES:
            return False

        price = C.VEHICLES[vehicle_key]['price']
        if not self.vehicles.get(vehicle_key, False) and \
           self.spend_coins(price):
            self.vehicles[vehicle_key] = True
            self.current_vehicle = vehicle_key
            self.save()
            return True
        return False

    def get_current_vehicle_stats(self):
        """Возвращает характеристики текущего выбранного транспорта."""
        return C.VEHICLES[self.current_vehicle]
