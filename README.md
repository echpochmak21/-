import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размер окна
screen_width = 800
screen_height = 600

# Создание окна
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Мой 2D Платформер")

# Загрузка изображения фона
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Загрузка изображения игрока
player_image = pygame.image.load("player.png")
player_width = 50
player_height = 50
player_image = pygame.transform.scale(player_image, (player_width, player_height))

# Загрузка изображения платформы
platform_image = pygame.image.load("platform.png")
platform_width = 200
platform_height = 20
platform_image = pygame.transform.scale(platform_image, (platform_width, platform_height))

# Позиция игрока
player_x = 100
player_y = 450

# Позиции платформ
platform_x = [300, 500, 200, 600, 200, 400, 700, 200, 100, 500, 300]
platform_y = [500, 450, 550, 400, 300, 350, 300, 250, 150, 200, 50]

# Уменьшенная скорость игрока
player_speed = 0.3

# Переменные для управления прыжком
is_jumping = False
jump_count = 10
initial_jump_count = jump_count

# Гравитация
gravity = 0.5
falling = False

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обработка управления
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Обработка прыжка
    if not is_jumping and not falling:
        if keys[pygame.K_SPACE]:
            is_jumping = True
    if is_jumping:
        player_y -= (jump_count ** 2) * 0.3
        jump_count -= 1
        if jump_count < 0:
            is_jumping = False
            falling = True
            jump_count = initial_jump_count
    else:
        # Гравитация
        if player_y < screen_height - player_height:
            player_y += gravity
        else:
            falling = False
            player_y = screen_height - player_height

    # Очистка экрана
    screen.blit(background, (0, 0))  # Фон

    # Отрисовка платформ
    for i in range(len(platform_x)):
        screen.blit(platform_image, (platform_x[i], platform_y[i]))

    # Проверка столкновения игрока с платформами
    for i in range(len(platform_x)):
        if (
            player_x + player_width > platform_x[i]
            and player_x < platform_x[i] + platform_width
            and player_y + player_height > platform_y[i]
            and player_y < platform_y[i] + platform_height
        ):
            # Если игрок касается платформы сверху, остановить падение
            if player_y + player_height <= platform_y[i] + 10:
                falling = False
                player_y = platform_y[i] - player_height
                break

    # Отрисовка игрока
    screen.blit(player_image, (player_x, player_y))

    pygame.display.flip()  # Обновление экрана

# Завершение Pygame
pygame.quit()
sys.exit()
