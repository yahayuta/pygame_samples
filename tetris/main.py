import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
COLUMNS, ROWS = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
COLORS = [(0, 255, 255), (0, 0, 255), (255, 165, 0), (255, 255, 0),
          (0, 255, 0), (128, 0, 128), (255, 0, 0)]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

# Game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)
title_font = pygame.font.SysFont("Arial", 20, bold=True)

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self):
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color,
                                     ((self.x + col_idx) * GRID_SIZE, (self.y + row_idx) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Tetris:
    def __init__(self):
        self.grid = [[BLACK] * COLUMNS for _ in range(ROWS)]
        self.tetromino = Tetromino()
        self.running = True
        self.score = 0

    def check_collision(self, dx=0, dy=0):
        for row_idx, row in enumerate(self.tetromino.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    x, y = self.tetromino.x + col_idx + dx, self.tetromino.y + row_idx + dy
                    if x < 0 or x >= COLUMNS or y >= ROWS or (y >= 0 and self.grid[y][x] != BLACK):
                        return True
        return False

    def merge_tetromino(self):
        for row_idx, row in enumerate(self.tetromino.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    self.grid[self.tetromino.y + row_idx][self.tetromino.x + col_idx] = self.tetromino.color
        self.tetromino = Tetromino()
        if self.check_collision():
            self.running = False

    def clear_lines(self):
        new_grid = [row for row in self.grid if BLACK in row]
        cleared_lines = ROWS - len(new_grid)
        self.score += cleared_lines * 100
        while len(new_grid) < ROWS:
            new_grid.insert(0, [BLACK] * COLUMNS)
        self.grid = new_grid

    def move_tetromino(self, dx, dy):
        if not self.check_collision(dx, dy):
            self.tetromino.x += dx
            self.tetromino.y += dy
        elif dy > 0:
            self.merge_tetromino()
            self.clear_lines()

    def rotate_tetromino(self):
        old_shape = self.tetromino.shape[:]
        self.tetromino.rotate()
        if self.check_collision():
            self.tetromino.shape = old_shape

    def draw_grid(self):
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def draw_score(self):
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    def draw_instructions(self):
        # Title
        title_text = title_font.render("TETRIS", True, WHITE)
        screen.blit(title_text, (10, 40))
        
        # Instructions
        instructions = [
            "OBJECTIVE: Complete horizontal lines",
            "CONTROLS:",
            "  Left/Right: Move",
            "  Up: Rotate",
            "  Down: Drop faster",
            "SCORING: 100 points per line"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, WHITE)
            screen.blit(text, (10, 70 + i * 18))

    def run(self):
        drop_time = 0
        while self.running:
            screen.fill(BLACK)
            self.draw_grid()
            self.tetromino.draw()
            self.draw_score()
            self.draw_instructions()
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_tetromino(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_tetromino(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_tetromino(0, 1)
                    elif event.key == pygame.K_UP:
                        self.rotate_tetromino()

            drop_time += clock.get_rawtime()
            if drop_time > 500:
                self.move_tetromino(0, 1)
                drop_time = 0

            clock.tick(30)

# Start game
tetris = Tetris()
tetris.run()
pygame.quit()
