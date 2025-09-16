
import pygame
import sys
import os
import random

# --- Constants ---
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 480
GRID_WIDTH = 6
GRID_HEIGHT = 12
CELL_SIZE = 30
PLAYFIELD_WIDTH = GRID_WIDTH * CELL_SIZE
PLAYFIELD_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Playfield position on screen
PLAYFIELD_X = (SCREEN_WIDTH - PLAYFIELD_WIDTH) // 2
PLAYFIELD_Y = (SCREEN_HEIGHT - PLAYFIELD_HEIGHT) // 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRID_COLOR = (50, 50, 50)
PUYO_COLORS = [
    (255, 0, 0),    # Red
    (0, 0, 255),    # Blue
    (0, 255, 0),    # Green
    (255, 255, 0),  # Yellow
    (128, 0, 128),  # Purple
]

# Game settings
DROP_INTERVAL_NORMAL = 700  # Milliseconds
DROP_INTERVAL_FAST = 50

# --- Game Setup ---
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Puyo Puyo")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

# --- Sound Loading ---
def load_sounds():
    sounds = {}
    sound_dir = os.path.join(os.path.dirname(__file__), 'sound_files')
    try:
        sounds['rotate'] = pygame.mixer.Sound(os.path.join(sound_dir, 'rotate.wav'))
        sounds['land'] = pygame.mixer.Sound(os.path.join(sound_dir, 'land.wav'))
        sounds['pop'] = pygame.mixer.Sound(os.path.join(sound_dir, 'pop.wav'))
        sounds['game_over'] = pygame.mixer.Sound(os.path.join(sound_dir, 'game_over.wav'))
        for i in range(2, 5):
            sounds[f'combo{i}'] = pygame.mixer.Sound(os.path.join(sound_dir, f'combo{i}.wav'))
    except pygame.error as e:
        print(f"Could not load sound file: {e}")
        # Create dummy sound objects if loading fails
        for key in ['rotate', 'land', 'pop', 'game_over', 'combo2', 'combo3', 'combo4']:
            if key not in sounds:
                sounds[key] = pygame.mixer.Sound(buffer=b'')
    return sounds

sounds = load_sounds()

# --- Game State ---
grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
score = 0

