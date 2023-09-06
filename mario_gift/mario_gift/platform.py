import pygame
import pyganim

PLATFORM_WIDTH = 32  # Ширина прямоугольника
PLATFORM_HEIGHT = 32  # Высота
PLATFORM_COLOR = "#006262"  # Цвет прямоугольника

ANIMATION_TELEPORT = [
    "images/portal1.png",
    "images/portal2.png"
]
ANIMATION_DELAY = 1
TELEPORT_COLOR = "#006262"



class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = pygame.image.load("images/platform.png")
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class DieBlock(Platform):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.image = pygame.image.load("images/dieBlock.png")


class Teleport(Platform):
    def __init__(self, x: int, y: int, to_x: int, to_y: int):
        super().__init__(x, y)
        self.to_x = to_x
        self.to_y = to_y

        self.image.set_colorkey(pygame.Color(TELEPORT_COLOR))

        temp_list = []
        for img in ANIMATION_TELEPORT:
            temp_list.append((img, ANIMATION_DELAY))
        self.anim = pyganim.PygAnimation(temp_list)
        self.anim.play()

        self.image.fill(pygame.Color(TELEPORT_COLOR))
        self.anim.blit(self.image, (0, 0))

    def update(self):
        self.image.fill(pygame.Color(TELEPORT_COLOR))
        self.anim.blit(self.image, (0, 0))