import pygame

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption("Vlad millionaire game")
icon = pygame.image.load("allIcons/iconmain.png").convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load("allIcons/background1.jpeg").convert_alpha()

walk_left = [
    pygame.image.load("allIcons/player_left/player_left1.png").convert_alpha(),
    pygame.image.load("allIcons/player_left/player_left2.png").convert_alpha(),
    pygame.image.load("allIcons/player_left/player_left3.png").convert_alpha(),
    pygame.image.load("allIcons/player_left/player_left4.png").convert_alpha()
]
walk_right = [
    pygame.image.load("allIcons/player_right/player_right1.png").convert_alpha(),
    pygame.image.load("allIcons/player_right/player_right2.png").convert_alpha(),
    pygame.image.load("allIcons/player_right/player_right3.png").convert_alpha(),
    pygame.image.load("allIcons/player_right/player_right4.png").convert_alpha()
]


enemy = pygame.image.load("allIcons/enemy.png").convert_alpha()
enemy_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = 190

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound('sounds/cowboybattle.mp3')
bg_sound.play()

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 2500)


label = pygame.font.Font("fonts/Rubik80sFade-Regular.ttf", 40)
lose_label = label.render("loser:)", False, (193, 196, 199))
restart_label = label.render("Try again", False, (115, 132, 140))
restart_label_rect = restart_label.get_rect(topleft=(180, 200))

bullets_left = 5
bullet = pygame.image.load("allIcons/bullet.png").convert_alpha()
bullets = []


gameplay = True

running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 640, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))
        if enemy_list_in_game:
            for (i, el) in enumerate(enemy_list_in_game):
                screen.blit(enemy, el)
                el.x -= 10

                if el.x < -10:
                    enemy_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 200:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -618:
            bg_x = 0



        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 630:
                    bullets.pop(i)

                if enemy_list_in_game:
                    for (index, enemy_i) in enumerate(enemy_list_in_game):
                        if el.colliderect(enemy_i):
                            enemy_list_in_game.pop(index)
                            bullets.pop(i)
    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (180, 100))
        screen.blit(restart_label, restart_label_rect)
        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            enemy_list_in_game.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy.get_rect(topleft=(620, 190)))

        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -= 1


    clock.tick(10)
