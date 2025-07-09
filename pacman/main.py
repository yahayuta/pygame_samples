import pygame
import random
import math

# Initialize pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Load sound files
try:
    eat_sound = pygame.mixer.Sound('sound_files/eat.wav')
    power_sound = pygame.mixer.Sound('sound_files/power.wav')
    ghost_eaten_sound = pygame.mixer.Sound('sound_files/ghost_eaten.wav')
    death_sound = pygame.mixer.Sound('sound_files/death.wav')
except:
    # Create simple sounds if files don't exist
    eat_sound = None
    power_sound = None
    ghost_eaten_sound = None
    death_sound = None

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PINK = (255, 105, 180)
CYAN = (0, 255, 255)
DARK_BLUE = (0, 0, 139)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Fonts
font = pygame.font.SysFont('Arial', 24)
title_font = pygame.font.SysFont('Arial', 28, bold=True)
instruction_font = pygame.font.SysFont('Arial', 16)

# Simple Pac-Man maze layout
MAZE_LAYOUT = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W......................................W",
    "W......................................W",
    "W......................................W",
    "W......................................W",
    "W......................................W",
    "W......................................W",
    "W......................................W",
    "W......................................W",
    "W......................................W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

# Power pellets in the four corners
POWER_PELLET_POSITIONS = [
    (1, 1),   # Top left
    (37, 1),  # Top right
    (1, 9),   # Bottom left
    (37, 9)   # Bottom right
]

def find_open_cell():
    # Find a random open cell (not a wall)
    import random
    open_cells = []
    for y, row in enumerate(MAZE_LAYOUT):
        for x, cell in enumerate(row):
            if cell == '.':
                open_cells.append((x, y))
    return random.choice(open_cells)

class PacMan:
    def __init__(self):
        x, y = find_open_cell()
        self.x = x * GRID_SIZE + GRID_SIZE // 2
        self.y = y * GRID_SIZE + GRID_SIZE // 2
        self.direction = [0, 0]
        self.next_direction = [0, 0]
        self.speed = 3
        self.radius = GRID_SIZE // 2
        self.score = 0
        self.lives = 3
        self.power_mode = False
        self.power_timer = 0
        self.power_duration = 600  # 10 seconds at 60 FPS

    def move(self, walls):
        # Try to change direction
        if self.next_direction != [0, 0]:
            new_x = self.x + self.next_direction[0] * self.speed
            new_y = self.y + self.next_direction[1] * self.speed
            grid_x = new_x // GRID_SIZE
            grid_y = new_y // GRID_SIZE
            
            # Check if new direction is valid
            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                if (grid_x, grid_y) not in walls:
                    self.direction = self.next_direction.copy()
                    self.next_direction = [0, 0]

        # Move in current direction
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        grid_x = new_x // GRID_SIZE
        grid_y = new_y // GRID_SIZE
        
        if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
            if (grid_x, grid_y) not in walls:
                self.x = new_x
                self.y = new_y

    def draw(self, screen):
        # Draw Pac-Man as a circle with a mouth
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        
        # Draw mouth (simple triangle)
        if self.direction[0] > 0:  # Right
            points = [(self.x + self.radius, self.y), (self.x + self.radius - 5, self.y - 5), (self.x + self.radius - 5, self.y + 5)]
        elif self.direction[0] < 0:  # Left
            points = [(self.x - self.radius, self.y), (self.x - self.radius + 5, self.y - 5), (self.x - self.radius + 5, self.y + 5)]
        elif self.direction[1] > 0:  # Down
            points = [(self.x, self.y + self.radius), (self.x - 5, self.y + self.radius - 5), (self.x + 5, self.y + self.radius - 5)]
        elif self.direction[1] < 0:  # Up
            points = [(self.x, self.y - self.radius), (self.x - 5, self.y - self.radius + 5), (self.x + 5, self.y - self.radius + 5)]
        else:
            points = []
        
        if points:
            pygame.draw.polygon(screen, BLACK, points)

