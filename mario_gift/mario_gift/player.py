import pygame
import pyganim
import platform
import monster

count = 0
MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = "#000000"
JUMP_POWER = 10
GRAVITY = 0.35

ANIMATION_DELAY = 1
ANIMATION_LEFT = ('images/hero/l1.png',
                  'images/hero/l2.png',
                  'images/hero/l3.png',
                  'images/hero/l4.png',
                  'images/hero/l5.png')
ANIMATION_RIGHT = ('images/hero/r1.png',
                   'images/hero/r2.png',
                   'images/hero/r3.png',
                   'images/hero/r4.png',
                   'images/hero/r5.png')
ANIMATION_JUMP = [('images/hero/j.png', ANIMATION_DELAY)]
ANIMATION_JUMP_LEFT = [('images/hero/jl.png', ANIMATION_DELAY)]
ANIMATION_JUMP_RIGHT = [('images/hero/jr.png', ANIMATION_DELAY)]
ANIMATION_STAY = [('images/hero/0.png', ANIMATION_DELAY)]


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # скорость перемещения. 0 - стоять на месте
        self.xvel = 0
        # скорость вертикального перемещения
        self.yvel = 0
        # Начальная позиция Х
        self.startX = x
        self.startY = y
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(pygame.Color(COLOR))

        self.image.set_colorkey(pygame.Color(COLOR))

        anim_temp = []
        for img in ANIMATION_LEFT:
            anim_temp.append((img, ANIMATION_DELAY))
        self.anim_left = pyganim.PygAnimation(anim_temp)
        self.anim_left.play()

        anim_temp = []
        for img in ANIMATION_RIGHT:
            anim_temp.append((img, ANIMATION_DELAY))
        self.anim_right = pyganim.PygAnimation(anim_temp)
        self.anim_right.play()

        self.anim_jump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.anim_jump.play()

        self.anim_jump_left = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.anim_jump_left.play()

        self.anim_jump_right = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.anim_jump_right.play()

        self.anim_stay = pyganim.PygAnimation(ANIMATION_STAY)
        self.anim_stay.play()
        self.anim_stay.blit(self.image, (0, 0))

        # прямоугольный объект
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)
        self.left = False
        self.right = False
        self.up = False
        self.onGround = False  # На земле ли я?

    def update(self, platforms):
        if self.left:
            self.xvel = -MOVE_SPEED  # Лево = x- n

            self.image.fill(pygame.Color(COLOR))
            if self.up and not self.onGround:
                self.anim_jump_left.blit(self.image, (0, 0))
            else:
                self.anim_left.blit(self.image, (0, 0))

        if self.right:
            self.xvel = MOVE_SPEED  # Право = x + n

            self.image.fill(pygame.Color(COLOR))
            if self.up and not self.onGround:
                self.anim_jump_right.blit(self.image, (0, 0))
            else:
                self.anim_right.blit(self.image, (0, 0))

        # стоим, когда нет указаний идти
        if not (self.left or self.right):
            self.xvel = 0

            self.image.fill(pygame.Color(COLOR))
            if not self.up:
                self.anim_stay.blit(self.image, (0, 0))
            else:
                self.anim_jump.blit(self.image, (0, 0))

        if self.up:
            # прыгаем, только когда можем оттолкнуться от земли
            if self.onGround:
                self.yvel = -JUMP_POWER

        if not self.onGround:
            self.yvel += GRAVITY

        # Мы не знаем, когда мы на земле
        self.onGround = False

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def collide(self, xvel, yvel, platforms):
        
        count = 0
        for p in platforms:
            # если есть пересечение платформы с игроком
            if pygame.sprite.collide_rect(self, p):

                if isinstance(p, platform.DieBlock) or isinstance(p, monster.Fire):

                    self.die()
                    count += 1
                    break

                elif isinstance(p, platform.Teleport):
                    self.teleporting(p.to_x, p.to_y)
                    break


                if xvel > 0:  # если движется вправо
                    # то не движется вправо
                    self.rect.right = p.rect.left

                if xvel < 0:  # если движется влево
                    # то не движется влево
                    self.rect.left = p.rect.right

                if yvel > 0:  # если падает вниз
                    # то не падает вниз
                    self.rect.bottom = p.rect.top
                    # и становится на что-то твердое
                    self.onGround = True
                    # и энергия падения пропадает
                    self.yvel = 0

                if yvel < 0:  # если движется вверх
                    # то не движется вверх
                    self.rect.top = p.rect.bottom
                    # и энергия прыжка пропадает
                    self.yvel = 0

    def move(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.left = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.right = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.up = True

        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            self.left = False
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            self.right = False
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            self.up = False

    def teleporting(self, x, y):
        self.rect.x = self.startX
        self.rect.y = self.startY

    def die(self):
        pygame.time.wait(500)
        self.teleporting(self.startX, self.startY)


