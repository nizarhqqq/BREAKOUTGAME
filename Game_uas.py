import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Dimensi layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker Game")

# Kecepatan refresh layar
clock = pygame.time.Clock()

# Kelas dasar GameObject (Inheritance)
class GameObject:
    def __init__(self, x, y, color):
        self._x = x  # Atribut private
        self._y = y  # Atribut private
        self._color = color

    def draw(self):
        pass

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

# Kelas Paddle (Inheritance dan Encapsulation)
class Paddle(GameObject):
    def __init__(self, x, y, color, width, height, speed):
        super().__init__(x, y, color)
        self._width = width
        self._height = height
        self._speed = speed

    def draw(self):
        pygame.draw.rect(screen, self._color, (self._x, self._y, self._width, self._height))

    def move(self, direction):
        if direction == "left" and self._x > 0:
            self._x -= self._speed
        if direction == "right" and self._x < SCREEN_WIDTH - self._width:
            self._x += self._speed

# Kelas Ball (Inheritance dan Encapsulation)
class Ball(GameObject):
    def __init__(self, x, y, color, radius, speed_x, speed_y):
        super().__init__(x, y, color)
        self._radius = radius
        self._speed_x = speed_x
        self._speed_y = speed_y

    def draw(self):
        pygame.draw.circle(screen, self._color, (self._x, self._y), self._radius)

    def move(self):
        self._x += self._speed_x
        self._y += self._speed_y

    def bounce(self):
        self._speed_y = -self._speed_y

    def bounce_x(self):
        self._speed_x = -self._speed_x

# Kelas Brick (Inheritance)
class Brick(GameObject):
    def __init__(self, x, y, color, width, height):
        super().__init__(x, y, color)
        self._width = width
        self._height = height
        self._hit = False

    def draw(self):
        if not self._hit:
            pygame.draw.rect(screen, self._color, (self._x, self._y, self._width, self._height))

    def hit(self):
        self._hit = True

    def is_hit(self):
        return self._hit

# Font untuk teks
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

# Fungsi untuk menampilkan teks
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Fungsi Main Menu
def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(WHITE)
        draw_text("BRICK BREAKER", font, BLACK, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50)
        draw_text("Press ENTER to Start", small_font, RED, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                menu_running = False

        pygame.display.flip()
        clock.tick(60)

# Fungsi untuk menampilkan layar menang/kalah
def end_screen(message):
    end_running = True
    while end_running:
        screen.fill(WHITE)
        draw_text(message, font, RED, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
        draw_text("Press ENTER to Return to Main Menu", small_font, BLACK, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                end_running = False

        pygame.display.flip()
        clock.tick(60)

# Fungsi utama permainan
def game():
    paddle = Paddle(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 30, BLUE, 100, 15, 10)
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, RED, 10, 5, 5)
    bricks = []

    # Membuat baris brick
    brick_width = 75
    brick_height = 20
    for i in range(7):
        for j in range(5):
            brick = Brick(i * (brick_width + 10) + 35, j * (brick_height + 10) + 30, GREEN, brick_width, brick_height)
            bricks.append(brick)

    # Skor
    score = 0

    # Game loop
    running = True
    while running:
        screen.fill(WHITE)

        # Periksa event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Gerakan paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move("left")
        if keys[pygame.K_RIGHT]:
            paddle.move("right")

        # Gerakan bola
        ball.move()

        # Pantulkan bola dari dinding
        if ball.get_x() <= 0 or ball.get_x() >= SCREEN_WIDTH:
            ball.bounce_x()
        if ball.get_y() <= 0:
            ball.bounce()

        # Pantulkan bola dari paddle
        if paddle.get_y() <= ball.get_y() + ball._radius <= paddle.get_y() + 15:
            if paddle.get_x() <= ball.get_x() <= paddle.get_x() + 100:
                ball.bounce()

        # Cek tabrakan dengan brick
        for brick in bricks:
            if not brick.is_hit() and brick.get_y() <= ball.get_y() <= brick.get_y() + 20:
                if brick.get_x() <= ball.get_x() <= brick.get_x() + 75:
                    brick.hit()
                    ball.bounce()
                    score += 1

        # Cek menang
        if all(brick.is_hit() for brick in bricks):
            end_screen("YOU WIN!")
            return

        # Game over jika bola jatuh ke bawah
        if ball.get_y() > SCREEN_HEIGHT:
            end_screen("GAME OVER!")
            return

        # Gambar objek
        paddle.draw()
        ball.draw()
        for brick in bricks:
            brick.draw()

        # Tampilkan skor
        draw_text(f"Score: {score}", small_font, BLACK, 10, 10)

        # Refresh layar
        pygame.display.flip()
        clock.tick(60)

# Main program
while True:
    main_menu()
    game()
