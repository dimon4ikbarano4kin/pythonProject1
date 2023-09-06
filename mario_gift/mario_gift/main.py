import pygame
import player
import level
import camera
import monster


# Объявляем переменные
TITLE = "О-мари!"


def main():
    pygame.init()

    window = pygame.display.set_mode(camera.DISPLAY)
    pygame.display.set_caption(TITLE)

    bg = pygame.image.load(level.BG_FILE)

    hero = player.Player(55, 55)
    timer = pygame.time.Clock()

    lvl_1 = level.Level()

    entities = pygame.sprite.Group()
    animated_entities = pygame.sprite.Group()
    monsters = pygame.sprite.Group()

    mn = monster.Fire(120, 200, 3, 3, 150, 20)
    entities.add(mn)
    monsters.add(mn)
    lvl_1.platforms.append(mn)

    tp = level.platform.Teleport(128, 512, 512, 128)
    entities.add(tp)
    animated_entities.add(tp)
    lvl_1.platforms.append(tp)

    for platform in lvl_1.platforms:
        entities.add(platform)
    entities.add(hero)

    main_camera = camera.Camera(lvl_1.width, lvl_1.height)

    while True:
        timer.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit(0)
            hero.move(event)

        window.blit(bg, (0, 0))
        hero.update(lvl_1.platforms)

        main_camera.update(hero)

        for entity in entities:
            window.blit(entity.image, main_camera.apply(entity))

        animated_entities.update()
        monsters.update(lvl_1.platforms)
        pygame.display.update()


if __name__ == "__main__":
    main()
