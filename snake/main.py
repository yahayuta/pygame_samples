import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Load sound files
try:
    eat_sound = pygame.mixer.Sound('sound_files/eat.wav')
    game_over_sound = pygame.mixer.Sound('sound_files/game_over.wav')
except:
    # Create simple sounds if files don't exist
    eat_sound = None
    game_over_sound = None

# Set up the display
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 200, 0)
GRAY = (100, 100, 100)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Fonts
font = pygame.font.SysFont('Arial', 24)
title_font = pygame.font.SysFont('Arial', 28, bold=True)
instruction_font = pygame.font.SysFont('Arial', 16)

class Snake:
    def __init__(self, wall_mode=False):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.speed = 10
        self.wall_mode = wall_mode

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new_x = cur[0] + x
        new_y = cur[1] + y
        
        if self.wall_mode:
            # Wall mode: Check for wall collision
            if new_x < 0 or new_x >= GRID_WIDTH or new_y < 0 or new_y >= GRID_HEIGHT:
                return False
            new = (new_x, new_y)
        else:
            # Wrap-around mode
            new = (new_x % GRID_WIDTH, new_y % GRID_HEIGHT)
        
        if new in self.positions[3:]:
            return False
        
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.speed = 10

    def render(self, surface):
        for i, p in enumerate(self.positions):
            color = DARK_GREEN if i == 0 else self.color
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE),
                             (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, WHITE, rect, 1)

class Food:
    def __init__(self, wall_mode=False):
        self.position = (0, 0)
        self.color = RED
        self.wall_mode = wall_mode
        self.randomize_position()

    def randomize_position(self):
        if self.wall_mode:
            # Avoid walls in wall mode
            self.position = (random.randint(1, GRID_WIDTH - 2),
                           random.randint(1, GRID_HEIGHT - 2))
        else:
            # Full grid in wrap-around mode
            self.position = (random.randint(0, GRID_WIDTH - 1),
                           random.randint(0, GRID_HEIGHT - 1))

    def render(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE,
                           self.position[1] * GRID_SIZE),
                          (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)

def draw_walls(surface):
    """Draw walls around the game area"""
    wall_thickness = 2
    # Top wall
    pygame.draw.rect(surface, GRAY, (0, 0, WIDTH, wall_thickness))
    # Bottom wall
    pygame.draw.rect(surface, GRAY, (0, HEIGHT - wall_thickness, WIDTH, wall_thickness))
    # Left wall
    pygame.draw.rect(surface, GRAY, (0, 0, wall_thickness, HEIGHT))
    # Right wall
    pygame.draw.rect(surface, GRAY, (WIDTH - wall_thickness, 0, wall_thickness, HEIGHT))

# Direction constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def draw_instructions(wall_mode):
    """Draw on-screen instructions"""
    # Title
    title_text = title_font.render("SNAKE", True, WHITE)
    screen.blit(title_text, (10, 10))
    
    # Instructions
    if wall_mode:
        instructions = [
            "OBJECTIVE: Eat food to grow longer",
            "CONTROLS: Arrow keys to change direction",
            "SCORING: Points for each food eaten",
            "GAME OVER: Hit yourself or walls",
            "WALL MODE: Visible walls around edges"
        ]
    else:
        instructions = [
            "OBJECTIVE: Eat food to grow longer",
            "CONTROLS: Arrow keys to change direction",
            "SCORING: Points for each food eaten",
            "GAME OVER: Hit yourself",
            "WRAP AROUND: Snake can pass through edges"
        ]
    
    for i, instruction in enumerate(instructions):
        text = instruction_font.render(instruction, True, WHITE)
        screen.blit(text, (10, 50 + i * 20))

def main():
    clock = pygame.time.Clock()
    
    # Choose game mode
    wall_mode = True  # Set to True for walls, False for wrap-around
    
    snake = Snake(wall_mode)
    food = Food(wall_mode)
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        food.randomize_position()
                        game_over = False
                else:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT

        if not game_over:
            # Update snake
            if not snake.update():
                game_over = True
                if game_over_sound:
                    game_over_sound.play()

            # Check for food collision
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 10
                snake.speed = min(20, 10 + snake.score // 50)  # Increase speed
                food.randomize_position()
                if eat_sound:
                    eat_sound.play()

        # Draw everything
        screen.fill(BLACK)
        
        # Draw walls if in wall mode
        if wall_mode:
            draw_walls(screen)
        
        # Draw grid (optional)
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

        snake.render(screen)
        food.render(screen)

        # Draw score
        score_text = font.render(f"Score: {snake.score}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT - 40))

        # Draw instructions
        draw_instructions(wall_mode)

        # Game over screen
        if game_over:
            game_over_text = title_font.render("GAME OVER!", True, RED)
            restart_text = font.render("Press SPACE to restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

        pygame.display.update()
        clock.tick(snake.speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 