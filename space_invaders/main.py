import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

# Set up the game clock
clock = pygame.time.Clock()

# Define game variables
player_speed = 10
enemy_speed = 3
bullet_speed = 7
bullet_delay = 500  # milliseconds
bullet_timer = 0
player_score = 0

# Define game object sizes
player_size = 50
enemy_size = 40
bullet_size = 5

# Create game objects
player = pygame.Rect(screen_width/2 - player_size/2, 
                     screen_height - player_size - 50, 
                     player_size, player_size)
enemies = []
for i in range(10):
    enemy = pygame.Rect(random.randint(0, screen_width - enemy_size), 
                        random.randint(-500, -50), 
                        enemy_size, enemy_size)
    enemies.append(enemy)
bullets = []

# Start the game loop
game_over = False
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x -= player_speed
            elif event.key == pygame.K_RIGHT:
                player.x += player_speed
            elif event.key == pygame.K_SPACE and pygame.time.get_ticks() - bullet_timer > bullet_delay:
                bullet = pygame.Rect(player.x + player.width/2 - bullet_size/2,
                                     player.y - bullet_size,
                                     bullet_size, bullet_size)
                bullets.append(bullet)
                bullet_timer = pygame.time.get_ticks()

    # Move game objects
    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > screen_height:
            enemy.y = random.randint(-500, -50)
            enemy.x = random.randint(0, screen_width - enemy_size)
    for bullet in bullets:
        bullet.y -= bullet_speed

    # Check for collisions
    for enemy in enemies:
        for bullet in bullets:
            if enemy.colliderect(bullet):
                bullets.remove(bullet)
                enemies.remove(enemy)
                player_score += 10
                break
    for enemy in enemies:
        if enemy.colliderect(player):
            game_over = True
            break

    # Draw game objects
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), player)
    for enemy in enemies:
        pygame.draw.rect(screen, (0, 255, 0), enemy)
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 0, 0), bullet)
    score_text = pygame.font.SysFont(None, 30).render("Score: {}".format(player_score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.update()

    # Cap the game frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
