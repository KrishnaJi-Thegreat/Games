import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Blocks")

# Colors
WHITE = (255, 255, 255)
PLAYER_COLOR = (0, 128, 255)
ENEMY_COLOR = (255, 0, 0)

# Player settings
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 10

# Enemy settings
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_speed = 5

# Clock
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

score = 0

def detect_collision(player_pos, enemy_pos):
    px, py = player_pos
    ex, ey = enemy_pos
    return (
        ex < px + player_size and
        ex + enemy_size > px and
        ey < py + player_size and
        ey + enemy_size > py
    )

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed

    # Move enemy
    enemy_pos[1] += enemy_speed
    if enemy_pos[1] > HEIGHT:
        enemy_pos[1] = 0
        enemy_pos[0] = random.randint(0, WIDTH - enemy_size)
        score += 1
        enemy_speed += 0.2  # Increase difficulty gradually

    # Check for collision
    if detect_collision(player_pos, enemy_pos):
        text = font.render("Game Over!", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - 70, HEIGHT // 2 - 20))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # Draw player and enemy
    pygame.draw.rect(screen, PLAYER_COLOR, (*player_pos, player_size, player_size))
    pygame.draw.rect(screen, ENEMY_COLOR, (*enemy_pos, enemy_size, enemy_size))

    # Show score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(30)
