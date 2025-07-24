import pygame
import random
import time
import os

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()


# Load sound files
paddle_sound = pygame.mixer.Sound('sound_files/paddle.wav')
brick_sound = pygame.mixer.Sound('sound_files/brick.wav')
wall_sound = pygame.mixer.Sound('sound_files/wall.wav')
levelup_sound = pygame.mixer.Sound('sound_files/levelup.wav')
gameover_sound = pygame.mixer.Sound('sound_files/gameover.wav')

# Background music
bgm_path = 'sound_files/bgm.wav'
pygame.mixer.music.load(bgm_path)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop forever
music_muted = False

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
level = 1  # Add level variable
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 24, bold=True)
instruction_font = pygame.font.SysFont(None, 16)
lives = 3
font_big = pygame.font.SysFont(None, 64)
game_over = False

# Set brick variables
brick_width = 60
brick_height = 15
brick_color = (200, 50, 50)
brick_padding = 5
brick_offset_top = 50
brick_offset_left = 20
brick_rows_base = 5  # base rows for level 1
brick_cols = int(screen_width / (brick_width + brick_padding))

# Power-up variables
powerup_active = False
powerup_timer = 0
powerup_rect = None
powerup_type = None
powerup_fall_speed = 1
powerup_duration = 500  # frames
powerup_chance = 0.2  # 20% chance to spawn on brick break

# Brick types
BRICK_NORMAL = 0
BRICK_MULTI = 1
BRICK_UNBREAKABLE = 2
brick_colors = {BRICK_NORMAL: (200, 50, 50), BRICK_MULTI: (50, 50, 200), BRICK_UNBREAKABLE: (120, 120, 120)}

combo_count = 0
combo_timer = 0
combo_time_window = 60  # frames
combo_bonus = 100
combo_display_timer = 0
combo_display_text = ''
level_start_time = time.time()
speed_bonus = 0
speed_display_timer = 0
speed_display_text = ''

high_score_file = 'breakout_high_score.txt'

def load_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, 'r') as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_high_score(score):
    with open(high_score_file, 'w') as f:
        f.write(str(score))

high_score = load_high_score()

def create_bricks(level):
    bricks = []
    brick_rows = brick_rows_base + (level - 1)
    for row in range(brick_rows):
        for col in range(brick_cols):
            brick_x = brick_offset_left + col * (brick_width + brick_padding)
            brick_y = brick_offset_top + row * (brick_height + brick_padding)
            # Randomly assign brick type
            r = random.random()
            if r < 0.7:
                brick_type = BRICK_NORMAL
                hits = 1
            elif r < 0.9:
                brick_type = BRICK_MULTI
                hits = 2
            else:
                brick_type = BRICK_UNBREAKABLE
                hits = -1
            bricks.append({'rect': pygame.Rect(brick_x, brick_y, brick_width, brick_height), 'type': brick_type, 'hits': hits})
    return bricks

