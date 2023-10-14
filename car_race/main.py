import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
ROAD_COLOR = (100, 100, 100)
CAR_WIDTH, CAR_HEIGHT = 80, 100
ENEMY_WIDTH, ENEMY_HEIGHT = 80, 80
ENEMY_COUNT = 5  # Number of enemy cars
LANE_COUNT = 5  # Number of lanes

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Race Game")

# Lane properties
lane_width = WIDTH // LANE_COUNT
lane_color = (255, 255, 255)

# Car properties
car_x = lane_width * (LANE_COUNT // 2) - CAR_WIDTH // 2
car_y = HEIGHT - CAR_HEIGHT - 10
car_speed = 5

# Enemy car properties
enemies = []
enemy_x_positions = [i * (WIDTH // LANE_COUNT) + (WIDTH // LANE_COUNT - ENEMY_WIDTH) // 2 for i in range(LANE_COUNT)]

for i in range(ENEMY_COUNT):
    enemy_x = enemy_x_positions[i]
    enemy_y = random.randint(-HEIGHT, 0)
    enemy_speed = random.randint(2, 6)
    enemy_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    enemies.append((enemy_x, enemy_y, enemy_speed, enemy_color))

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < WIDTH - CAR_WIDTH:
        car_x += car_speed

    # Move the enemy cars
    for i in range(ENEMY_COUNT):
        enemies[i] = (enemies[i][0], enemies[i][1] + enemies[i][2], enemies[i][2], enemies[i][3])

        # Reset the enemy car when it goes off-screen
        if enemies[i][1] > HEIGHT:
            enemy_x = enemy_x_positions[i]
            enemy_y = random.randint(-HEIGHT, 0)
            enemy_speed = random.randint(2, 6)
            enemy_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            enemies[i] = (enemy_x, enemy_y, enemy_speed, enemy_color)

        # Check for collisions
        if (
            car_x < enemies[i][0] + ENEMY_WIDTH
            and car_x + CAR_WIDTH > enemies[i][0]
            and car_y < enemies[i][1] + ENEMY_HEIGHT
            and car_y + CAR_HEIGHT > enemies[i][1]
        ):
            print("Game Over!")
            running = False

    # Clear the screen
    screen.fill(ROAD_COLOR)

    # Draw lane lines
    for i in range(LANE_COUNT - 1):
        lane_x = (i + 1) * lane_width
        pygame.draw.rect(screen, lane_color, (lane_x, 0, 4, HEIGHT))

    # Draw the car
    pygame.draw.rect(screen, (255, 0, 0), (car_x, car_y, CAR_WIDTH, CAR_HEIGHT))

    # Draw the enemy cars
    for enemy in enemies:
        pygame.draw.rect(screen, enemy[3], (enemy[0], enemy[1], ENEMY_WIDTH, ENEMY_HEIGHT))

    # Update the screen
    pygame.display.update()

    # Control the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()
