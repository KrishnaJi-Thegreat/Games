import pygame
import random

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Run Clone")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
FPS = 60
clock = pygame.time.Clock()

# Load assets (use simple rectangles for now)
dino_width, dino_height = 50, 50
cactus_width, cactus_height = 20, 50
gravity = 1

# Fonts
font = pygame.font.SysFont(None, 36)

def draw_dino(x, y):
    pygame.draw.rect(WIN, (0, 255, 0), (x, y, dino_width, dino_height))

def draw_cactus(x, y):
    pygame.draw.rect(WIN, (255, 0, 0), (x, y, cactus_width, cactus_height))

def main():
    dino_x = 100
    dino_y = HEIGHT - dino_height - 20
    dino_y_vel = 0
    is_jumping = False

    cactus_x = WIDTH
    cactus_y = HEIGHT - cactus_height - 20
    cactus_speed = 7

    score = 0
    run = True
    while run:
        clock.tick(FPS)
        WIN.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Handle jump
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not is_jumping:
            is_jumping = True
            dino_y_vel = -20

        if is_jumping:
            dino_y += dino_y_vel
            dino_y_vel += gravity
            if dino_y >= HEIGHT - dino_height - 20:
                dino_y = HEIGHT - dino_height - 20
                is_jumping = False

        # Move cactus
        cactus_x -= cactus_speed
        if cactus_x < -cactus_width:
            cactus_x = WIDTH + random.randint(100, 300)
            score += 1
            cactus_speed += 0.2  # Increase speed to raise difficulty

        # Collision detection
        dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
        cactus_rect = pygame.Rect(cactus_x, cactus_y, cactus_width, cactus_height)
        if dino_rect.colliderect(cactus_rect):
            print("Game Over!")
            run = False

        # Draw everything
        draw_dino(dino_x, dino_y)
        draw_cactus(cactus_x, cactus_y)

        score_text = font.render(f"Score: {score}", True, BLACK)
        WIN.blit(score_text, (10, 10))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
