import pygame

# Константы для определения размера экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Цвета
SKY_COLOR = (135, 206, 235) # Небо (голубой цвет)
ROAD_COLOR = (50, 50, 50) # Дорога (тёмно-серый цвет)
PLAYER_COLOR = (255, 0, 0) # Игрок (красный цвет)
OBSTACLE_COLORS = {
  "manhole": (0, 0, 255), # Люк (синий цвет)
  "car": (255, 255, 0) # Машина (жёлтый цвет)
}

# Размеры объектов
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
OBSTACLE_SIZE = 50

# Позиции полос
LANE_POSITIONS = [200, 400, 600] # Координаты для расположения трёх полос

# Скорости (для дальнейшего усовершенствования программы)
PLAYER_SPEED = 10
OBSTACLE_SPEED = 5
