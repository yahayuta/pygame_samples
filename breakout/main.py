import pygame
import random

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Load sound file
paddle_sound = pygame.mixer.Sound('sound_files/paddle.mp3')
brick_sound = pygame.mixer.Sound('sound_files/brick.mp3')
wall_sound = pygame.mixer.Sound('sound_files/wall.mp3')

# Set screen dimensions
screen_width = 640
screen_height = 480

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")

# Set game variables
ball_x = int(screen_width/2)
ball_y = int(screen_height/2)
ball_radius = 20
ball_speed_x = 0.1
ball_speed_y = -0.1
paddle_x = int(screen_width/2)
paddle_y = screen_height - 50
paddle_width = 120
paddle_height = 10
paddle_speed = 1
score = 0
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 24, bold=True)
instruction_font = pygame.font.SysFont(None, 16)

# Set brick variables
brick_width = 60
brick_height = 15
brick_color = (200, 50, 50)
brick_padding = 5
brick_offset_top = 50
brick_offset_left = 20
brick_rows = 5
brick_cols = int(screen_width / (brick_width + brick_padding))

# Create bricks
bricks = []
for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x = brick_offset_left + col * (brick_width + brick_padding)
        brick_y = brick_offset_top + row * (brick_height + brick_padding)
        bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

# Function to draw instructions
def draw_instructions():
    # Title
    title_text = title_font.render("BREAKOUT", True, (255, 255, 255))
    screen.blit(title_text, (10, 10))
    
    # Instructions
    instructions = [
        "OBJECTIVE: Break all bricks with the ball",
        "CONTROLS: Left/Right arrows to move paddle",
        "SCORING: Points for bricks broken",
        "GAME OVER: Ball falls below paddle"
    ]
    
    for i, instruction in enumerate(instructions):
        text = instruction_font.render(instruction, True, (255, 255, 255))
        screen.blit(text, (10, 40 + i * 18))

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Handle ball collisions with walls
    if ball_x < ball_radius or ball_x > screen_width - ball_radius:
        wall_sound.play()
        ball_speed_x *= -1
    if ball_y < ball_radius:
        wall_sound.play()
        ball_speed_y *= -1
    if ball_y > screen_height - ball_radius:
        running = False

    # Handle ball collisions with paddle
    if ball_speed_y > 0 and paddle_x - paddle_width/2 < ball_x < paddle_x + paddle_width/2 and \
            paddle_y - paddle_height/2 < ball_y < paddle_y + paddle_height/2:
        paddle_sound.play()
        ball_speed_y *= -1
        score += 10

    # Handle ball collisions with bricks
    for brick in bricks:
        if ball_speed_y < 0 and brick.collidepoint(ball_x, ball_y):
            brick_sound.play()
            bricks.remove(brick)
            ball_speed_y *= -1
            score += 20

    # Handle paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > paddle_width/2:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width/2:
        paddle_x += paddle_speed

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_x), int(ball_y)), ball_radius)
    pygame.draw.rect(screen, (255, 255, 255), (int(paddle_x - paddle_width/2), int(paddle_y - paddle_height/2), paddle_width, paddle_height))
    for brick in bricks:
        pygame.draw.rect(screen, brick_color, brick)
    score_text = font.render("Score:    {}".format(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 200))
    
    # Draw instructions
    draw_instructions()
    
    pygame.display.update()

# Quit Pygame
pygame.quit()
