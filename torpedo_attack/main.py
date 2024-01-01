import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Torpedo Attack")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Torpedo settings
torpedo_width = 10
torpedo_height = 50
torpedo_speed = 5
torpedo_fired = False

# Enemy ship settings
ship_width = 100
ship_height = 10
ship_speed = random.randint(2, 5)  # Random speed

# Initialize ship position
ship_x = -ship_width  # Start off-screen
ship_y = 50  # Place ship at the top of the screen

# Score
score = 0

def draw_torpedo(x, y):
    pygame.draw.rect(screen, white, (x, y, torpedo_width, torpedo_height))

def draw_enemy_ship(x, y):
    pygame.draw.rect(screen, red, (x, y, ship_width, ship_height))

# Game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not torpedo_fired:
                torpedo_fired = True
                torpedo_x = screen_width // 2 - torpedo_width // 2
                torpedo_y = screen_height - torpedo_height

    # Update torpedo position
    if torpedo_fired:
        torpedo_y -= torpedo_speed
        if torpedo_y < -torpedo_height:
            torpedo_fired = False

    # Update enemy ship position
    ship_x += ship_speed
    if ship_x > screen_width:
        ship_x = -ship_width
        ship_speed = random.randint(2, 5)  # Reset speed

    # Check for collisions
    if torpedo_fired and torpedo_x < ship_x + ship_width and torpedo_x + torpedo_width > ship_x and torpedo_y < ship_y + ship_height and torpedo_y + torpedo_height > ship_y:
        score += 1
        torpedo_fired = False
        ship_x = -ship_width  # Reset ship position

    # Fill the screen with black
    screen.fill(black)

    # Draw objects
    if torpedo_fired:
        draw_torpedo(torpedo_x, torpedo_y)
        
    draw_enemy_ship(ship_x, ship_y)  # Adjust ship position

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, white)
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
