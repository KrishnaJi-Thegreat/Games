import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRICK_COLOR = (200, 0, 0)
PADDLE_COLOR = (0, 128, 255)
BALL_COLOR = (0, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Paddle
paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 30, 120, 15)
paddle_speed = 10

# Ball
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT - 45, 20, 20)
ball_speed = [5, -5]

# Bricks
brick_rows = 5
brick_cols = 10
brick_width = WIDTH // brick_cols
brick_height = 30
bricks = []

for row in range(brick_rows):
    for col in range(brick_cols):
        bricks.append(pygame.Rect(col * brick_width, row * brick_height, brick_width - 2, brick_height - 2))

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # Move ball
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]
    if ball.bottom >= HEIGHT:
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Ball collision with paddle
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]

    # Ball collision with bricks
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed[1] = -ball_speed[1]
            break

    # Draw bricks
    for brick in bricks:
        pygame.draw.rect(screen, BRICK_COLOR, brick)

    # Draw paddle and ball
    pygame.draw.rect(screen, PADDLE_COLOR, paddle)
    pygame.draw.ellipse(screen, BALL_COLOR, ball)

    # Check win
    if not bricks:
        font = pygame.font.SysFont(None, 48)
        win_text = font.render("You Win!", True, WHITE)
        screen.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        break

    pygame.display.update()

pygame.quit()
