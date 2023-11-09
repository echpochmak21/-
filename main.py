import pygame

pygame.init()

# Получить разрешение экрана
screen_info = pygame.display.Info()
d_width = screen_info.current_w
d_height = screen_info.current_h

display = pygame.display.set_mode((d_width, d_height), pygame.FULLSCREEN)

# Загрузите изображение фона
background = pygame.image.load("background.jpg")  # Замените "background.jpg" на имя вашего изображения фона
background = pygame.transform.scale(background, (d_width, d_height))

class Character:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.jumping = False
        self.jump_count = 10
        # Загрузите изображение персонажа
        self.image = pygame.image.load("character.png")  # Замените "character.png" на имя вашего изображения персонажа
        self.image = pygame.transform.scale(self.image, (width, height))

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def jump(self):
        if not self.jumping:
            self.jumping = True

    def update(self):
        if self.jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.jump_count = 10
                self.jumping = False

def game_constructor():
    game = True
    character = Character(90, 100, d_width // 3, d_height - 100)

    clock = pygame.time.Clock()

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            character.jump()

        if keys[pygame.K_LEFT]:
            character.move_left()
        if keys[pygame.K_RIGHT]:
            character.move_right()

        display.blit(background, (0, 0))  # Отобразить фон
        display.blit(character.image, (character.x, character.y))  # Отобразить персонажа
        pygame.display.update()

        character.update()
        clock.tick(60)

game_constructor()