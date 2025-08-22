import pygame
import random
import os

# Constants
GRID_WIDTH = 20
GRID_HEIGHT = 15
CELL_SIZE = 40
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + 50 # Space for UI
NUM_ENEMIES = 3
NUM_ROCKS = 4

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game Assets
DIRT_IMG = None
PLAYER_IMG = None
POOKA_IMG = None
ROCK_IMG = None

HIGH_SCORE_FILE = "digdug_high_score.txt"
SCRIPT_DIR = os.path.dirname(__file__) #<-- absolute dir the script is in

# --- Classes ---
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = (1, 0)
        self.is_pumping = False
        self.attached_enemy = None
        self.lives = 3

    def draw(self, screen):
        screen.blit(PLAYER_IMG, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        if self.is_pumping and self.attached_enemy:
            start_pos = (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2)
            end_pos = (self.attached_enemy.x * CELL_SIZE + CELL_SIZE // 2, self.attached_enemy.y * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.line(screen, WHITE, start_pos, end_pos, 5)

class Rock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 'stable'
        self.fall_timer = 0

    def draw(self, screen):
        screen.blit(ROCK_IMG, (self.x * CELL_SIZE, self.y * CELL_SIZE))

    def update(self, dirt_grid):
        if self.state == 'stable':
            if self.y < GRID_HEIGHT - 1 and dirt_grid[self.x][self.y + 1].is_dug:
                self.fall_timer += 1
                if self.fall_timer > 30:
                    self.state = 'falling'
            else:
                self.fall_timer = 0
        elif self.state == 'falling':
            self.y += 0.2
            if self.y >= GRID_HEIGHT - 1 or not dirt_grid[self.x][int(self.y + 1)].is_dug:
                self.state = 'dead'
                self.y = int(self.y)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.move_timer = 0
        self.state = 'normal'
        self.inflation = 0
        self.ghost_timer = random.randint(100, 300)

    def draw(self, screen):
        if self.state == 'dying': return
        img_to_draw = POOKA_IMG.copy()
        if self.state == 'inflating':
            scale = 1 + self.inflation * 0.2
            img_to_draw = pygame.transform.scale(POOKA_IMG, (int(CELL_SIZE * scale), int(CELL_SIZE * scale)))
        elif self.state == 'ghost':
            img_to_draw.set_alpha(128)
        screen.blit(img_to_draw, (self.x * CELL_SIZE, self.y * CELL_SIZE))

    def update(self, dirt_grid, player):
        if self.state in ['normal', 'ghost']:
            self.move(dirt_grid, player)
            if self.inflation > 0: self.inflation -= 0.05
        elif self.state == 'inflating':
            if self.inflation >= 4:
                self.state = 'dying'

    def move(self, dirt_grid, player):
        if self.state == 'inflating': return
        self.move_timer += 1
        if self.move_timer < 20: return
        self.move_timer = 0
        self.ghost_timer -= 1
        if self.ghost_timer <= 0 and self.state == 'normal':
            self.state = 'ghost'
            self.ghost_timer = random.randint(200, 400)
        if self.state == 'ghost' and dirt_grid[self.x][self.y].is_dug:
            self.state = 'normal'
            self.ghost_timer = random.randint(300, 600)
        dx, dy = player.x - self.x, player.y - self.y
        moves = sorted([(1, 0), (-1, 0), (0, 1), (0, -1)], key=lambda m: (m[0]*dx + m[1]*dy), reverse=True)
        for move_x, move_y in moves:
            new_x, new_y = self.x + move_x, self.y + move_y
            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                if self.state == 'ghost' or dirt_grid[new_x][new_y].is_dug:
                    self.x, self.y = new_x, new_y
                    return

class Dirt:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_dug = False
        self.is_rock = False

    def draw(self, screen):
        if not self.is_dug and not self.is_rock:
            screen.blit(DIRT_IMG, (self.x * CELL_SIZE, self.y * CELL_SIZE))

# --- Game State & UI Functions ---
def load_high_score():
    file_path = os.path.join(SCRIPT_DIR, HIGH_SCORE_FILE)
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return int(f.read())
    return 0

def save_high_score(score):
    file_path = os.path.join(SCRIPT_DIR, HIGH_SCORE_FILE)
    with open(file_path, 'w') as f:
        f.write(str(score))

def reset_level(player):
    player.x, player.y = GRID_WIDTH // 2, GRID_HEIGHT // 2
    dirt_grid = [[Dirt(x, y) for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
    dirt_grid[player.x][player.y].is_dug = True
    rocks = []
    for _ in range(NUM_ROCKS):
        while True:
            x, y = random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 5)
            if not dirt_grid[x][y].is_dug and not dirt_grid[x][y].is_rock:
                dirt_grid[x][y].is_rock = True
                rocks.append(Rock(x, y))
                break
    enemies = []
    for _ in range(NUM_ENEMIES):
        while True:
            x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
            if not dirt_grid[x][y].is_dug and not dirt_grid[x][y].is_rock:
                dirt_grid[x][y].is_dug = True
                enemies.append(Enemy(x, y))
                break
    return player, dirt_grid, rocks, enemies

def draw_ui(screen, score, high_score, lives):
    ui_area = pygame.Rect(0, GRID_HEIGHT * CELL_SIZE, SCREEN_WIDTH, 50)
    pygame.draw.rect(screen, BLACK, ui_area)
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, GRID_HEIGHT * CELL_SIZE + 10))
    highscore_text = font.render(f'High Score: {high_score}', True, YELLOW)
    screen.blit(highscore_text, (SCREEN_WIDTH // 2 - highscore_text.get_width() // 2, GRID_HEIGHT * CELL_SIZE + 10))
    lives_text = font.render(f'Lives: {lives}', True, WHITE)
    screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, GRID_HEIGHT * CELL_SIZE + 10))

def draw_game_over(screen):
    font = pygame.font.Font(None, 74)
    text = font.render('GAME OVER', True, RED)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
    font = pygame.font.Font(None, 36)
    text = font.render('Press R to Restart', True, WHITE)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 + 50))

