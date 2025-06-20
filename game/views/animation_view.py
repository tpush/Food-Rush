import pygame
from .. import constants as C
from ..services.asset_loader import AssetLoader


class DeliveryAnimationView:
    """Управление и отрисовка анимации доставки."""

    def __init__(self):
        self.font = AssetLoader.get_font(C.FONT_SIZE_LARGE)
        self.timer = 0
        self.active = False

        self.player_frames = []
        for frame_name in C.IMG_DELIVERY_PLAYER_FRAMES:
            self.player_frames.append(AssetLoader.get_image(
                frame_name, C.DELIVERY_PLAYER_SIZE))
        self.current_frame_index = 0
        self.frame_timer = 0.0

    def start(self):
        """Запуск анимации."""
        self.timer = C.DELIVERY_ANIMATION_DURATION
        self.active = True
        self.current_frame_index = 0
        self.frame_timer = 0.0

    def update(self, dt):
        """Обновление таймера и анимации спрайтов."""
        if self.active:
            self.timer -= dt

            self.frame_timer += dt
            if self.frame_timer >= C.DELIVERY_ANIMATION_FRAME_DURATION:
                self.frame_timer -= C.DELIVERY_ANIMATION_FRAME_DURATION
                self.current_frame_index = (self.current_frame_index + 1) % \
                    len(self.player_frames)

            if self.timer <= 0:
                self.active = False
                return True
        return False

    def draw(self, screen):
        """Отрисовка сцены анимации."""
        if not self.active:
            return

        screen.fill(C.COLOR_BLUE_SKY)
        pygame.draw.rect(screen, C.COLOR_GREEN_GRASS,
                         (0, C.WINDOW_HEIGHT - 200, C.WINDOW_WIDTH, 200))
        pygame.draw.rect(screen, C.COLOR_GRAY_ROAD,
                         (0, C.WINDOW_HEIGHT - 150, C.WINDOW_WIDTH, 100))

        progress = 1.0 - (self.timer / C.DELIVERY_ANIMATION_DURATION)

        player_x = (-C.DELIVERY_PLAYER_SIZE[0] +
                    (C.WINDOW_WIDTH + C.DELIVERY_PLAYER_SIZE[0] - 200) *
                    progress)

        player_y = C.WINDOW_HEIGHT - 140 - C.DELIVERY_PLAYER_SIZE[1] / 2

        player_rect = pygame.Rect(player_x, player_y,
                                  C.DELIVERY_PLAYER_SIZE[0],
                                  C.DELIVERY_PLAYER_SIZE[1])

        if self.player_frames:
            screen.blit(self.player_frames[self.current_frame_index],
                        player_rect.topleft)

        # Изображение дома
        house_base_x = C.WINDOW_WIDTH - 250
        house_base_y = C.WINDOW_HEIGHT - 300

        pygame.draw.rect(screen, (160, 82, 45),
                         (house_base_x, house_base_y, 180, 150))

        roof_points = [
            (house_base_x - 20, house_base_y),
            (house_base_x + 180 + 20, house_base_y),
            (house_base_x + 180 / 2, house_base_y - 80)
        ]
        pygame.draw.polygon(screen, (139, 0, 0), roof_points)

        pygame.draw.rect(screen, (173, 216, 230),
                         (house_base_x + 40, house_base_y + 40, 40, 40))
        pygame.draw.rect(screen, C.COLOR_BLACK,
                         (house_base_x + 40, house_base_y + 40, 40, 40), 2)

        pygame.draw.rect(screen, (101, 67, 33),
                         (house_base_x + 100, house_base_y + 70, 50, 80))
        pygame.draw.circle(screen, C.COLOR_GOLD,
                           (house_base_x + 140, house_base_y + 110), 5)

        text_surf = self.font.render("Заказ доставлен!", True, C.COLOR_WHITE)
        alpha = 0
        if progress > 0.5:
            alpha = min(255, int(255 * ((progress - 0.5) * 2)))

        text_surf.set_alpha(alpha)
        text_rect = text_surf.get_rect(center=(C.WINDOW_WIDTH/2,
                                               C.WINDOW_HEIGHT/2))
        screen.blit(text_surf, text_rect)
