import pygame
import pyganim

FIRE_WIDTH = 32
FIRE_HEIGHT = 32

FIRE_COLOR = "#BEBEBE"

ANIMATION_FIRE = [
    "images/fire1.png",
    "images/fire2.png"
]

ANIMATION_DELAY = 1

class Fire(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int,
                 x_vel: int, y_vel: int,
                 max_length: int, max_width: int):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((FIRE_WIDTH, FIRE_HEIGHT))
        self.image.fill(pygame.Color(FIRE_COLOR))
        self.image.set_colorkey(pygame.Color(FIRE_COLOR))

        temp_list = []
        for img in ANIMATION_FIRE:
            temp_list.append((img, ANIMATION_DELAY))
        self.anim = pyganim.PygAnimation(temp_list)
        self.anim.play()

        self.anim.blit(self.image, (0, 0))

        self.rect = pygame.Rect(x, y, FIRE_WIDTH, FIRE_HEIGHT)

        self.stsrt_x = x
        self.stsrt_y = y

        self.x_vel = x_vel
        self.y_vel = y_vel

        self.max_length = max_length
        self.max_width = max_width

    def update(self, platforms):
        self.image.fill(pygame.Color(FIRE_COLOR))
        self.anim.blit(self.image, (0, 0))

        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        self.collide(platforms)

        if abs(self.stsrt_x - self.rect.x) > self.max_length:
            self.x_vel = -self.x_vel
        if abs(self.stsrt_y - self.rect.y) > self.max_width:
            self.y_vel = -self.y_vel


    def collide(self, platforms: list):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p) and self != p:
                self.x_vel = -self.x_vel
                self.y_vel = -self.y_vel
