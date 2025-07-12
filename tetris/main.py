import pygame
import random
import json
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
GRID_SIZE = 22
COLUMNS, ROWS = 10, 20
GRID_X = 40
GRID_Y = 60
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
COLORS = [(0, 255, 255), (0, 0, 255), (255, 165, 0), (255, 255, 0),
          (0, 255, 0), (128, 0, 128), (255, 0, 0)]

# Scoring system
SCORE_VALUES = {1: 100, 2: 300, 3: 500, 4: 800}
COMBO_MULTIPLIER = 50

# Tetromino shapes with proper wall kick data
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

# Game states
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game_over"

# Game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris Enhanced")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 12)
title_font = pygame.font.SysFont("Arial", 16, bold=True)
large_font = pygame.font.SysFont("Arial", 24, bold=True)
huge_font = pygame.font.SysFont("Arial", 32, bold=True)

class Tetromino:
    def __init__(self, shape_idx=None):
        if shape_idx is None:
            shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = [row[:] for row in SHAPES[shape_idx]]
        self.color = COLORS[shape_idx]
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.shape_idx = shape_idx

    def rotate(self):
        # Rotate the shape
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def get_ghost_position(self, grid):
        """Calculate where the piece would land"""
        ghost_y = self.y
        while not self.check_collision_at_position(self.x, ghost_y + 1, self.shape, grid):
            ghost_y += 1
        return ghost_y

    def check_collision_at_position(self, x, y, shape, grid):
        """Check collision at specific position"""
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    check_x, check_y = x + col_idx, y + row_idx
                    if (check_x < 0 or check_x >= COLUMNS or 
                        check_y >= ROWS or 
                        (check_y >= 0 and grid[check_y][check_x] != BLACK)):
                        return True
        return False

    def draw(self, x_offset=0, y_offset=0, alpha=255):
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    color = list(self.color)
                    if alpha < 255:
                        color.append(alpha)
                    pygame.draw.rect(screen, color,
                                   ((self.x + col_idx) * GRID_SIZE + GRID_X + x_offset, 
                                    (self.y + row_idx) * GRID_SIZE + GRID_Y + y_offset, 
                                    GRID_SIZE, GRID_SIZE))