class Ghost:
    def __init__(self, color, personality):
        x, y = find_open_cell()
        self.x = x * GRID_SIZE + GRID_SIZE // 2
        self.y = y * GRID_SIZE + GRID_SIZE // 2
        self.color = color
        self.personality = personality  # 'chase', 'scatter', 'frightened'
        self.speed = 2
        self.direction = random.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])
        self.target_x = 0
        self.target_y = 0
        self.radius = GRID_SIZE // 2
        self.frightened_timer = 0
        self.frightened_duration = 300  # 5 seconds

    def set_target(self, pacman_x, pacman_y):
        if self.personality == 'chase':
            # Chase Pac-Man
            self.target_x = pacman_x
            self.target_y = pacman_y
        elif self.personality == 'scatter':
            # Move to corners (adjusted for open maze)
            if self.color == RED:
                self.target_x = WIDTH - GRID_SIZE * 2
                self.target_y = GRID_SIZE * 2
            elif self.color == PINK:
                self.target_x = GRID_SIZE * 2
                self.target_y = GRID_SIZE * 2
            elif self.color == CYAN:
                self.target_x = WIDTH - GRID_SIZE * 2
                self.target_y = HEIGHT - GRID_SIZE * 2
            elif self.color == ORANGE:
                self.target_x = GRID_SIZE * 2
                self.target_y = HEIGHT - GRID_SIZE * 2
        elif self.personality == 'frightened':
            # Run away from Pac-Man
            dx = self.x - pacman_x
            dy = self.y - pacman_y
            self.target_x = self.x + dx * 2
            self.target_y = self.y + dy * 2

    def move(self, walls, pacman_x, pacman_y):
        # Update personality based on timer
        if self.frightened_timer > 0:
            self.frightened_timer -= 1
            if self.frightened_timer == 0:
                self.personality = 'chase'

        # Set target based on personality
        self.set_target(pacman_x, pacman_y)

        # Calculate direction to target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        
        # Get possible directions
        possible_directions = []
        for direction in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            new_x = self.x + direction[0] * self.speed
            new_y = self.y + direction[1] * self.speed
            grid_x = new_x // GRID_SIZE
            grid_y = new_y // GRID_SIZE
            
            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                if (grid_x, grid_y) not in walls:
                    possible_directions.append(direction)

        if possible_directions:
            # Choose best direction
            best_direction = possible_directions[0]
            best_distance = float('inf')
            
            for direction in possible_directions:
                new_x = self.x + direction[0] * self.speed
                new_y = self.y + direction[1] * self.speed
                distance = math.sqrt((new_x - self.target_x)**2 + (new_y - self.target_y)**2)
                
                if distance < best_distance:
                    best_distance = distance
                    best_direction = direction
            
            self.direction = best_direction

        # Move
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        grid_x = new_x // GRID_SIZE
        grid_y = new_y // GRID_SIZE
        
        if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
            if (grid_x, grid_y) not in walls:
                self.x = new_x
                self.y = new_y

    def draw(self, screen):
        if self.personality == 'frightened':
            color = DARK_BLUE
        else:
            color = self.color
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

class Dot:
    def __init__(self, x, y, is_power=False):
        self.x = x
        self.y = y
        self.is_power = is_power
        self.radius = 3 if not is_power else 8

    def draw(self, screen):
        color = WHITE if not self.is_power else YELLOW
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

def create_maze():
    walls = set()
    dots = []
    power_pellets = []
    
    for y, row in enumerate(MAZE_LAYOUT):
        for x, cell in enumerate(row):
            if cell == 'W':
                walls.add((x, y))
            elif cell == '.':
                dots.append(Dot(x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2))
    
    # Add power pellets at specific positions with better error handling
    for x, y in POWER_PELLET_POSITIONS:
        try:
            if 0 <= x < len(MAZE_LAYOUT[0]) and 0 <= y < len(MAZE_LAYOUT):
                if MAZE_LAYOUT[y][x] == '.':
                    power_pellets.append(Dot(x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2, True))
        except IndexError:
            # Skip invalid positions
            continue
    
    return walls, dots, power_pellets

def draw_instructions():
    # Title
    title_text = title_font.render("PAC-MAN", True, YELLOW)
    screen.blit(title_text, (10, 10))
    
    # Instructions
    instructions = [
        "OBJECTIVE: Eat all dots while avoiding ghosts",
        "CONTROLS: Arrow Keys to move",
        "POWER PELLETS: Make ghosts vulnerable",
        "SCORING: Dots = 10, Power Pellets = 50",
        "GHOSTS: 200 points each when vulnerable",
        "STRATEGY: Use open maze to outmaneuver ghosts"
    ]
    
    for i, instruction in enumerate(instructions):
        text = instruction_font.render(instruction, True, WHITE)
        screen.blit(text, (10, 50 + i * 20))