class Puyo:
    """ A single Puyo block """
    def __init__(self, row, col, color_index):
        self.row = row
        self.col = col
        self.color_index = color_index

    def draw(self, surface):
        x = PLAYFIELD_X + self.col * CELL_SIZE
        y = PLAYFIELD_Y + self.row * CELL_SIZE
        pygame.draw.circle(surface, PUYO_COLORS[self.color_index], 
                           (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 2)

class Piece:
    """ The falling pair of Puyos """
    def __init__(self):
        self.puyos = [
            Puyo(0, GRID_WIDTH // 2 -1, random.randint(0, len(PUYO_COLORS) - 1)), # Center Puyo
            Puyo(-1, GRID_WIDTH // 2-1, random.randint(0, len(PUYO_COLORS) - 1))  # Pivot Puyo
        ]
        self.rotation_state = 0 # 0: Up, 1: Right, 2: Down, 3: Left

    def move(self, dx, dy):
        for puyo in self.puyos:
            puyo.col += dx
            puyo.row += dy

    def rotate(self):
        pivot = self.puyos[1]
        center = self.puyos[0]
        
        self.rotation_state = (self.rotation_state + 1) % 4
        
        if self.rotation_state == 0: # Up
            center.col, center.row = pivot.col, pivot.row - 1
        elif self.rotation_state == 1: # Right
            center.col, center.row = pivot.col + 1, pivot.row
        elif self.rotation_state == 2: # Down
            center.col, center.row = pivot.col, pivot.row + 1
        elif self.rotation_state == 3: # Left
            center.col, center.row = pivot.col - 1, pivot.row

    def draw(self, surface):
        for puyo in self.puyos:
            puyo.draw(surface)

# --- Helper Functions ---
def is_valid_position(piece):
    for puyo in piece.puyos:
        if not (0 <= puyo.col < GRID_WIDTH and puyo.row < GRID_HEIGHT):
            return False
        if puyo.row >= 0 and grid[puyo.row][puyo.col] is not None:
            return False
    return True

def lock_piece(piece):
    for puyo in piece.puyos:
        if puyo.row >= 0:
            grid[puyo.row][puyo.col] = puyo
    sounds['land'].play()

def find_and_clear_puyos():
    to_clear = set()
    visited = set()
    
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            if grid[r][c] is not None and (r, c) not in visited:
                color = grid[r][c].color_index
                group = set()
                q = [(r, c)]
                visited.add((r,c))
                
                while q:
                    curr_r, curr_c = q.pop(0)
                    group.add((curr_r, curr_c))
                    
                    for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < GRID_HEIGHT and 0 <= nc < GRID_WIDTH and \
                           (nr, nc) not in visited and grid[nr][nc] is not None and \
                           grid[nr][nc].color_index == color:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                if len(group) >= 4:
                    to_clear.update(group)

    if to_clear:
        for r, c in to_clear:
            grid[r][c] = None
        return len(to_clear)
    return 0

def apply_gravity():
    moved = False
    for c in range(GRID_WIDTH):
        empty_row = GRID_HEIGHT - 1
        for r in range(GRID_HEIGHT - 1, -1, -1):
            if grid[r][c] is not None:
                if r != empty_row:
                    grid[empty_row][c] = grid[r][c]
                    grid[empty_row][c].row = empty_row
                    grid[r][c] = None
                    moved = True
                empty_row -= 1
    return moved

def draw_playfield(surface):
    # Draw border
    pygame.draw.rect(surface, WHITE, (PLAYFIELD_X - 2, PLAYFIELD_Y - 2, PLAYFIELD_WIDTH + 4, PLAYFIELD_HEIGHT + 4), 2)
    # Draw grid cells
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            x = PLAYFIELD_X + c * CELL_SIZE
            y = PLAYFIELD_Y + r * CELL_SIZE
            pygame.draw.rect(surface, GRID_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 1)
    # Draw landed puyos
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            if grid[r][c] is not None:
                grid[r][c].draw(surface)

def draw_ui(surface, score, next_piece):
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (20, 20))
    
    # Draw next piece
    next_text = font.render("Next:", True, WHITE)
    surface.blit(next_text, (PLAYFIELD_X + PLAYFIELD_WIDTH + 30, PLAYFIELD_Y))
    for puyo in next_piece.puyos:
        x = PLAYFIELD_X + PLAYFIELD_WIDTH + 50 + (puyo.col - GRID_WIDTH // 2 + 1) * CELL_SIZE
        y = PLAYFIELD_Y + 60 + (puyo.row + 1) * CELL_SIZE
        pygame.draw.circle(surface, PUYO_COLORS[puyo.color_index], 
                           (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 2)

def draw_game_over(surface):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    
    text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40))
    surface.blit(text, text_rect)
    
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
    surface.blit(score_text, score_rect)

    restart_text = font.render("Press R to Restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 70))
    surface.blit(restart_text, restart_rect)

# --- Main Game Loop ---
def main():
    global grid, score
    
    running = True
    game_over = False
    
    current_piece = Piece()
    next_piece = Piece()
    
    drop_time = 0
    drop_interval = DROP_INTERVAL_NORMAL
    
    score = 0
    
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_piece.move(-1, 0)
                        if not is_valid_position(current_piece):
                            current_piece.move(1, 0)
                    elif event.key == pygame.K_RIGHT:
                        current_piece.move(1, 0)
                        if not is_valid_position(current_piece):
                            current_piece.move(-1, 0)
                    elif event.key == pygame.K_UP:
                        original_state = current_piece.rotation_state
                        original_puyos = [(p.row, p.col) for p in current_piece.puyos]
                        current_piece.rotate()
                        if not is_valid_position(current_piece):
                            # Revert rotation
                            current_piece.rotation_state = original_state
                            for i, (r, c) in enumerate(original_puyos):
                                current_piece.puyos[i].row = r
                                current_piece.puyos[i].col = c
                        else:
                            sounds['rotate'].play()
                    elif event.key == pygame.K_DOWN:
                        drop_interval = DROP_INTERVAL_FAST
            
            if event.type == pygame.KEYUP:
                if not game_over and event.key == pygame.K_DOWN:
                    drop_interval = DROP_INTERVAL_NORMAL

            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset game
                    grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
                    score = 0
                    current_piece = Piece()
                    next_piece = Piece()
                    game_over = False

        if not game_over:
            # Piece falling logic
            delta_time = clock.get_rawtime()
            drop_time += delta_time
            if drop_time > drop_interval:
                drop_time = 0
                current_piece.move(0, 1)
                if not is_valid_position(current_piece):
                    current_piece.move(0, -1)
                    lock_piece(current_piece)
                    
                    # --- Clearing and Combo Logic ---
                    combo = 0
                    while True:
                        cleared_count = find_and_clear_puyos()
                        if cleared_count > 0:
                            combo += 1
                            score += cleared_count * combo * 10
                            if combo > 1:
                                sound_key = f'combo{min(combo, 4)}'
                                sounds[sound_key].play()
                            else:
                                sounds['pop'].play()
                            
                            pygame.time.wait(300) # Pause for effect
                            apply_gravity()
                            # Redraw after gravity before next check
                            screen.fill(BLACK)
                            draw_playfield(screen)
                            draw_ui(screen, score, next_piece)
                            pygame.display.flip()
                            pygame.time.wait(300)
                        else:
                            break # No more clears, exit combo loop

                    # Spawn next piece
                    current_piece = next_piece
                    next_piece = Piece()
                    if not is_valid_position(current_piece):
                        game_over = True
                        sounds['game_over'].play()

        # --- Drawing ---
        draw_playfield(screen)
        if not game_over:
            current_piece.draw(screen)
            draw_ui(screen, score, next_piece)
        else:
            draw_game_over(screen)
            
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
