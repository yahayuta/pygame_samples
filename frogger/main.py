import pygame
import random

# Initialize Pygame
pygame.init()

# Set the dimensions of the game window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the title of the game window
pygame.display.set_caption("Frogger")

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the font for the score
font = pygame.font.SysFont(None, 30)

# Set the starting position of the player
player_x = WINDOW_WIDTH // 2
player_y = WINDOW_HEIGHT - 50

# Set the speed of the player and the enemies
player_speed = 1
enemy_speed = 0.1

# Set the number of enemies
num_enemies = 5

# Create a list to hold the enemies
enemies = []
for i in range(num_enemies):
    enemy_x = random.randint(0, WINDOW_WIDTH)
    enemy_y = random.randint(50, 200)
    enemies.append((enemy_x, enemy_y))

# Set the starting score
score = 0

# Set the game loop to run
game_running = True
while game_running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Clear the screen
    game_window.fill(BLACK)

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Draw the player
    pygame.draw.rect(game_window, GREEN, (player_x, player_y, 20, 20))

    # Move the enemies
    for i in range(num_enemies):
        enemy_x, enemy_y = enemies[i]
        enemy_x += enemy_speed
        if enemy_x > WINDOW_WIDTH:
            enemy_x = 0
            enemy_y = random.randint(50, 200)
        enemies[i] = (enemy_x, enemy_y)

    # Draw the enemies
    for enemy in enemies:
        pygame.draw.rect(game_window, RED, (enemy[0], enemy[1], 20, 20))

    # Check for collisions between the player and the enemies
    for enemy in enemies:
        if player_x < enemy[0] + 20 and player_x + 20 > enemy[0] and player_y < enemy[1] + 20 and player_y + 20 > enemy[1]:
            # Player has collided with an enemy, reset the game
            score = 0
            player_x = WINDOW_WIDTH // 2
            player_y = WINDOW_HEIGHT - 50
            for i in range(num_enemies):
                enemy_x = random.randint(0, WINDOW_WIDTH)
                enemy_y = random.randint(50, 200)
                enemies[i] = (enemy_x, enemy_y)

    # Check if the player has reached the top of the screen
    if player_y < 0:
        score += 10
        player_x = WINDOW_WIDTH // 2
        player_y = WINDOW_HEIGHT - 50

    # Draw the score on the screen
    score_text = font.render("Score: " + str(score), True, WHITE)
    game_window.blit(score_text, (10, 10))

    # Draw the player on the screen
    pygame.draw.rect(game_window, GREEN, (player_x, player_y, 20, 20))

    # Move the enemies
    for i in range(num_enemies):
        enemy_x, enemy_y = enemies[i]
        enemy_x += enemy_speed
        if enemy_x > WINDOW_WIDTH:
            enemy_x = 0
            enemy_y = random.randint(50, 400)
        enemies[i] = (enemy_x, enemy_y)

    # Draw the enemies on the screen
    for enemy in enemies:
        pygame.draw.rect(game_window, RED, (enemy[0], enemy[1], 20, 20))

    # Check for collisions between the player and the enemies
    for enemy in enemies:
        if player_x < enemy[0] + 20 and player_x + 20 > enemy[0] and player_y < enemy[1] + 20 and player_y + 20 > enemy[1]:
            score = 0
            player_x = WINDOW_WIDTH // 2
            player_y = WINDOW_HEIGHT - 50
            for i in range(num_enemies):
                enemy_x = random.randint(0, WINDOW_WIDTH)
                enemy_y = random.randint(50, 200)
                enemies[i] = (enemy_x, enemy_y)

    # Update the screen
    pygame.display.update()

# Quit Pygame
pygame.quit()
