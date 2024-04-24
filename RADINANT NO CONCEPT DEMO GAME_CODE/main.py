import pygame, sys
from CODE.player import Player
from CODE.particles import Particles

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((640, 360))
screen_1280_720 = pygame.Surface((1280, 720), pygame.FULLSCREEN)

player = Player(100, 0, [50, 4, 30], ['DATA/images/player/not_run', 'DATA/images/player/run', 'DATA/images/player/jump'], '.png', [40, 52])
particle = Particles([False, False], [[0, 1], [0]], 2)
rect1 = pygame.Rect(50, 200, 500, 50)
screen_feel = [255, 0, 0]
player.load_images(), player.collision()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.movement(1), player.animate(player.movement_bool[0][0], player.movement_bool[0][1], player.gravity_bool), player.jump(10, 10)

    if screen_feel[0] == 255 and screen_feel[1] <= 254 and screen_feel[2] == 0:
        screen_feel[1] += 1
    elif screen_feel[1] == 255 and screen_feel[0] >= 1 and screen_feel[2] == 0:
        screen_feel[0] -= 1
    elif screen_feel[0] == 0 and screen_feel[2] <= 254:
        screen_feel[2] += 1
    elif screen_feel[2] == 255 and screen_feel[1] >= 1:
        screen_feel[1] -= 1
    elif screen_feel[1] == 0 and screen_feel[0] <= 254:
        screen_feel[0] += 1
    elif screen_feel[0] == 255 and screen_feel[2] >= 1 and screen_feel[1] == 0:
        screen_feel[2] -= 1

    screen.fill(screen_feel)
    player.collision_rect_lists[player.image_list_index][player.image_index[0]].topleft = (player.x, player.y)
    screen.blit(player.image_lists[player.image_list_index][player.image_index[0]], (player.x, player.y))
    pygame.draw.rect(screen, (0, 200, 100), rect1)

    if rect1.colliderect(player.collision_rect_lists[player.image_list_index][player.image_index[0]]):
        if player.y >= 150 or player.y <= 190:
            player.y = 149
            player.gravity(False)
            particle.count[0][0] += particle.count[0][1]
            if particle.count[0][0] == 1:
                particle.bool[0] = True
            else:
                particle.bool[0] = False
                particle.count[0][1] = 0
    elif not rect1.colliderect(player.collision_rect_lists[player.image_list_index][player.image_index[0]]):
        player.gravity(True)
        particle.bool[0] = False
        particle.count[0] = [0, 1]
    particle.particle1(player.x + (player.image_size[0] // 2), player.y + player.image_size[1], 10, [5, 8], screen, 5, 2, particle.bool[0], 1)

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and player.jump_count[1] == 2 and particle.count[1][0] == 0:
        particle.bool[1] = True
        particle.count[1][0] = 1
    elif particle.count[1][0] == 1:
        particle.bool[1] = False
    if not player.gravity_bool and not (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]):
        particle.count[1][0] = 0
    particle.particle1(player.x + (player.image_size[0] // 2), player.y + (player.image_size[1] / 2), 15, [4, 7], screen, 5, 2.5, particle.bool[1], 2)

    pygame.display.update()
    clock.tick(60)