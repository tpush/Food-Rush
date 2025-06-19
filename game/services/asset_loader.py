import pygame
import os
from .. import constants as C


class AssetLoader:
    _images = {}
    _sounds = {}
    _fonts = {}
    _is_initialized = False

    @staticmethod
    def initialize():
        """Инициализирует микшер и шрифты Pygame."""
        if not AssetLoader._is_initialized:
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
            pygame.font.init()
            AssetLoader._is_initialized = True

    @staticmethod
    def _get_path(filename):
        """Возвращает полный путь к файлу ресурса."""
        return os.path.join(C.ASSETS_DIR, filename)

    @classmethod
    def get_image(cls, filename, scale=None):
        """Загружает изображение, кэширует и опционально масштабирует его."""
        cache_key = (filename, scale)
        if cache_key in cls._images:
            return cls._images[cache_key]

        if filename not in cls._images:
            try:
                image = pygame.image.load(
                    cls._get_path(filename)).convert_alpha()
                cls._images[filename] = image
            except pygame.error as e:
                print(
                    f"Ошибка: не удалось загрузить изображение '{filename}': {e}")
                size = scale or (50, 50)
                fallback_surface = pygame.Surface(size, pygame.SRCALPHA)
                fallback_surface.fill(C.COLOR_RED)
                cls._images[filename] = fallback_surface

        image_to_scale = cls._images[filename]
        if scale:
            scaled_image = pygame.transform.scale(image_to_scale, scale)
            cls._images[cache_key] = scaled_image
            return scaled_image

        return image_to_scale

    @classmethod
    def get_sound(cls, filename):
        """Загружает и кэширует звуковой эффект."""
        if filename in cls._sounds:
            return cls._sounds[filename]

        try:
            sound = pygame.mixer.Sound(cls._get_path(filename))
            cls._sounds[filename] = sound
            return sound
        except pygame.error as e:
            print(f"Ошибка: не удалось загрузить звук '{filename}': {e}")
            return None

    @classmethod
    def get_font(cls, size, name=C.FONT_PATH):
        """Загружает и кэширует шрифт."""
        if (name, size) in cls._fonts:
            return cls._fonts[(name, size)]

        try:
            font = pygame.font.Font(name, size)
            cls._fonts[(name, size)] = font
            return font
        except pygame.error as e:
            print(f"Ошибка: не удалось загрузить шрифт '{name}': {e}")
            return pygame.font.Font(None, size)

    @classmethod
    def play_sound(cls, filename):
        """Проигрывает звуковой эффект."""
        sound = cls.get_sound(filename)
        if sound:
            sound.play()

    @classmethod
    def play_music(cls, filename, loops=-1):
        """Загружает и проигрывает фоновую музыку."""
        path = cls._get_path(filename)
        if not os.path.exists(path):
            print(f"Ошибка: файл музыки не найден '{filename}'")
            return

        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops)

    @classmethod
    def stop_music(cls):
        """Останавливает воспроизведение музыки."""
        pygame.mixer.music.stop()
