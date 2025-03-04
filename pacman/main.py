import pygame
import random
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 30
PLAYER_SPEED = 4
ENEMY_SPEED = 1
DOT_RADIUS = GRID_SIZE // 4
COLLISION_DISTANCE = GRID_SIZE // 2

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pac-Man")

# Load assets
player_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
player_img.fill(YELLOW)

enemy_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
enemy_img.fill(RED)

# Player class
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vel_x = 0
        self.vel_y = 0

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Keep within bounds
        self.x = max(0, min(WIDTH - GRID_SIZE, self.x))
        self.y = max(0, min(HEIGHT - GRID_SIZE, self.y))
    
    def draw(self, screen):
        screen.blit(player_img, (self.x, self.y))

# Enemy class
class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH // GRID_SIZE) * GRID_SIZE
        self.y = random.randint(0, HEIGHT // GRID_SIZE) * GRID_SIZE

    def move_towards_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist != 0:
            self.x += (dx / dist) * ENEMY_SPEED
            self.y += (dy / dist) * ENEMY_SPEED

    def draw(self, screen):
        screen.blit(enemy_img, (self.x, self.y))

# Dot class
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x + GRID_SIZE//2, self.y + GRID_SIZE//2), DOT_RADIUS)

# Function to reset the game
def reset_game():
    global player, enemy, dots
    player = Player()
    enemy = Enemy()
    dots = [Dot(random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE, random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE) for _ in range(10)]

# Initialize game objects
reset_game()

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.vel_x = -PLAYER_SPEED
                player.vel_y = 0
            elif event.key == pygame.K_RIGHT:
                player.vel_x = PLAYER_SPEED
                player.vel_y = 0
            elif event.key == pygame.K_UP:
                player.vel_y = -PLAYER_SPEED
                player.vel_x = 0
            elif event.key == pygame.K_DOWN:
                player.vel_y = PLAYER_SPEED
                player.vel_x = 0
    
    # Move player and enemy
    player.move()
    enemy.move_towards_player(player)
    
    # Check for dot collection using distance-based collision detection
    dots = [dot for dot in dots if math.hypot(player.x - dot.x, player.y - dot.y) > COLLISION_DISTANCE]
    
    # Restart game if all dots are collected or if the enemy eats the player
    if not dots or (math.hypot(player.x - enemy.x, player.y - enemy.y) < COLLISION_DISTANCE):
        reset_game()
    
    # Draw everything
    player.draw(screen)
    enemy.draw(screen)
    for dot in dots:
        dot.draw(screen)
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()