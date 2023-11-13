import pygame
import random
import time

# Инициализация pygame
pygame.init()

# Получение разрешения экрана
screen_info = pygame.display.Info()
d_width = screen_info.current_w
d_height = screen_info.current_h

# Настройка отображения в полноэкранном режиме
display = pygame.display.set_mode((d_width, d_height), pygame.FULLSCREEN)

# Загрузка фонового изображения
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (d_width, d_height))

# Загрузка изображения для паузы
pause_image = pygame.image.load("pause.png")
pause_width, pause_height = d_width // 2, d_height // 2  # Set the size of the pause image
pause_image = pygame.transform.scale(pause_image, (pause_width, pause_height))

class Character:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.jumping = False
        self.jump_count = 10
        self.falling = False
        self.gravity = 5.5  # Adjust this value to control the strength of gravity
        self.image = pygame.image.load("character.png")
        self.image = pygame.transform.scale(self.image, (width, height))

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def jump(self):
        self.jumping = True

    def update(self):
        if self.jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                new_y = self.y - (self.jump_count ** 2) * 0.5 * neg
                if new_y >= 0 and new_y + self.height <= d_height:
                    self.y = new_y
                self.jump_count -= 1
            else:
                self.jump_count = 10
                self.jumping = False
                self.falling = True

        if self.falling:
            if self.y + self.height < d_height:
                self.y += self.gravity  # Apply gravity to simulate falling
            else:
                self.y = d_height - self.height
                self.falling = False

class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("platform.png")  # Загрузите изображение для платформы
        self.image = pygame.transform.scale(self.image, (200, 50))  # Установите размер платформы

    def draw(self, display):
        display.blit(self.image, (self.x, self.y))

class Spike:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("spike.png")  # Load spike image
        self.image = pygame.transform.scale(self.image, (50, 50))  # Set spike size

    def draw(self, display):
        display.blit(self.image, (self.x, self.y))

def display_game_over():
    game_over_image = pygame.image.load("game_over.png")  # Replace with your game over image
    game_over_image = pygame.transform.scale(game_over_image, (d_width, d_height))
    display.blit(game_over_image, (0, 0))
    pygame.display.update()
    time.sleep(2)  # Display the game over image for 2 seconds
    pygame.quit()
    quit()

# Создание экземпляров платформ и шипов
platforms = [Platform(random.randint(0, d_width - 200), d_height - 20) for _ in range(5)]
spikes = [Spike(random.randint(0, d_width - 50), 0) for _ in range(5)]

def spawn_new_platform():
    x = random.randint(0, d_width - 200)
    platform = Platform(x, d_height)
    platforms.append(platform)

def spawn_new_spike():
    x = random.randint(0, d_width - 50)
    spike = Spike(x, 0)  # Spawn spikes at the top of the screen
    spikes.append(spike)

def remove_offscreen_objects(objects):
    objects[:] = [obj for obj in objects if obj.y > 0]

def game_constructor():
    game = True
    pause = False
    character = Character(90, 100, d_width // 3, d_height - 100)

    clock = pygame.time.Clock()
    spawn_delay = 0.5
    last_spawn_time = time.time()
    start_time = time.time()
    platform_rise_speed = 5  # Adjust the platform rise speed

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = False
                elif event.key == pygame.K_r:
                    pause = not pause  # Toggle pause on 'R' key

        keys = pygame.key.get_pressed()

        if not pause:
            if keys[pygame.K_SPACE]:
                character.jump()

            if keys[pygame.K_LEFT]:
                character.move_left()
            if keys[pygame.K_RIGHT]:
                character.move_right()

            display.blit(background, (0, 0))

            for platform in platforms:
                platform.draw(display)

            for spike in spikes:
                spike.draw(display)

            on_platform = False
            on_spike = False

            for platform in platforms:
                if character.y + character.height >= platform.y and character.y <= platform.y + 10 and character.x + character.width > platform.x and character.x < platform.x + 200:
                    character.y = platform.y - character.height
                    character.jump_count = 0
                    character.jumping = False
                    on_platform = True

            for spike in spikes:
                if character.x < spike.x + 50 and character.x + character.width > spike.x and character.y < spike.y + 50 and character.y + character.height > spike.y:
                    game = False  # End the game if the character touches a spike
                    on_spike = True

            if not on_platform and not character.jumping:
                character.falling = True

            character.update()

            display.blit(character.image, (character.x, character.y))

            # Display the timer as the score
            elapsed_time = int(time.time() - start_time)
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"RECORD: {elapsed_time} seconds", True, (255, 255, 255))
            display.blit(score_text, (10, 10))

            if pause:
                display.blit(pause_image, ((d_width - pause_width) // 2, (d_height - pause_height) // 2))

            pygame.display.update()
            clock.tick(60)

            for platform in platforms:
                platform.y -= platform_rise_speed  # Move platforms from bottom to top

            for spike in spikes:
                spike.y += 5  # Move spikes from top to bottom

            remove_offscreen_objects(platforms)
            remove_offscreen_objects(spikes)

            # Check if the character touches the top or bottom of the screen
            if character.y <= 0 or character.y + character.height >= d_height:
                game = False  # End the game if the character touches the top or bottom

            current_time = time.time()
            if current_time - last_spawn_time >= spawn_delay:
                spawn_new_platform()
                spawn_new_spike()
                last_spawn_time = current_time
        else:
            display.blit(pause_image, ((d_width - pause_width) // 2, (d_height - pause_height) // 2))
            pygame.display.update()

    display_game_over()

game_constructor()
