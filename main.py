import pygame
from game.game_manager import GameManager
from game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE
from game.services.asset_loader import AssetLoader


def main():
    """Главная функция для запуска игры."""
    pygame.init()

    AssetLoader.initialize()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)

    clock = pygame.time.Clock()
    game_manager = GameManager(screen, clock)

    game_manager.run()

    pygame.quit()


if __name__ == "__main__":
    main()
