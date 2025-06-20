import pygame

# Настройки игры
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
GAME_TITLE = "Food Rush"
FPS = 60

# Состояния игры


class GameState:
    MENU = "MENU"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    DELIVERY_ANIMATION = "DELIVERY_ANIMATION"
    POST_GAME_SUMMARY = "POST_GAME_SUMMARY"
    REVIVE_MINIGAME = "REVIVE_MINIGAME"
    GAME_OVER_SCREEN = "GAME_OVER_SCREEN"


# Цвета
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (220, 50, 50)
COLOR_GREEN = (50, 200, 50)
COLOR_GOLD = (255, 215, 0)
COLOR_BLUE = (100, 149, 237)
COLOR_BLUE_SKY = (135, 206, 235)
COLOR_GRAY_ROAD = (40, 40, 45)
COLOR_GREEN_GRASS = (34, 139, 34)
COLOR_UI_BG = (40, 40, 50, 200)

# UI Элементы
BUTTON_COLOR = (80, 80, 100)
BUTTON_HOVER_COLOR = (110, 110, 130)
BUTTON_DISABLED_COLOR = (60, 60, 60)
PAUSE_OVERLAY_COLOR = (0, 0, 0, 170)

# Мини-игра "Лабиринт"
MINIGAME_WALL_COLOR = (50, 50, 60)
MINIGAME_PATH_COLOR = (120, 120, 130)
MINIGAME_PLAYER_COLOR = COLOR_GREEN
MINIGAME_TARGET_COLOR = COLOR_RED
MINIGAME_PATHFIND_COLOR = (70, 130, 180)

# Размер шрифтов
FONT_PATH = None
FONT_SIZE_TITLE = 74
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 36
FONT_SIZE_SMALL = 28

# Путь к ресурсам
ASSETS_DIR = 'assets'
SAVES_DIR = 'saves'
PROGRESS_FILE = 'progress.json'

# Спрайты и звуки
IMG_BACKGROUND = 'background.png'
IMG_PLAYER = 'player.png'
IMG_MANHOLE = 'manhole.png'
IMG_LIFE = 'life.png'
SND_MOVE = 'move.wav'
SND_COLLISION = 'collision.wav'
SND_ORDER_FAILED = 'order_failed.wav'
SND_ORDER_COMPLETED = 'order_completed.wav'
MSC_MENU = 'menu_music.mp3'
MSC_GAME = 'game_music.mp3'

# Кадры для анимации успешной доставки
IMG_DELIVERY_PLAYER_FRAMES = ['player2.png', 'player3.png']
DELIVERY_PLAYER_SIZE = (80, 80)

# Настройки игрока
PLAYER_WIDTH = 160
PLAYER_HEIGHT = 160
PLAYER_MAX_ENERGY = 100.0
PLAYER_ENERGY_REGEN_RATE = 6.0
PLAYER_ENERGY_DRAIN_RATE = 24.0
PLAYER_BASE_SPEED = 350.0
PLAYER_ACCELERATION = 10.0
PLAYER_DECELERATION = 12.0
PLAYER_BOOST_MULTIPLIER = 1.5

# Настройки дороги
ROAD_WIDTH_RATIO = 0.6
LANE_1_POS_RATIO = 0.165
LANE_2_POS_RATIO = 0.5
LANE_3_POS_RATIO = 0.835
ROAD_LINE_WIDTH = 10
ROAD_LINE_LENGTH = 70
ROAD_LINE_GAP = 50

# Настройки препятствий
OBSTACLE_SPAWN_RATE = 1.2
CAR_SPAWN_CHANCE = 0.7
CAR_WIDTH = 80
CAR_HEIGHT = 150
MANHOLE_SIZE = 100
MANHOLE_OPEN_Y_THRESHOLD_RATIO = 0.4
MANHOLE_TRANSITION_SPEED = 2.5
MANHOLE_OPEN_OFFSET_MULTIPLIER = 0.3
MANHOLE_DIAGONAL_OFFSET_FACTOR = 0.1

# Настройки анимации успешной доставки
DELIVERY_ANIMATION_DURATION = 3.5
DELIVERY_ANIMATION_FRAME_DURATION = 0.1

# Настройки мини-игры "Лабиринт"
MINIGAME_ROWS = 15
MINIGAME_COLS = 20
MINIGAME_CELL_SIZE = 30
MINIGAME_MOVE_DELAY = 0.15

# Настройки Магазина и Транспорта
VEHICLES = {
    'bicycle': {'name': 'Велосипед', 'speed_multiplier': 1.0,
                'lives': 3, 'price': 0},
    'scooter': {'name': 'Скутер', 'speed_multiplier': 1.2,
                'lives': 4, 'price': 1000},
    'motorcycle': {'name': 'Мотоцикл', 'speed_multiplier': 1.5,
                   'lives': 5, 'price': 2000}
}

# Настройки декораций на газоне
DECORATION_SPAWN_CHANCE_PER_FRAME = 0.15
DECORATION_MIN_Y_SPAWN = -200
DECORATION_INITIAL_SPAWN_INTERVAL = 40

# Определение типов декораций
DECORATION_TYPES = {
    'small_stone': {},
}

# Параметры для создания камней на газоне
SMALL_STONE_COLORS = [(70, 70, 70), (90, 90, 90), (110, 110, 110)]
SMALL_STONE_SIZE_RANGE = (10, 25)
SMALL_STONE_ASPECT_RATIO_VARIATION = (0.7, 1.3)

# Границы для появления декораций на газоне
DECORATION_SIDE_MARGIN_PERCENT = 0.02
