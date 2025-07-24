import pygame
import random
import os

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

# Initialize high score
high_score = 0

# Load assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
PLAYER_SPRITE = pygame.image.load(os.path.join(ASSETS_DIR, 'player.png'))
ENEMY_SPRITE = pygame.image.load(os.path.join(ASSETS_DIR, 'enemy.png'))

# Scale sprites
PLAYER_SPRITE = pygame.transform.scale(PLAYER_SPRITE, (20, 20))
ENEMY_SPRITE = pygame.transform.scale(ENEMY_SPRITE, (20, 20))

# Load sound effects
COLLISION_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'sounds', 'collision.wav'))
SCORE_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'sounds', 'score.wav'))
MOVE_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'sounds', 'move.wav'))

# Adjust enemy speed based on score
def get_enemy_speed(score):
    base_speed = 0.05  # Reduced from 0.1
    speed_increment = 0.02
    return base_speed + (score // 10) * speed_increment

# Update enemy speed dynamically
enemy_speed = get_enemy_speed(score)

# Add pause functionality
def toggle_pause(paused):
    return not paused

# Initialize pause state
paused = False

# Display Game Over screen
def game_over_screen(final_score):
    game_window.fill(BLACK)
    font_large = pygame.font.SysFont(None, 60)
    game_over_text = font_large.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {final_score}", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)

    game_window.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 3))
    game_window.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2))
    game_window.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 1.5))

    # Display high score on the Game Over screen
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    game_window.blit(high_score_text, (WINDOW_WIDTH // 2 - high_score_text.get_width() // 2, WINDOW_HEIGHT // 1.8))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False

# Initialize power-ups
power_up_active = False
power_up_timer = 0
power_up_duration = 5000  # 5 seconds

# Create a power-up
power_up_x = random.randint(0, WINDOW_WIDTH - 20)
power_up_y = random.randint(50, WINDOW_HEIGHT - 100)

# Initialize level
level = 1

# Function to increase level
def increase_level():
    global num_enemies, enemy_speed, level
    level += 1
    num_enemies += 2  # Add more enemies each level
    enemy_speed += 0.05  # Increase enemy speed

# Update enemies list when the number of enemies changes
def update_enemies():
    global enemies
    while len(enemies) < num_enemies:
        enemy_x = random.randint(0, WINDOW_WIDTH)
        enemy_y = random.randint(50, 200)
        enemies.append((enemy_x, enemy_y))
    while len(enemies) > num_enemies:
        enemies.pop()

# Set the game loop to run
game_running = True
while game_running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

        # Check for pause toggle
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = toggle_pause(paused)

    # Pause the game
    if paused:
        continue

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

    # Allow diagonal movement
    if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
        player_x -= player_speed
        player_y -= player_speed
    elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
        player_x -= player_speed
        player_y += player_speed
    elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
        player_x += player_speed
        player_y -= player_speed
    elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
        player_x += player_speed
        player_y += player_speed

    # Play movement sound
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
        MOVE_SOUND.play()

    # Prevent the player from moving outside the game window
    player_x = max(0, min(player_x, WINDOW_WIDTH - 20))
    player_y = max(-20, min(player_y, WINDOW_HEIGHT - 20))

    # Draw the player
    game_window.blit(PLAYER_SPRITE, (player_x, player_y))

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
        game_window.blit(ENEMY_SPRITE, (enemy[0], enemy[1]))

    # Enhanced collision detection using pygame's Rect
    player_rect = pygame.Rect(player_x, player_y, 20, 20)
    for i in range(num_enemies):
        enemy_x, enemy_y = enemies[i]
        enemy_rect = pygame.Rect(enemy_x, enemy_y, 20, 20)
        if player_rect.colliderect(enemy_rect):
            # Player has collided with an enemy
            COLLISION_SOUND.play()
            # Trigger Game Over screen
            game_over_screen(score)
            # Reset game state
            score = 0
            player_x = WINDOW_WIDTH // 2
            player_y = WINDOW_HEIGHT - 50
            for j in range(num_enemies):
                enemy_x = random.randint(0, WINDOW_WIDTH)
                enemy_y = random.randint(50, 200)
                enemies[j] = (enemy_x, enemy_y)

    # Check if the player has reached the top of the screen
    if player_y < 0:
        score += 10
        player_x = WINDOW_WIDTH // 2
        player_y = WINDOW_HEIGHT - 50
        increase_level()  # Progress to the next level

    # Update high score if necessary
    if score > high_score:
        high_score = score

    # Draw the score on the screen
    score_text = font.render("Score: " + str(score), True, WHITE)
    game_window.blit(score_text, (10, 10))

    # Display level on the screen
    level_text = font.render(f"Level: {level}", True, WHITE)
    game_window.blit(level_text, (10, 40))

    # Update enemy speed based on score
    enemy_speed = get_enemy_speed(score)

    # Draw the power-up
    if not power_up_active:
        pygame.draw.circle(game_window, WHITE, (power_up_x + 10, power_up_y + 10), 10)

    # Check for collision with power-up
    power_up_rect = pygame.Rect(power_up_x, power_up_y, 20, 20)
    if player_rect.colliderect(power_up_rect) and not power_up_active:
        power_up_active = True
        power_up_timer = pygame.time.get_ticks()
        player_speed *= 2  # Double the player's speed

    # Deactivate power-up after duration
    if power_up_active and pygame.time.get_ticks() - power_up_timer > power_up_duration:
        power_up_active = False
        player_speed //= 2  # Reset the player's speed
        power_up_x = random.randint(0, WINDOW_WIDTH - 20)
        power_up_y = random.randint(50, WINDOW_HEIGHT - 100)

    # Check for level progression
    if score % 50 == 0 and score > 0:
        increase_level()

    # Ensure enemies list matches the current number of enemies
    update_enemies()

    # Update the screen
    pygame.display.update()

# Quit Pygame
pygame.quit()
