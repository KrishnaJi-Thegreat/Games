import pygame
import sys
import random

# Initialize
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Snake and food
snake = [[100, 100], [80, 100], [60, 100]]
direction = "RIGHT"
food = [random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE)]

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

def move_snake(snake, direction):
    head = snake[0][:]
    if direction == "UP":
        head[1] -= CELL_SIZE
    elif direction == "DOWN":
        head[1] += CELL_SIZE
    elif direction == "LEFT":
        head[0] -= CELL_SIZE
    elif direction == "RIGHT":
        head[0] += CELL_SIZE
    snake.insert(0, head)
    return snake

def check_collision(snake):
    head = snake[0]
    return (
        head in snake[1:] or
        head[0] < 0 or head[0] >= WIDTH or
        head[1] < 0 or head[1] >= HEIGHT
    )

# Game loop
score = 0
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != "DOWN":
        direction = "UP"
    elif keys[pygame.K_DOWN] and direction != "UP":
        direction = "DOWN"
    elif keys[pygame.K_LEFT] and direction != "RIGHT":
        direction = "LEFT"
    elif keys[pygame.K_RIGHT] and direction != "LEFT":
        direction = "RIGHT"

    # Move
    move_snake(snake, direction)

    # Check food
    if snake[0] == food:
        score += 1
        food = [random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE)]
    else:
        snake.pop()  # Remove tail if not eating

    # Check collisions
    if check_collision(snake):
        print("Game Over! Final Score:", score)
        pygame.quit()
        sys.exit()

    # Draw everything
    draw_snake(snake)
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

    # Display score
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.update()