def main():
    clock = pygame.time.Clock()
    
    # Create maze
    walls, dots, power_pellets = create_maze()
    
    # Create game objects
    pacman = PacMan()
    ghosts = [
        Ghost(RED, 'chase'),
        Ghost(PINK, 'scatter'),
        Ghost(CYAN, 'chase'),
        Ghost(ORANGE, 'scatter')
    ]
    
    # Add personality switching timer for more dynamic gameplay
    personality_timer = 0
    personality_switch_interval = 1800  # 30 seconds at 60 FPS
    
    running = True
    game_over = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.next_direction = [-1, 0]
                elif event.key == pygame.K_RIGHT:
                    pacman.next_direction = [1, 0]
                elif event.key == pygame.K_UP:
                    pacman.next_direction = [0, -1]
                elif event.key == pygame.K_DOWN:
                    pacman.next_direction = [0, 1]

        if not game_over:
            # Move Pac-Man
            pacman.move(walls)
            
            # Update power mode
            if pacman.power_mode:
                pacman.power_timer -= 1
                if pacman.power_timer <= 0:
                    pacman.power_mode = False
                    for ghost in ghosts:
                        if ghost.personality == 'frightened':
                            ghost.personality = 'chase'
            
            # Update ghost personalities periodically
            personality_timer += 1
            if personality_timer >= personality_switch_interval:
                personality_timer = 0
                for ghost in ghosts:
                    if ghost.personality != 'frightened':
                        ghost.personality = 'scatter' if ghost.personality == 'chase' else 'chase'
            
            # Move ghosts
            for ghost in ghosts:
                ghost.move(walls, pacman.x, pacman.y)
            
            # Check dot collection
            for dot in dots[:]:
                if math.hypot(pacman.x - dot.x, pacman.y - dot.y) < GRID_SIZE // 2:
                    dots.remove(dot)
                    pacman.score += 10
                    if eat_sound:
                        eat_sound.play()
            
            # Check power pellet collection
            for pellet in power_pellets[:]:
                if math.hypot(pacman.x - pellet.x, pacman.y - pellet.y) < GRID_SIZE // 2:
                    power_pellets.remove(pellet)
                    pacman.score += 50
                    pacman.power_mode = True
                    pacman.power_timer = pacman.power_duration
                    if power_sound:
                        power_sound.play()
                    
                    # Make all ghosts frightened
                    for ghost in ghosts:
                        ghost.personality = 'frightened'
                        ghost.frightened_timer = pacman.power_duration
            
            # Check ghost collisions
            for ghost in ghosts:
                if math.hypot(pacman.x - ghost.x, pacman.y - ghost.y) < GRID_SIZE:
                    if ghost.personality == 'frightened':
                        # Eat ghost
                        pacman.score += 200
                        if ghost_eaten_sound:
                            ghost_eaten_sound.play()
                        # Reset ghost position
                        ghost_cell_x, ghost_cell_y = find_open_cell()
                        ghost.x = ghost_cell_x * GRID_SIZE + GRID_SIZE // 2
                        ghost.y = ghost_cell_y * GRID_SIZE + GRID_SIZE // 2
                        ghost.personality = 'chase'
                    else:
                        # Pac-Man dies
                        pacman.lives -= 1
                        if death_sound:
                            death_sound.play()
                        if pacman.lives <= 0:
                            game_over = True
                        else:
                            # Reset positions
                            pac_cell_x, pac_cell_y = find_open_cell()
                            pacman.x = pac_cell_x * GRID_SIZE + GRID_SIZE // 2
                            pacman.y = pac_cell_y * GRID_SIZE + GRID_SIZE // 2
                            for ghost in ghosts:
                                ghost_cell_x, ghost_cell_y = find_open_cell()
                                ghost.x = ghost_cell_x * GRID_SIZE + GRID_SIZE // 2
                                ghost.y = ghost_cell_y * GRID_SIZE + GRID_SIZE // 2

        # Draw everything
        screen.fill(BLACK)
        
        # Draw walls
        for wall in walls:
            pygame.draw.rect(screen, BLUE, (wall[0] * GRID_SIZE, wall[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Draw dots
        for dot in dots:
            dot.draw(screen)
        
        # Draw power pellets
        for pellet in power_pellets:
            pellet.draw(screen)
        
        # Draw Pac-Man
        pacman.draw(screen)
        
        # Draw ghosts
        for ghost in ghosts:
            ghost.draw(screen)
        
        # Draw score and lives
        score_text = font.render(f"Score: {pacman.score}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT - 60))
        
        lives_text = font.render(f"Lives: {pacman.lives}", True, WHITE)
        screen.blit(lives_text, (10, HEIGHT - 30))
        
        # Draw instructions
        draw_instructions()
        
        # Game over screen
        if game_over:
            game_over_text = title_font.render("GAME OVER!", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
