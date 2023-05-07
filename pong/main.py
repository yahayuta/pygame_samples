import pygame
import random

# Initialize Pygame
pygame.init()

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

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Move the paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.move_ip(0, -paddle_speed)
    if keys[pygame.K_s] and left_paddle.bottom < height:
        left_paddle.move_ip(0, paddle_speed)
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.move_ip(0, -paddle_speed)
    if keys[pygame.K_DOWN] and right_paddle.bottom < height:
        right_paddle.move_ip(0, paddle_speed)
    
    # Move the ball
    ball.move_ip(ball_velocity[0], ball_velocity[1])
    
    # Check for collisions
    if ball.left < 0:
        right_score += 1
        ball_velocity = [random.choice([ball_speed, -ball_speed]), random.randint(-ball_speed, ball_speed)]
        ball = pygame.Rect(width/2 - ball_size/2, height/2 - ball_size/2, ball_size, ball_size)
    if ball.right > width:
        left_score += 1
        ball_velocity = [random.choice([ball_speed, -ball_speed]), random.randint(-ball_speed, ball_speed)]
        ball = pygame.Rect(width/2 - ball_size/2, height/2 - ball_size/2, ball_size, ball_size)
    if ball.top < 0 or ball.bottom > height:
        ball_velocity[1] = -ball_velocity[1]
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
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

    # Update the screen
    pygame.display.flip()

    # Wait for the next frame
    clock.tick(60)

#Clean up Pygame
pygame.quit()