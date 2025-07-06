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
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PINK = (255, 105, 180)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pac-Man")

# Load assets
player_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
player_img.fill(YELLOW)

enemy_colors = [RED, BLUE, GREEN, ORANGE]

# Walls layout (simple border walls)
walls = set()
for x in range(0, WIDTH, GRID_SIZE):
    walls.add((x, 0))
    walls.add((x, HEIGHT - GRID_SIZE))
for y in range(0, HEIGHT, GRID_SIZE):
    walls.add((0, y))
    walls.add((WIDTH - GRID_SIZE, y))

# Font for instructions
font = pygame.font.SysFont('Arial', 16)
title_font = pygame.font.SysFont('Arial', 24, bold=True)

# Player class
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vel_x = 0
        self.vel_y = 0

    def move(self, walls):
        new_x = self.x + self.vel_x
        new_y = self.y + self.vel_y
        if (new_x // GRID_SIZE * GRID_SIZE, new_y // GRID_SIZE * GRID_SIZE) not in walls:
            self.x = new_x
            self.y = new_y
    
    def draw(self, screen):
        screen.blit(player_img, (self.x, self.y))

# Enemy class
class Enemy:
    def __init__(self, chase=False, color=RED):
        self.x = random.randint(1, (WIDTH // GRID_SIZE) - 2) * GRID_SIZE
        self.y = random.randint(1, (HEIGHT // GRID_SIZE) - 2) * GRID_SIZE
        self.chase = chase
        self.vel_x = random.choice([-ENEMY_SPEED, ENEMY_SPEED])
        self.vel_y = random.choice([-ENEMY_SPEED, ENEMY_SPEED])
        self.color = color
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(self.color)

    def move(self, player):
        if self.chase:
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.sqrt(dx**2 + dy**2)
            if dist != 0:
                self.x += (dx / dist) * ENEMY_SPEED
                self.y += (dy / dist) * ENEMY_SPEED
        else:
            if random.random() < 0.02:  # Randomly change direction
                self.vel_x = random.choice([-ENEMY_SPEED, ENEMY_SPEED])
                self.vel_y = random.choice([-ENEMY_SPEED, ENEMY_SPEED])
            self.x += self.vel_x
            self.y += self.vel_y
            # Keep within bounds
            self.x = max(GRID_SIZE, min(WIDTH - GRID_SIZE * 2, self.x))
            self.y = max(GRID_SIZE, min(HEIGHT - GRID_SIZE * 2, self.y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Dot class
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x + GRID_SIZE//2, self.y + GRID_SIZE//2), DOT_RADIUS)

# Function to draw instructions
def draw_instructions():
    # Title
    title_text = title_font.render("PAC-MAN", True, YELLOW)
    screen.blit(title_text, (10, 10))
    
    # Instructions
    instructions = [
        "OBJECTIVE: Eat all dots while avoiding ghosts",
        "CONTROLS: Arrow Keys to move",
        "SCORING: Points for dots eaten",
        "GAME OVER: Touch a ghost"
    ]
    
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, WHITE)
        screen.blit(text, (10, 40 + i * 20))

# Function to reset the game
def reset_game():
    global player, enemies, dots
    player = Player()
    enemies = [Enemy(chase=True, color=PINK)] + [Enemy(color=enemy_colors[i]) for i in range(3)]  # One chasing enemy (Pink), three random movers
    dots = [Dot(random.randint(1, WIDTH // GRID_SIZE - 2) * GRID_SIZE, random.randint(1, HEIGHT // GRID_SIZE - 2) * GRID_SIZE) for _ in range(10)]

# Initialize game objects
reset_game()

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)
    
    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, BLUE, (wall[0], wall[1], GRID_SIZE, GRID_SIZE))
    
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
    
    # Move player and enemies
    player.move(walls)
    for enemy in enemies:
        enemy.move(player)
    
    # Check for dot collection using distance-based collision detection
    dots = [dot for dot in dots if math.hypot(player.x - dot.x, player.y - dot.y) > COLLISION_DISTANCE]
    
    # Restart game if all dots are collected or if any enemy eats the player
    if not dots or any(math.hypot(player.x - enemy.x, player.y - enemy.y) < COLLISION_DISTANCE for enemy in enemies):
        reset_game()
    
    # Draw everything
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for dot in dots:
        dot.draw(screen)
    
    # Draw instructions
    draw_instructions()
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
