import pygame

WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)


class Camera:
    def __init__(self, width: int, height: int):
        self.camera_configure = self.center_config
        self.state = pygame.Rect(0, 0, width, height)

    def update(self, hero):
        self.state = self.camera_configure(self.state, hero.rect)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    @staticmethod
    def center_config(old_state, hero_rect):
        _, _, w, h = old_state
        x, y, _, _ = hero_rect

        x = WIN_WIDTH // 2 - x
        y = WIN_HEIGHT // 2 - y

        x = min(0, x)
        x = max(-(w - WIN_WIDTH), x)

        y = min(0, y)
        y = max(-(h - WIN_HEIGHT), y)

        return pygame.Rect(x, y, w, h)
