import pygame
from ... import constants as C
from ...services.asset_loader import AssetLoader
from .maze_generator import MazeGenerator, AStarPathfinder


class MinigameView:
    """Представление для мини-игры 'Лабиринт'."""

    def __init__(self):
        self.maze = []
        self.rows = C.MINIGAME_ROWS
        self.cols = C.MINIGAME_COLS
        self.cell_size = C.MINIGAME_CELL_SIZE

        self.width = self.cols * self.cell_size
        self.height = self.rows * self.cell_size
        self.x_offset = (C.WINDOW_WIDTH - self.width) / 2
        self.y_offset = (C.WINDOW_HEIGHT - self.height) / 2

        self.player_pos = (0, 0)
        self.start_pos = (1, 0)
        self.end_pos = (self.rows - 2, self.cols - 1)

        self.move_timer = 0
        self.active = False

        self.font = AssetLoader.get_font(C.FONT_SIZE_MEDIUM)
        self.font_small = AssetLoader.get_font(C.FONT_SIZE_SMALL)

    def start(self):
        """Начинает новую сессию мини-игры, генерируя новый лабиринт."""
        generator = MazeGenerator(self.rows, self.cols)
        self.maze = generator.generate()
        self.player_pos = self.start_pos
        self.active = True

    def handle_event(self, event):
        """Обрабатывает ввод для перемещения по лабиринту."""
        if not self.active or self.move_timer > 0:
            return None

        if event.type == pygame.KEYDOWN:
            r, c = self.player_pos
            dr, dc = 0, 0
            if event.key in (pygame.K_UP, pygame.K_w):
                dr = -1
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                dr = 1
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                dc = -1
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                dc = 1

            if dr != 0 or dc != 0:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.maze[nr][nc] == 1:
                        self.active = False
                        AssetLoader.play_sound(C.SND_ORDER_FAILED)
                        return 'lose'
                    else:
                        self.player_pos = (nr, nc)
                        self.move_timer = C.MINIGAME_MOVE_DELAY

                        if self.player_pos == self.end_pos:
                            self.active = False
                            return 'win'
        return None

    def update(self, dt):
        """Обновляет состояние мини-игры."""
        if self.move_timer > 0:
            self.move_timer -= dt

    def draw(self, screen):
        """Отрисовывает лабиринт, игрока и цель."""
        if not self.active:
            return

        screen.fill(C.COLOR_UI_BG)

        main_title_text = "Шанс на возрождение: доберитесь до выхода!"
        instruction_text = "Осторожно: прикосновение к стене = поражение!"

        main_title_surf = self.font.render(main_title_text, True,
                                           C.COLOR_WHITE)
        instruction_surf = self.font_small.render(instruction_text, True,
                                                  C.COLOR_RED)

        screen.blit(main_title_surf,
                    main_title_surf.get_rect(centerx=C.WINDOW_WIDTH/2, y=30))
        screen.blit(instruction_surf,
                    instruction_surf.get_rect(centerx=C.WINDOW_WIDTH/2, y=80))

        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(self.x_offset + c * self.cell_size,
                                   self.y_offset + r * self.cell_size,
                                   self.cell_size, self.cell_size)
                if self.maze[r][c] == 1:
                    pygame.draw.rect(screen, C.MINIGAME_WALL_COLOR, rect)
                else:
                    pygame.draw.rect(screen, C.MINIGAME_PATH_COLOR, rect)

        end_rect = pygame.Rect(self.x_offset + self.end_pos[1] *
                               self.cell_size,
                               self.y_offset + self.end_pos[0] *
                               self.cell_size,
                               self.cell_size, self.cell_size)
        pygame.draw.rect(screen, C.MINIGAME_TARGET_COLOR, end_rect)

        player_r, player_c = self.player_pos
        player_rect = pygame.Rect(self.x_offset + player_c *
                                  self.cell_size,
                                  self.y_offset + player_r *
                                  self.cell_size,
                                  self.cell_size, self.cell_size)
        pygame.draw.rect(screen, C.MINIGAME_PLAYER_COLOR, player_rect)
