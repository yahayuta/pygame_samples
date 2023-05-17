import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = WINDOW_WIDTH // BLOCK_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // BLOCK_SIZE
WINDOW_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Tetris')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Define Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I-shape
    [[1, 1], [1, 1]],  # O-shape
    [[1, 1, 0], [0, 1, 1]],  # Z-shape
    [[0, 1, 1], [1, 1, 0]],  # S-shape
    [[1, 1, 1], [0, 1, 0]],  # T-shape
    [[1, 1, 1], [0, 0, 1]],  # L-shape
    [[1, 1, 1], [1, 0, 0]]   # J-shape
]

# Define Tetromino colors
COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]

# Initialize the grid
grid = [[BLACK] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

def draw_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            pygame.draw.rect(WINDOW_SURFACE, grid[row][col], (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_tetromino(tetromino, row, col, color):
    for r in range(len(tetromino)):
        for c in range(len(tetromino[r])):
            if tetromino[r][c] == 1:
                pygame.draw.rect(WINDOW_SURFACE, color, ((col + c) * BLOCK_SIZE, (row + r) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def is_collision(tetromino, row, col):
    for r in range(len(tetromino)):
        for c in range(len(tetromino[r])):
            if tetromino[r][c] and (row + r >= GRID_HEIGHT or col + c < 0 or col + c >= GRID_WIDTH or grid[row + r][col + c] != BLACK):
                return True
    return False

def rotate_tetromino(tetromino):
    return list(zip(*reversed(tetromino)))

def clear_rows():
    full_rows = [row for row in range(GRID_HEIGHT) if all(cell != BLACK for cell in grid[row])]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [BLACK] * GRID_WIDTH)

# Initialize the current tetromino
current_tetromino = random.choice(SHAPES)
current_color = random.choice(COLORS)
rotation = 0
tetromino_row = 0
tetromino_col = GRID_WIDTH // 2 - len(current_tetromino[0]) // 2

# Game loop
running = True
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.5

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not is_collision(current_tetromino, tetromino_row, tetromino_col - 1):
                    tetromino_col -= 1
            elif event.key == pygame.K_RIGHT:
                if not is_collision(current_tetromino, tetromino_row, tetromino_col + 1):
                    tetromino_col += 1
            elif event.key == pygame.K_DOWN:
                if not is_collision(current_tetromino, tetromino_row + 1, tetromino_col):
                    tetromino_row += 1
            elif event.key == pygame.K_UP:
                rotated = rotate_tetromino(current_tetromino)
                if not is_collision(rotated, tetromino_row, tetromino_col):
                    current_tetromino = rotated

    # Update the game
    if not is_collision(current_tetromino, tetromino_row + 1, tetromino_col):
        tetromino_row += 1
        fall_time = pygame.time.get_ticks()
    else:
        for r in range(len(current_tetromino)):
            for c in range(len(current_tetromino[r])):
                if current_tetromino[r][c] == 1:
                    grid[tetromino_row + r][tetromino_col + c] = current_color
        clear_rows()
        current_tetromino = random.choice(SHAPES)
        current_color = random.choice(COLORS)
        tetromino_row = 0
        tetromino_col = GRID_WIDTH // 2 - len(current_tetromino[0]) // 2

    # Draw the game
    WINDOW_SURFACE.fill(BLACK)
    draw_grid()
    draw_tetromino(current_tetromino, tetromino_row, tetromino_col, current_color)
    pygame.display.update()

    # Check if the game is over
    if any(cell != BLACK for cell in grid[0]):
        running = False

    # Adjust the game speed
    if pygame.time.get_ticks() - fall_time >= fall_speed * 1000:
        if not is_collision(current_tetromino, tetromino_row + 1, tetromino_col):
            tetromino_row += 1
            fall_time = pygame.time.get_ticks()

    # Set the maximum FPS
    clock.tick(60)

# Quit the game
pygame.quit()
