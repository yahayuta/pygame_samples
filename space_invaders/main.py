import pygame
import random

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Load sound file
explosion = pygame.mixer.Sound('sound_files/explosion.wav')
invaderkilled = pygame.mixer.Sound('sound_files/invaderkilled.wav')
shoot = pygame.mixer.Sound('sound_files/shoot.wav')

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
enemy_spawn_timer = 0
enemy_spawn_delay = 2000  # milliseconds

# Define game object sizes
player_size = 50
enemy_size = 40
bullet_size = 5

# Font for instructions
font = pygame.font.SysFont(None, 20)
title_font = pygame.font.SysFont(None, 28, bold=True)

# Enemy types with different properties
enemy_types = [
    {"color": (0, 255, 0), "speed": 2, "points": 10, "size": 40},  # Green - slow, basic
    {"color": (255, 165, 0), "speed": 3, "points": 20, "size": 35},  # Orange - medium speed
    {"color": (255, 0, 0), "speed": 4, "points": 30, "size": 30},  # Red - fast, small
]

# Create game objects
player = pygame.Rect(screen_width/2 - player_size/2, 
                     screen_height - player_size - 50, 
                     player_size, player_size)
enemies = []
bullets = []

# Initialize enemies with different types
for i in range(8):
    enemy_type = random.choice(enemy_types)
    enemy = {
        "rect": pygame.Rect(random.randint(0, screen_width - enemy_type["size"]), 
                           random.randint(-500, -50), 
                           enemy_type["size"], enemy_type["size"]),
        "type": enemy_type,
        "direction": random.choice([-1, 1]),  # Random horizontal direction
        "move_timer": 0
    }
    enemies.append(enemy)

# Function to draw instructions
def draw_instructions():
    # Title
    title_text = title_font.render("SPACE INVADERS", True, (255, 255, 255))
    screen.blit(title_text, (10, 10))
    
    # Instructions
    instructions = [
        "OBJECTIVE: Shoot all alien invaders",
        "CONTROLS:",
        "  Arrow Keys: Move",
        "  Spacebar: Shoot",
        "SCORING: Points for each alien destroyed",
        "GAME OVER: Alien touches player"
    ]
    
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, (255, 255, 255))
        screen.blit(text, (10, 50 + i * 20))

# Start the game loop
game_over = False
while not game_over:
    current_time = pygame.time.get_ticks()
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x -= player_speed
            elif event.key == pygame.K_RIGHT:
                player.x += player_speed
            elif event.key == pygame.K_UP:
                player.y -= player_speed
            elif event.key == pygame.K_DOWN:
                player.y += player_speed
            elif event.key == pygame.K_SPACE and current_time - bullet_timer > bullet_delay:
                shoot.play()
                bullet = pygame.Rect(player.x + player.width/2 - bullet_size/2,
                                     player.y - bullet_size,
                                     bullet_size, bullet_size)
                bullets.append(bullet)
                bullet_timer = current_time

    # Spawn new enemies periodically
    if current_time - enemy_spawn_timer > enemy_spawn_delay:
        enemy_type = random.choice(enemy_types)
        enemy = {
            "rect": pygame.Rect(random.randint(0, screen_width - enemy_type["size"]), 
                               -enemy_type["size"], 
                               enemy_type["size"], enemy_type["size"]),
            "type": enemy_type,
            "direction": random.choice([-1, 1]),
            "move_timer": 0
        }
        enemies.append(enemy)
        enemy_spawn_timer = current_time

    # Move game objects
    for enemy in enemies:
        # Move enemy down
        enemy["rect"].y += enemy["type"]["speed"]
        
        # Add horizontal movement for variety
        enemy["move_timer"] += 1
        if enemy["move_timer"] % 30 == 0:  # Change direction every 30 frames
            enemy["direction"] *= -1
        enemy["rect"].x += enemy["direction"] * 2
        
        # Keep enemy within screen bounds
        if enemy["rect"].x < 0:
            enemy["rect"].x = 0
            enemy["direction"] *= -1
        elif enemy["rect"].x > screen_width - enemy["type"]["size"]:
            enemy["rect"].x = screen_width - enemy["type"]["size"]
            enemy["direction"] *= -1
        
        # Reset enemy if it goes off screen
        if enemy["rect"].y > screen_height:
            enemy["rect"].y = random.randint(-500, -50)
            enemy["rect"].x = random.randint(0, screen_width - enemy["type"]["size"])
    
    for bullet in bullets:
        bullet.y -= bullet_speed

    # Remove bullets that go off screen
    bullets = [bullet for bullet in bullets if bullet.y > -bullet_size]

    # Check for collisions
    for enemy in enemies[:]:  # Use slice to avoid modifying list during iteration
        for bullet in bullets[:]:
            if enemy["rect"].colliderect(bullet):
                invaderkilled.play()
                bullets.remove(bullet)
                enemies.remove(enemy)
                player_score += enemy["type"]["points"]
                break
    
    for enemy in enemies:
        if enemy["rect"].colliderect(player):
            explosion.play()
            pygame.time.delay(2000)
            game_over = True
            break

    # Draw game objects
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), player)
    
    for enemy in enemies:
        pygame.draw.rect(screen, enemy["type"]["color"], enemy["rect"])
    
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 0, 0), bullet)
    
    score_text = pygame.font.SysFont(None, 30).render("Score: {}".format(player_score), True, (255, 255, 255))
    screen.blit(score_text, (10, 200))
    
    # Display enemy count
    enemy_count_text = pygame.font.SysFont(None, 30).render("Enemies: {}".format(len(enemies)), True, (255, 255, 255))
    screen.blit(enemy_count_text, (10, 230))
    
    # Draw instructions
    draw_instructions()
    
    pygame.display.update()

    # Cap the game frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
