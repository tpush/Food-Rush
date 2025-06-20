import pygame
from .. import constants as C
from ..services.asset_loader import AssetLoader


class HUDView:
    """Отрисовка HUD: жизни, энергия, расстояние и монеты."""

    def __init__(self):
        self.font_medium = AssetLoader.get_font(C.FONT_SIZE_MEDIUM)
        self.font_small = AssetLoader.get_font(C.FONT_SIZE_SMALL)
        self.life_image = AssetLoader.get_image(C.IMG_LIFE, (30, 30))

    def draw(self, screen, player, distance_left, reward, coins):
        # Панель сверху
        ui_panel_rect = pygame.Rect(0, 0, C.WINDOW_WIDTH, 70)
        pygame.draw.rect(screen, C.COLOR_UI_BG, ui_panel_rect)

        # Расстояние и награда
        dist_text = f"Осталось: {max(0, int(distance_left / 1000))} км"
        reward_text = f"Награда: {int(reward)}"

        dist_surf = self.font_small.render(dist_text, True, C.COLOR_WHITE)
        reward_surf = self.font_small.render(reward_text, True, C.COLOR_GOLD)

        screen.blit(dist_surf, (20, 10))
        screen.blit(reward_surf, (20, 35))

        # Монеты
        coins_text = f"Монеты: {coins}"
        coins_surf = self.font_small.render(coins_text, True, C.COLOR_GOLD)
        screen.blit(coins_surf,
                    coins_surf.get_rect(right=C.WINDOW_WIDTH - 20, top=10))

        # Жизни
        for i in range(player.lives):
            screen.blit(self.life_image,
                        (C.WINDOW_WIDTH - 30 - 10 - i * 35, 35))

        # Полоска бонусной энергии снизу
        self._draw_bar(screen, C.WINDOW_WIDTH/2 - 150, C.WINDOW_HEIGHT-40,
                       300, 25, player.energy / C.PLAYER_MAX_ENERGY,
                       C.COLOR_BLUE, "Энергия")

    def _draw_bar(self, screen, x, y, w, h, percent, color, label):
        """Вспомогательный метод для отрисовки полосок."""
        if percent < 0:
            percent = 0
        if percent > 1:
            percent = 1

        bg_rect = pygame.Rect(x-2, y-2, w+4, h+4)
        pygame.draw.rect(screen, C.COLOR_UI_BG, bg_rect, border_radius=7)

        fill_rect = pygame.Rect(x, y, int(w * percent), h)
        pygame.draw.rect(screen, color, fill_rect, border_radius=5)

        label_surf = self.font_small.render(label, True, C.COLOR_WHITE)
        screen.blit(label_surf, label_surf.get_rect(center=bg_rect.center))
