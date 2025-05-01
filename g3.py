import pygame
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Platformer")

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player
player_width, player_height = 40, 60
player_x, player_y = 100, HEIGHT - player_height - 10
player_speed = 5
jump_speed = 15
gravity = 1

player_vel_y = 0
on_ground = False

# Platforms
platforms = [
    pygame.Rect(0, HEIGHT - 20, WIDTH, 20),  # Ground
    pygame.Rect(150, 450, 120, 20),
    pygame.Rect(300, 350, 150, 20),
    pygame.Rect(500, 250, 120, 20),
    pygame.Rect(680, 150, 100, 20),
]

def draw():
    win.fill(WHITE)
    pygame.draw.rect(win, BLUE, (player_x, player_y, player_width, player_height))
    for plat in platforms:
        pygame.draw.rect(win, GREEN, plat)
    pygame.display.update()

# Game loop
running = True
while running:
    clock.tick(FPS)

    # Handle quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movement keys
    keys = pygame.key.get_pressed()
    dx = 0
    if keys[pygame.K_LEFT]:
        dx = -player_speed
    if keys[pygame.K_RIGHT]:
        dx = player_speed
    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = -jump_speed
        on_ground = False

    # Apply movement
    player_x += dx
    player_vel_y += gravity
    player_y += player_vel_y

    # Collision detection
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    on_ground = False
    for plat in platforms:
        if player_rect.colliderect(plat) and player_vel_y >= 0:
            player_y = plat.top - player_height
            player_vel_y = 0
            on_ground = True

    # Game over if fall
    if player_y > HEIGHT:
        print("Game Over!")
        pygame.quit()
        sys.exit()

    draw()