bricks = create_bricks(level)

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                # Mute/unmute music
                music_muted = not music_muted
                if music_muted:
                    pygame.mixer.music.set_volume(0)
                else:
                    pygame.mixer.music.set_volume(0.5)

    if game_over:
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        # Play game over sound once
        if not hasattr(game_over, 'played_sound'):
            gameover_sound.play()
            game_over.played_sound = True
        screen.fill((0, 0, 0))
        over_text = font_big.render('GAME OVER', True, (255, 0, 0))
        screen.blit(over_text, (screen_width//2 - 180, screen_height//2 - 60))
        restart_text = font.render('Press R to Restart or Q to Quit', True, (255, 255, 255))
        screen.blit(restart_text, (screen_width//2 - 200, screen_height//2 + 10))
        high_score_text = font.render(f'High Score: {high_score}', True, (0, 255, 255))
        screen.blit(high_score_text, (screen_width//2 - 120, screen_height//2 + 60))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_r:
                    # Reset all game state
                    lives = 3
                    score = 0
                    level = 1
                    ball_x = int(screen_width/2)
                    ball_y = int(screen_height/2)
                    paddle_x = int(screen_width/2)
                    paddle_width = 120
                    bricks = create_bricks(level)
                    powerup_active = False
                    powerup_rect = None
                    powerup_type = None
                    combo_count = 0
                    combo_timer = 0
                    combo_display_timer = 0
                    combo_display_text = ''
                    speed_display_timer = 0
                    speed_display_text = ''
                    level_start_time = time.time()
                    game_over = False
                    if hasattr(game_over, 'played_sound'):
                        delattr(game_over, 'played_sound')
        continue

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
        lives -= 1
        if lives <= 0:
            game_over = True
        else:
            # Reset ball and paddle
            ball_x = int(screen_width/2)
            ball_y = int(screen_height/2)
            paddle_x = int(screen_width/2)
            paddle_width = 120
            powerup_active = False
            powerup_rect = None
            powerup_type = None
            combo_count = 0
            combo_timer = 0
            combo_display_timer = 0
            combo_display_text = ''
            speed_display_timer = 0
            speed_display_text = ''
            # Small pause
            pygame.display.update()
            pygame.time.delay(1000)

    # Handle ball collisions with paddle
    if ball_speed_y > 0 and paddle_x - paddle_width/2 < ball_x < paddle_x + paddle_width/2 and \
            paddle_y - paddle_height/2 < ball_y < paddle_y + paddle_height/2:
        paddle_sound.play()
        ball_speed_y *= -1
        score += 10

    # Handle ball collisions with bricks
    for brick in bricks[:]:
        brect = brick['rect'] if isinstance(brick, dict) else brick
        if ball_speed_y < 0 and brect.collidepoint(ball_x, ball_y):
            brick_sound.play()
            # Unbreakable
            if brick.get('type', BRICK_NORMAL) == BRICK_UNBREAKABLE:
                ball_speed_y *= -1
                continue
            # Multi-hit
            if brick.get('type', BRICK_NORMAL) == BRICK_MULTI:
                brick['hits'] -= 1
                if brick['hits'] <= 0:
                    bricks.remove(brick)
                    score += 40
                else:
                    score += 10
                ball_speed_y *= -1
                # Combo logic
                combo_count += 1
                combo_timer = combo_time_window
                continue
            # Normal
            bricks.remove(brick)
            ball_speed_y *= -1
            score += 20
            # Combo logic
            combo_count += 1
            combo_timer = combo_time_window
            # Power-up spawn
            if not powerup_active and random.random() < powerup_chance:
                powerup_rect = pygame.Rect(brect.x + brick_width//4, brect.y, brick_width//2, brick_height)
                powerup_type = 'expand'
                powerup_active = True
                powerup_timer = 0
    # Combo timer and bonus
    if combo_timer > 0:
        combo_timer -= 1
        if combo_timer == 0 and combo_count > 1:
            score += combo_bonus * (combo_count - 1)
            combo_display_text = f'Combo! +{combo_bonus * (combo_count - 1)}'
            combo_display_timer = 60
            combo_count = 0
    # Power-up falling
    if powerup_active and powerup_rect:
        powerup_rect.y += powerup_fall_speed
        # Check for catch by paddle
        paddle_rect = pygame.Rect(int(paddle_x - paddle_width/2), int(paddle_y - paddle_height/2), paddle_width, paddle_height)
        if powerup_rect.colliderect(paddle_rect):
            if powerup_type == 'expand':
                paddle_width *= 1.5
                powerup_timer = 0
            powerup_active = False
            powerup_rect = None
            powerup_type = None
        # Missed (falls below screen)
        elif powerup_rect.y > screen_height:
            powerup_active = False
            powerup_rect = None
            powerup_type = None
    # Power-up timer (shrink paddle back after duration)
    if paddle_width > 120:
        powerup_timer += 1
        if powerup_timer > powerup_duration:
            paddle_width = 120
            powerup_timer = 0
    # Check for level completion
    if not bricks:
        # Speed bonus
        elapsed = time.time() - level_start_time
        if elapsed < 30:
            speed_bonus = int(500 - 10 * elapsed)
            if speed_bonus > 0:
                score += speed_bonus
                speed_display_text = f'Speed Bonus! +{speed_bonus}'
                speed_display_timer = 90
        levelup_sound.play()
        level_start_time = time.time()
        level += 1
        # Increase ball speed slightly each level
        ball_speed_x *= 1.15 if ball_speed_x > 0 else -1.15
        ball_speed_y *= 1.15 if ball_speed_y > 0 else -1.15
        # Reset ball and paddle
        ball_x = int(screen_width/2)
        ball_y = int(screen_height/2)
        paddle_x = int(screen_width/2)
        # Create new bricks for next level
        bricks = create_bricks(level)

    # Handle paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > paddle_width/2:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width/2:
        paddle_x += paddle_speed

    # Draw everything
    # --- Background Gradient ---
    for y in range(screen_height):
        color = (
            int(10 + 30 * y / screen_height),
            int(10 + 60 * y / screen_height),
            int(40 + 120 * y / screen_height)
        )
        pygame.draw.line(screen, color, (0, y), (screen_width, y))

    # --- Ball with Shine and Border ---
    ball_center = (int(ball_x), int(ball_y))
    pygame.draw.circle(screen, (255, 255, 255), ball_center, ball_radius)
    pygame.draw.circle(screen, (0, 200, 255), ball_center, ball_radius, 3)  # Border
    # Shine effect
    shine_rect = pygame.Rect(ball_center[0] - ball_radius//2, ball_center[1] - ball_radius//2, ball_radius, ball_radius//2)
    pygame.draw.ellipse(screen, (220, 255, 255), shine_rect)

    # --- Paddle with Border ---
    paddle_rect = pygame.Rect(int(paddle_x - paddle_width/2), int(paddle_y - paddle_height/2), paddle_width, paddle_height)
    pygame.draw.rect(screen, (255, 255, 255), paddle_rect)
    pygame.draw.rect(screen, (0, 200, 255), paddle_rect, 3)

    # --- Bricks with Fade Animation (simple color effect) ---
    for brick in bricks:
        color = brick_colors.get(brick.get('type', BRICK_NORMAL), (200, 50, 50)) if isinstance(brick, dict) else (200, 50, 50)
        rect = brick['rect'] if isinstance(brick, dict) else brick
        # Add a border and a slight gradient
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)
        # Simulate a shine on the top of the brick
        shine = pygame.Rect(rect.x, rect.y, rect.width, rect.height//3)
        pygame.draw.rect(screen, (min(color[0]+55,255), min(color[1]+55,255), min(color[2]+55,255)), shine)

    # Draw power-up
    if powerup_active and powerup_rect:
        pygame.draw.rect(screen, (0, 255, 0), powerup_rect)
        pygame.draw.rect(screen, (255, 255, 255), powerup_rect, 2)

    # Draw combo bonus
    if combo_display_timer > 0:
        combo_display_timer -= 1
        combo_text = font.render(combo_display_text, True, (255, 255, 0))
        screen.blit(combo_text, (screen_width//2 - 80, 100))
    # Draw speed bonus
    if speed_display_timer > 0:
        speed_display_timer -= 1
        speed_text = font.render(speed_display_text, True, (0, 255, 255))
        screen.blit(speed_text, (screen_width//2 - 100, 140))
    score_text = font.render("Score:    {}".format(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 200))
    # Draw lives
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 0))
    screen.blit(lives_text, (10, 240))
    level_text = font.render("Level: {}".format(level), True, (255, 255, 0))
    screen.blit(level_text, (10, 280))
    # Draw high score
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 255, 255))
    screen.blit(high_score_text, (10, 320))
    # Draw instructions
    draw_instructions()
    pygame.display.update()

# Quit Pygame
pygame.quit()
