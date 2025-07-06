import pygame
import random

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Load sound file
ping = pygame.mixer.Sound('sound_files/ping.mp3')
pong = pygame.mixer.Sound('sound_files/pong.mp3')
get = pygame.mixer.Sound('sound_files/get.mp3')

# Set up the display
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

# Set up the game clock
clock = pygame.time.Clock()

# Set up the game's colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up the paddles and ball
paddle_width = 10
paddle_height = 100
paddle_speed = 5
ball_speed = 5
ball_size = 10
left_paddle = pygame.Rect(50, height/2 - paddle_height/2, paddle_width, paddle_height)
right_paddle = pygame.Rect(width - 50 - paddle_width, height/2 - paddle_height/2, paddle_width, paddle_height)
ball = pygame.Rect(width/2 - ball_size/2, height/2 - ball_size/2, ball_size, ball_size)

# Set up the ball's velocity
ball_velocity = [random.choice([ball_speed, -ball_speed]), random.randint(-ball_speed, ball_speed)]

# Set up the score
left_score = 0
right_score = 0
score_font = pygame.font.SysFont(None, 50)
title_font = pygame.font.SysFont(None, 24, bold=True)
instruction_font = pygame.font.SysFont(None, 18)

# Computer AI settings
computer_speed = 4  # Slightly slower than player for fairness
computer_reaction_delay = 0.1  # Small delay to make it beatable

# Function to make computer move
def computer_move():
    # Predict where the ball will be
    ball_center_y = ball.centery
    
    # Add some randomness to make it beatable
    if random.random() < 0.1:  # 10% chance to make a mistake
        ball_center_y += random.randint(-20, 20)
    
    # Move computer paddle towards ball
    if left_paddle.centery < ball_center_y - 10:
        left_paddle.y += computer_speed
    elif left_paddle.centery > ball_center_y + 10:
        left_paddle.y -= computer_speed
    
    # Keep paddle within screen bounds
    if left_paddle.top < 0:
        left_paddle.top = 0
    if left_paddle.bottom > height:
        left_paddle.bottom = height

# Function to draw instructions
def draw_instructions():
    # Title
    title_text = title_font.render("PONG vs COMPUTER", True, white)
    screen.blit(title_text, (10, 10))
    
    # Instructions
    instructions = [
        "OBJECTIVE: Score by getting ball past computer",
        "CONTROLS: Up/Down arrows to move right paddle",
        "SCORING: Points when ball passes opponent",
        "COMPUTER: Left paddle (AI controlled)",
        "FIRST TO SCORE WINS!"
    ]
    
    for i, instruction in enumerate(instructions):
        text = instruction_font.render(instruction, True, white)
        screen.blit(text, (10, 40 + i * 20))

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Move the computer paddle (left side)
    computer_move()
    
    # Move the player paddle (right side)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.move_ip(0, -paddle_speed)
    if keys[pygame.K_DOWN] and right_paddle.bottom < height:
        right_paddle.move_ip(0, paddle_speed)
    
    # Move the ball
    ball.move_ip(ball_velocity[0], ball_velocity[1])
    
    # Check for collisions
    if ball.left < 0:
        get.play()
        right_score += 1
        ball_velocity = [random.choice([ball_speed, -ball_speed]), random.randint(-ball_speed, ball_speed)]
        ball = pygame.Rect(width/2 - ball_size/2, height/2 - ball_size/2, ball_size, ball_size)
    if ball.right > width:
        get.play()
        left_score += 1
        ball_velocity = [random.choice([ball_speed, -ball_speed]), random.randint(-ball_speed, ball_speed)]
        ball = pygame.Rect(width/2 - ball_size/2, height/2 - ball_size/2, ball_size, ball_size)
    if ball.top < 0 or ball.bottom > height:
        pong.play()
        ball_velocity[1] = -ball_velocity[1]
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ping.play()
        ball_velocity[0] = -ball_velocity[0]
    
    # Draw the game
    screen.fill(black)
    pygame.draw.rect(screen, white, left_paddle)
    pygame.draw.rect(screen, white, right_paddle)
    pygame.draw.ellipse(screen, white, ball)
    left_score_text = score_font.render(str(left_score), True, white)
    right_score_text = score_font.render(str(right_score), True, white)
    screen.blit(left_score_text, (width/4 - left_score_text.get_width()/2, 50))
    screen.blit(right_score_text, (3*width/4 - right_score_text.get_width()/2, 50))

    # Draw instructions
    draw_instructions()

    # Update the screen
    pygame.display.flip()

    # Wait for the next frame
    clock.tick(60)

#Clean up Pygame
pygame.quit()