class Tetris:
    def __init__(self):
        self.reset_game()
        self.high_score = self.load_high_score()

    def reset_game(self):
        self.grid = [[BLACK] * COLUMNS for _ in range(ROWS)]
        self.tetromino = Tetromino()
        self.next_piece = Tetromino()
        self.held_piece = None
        self.can_hold = True
        self.running = True
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.combo = 0
        self.game_state = MENU
        self.drop_time = 0
        self.drop_speed = 500  # milliseconds

    def load_high_score(self):
        try:
            with open('tetris_high_score.json', 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
        except:
            return 0

    def save_high_score(self):
        try:
            with open('tetris_high_score.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass

    def check_collision(self, dx=0, dy=0, shape=None):
        if shape is None:
            shape = self.tetromino.shape
        return self.tetromino.check_collision_at_position(
            self.tetromino.x + dx, self.tetromino.y + dy, shape, self.grid)

    def merge_tetromino(self):
        for row_idx, row in enumerate(self.tetromino.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    self.grid[self.tetromino.y + row_idx][self.tetromino.x + col_idx] = self.tetromino.color
        self.tetromino = self.next_piece
        self.next_piece = Tetromino()
        self.can_hold = True
        if self.check_collision():
            self.game_state = GAME_OVER
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

    def clear_lines(self):
        lines_to_clear = []
        for y in range(ROWS):
            if all(cell != BLACK for cell in self.grid[y]):
                lines_to_clear.append(y)
        
        if lines_to_clear:
            # Remove cleared lines
            for y in reversed(lines_to_clear):
                del self.grid[y]
            
            # Add new empty lines at top
            for _ in range(len(lines_to_clear)):
                self.grid.insert(0, [BLACK] * COLUMNS)
            
            # Update score and combo
            lines_cleared = len(lines_to_clear)
            self.lines_cleared += lines_cleared
            self.score += SCORE_VALUES.get(lines_cleared, 0) * self.level
            self.score += self.combo * COMBO_MULTIPLIER
            
            # Level up every 10 lines
            self.level = self.lines_cleared // 10 + 1
            self.drop_speed = max(50, 500 - (self.level - 1) * 50)
        else:
            self.combo = 0

    def move_tetromino(self, dx, dy):
        if not self.check_collision(dx, dy):
            self.tetromino.x += dx
            self.tetromino.y += dy
        elif dy > 0:
            self.merge_tetromino()
            self.clear_lines()

    def rotate_tetromino(self):
        old_shape = [row[:] for row in self.tetromino.shape]
        self.tetromino.rotate()
        
        # Wall kick system
        if self.check_collision():
            # Try wall kicks
            kicks = [
                (-1, 0), (1, 0), (0, -1),  # Left, Right, Up
                (-1, -1), (1, -1), (-2, 0), (2, 0)  # Diagonal and further
            ]
            
            for dx, dy in kicks:
                if not self.check_collision(dx, dy):
                    self.tetromino.x += dx
                    self.tetromino.y += dy
                    return
            
            # If no wall kick works, revert rotation
            self.tetromino.shape = old_shape

    def hold_piece(self):
        if not self.can_hold:
            return
        
        if self.held_piece is None:
            self.held_piece = Tetromino(self.tetromino.shape_idx)
            self.tetromino = self.next_piece
            self.next_piece = Tetromino()
        else:
            # Swap current piece with held piece
            current_shape_idx = self.tetromino.shape_idx
            self.tetromino = Tetromino(self.held_piece.shape_idx)
            self.held_piece = Tetromino(current_shape_idx)
        
        self.can_hold = False

    def hard_drop(self):
        while not self.check_collision(0, 1):
            self.tetromino.y += 1
            self.score += 2  # Bonus points for hard drop
        self.merge_tetromino()
        self.clear_lines()

    def draw_grid(self):
        # Draw background
        pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH, HEIGHT))
        
        # Draw grid background with better styling
        grid_rect = (GRID_X - 3, GRID_Y - 3, 
                    COLUMNS * GRID_SIZE + 6, ROWS * GRID_SIZE + 6)
        pygame.draw.rect(screen, LIGHT_GRAY, grid_rect)
        pygame.draw.rect(screen, GRAY, grid_rect, 3)
        
        # Draw grid lines
        for x in range(COLUMNS + 1):
            pygame.draw.line(screen, DARK_GRAY, 
                           (GRID_X + x * GRID_SIZE, GRID_Y), 
                           (GRID_X + x * GRID_SIZE, GRID_Y + ROWS * GRID_SIZE))
        for y in range(ROWS + 1):
            pygame.draw.line(screen, DARK_GRAY, 
                           (GRID_X, GRID_Y + y * GRID_SIZE), 
                           (GRID_X + COLUMNS * GRID_SIZE, GRID_Y + y * GRID_SIZE))
        
        # Draw placed pieces with borders
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                if color != BLACK:
                    piece_rect = (x * GRID_SIZE + GRID_X, y * GRID_SIZE + GRID_Y, 
                                GRID_SIZE, GRID_SIZE)
                    pygame.draw.rect(screen, color, piece_rect)
                    pygame.draw.rect(screen, BLACK, piece_rect, 1)

    def draw_ghost_piece(self):
        if self.game_state == PLAYING:
            ghost_y = self.tetromino.get_ghost_position(self.grid)
            # Draw ghost piece with better visibility
            for row_idx, row in enumerate(self.tetromino.shape):
                for col_idx, cell in enumerate(row):
                    if cell:
                        ghost_rect = ((self.tetromino.x + col_idx) * GRID_SIZE + GRID_X, 
                                     (ghost_y + row_idx) * GRID_SIZE + GRID_Y, 
                                     GRID_SIZE, GRID_SIZE)
                        pygame.draw.rect(screen, (*self.tetromino.color, 80), ghost_rect)
                        pygame.draw.rect(screen, self.tetromino.color, ghost_rect, 2)

    def draw_side_panel(self):
        panel_x = GRID_X + COLUMNS * GRID_SIZE + 20
        
        # Draw side panel background
        panel_rect = (panel_x - 10, 40, 150, HEIGHT - 80)
        pygame.draw.rect(screen, DARK_GRAY, panel_rect)
        pygame.draw.rect(screen, GRAY, panel_rect, 2)
        
        # Score
        score_text = title_font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (panel_x, 60))
        
        # Level
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(level_text, (panel_x, 80))
        
        # Lines cleared
        lines_text = font.render(f"Lines: {self.lines_cleared}", True, WHITE)
        screen.blit(lines_text, (panel_x, 100))
        
        # Combo
        if self.combo > 0:
            combo_text = font.render(f"Combo: {self.combo}", True, (255, 255, 0))
            screen.blit(combo_text, (panel_x, 120))
        
        # High score
        high_score_text = font.render(f"High Score: {self.high_score}", True, (255, 215, 0))
        screen.blit(high_score_text, (panel_x, 150))
        
        # Next piece section
        next_text = title_font.render("Next:", True, WHITE)
        screen.blit(next_text, (panel_x, 180))
        
        # Draw next piece with better styling
        next_piece_x = panel_x + 15
        next_piece_y = 200
        for row_idx, row in enumerate(self.next_piece.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    piece_rect = (next_piece_x + col_idx * 15, next_piece_y + row_idx * 15, 15, 15)
                    pygame.draw.rect(screen, self.next_piece.color, piece_rect)
                    pygame.draw.rect(screen, BLACK, piece_rect, 1)
        
        # Held piece section
        hold_text = title_font.render("Hold:", True, WHITE)
        screen.blit(hold_text, (panel_x, 270))
        
        if self.held_piece:
            hold_piece_x = panel_x + 15
            hold_piece_y = 290
            for row_idx, row in enumerate(self.held_piece.shape):
                for col_idx, cell in enumerate(row):
                    if cell:
                        color = self.held_piece.color if self.can_hold else GRAY
                        piece_rect = (hold_piece_x + col_idx * 15, hold_piece_y + row_idx * 15, 15, 15)
                        pygame.draw.rect(screen, color, piece_rect)
                        pygame.draw.rect(screen, BLACK, piece_rect, 1)
        
        # Controls reminder
        controls_text = font.render("Controls:", True, WHITE)
        screen.blit(controls_text, (panel_x, 360))
        
        controls = [
            "←→ Move",
            "↑ Rotate", 
            "↓ Soft Drop",
            "Space Hard Drop",
            "H Hold Piece",
            "P Pause"
        ]
        
        for i, control in enumerate(controls):
            control_text = font.render(control, True, LIGHT_GRAY)
            screen.blit(control_text, (panel_x, 380 + i * 16))

    def draw_menu(self):
        # Draw background with gradient effect
        for y in range(HEIGHT):
            color_value = int(255 * (1 - y / HEIGHT))
            pygame.draw.line(screen, (color_value, color_value, color_value), (0, y), (WIDTH, y))
        
        # Title with shadow effect
        title_text = huge_font.render("TETRIS", True, WHITE)
        title_shadow = huge_font.render("TETRIS", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2 + 2, 120 + 2))
        screen.blit(title_shadow, title_rect)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 120))
        screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = title_font.render("Enhanced Edition", True, (255, 215, 0))
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, 150))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Menu options with better styling
        options = [
            ("Press SPACE to Start", WHITE),
            ("Press H for Hold Piece", LIGHT_GRAY),
            ("Press SPACE for Hard Drop", LIGHT_GRAY),
            ("Press P to Pause", LIGHT_GRAY),
            ("Arrow Keys to Move/Rotate", LIGHT_GRAY)
        ]
        
        for i, (option, color) in enumerate(options):
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, 220 + i * 30))
            screen.blit(text, text_rect)

    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Game over text with shadow
        game_over_text = huge_font.render("GAME OVER", True, (255, 0, 0))
        game_over_shadow = huge_font.render("GAME OVER", True, BLACK)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2 + 2, 180 + 2))
        screen.blit(game_over_shadow, game_over_rect)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, 180))
        screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = large_font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, 230))
        screen.blit(score_text, score_rect)
        
        # High score
        if self.score > self.high_score:
            high_score_text = title_font.render("NEW HIGH SCORE!", True, (255, 215, 0))
            high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, 260))
            screen.blit(high_score_text, high_score_rect)
        
        # Restart instruction
        restart_text = font.render("Press SPACE to Restart", True, LIGHT_GRAY)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, 320))
        screen.blit(restart_text, restart_rect)

    def draw_pause_screen(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Pause text with shadow
        pause_text = huge_font.render("PAUSED", True, (255, 255, 0))
        pause_shadow = huge_font.render("PAUSED", True, BLACK)
        pause_rect = pause_text.get_rect(center=(WIDTH // 2 + 2, HEIGHT // 2 + 2))
        screen.blit(pause_shadow, pause_rect)
        pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(pause_text, pause_rect)
        
        # Resume instruction
        resume_text = font.render("Press P to Resume", True, LIGHT_GRAY)
        resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(resume_text, resume_rect)

    def run(self):
        while self.running:
            # Clear screen with dark background
            screen.fill(DARK_GRAY)
            
            if self.game_state == MENU:
                self.draw_menu()
            elif self.game_state == PLAYING:
                self.draw_grid()
                self.draw_ghost_piece()
                self.tetromino.draw()
                self.draw_side_panel()
            elif self.game_state == PAUSED:
                self.draw_grid()
                self.draw_ghost_piece()
                self.tetromino.draw()
                self.draw_side_panel()
                self.draw_pause_screen()
            elif self.game_state == GAME_OVER:
                self.draw_grid()
                self.draw_side_panel()
                self.draw_game_over()
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_state == MENU:
                        if event.key == pygame.K_SPACE:
                            self.game_state = PLAYING
                    elif self.game_state == PLAYING:
                        if event.key == pygame.K_LEFT:
                            self.move_tetromino(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.move_tetromino(1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.move_tetromino(0, 1)
                        elif event.key == pygame.K_UP:
                            self.rotate_tetromino()
                        elif event.key == pygame.K_SPACE:
                            self.hard_drop()
                        elif event.key == pygame.K_h:
                            self.hold_piece()
                        elif event.key == pygame.K_p:
                            self.game_state = PAUSED
                    elif self.game_state == PAUSED:
                        if event.key == pygame.K_p:
                            self.game_state = PLAYING
                    elif self.game_state == GAME_OVER:
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                            self.game_state = PLAYING

            # Auto-drop
            if self.game_state == PLAYING:
                self.drop_time += clock.get_rawtime()
                if self.drop_time > self.drop_speed:
                    self.move_tetromino(0, 1)
                    self.drop_time = 0

            clock.tick(60)

# Start game
tetris = Tetris()
tetris.run()
pygame.quit()