def draw_gameplay(screen, player, dirt_grid, rocks, enemies):
    screen.fill(BLACK)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            dirt_grid[x][y].draw(screen)
    for rock in rocks:
        rock.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    player.draw(screen)

# --- Main Game Loop ---
def main():
    global DIRT_IMG, PLAYER_IMG, POOKA_IMG, ROCK_IMG
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dig Dug")
    clock = pygame.time.Clock()

    DIRT_IMG = pygame.image.load(os.path.join(SCRIPT_DIR, "assets", "dirt.png")).convert()
    PLAYER_IMG = pygame.image.load(os.path.join(SCRIPT_DIR, "assets", "player.png")).convert_alpha()
    POOKA_IMG = pygame.image.load(os.path.join(SCRIPT_DIR, "assets", "pooka.png")).convert_alpha()
    ROCK_IMG = pygame.image.load(os.path.join(SCRIPT_DIR, "assets", "rock.png")).convert_alpha()

    player, dirt_grid, rocks, enemies = reset_level(Player(0,0)) # Initial reset
    player.lives = 3
    score = 0
    high_score = load_high_score()
    game_state = 'playing'

    running = True
    while running:
        if game_state == 'playing':
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.KEYDOWN:
                    moved = False
                    if event.key == pygame.K_LEFT:
                        player.direction = (-1, 0)
                        if player.x > 0 and not dirt_grid[player.x - 1][player.y].is_rock: player.x -= 1; moved = True
                    elif event.key == pygame.K_RIGHT:
                        player.direction = (1, 0)
                        if player.x < GRID_WIDTH -1 and not dirt_grid[player.x + 1][player.y].is_rock: player.x += 1; moved = True
                    elif event.key == pygame.K_UP:
                        player.direction = (0, -1)
                        if player.y > 0 and not dirt_grid[player.x][player.y - 1].is_rock: player.y -= 1; moved = True
                    elif event.key == pygame.K_DOWN:
                        player.direction = (0, 1)
                        if player.y < GRID_HEIGHT -1 and not dirt_grid[player.x][player.y + 1].is_rock: player.y += 1; moved = True
                    if moved:
                        dirt_grid[player.x][player.y].is_dug = True
                        if player.is_pumping:
                            player.attached_enemy.state = 'normal'
                            player.is_pumping = False
                            player.attached_enemy = None
                    if event.key == pygame.K_SPACE:
                        if player.is_pumping:
                            player.attached_enemy.inflation += 1
                        else:
                            check_x, check_y = player.x + player.direction[0], player.y + player.direction[1]
                            for enemy in enemies:
                                if enemy.x == check_x and enemy.y == check_y: 
                                    player.is_pumping = True
                                    player.attached_enemy = enemy
                                    enemy.state = 'inflating'
                                    break
            
            # Update Logic
            for rock in rocks: rock.update(dirt_grid)
            for enemy in enemies: enemy.update(dirt_grid, player)
            
            # Collision & Scoring
            player_rect = pygame.Rect(player.x * CELL_SIZE, player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            for enemy in enemies:
                if enemy.state != 'dying' and player_rect.colliderect(pygame.Rect(enemy.x*CELL_SIZE, enemy.y*CELL_SIZE, CELL_SIZE, CELL_SIZE)):
                    player.lives -= 1
                    if player.lives <= 0: game_state = 'game_over'
                    else: player, dirt_grid, rocks, enemies = reset_level(player)
            for rock in rocks:
                if rock.state == 'falling':
                    rock_rect = pygame.Rect(rock.x*CELL_SIZE, rock.y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    if player_rect.colliderect(rock_rect):
                        player.lives -= 1
                        if player.lives <= 0: game_state = 'game_over'
                        else: player, dirt_grid, rocks, enemies = reset_level(player)
                    for enemy in enemies:
                        if rock_rect.colliderect(pygame.Rect(enemy.x*CELL_SIZE, enemy.y*CELL_SIZE, CELL_SIZE, CELL_SIZE)):
                            enemy.state = 'dying'
                            score += 500 # Crushed enemy score

            # Remove dead enemies and add score
            dead_enemies = [e for e in enemies if e.state == 'dying']
            for dead_enemy in dead_enemies:
                score += (dead_enemy.y + 1) * 100 # Deeper enemies are worth more
            enemies = [e for e in enemies if e.state != 'dying']
            rocks = [r for r in rocks if r.state != 'dead']

            # Drawing
            draw_gameplay(screen, player, dirt_grid, rocks, enemies)
            draw_ui(screen, score, high_score, player.lives)

        elif game_state == 'game_over':
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            draw_game_over(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    player, dirt_grid, rocks, enemies = reset_level(Player(0,0))
                    player.lives = 3
                    score = 0
                    game_state = 'playing'

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()