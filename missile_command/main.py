import pygame
import sys
import random
import math
import json
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load sound effects
try:
    launch_sound = pygame.mixer.Sound('launch.wav')
    explosion_sound = pygame.mixer.Sound('explosion.wav')
    city_destroyed_sound = pygame.mixer.Sound('city_destroyed.wav')
    game_over_sound = pygame.mixer.Sound('game_over.wav')
except:
    print("Warning: Could not load sound files. Game will run without sound.")
    launch_sound = explosion_sound = city_destroyed_sound = game_over_sound = None

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Missile Command')

# City settings
CITY_WIDTH = 50
CITY_HEIGHT = 30
CITY_COLOR = (0, 200, 255)
NUM_CITIES = 6
CITY_SPACING = (WIDTH - NUM_CITIES * CITY_WIDTH) // (NUM_CITIES + 1)
CITY_DESTROYED_COLOR = (80, 80, 80)
city_status = [True] * NUM_CITIES  # True = alive, False = destroyed

# Calculate city positions
cities = []
for i in range(NUM_CITIES):
    x = CITY_SPACING + i * (CITY_WIDTH + CITY_SPACING)
    y = HEIGHT - CITY_HEIGHT - 10
    cities.append(pygame.Rect(x, y, CITY_WIDTH, CITY_HEIGHT))

# Enemy missile settings
MISSILE_COLOR = (255, 0, 0)
MISSILE_WIDTH = 2
MISSILE_SPEED = 0.05  # Was 0.1 - extremely slow missiles
MISSILE_SPAWN_INTERVAL = 180  # Was 120 - much slower spawn rate

def spawn_enemy_missile():
    start_x = random.randint(0, WIDTH)
    start_y = 0
    # Target a random city
    target_city = random.choice(cities)
    target_x = target_city.centerx
    target_y = target_city.bottom
    # Calculate direction
    dx = target_x - start_x
    dy = target_y - start_y
    distance = math.hypot(dx, dy)
    vx = dx / distance * MISSILE_SPEED
    vy = dy / distance * MISSILE_SPEED
    return {
        'start': (start_x, start_y),
        'pos': [start_x, start_y],
        'target': (target_x, target_y),
        'vel': (vx, vy)
    }

# List to store enemy missiles
enemy_missiles = []
missile_spawn_timer = 0

# Player missile settings
PLAYER_MISSILE_COLOR = (255, 255, 0)
PLAYER_MISSILE_WIDTH = 2
PLAYER_MISSILE_SPEED = 10  # Was 7 - faster player missiles
PLAYER_MISSILE_ORIGIN = (WIDTH // 2, HEIGHT - 10)

# List to store player missiles
player_missiles = []

# Crosshair settings
def draw_crosshair(surface, pos):
    x, y = pos
    pygame.draw.line(surface, (0,255,0), (x-10, y), (x+10, y), 1)
    pygame.draw.line(surface, (0,255,0), (x, y-10), (x, y+10), 1)

# Function to spawn player missile
def spawn_player_missile(target_x, target_y):
    start_x, start_y = PLAYER_MISSILE_ORIGIN
    dx = target_x - start_x
    dy = target_y - start_y
    distance = math.hypot(dx, dy)
    if distance == 0:
        return None
    vx = dx / distance * PLAYER_MISSILE_SPEED
    vy = dy / distance * PLAYER_MISSILE_SPEED
    return {
        'start': (start_x, start_y),
        'pos': [start_x, start_y],
        'target': (target_x, target_y),
        'vel': (vx, vy)
    }

# Explosion settings
EXPLOSION_COLOR = (255, 255, 255)
EXPLOSION_MAX_RADIUS = 80  # Was 60 - much bigger explosions
EXPLOSION_GROWTH = 3
EXPLOSION_DURATION = 60  # Was 40 - longer lasting explosions

explosions = []  # Each: {'pos': (x, y), 'radius': r, 'timer': t, 'maxed': bool}

# High score system
HIGH_SCORE_FILE = 'missile_command_high_score.json'

def load_high_score():
    """Load high score from file"""
    try:
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
    except:
        pass
    return 0

def save_high_score(score):
    """Save high score to file"""
    try:
        with open(HIGH_SCORE_FILE, 'w') as f:
            json.dump({'high_score': score}, f)
    except:
        pass

# Load high score at start
high_score = load_high_score()

# Level system
current_level = 1
level_timer = 0
LEVEL_ADVANCE_TIME = 3000  # frames (about 50 seconds at 60 FPS)
level_survival_time = 0

def get_level_difficulty(level):
    """Get difficulty settings for current level"""
    base_spawn_interval = 120
    base_missile_speed = 1
    base_explosion_radius = 60
    base_explosion_duration = 40
    
    # Increase difficulty every 3 levels
    difficulty_multiplier = 1 + (level - 1) // 3
    
    return {
        'spawn_interval': max(60, base_spawn_interval - (level - 1) * 5),  # Was 10 - slower difficulty increase
        'missile_speed': base_missile_speed + (level - 1) * 0.1,  # Was 0.2 - slower speed increase
        'explosion_radius': max(50, base_explosion_radius - (level - 1) * 1),  # Was 2 - slower radius decrease
        'explosion_duration': max(30, base_explosion_duration - (level - 1) * 1)  # Was 2 - slower duration decrease
    }

def advance_level():
    """Advance to next level"""
    global current_level, level_survival_time
    current_level += 1
    level_survival_time = 0
    print(f"Level {current_level} reached!")

# Missile bases system
MISSILE_BASES = [
    {'pos': (WIDTH // 4, HEIGHT - 20), 'ammo': 999, 'color': (255, 100, 100)},      # Unlimited ammo
    {'pos': (WIDTH // 2, HEIGHT - 20), 'ammo': 999, 'color': (100, 255, 100)},      # Unlimited ammo
    {'pos': (3 * WIDTH // 4, HEIGHT - 20), 'ammo': 999, 'color': (100, 100, 255)}   # Unlimited ammo
]
selected_base = 1  # 0=left, 1=center, 2=right

def draw_missile_bases(surface):
    """Draw missile bases and their ammo"""
    for i, base in enumerate(MISSILE_BASES):
        # Draw base
        color = base['color']
        if i == selected_base:
            color = (255, 255, 255)  # Highlight selected base
        pygame.draw.rect(surface, color, (base['pos'][0] - 15, base['pos'][1] - 10, 30, 20))
        
        # Draw ammo count
        ammo_text = font.render(str(base['ammo']), True, (255, 255, 255))
        ammo_rect = ammo_text.get_rect(center=(base['pos'][0], base['pos'][1] + 25))
        surface.blit(ammo_text, ammo_rect)

def fire_from_base(base_index, target_x, target_y):
    """Fire a missile from the specified base"""
    if MISSILE_BASES[base_index]['ammo'] > 0:  # Always true with 999 ammo
        base_pos = MISSILE_BASES[base_index]['pos']
        dx = target_x - base_pos[0]
        dy = target_y - base_pos[1]
        distance = math.hypot(dx, dy)
        if distance == 0:
            return None
        vx = dx / distance * PLAYER_MISSILE_SPEED
        vy = dy / distance * PLAYER_MISSILE_SPEED
        
        # Don't reduce ammo - unlimited firing
        return {
            'start': base_pos,
            'pos': [base_pos[0], base_pos[1]],
            'target': (target_x, target_y),
            'vel': (vx, vy)
        }
    return None

# Background stars
STARS = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(50)]

def draw_stars(surface):
    """Draw background stars"""
    for star in STARS:
        pygame.draw.circle(surface, (255, 255, 255), star, 1)

def draw_city(surface, city_rect, is_destroyed):
    """Draw a detailed city sprite"""
    x, y, w, h = city_rect
    if is_destroyed:
        # Draw destroyed city (rubble)
        pygame.draw.rect(surface, (80, 80, 80), city_rect)
        # Add some rubble details
        for i in range(3):
            rubble_x = x + random.randint(0, w)
            rubble_y = y + random.randint(0, h)
            pygame.draw.circle(surface, (60, 60, 60), (rubble_x, rubble_y), 2)
    else:
        # Draw city buildings
        building_width = w // 3
        building_height = h
        
        # Main building
        pygame.draw.rect(surface, (0, 200, 255), (x + w//2 - building_width//2, y, building_width, building_height))
        
        # Side buildings
        pygame.draw.rect(surface, (0, 180, 235), (x, y + h//4, building_width, building_height * 3//4))
        pygame.draw.rect(surface, (0, 180, 235), (x + w - building_width, y + h//4, building_width, building_height * 3//4))
        
        # Windows
        for i in range(2):
            for j in range(3):
                window_x = x + w//2 - building_width//2 + (i * building_width//2)
                window_y = y + h//4 + (j * h//4)
                pygame.draw.rect(surface, (255, 255, 200), (window_x + 2, window_y + 2, 4, 4))

def draw_animated_explosion(surface, explosion):
    """Draw an animated explosion with multiple circles"""
    x, y = explosion['pos']
    radius = explosion['radius']
    
    # Main explosion circle
    pygame.draw.circle(surface, EXPLOSION_COLOR, (int(x), int(y)), int(radius), 2)
    
    # Inner bright circle
    inner_radius = max(1, radius // 3)
    pygame.draw.circle(surface, (255, 255, 200), (int(x), int(y)), int(inner_radius))
    
    # Outer shockwave
    outer_radius = radius + 5
    pygame.draw.circle(surface, (255, 100, 100), (int(x), int(y)), int(outer_radius), 1)

def draw_enhanced_missile_base(surface, base, is_selected):
    """Draw an enhanced missile base with more detail"""
    x, y = base['pos']
    
    # Base platform
    pygame.draw.rect(surface, (100, 100, 100), (x - 20, y - 5, 40, 10))
    
    # Missile launcher
    launcher_color = (255, 255, 255) if is_selected else base['color']
    pygame.draw.rect(surface, launcher_color, (x - 8, y - 15, 16, 20))
    
    # Launcher details
    pygame.draw.rect(surface, (80, 80, 80), (x - 6, y - 13, 12, 16))
    
    # Ammo indicator
    ammo_percent = base['ammo'] / 10.0
    ammo_width = int(16 * ammo_percent)
    if ammo_percent > 0.5:
        ammo_color = (0, 255, 0)
    elif ammo_percent > 0.2:
        ammo_color = (255, 255, 0)
    else:
        ammo_color = (255, 0, 0)
    
    pygame.draw.rect(surface, ammo_color, (x - 6, y - 11, ammo_width, 4))
    
    # Ammo count
    ammo_text = font.render(str(base['ammo']), True, (255, 255, 255))
    ammo_rect = ammo_text.get_rect(center=(x, y + 25))
    surface.blit(ammo_text, ammo_rect)

# Game states
MENU = 'menu'
INSTRUCTIONS = 'instructions'
PLAYING = 'playing'
GAME_OVER = 'game_over'

game_state = MENU
menu_selection = 0
menu_options = ['Start Game', 'Instructions', 'Quit']

def draw_menu(surface):
    """Draw the main menu"""
    # Title
    title_font = pygame.font.SysFont(None, 72)
    title_text = title_font.render('MISSILE COMMAND', True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//3))
    surface.blit(title_text, title_rect)
    
    # Menu options
    for i, option in enumerate(menu_options):
        color = (255, 255, 0) if i == menu_selection else (255, 255, 255)
        option_text = font.render(option, True, color)
        option_rect = option_text.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 50))
        surface.blit(option_text, option_rect)
    
    # Instructions
    instr_font = pygame.font.SysFont(None, 24)
    instr_text = instr_font.render('Use Arrow Keys to navigate, Enter to select', True, (150, 150, 150))
    instr_rect = instr_text.get_rect(center=(WIDTH//2, HEIGHT - 50))
    surface.blit(instr_text, instr_rect)

def draw_instructions(surface):
    """Draw the instructions screen"""
    # Title
    title_font = pygame.font.SysFont(None, 48)
    title_text = title_font.render('HOW TO PLAY', True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH//2, 50))
    surface.blit(title_text, title_rect)
    
    # Instructions
    instructions = [
        'OBJECTIVE: Defend your cities from incoming missiles!',
        '',
        'CONTROLS:',
        '• Mouse: Move crosshair and left-click to fire',
        '• Arrow Keys: Move crosshair',
        '• Spacebar: Fire missile',
        '• 1, 2, 3: Select missile base',
        '',
        'GAMEPLAY:',
        '• Each missile base has limited ammo',
        '• Explosions destroy enemy missiles',
        '• Survive to advance to next level',
        '• All cities destroyed = Game Over',
        '',
        'Press ENTER to start game or ESC to return to menu'
    ]
    
    for i, line in enumerate(instructions):
        if line.startswith('•'):
            color = (255, 255, 0)
        elif line in ['CONTROLS:', 'GAMEPLAY:', 'OBJECTIVE:']:
            color = (0, 255, 255)
        else:
            color = (255, 255, 255)
        
        text = font.render(line, True, color)
        rect = text.get_rect(center=(WIDTH//2, 120 + i * 30))
        surface.blit(text, rect)

def reset_game():
    """Reset all game variables for a new game"""
    global score, current_level, level_survival_time, city_status, enemy_missiles, player_missiles, explosions, crosshair_x, crosshair_y, selected_base
    
    score = 0
    current_level = 1
    level_survival_time = 0
    city_status[:] = [True] * NUM_CITIES
    enemy_missiles.clear()
    player_missiles.clear()
    explosions.clear()
    crosshair_x = WIDTH // 2
    crosshair_y = HEIGHT // 2
    selected_base = 1
    
    # Reset missile bases
    for base in MISSILE_BASES:
        base['ammo'] = 999  # Unlimited ammo

def handle_menu_input(event):
    """Handle input in menu state"""
    global game_state, menu_selection
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            menu_selection = (menu_selection - 1) % len(menu_options)
        elif event.key == pygame.K_DOWN:
            menu_selection = (menu_selection + 1) % len(menu_options)
        elif event.key == pygame.K_RETURN:
            if menu_selection == 0:  # Start Game
                game_state = PLAYING
                reset_game()
            elif menu_selection == 1:  # Instructions
                game_state = INSTRUCTIONS
            elif menu_selection == 2:  # Quit
                return False
    return True

def handle_instructions_input(event):
    """Handle input in instructions state"""
    global game_state
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            game_state = PLAYING
            reset_game()
        elif event.key == pygame.K_ESCAPE:
            game_state = MENU
    return True

# Main loop
running = True
score = 0
font = pygame.font.SysFont(None, 36)
# Crosshair position (for keyboard controls)
crosshair_x = WIDTH // 2
crosshair_y = HEIGHT // 2
CROSSHAIR_SPEED = 5

def update_crosshair_position():
    """Update crosshair position based on keyboard input"""
    global crosshair_x, crosshair_y
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and crosshair_x > 0:
        crosshair_x -= CROSSHAIR_SPEED
    if keys[pygame.K_RIGHT] and crosshair_x < WIDTH:
        crosshair_x += CROSSHAIR_SPEED
    if keys[pygame.K_UP] and crosshair_y > 0:
        crosshair_y -= CROSSHAIR_SPEED
    if keys[pygame.K_DOWN] and crosshair_y < HEIGHT:
        crosshair_y += CROSSHAIR_SPEED

# Power-up system
POWERUP_TYPES = ['big_explosion', 'slow_motion', 'extra_city']
POWERUP_COLORS = {
    'big_explosion': (255, 255, 0),    # Yellow
    'slow_motion': (0, 255, 255),      # Cyan
    'extra_city': (0, 255, 0)          # Green
}

powerups = []  # List of active power-ups
active_effects = {
    'big_explosion': 0,
    'slow_motion': 0,
    'extra_city': 0
}
POWERUP_DURATION = 600  # Was 300 - 10 seconds instead of 5
POWERUP_DROP_CHANCE = 0.6  # Was 0.3 - 60% chance instead of 30%

def create_powerup(x, y):
    """Create a power-up at the specified position"""
    powerup_type = random.choice(POWERUP_TYPES)
    return {
        'type': powerup_type,
        'pos': [x, y],
        'vel': [0, 2],  # Falls down
        'color': POWERUP_COLORS[powerup_type],
        'radius': 8
    }

def draw_powerup(surface, powerup):
    """Draw a power-up"""
    x, y = powerup['pos']
    color = powerup['color']
    
    # Draw power-up as a pulsing circle
    pulse = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 3
    radius = powerup['radius'] + pulse
    pygame.draw.circle(surface, color, (int(x), int(y)), int(radius))
    pygame.draw.circle(surface, (255, 255, 255), (int(x), int(y)), int(radius), 2)

def apply_powerup(powerup_type):
    """Apply a power-up effect"""
    active_effects[powerup_type] = POWERUP_DURATION
    print(f"Power-up activated: {powerup_type}")

def update_powerup_effects():
    """Update active power-up effects"""
    for effect in active_effects:
        if active_effects[effect] > 0:
            active_effects[effect] -= 1

def get_explosion_radius():
    """Get explosion radius considering power-ups"""
    base_radius = difficulty['explosion_radius']
    if active_effects['big_explosion'] > 0:
        return base_radius * 1.5
    return base_radius

def get_missile_speed():
    """Get missile speed considering slow motion"""
    base_speed = difficulty['missile_speed']
    if active_effects['slow_motion'] > 0:
        return base_speed * 0.5
    return base_speed

def draw_powerup_indicators(surface):
    """Draw active power-up indicators"""
    y_offset = 130
    for effect, duration in active_effects.items():
        if duration > 0:
            # Effect name
            effect_text = font.render(f'{effect.replace("_", " ").title()}: {duration//60}s', True, POWERUP_COLORS[effect])
            surface.blit(effect_text, (10, y_offset))
            y_offset += 25

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_state == MENU:
            running = handle_menu_input(event)
        elif game_state == INSTRUCTIONS:
            running = handle_instructions_input(event)
        elif game_state == PLAYING:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                missile = fire_from_base(selected_base, mx, my)
                if missile:
                    player_missiles.append(missile)
                    if launch_sound:
                        launch_sound.play()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_base = 0
                elif event.key == pygame.K_2:
                    selected_base = 1
                elif event.key == pygame.K_3:
                    selected_base = 2
                elif event.key == pygame.K_SPACE:
                    # Fire with spacebar
                    missile = fire_from_base(selected_base, crosshair_x, crosshair_y)
                    if missile:
                        player_missiles.append(missile)
                        if launch_sound:
                            launch_sound.play()

    screen.fill((0, 0, 0))  # Black background
    
    if game_state == MENU:
        draw_stars(screen)
        draw_menu(screen)
    elif game_state == INSTRUCTIONS:
        draw_stars(screen)
        draw_instructions(screen)
    elif game_state == PLAYING:
        # Draw background stars
        draw_stars(screen)
        
        # Spawn enemy missiles
        missile_spawn_timer += 1
        difficulty = get_level_difficulty(current_level)
        if missile_spawn_timer >= difficulty['spawn_interval']:
            enemy_missiles.append(spawn_enemy_missile())
            missile_spawn_timer = 0

        # Move and draw player missiles
        missiles_to_remove = []
        for missile in player_missiles:
            missile['pos'][0] += missile['vel'][0]
            missile['pos'][1] += missile['vel'][1]
            pygame.draw.line(screen, PLAYER_MISSILE_COLOR, missile['start'], missile['pos'], PLAYER_MISSILE_WIDTH)
            # Check if reached target
            dx = missile['pos'][0] - missile['target'][0]
            dy = missile['pos'][1] - missile['target'][1]
            if dx*dx + dy*dy < PLAYER_MISSILE_SPEED*PLAYER_MISSILE_SPEED:
                explosions.append({'pos': (missile['target'][0], missile['target'][1]), 'radius': 1, 'timer': 0, 'maxed': False})
                missiles_to_remove.append(missile)
        for m in missiles_to_remove:
            player_missiles.remove(m)

        # Update and draw explosions
        explosions_to_remove = []
        for exp in explosions:
            if not exp['maxed']:
                exp['radius'] += EXPLOSION_GROWTH
                if exp['radius'] >= get_explosion_radius():
                    exp['radius'] = get_explosion_radius()
                    exp['maxed'] = True
            else:
                exp['timer'] += 1
                if exp['timer'] >= difficulty['explosion_duration']:
                    explosions_to_remove.append(exp)
            draw_animated_explosion(screen, exp)
        for e in explosions_to_remove:
            explosions.remove(e)

        # Move and draw enemy missiles
        enemy_to_remove = []
        for missile in enemy_missiles:
            missile['pos'][0] += missile['vel'][0] * get_missile_speed()
            missile['pos'][1] += missile['vel'][1] * get_missile_speed()
            # Collision with explosions
            for exp in explosions:
                dx = missile['pos'][0] - exp['pos'][0]
                dy = missile['pos'][1] - exp['pos'][1]
                if dx*dx + dy*dy < exp['radius']*exp['radius']:
                    enemy_to_remove.append(missile)
                    score += 100
                    if explosion_sound:
                        explosion_sound.play()
                    
                    # Chance to drop power-up
                    if random.random() < POWERUP_DROP_CHANCE:
                        powerups.append(create_powerup(missile['pos'][0], missile['pos'][1]))
                    break
            else:
                # Collision with cities
                for idx, city in enumerate(cities):
                    if city_status[idx] and city.collidepoint(missile['pos'][0], missile['pos'][1]):
                        city_status[idx] = False
                        enemy_to_remove.append(missile)
                        if city_destroyed_sound:
                            city_destroyed_sound.play()
                        break
                else:
                    pygame.draw.line(screen, MISSILE_COLOR, missile['start'], missile['pos'], MISSILE_WIDTH)
        for m in enemy_to_remove:
            if m in enemy_missiles:
                enemy_missiles.remove(m)

        # Draw cities (after updating status)
        for idx, city in enumerate(cities):
            draw_city(screen, city, not city_status[idx])

        # Draw score
        score_text = font.render(f'Score: {score}', True, (255,255,255))
        screen.blit(score_text, (10, 10))
        
        # Draw high score
        high_score_text = font.render(f'High Score: {high_score}', True, (255,255,0))
        screen.blit(high_score_text, (10, 50))

        # Draw level info
        level_text = font.render(f'Level: {current_level}', True, (0,255,255))
        screen.blit(level_text, (WIDTH - 150, 10))
        
        # Check for level advancement
        if all(city_status):  # All cities still alive
            level_survival_time += 1
            if level_survival_time >= LEVEL_ADVANCE_TIME:
                advance_level()
        else:
            level_survival_time = 0

        # Check for game over
        if not any(city_status):
            if game_over_sound:
                game_over_sound.play()
            
            # Check if new high score
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            
            game_state = GAME_OVER

        # Update crosshair position for keyboard controls
        update_crosshair_position()
        
        # Get mouse position for crosshair (keyboard takes priority if both are used)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        
        # Use keyboard position if arrow keys are pressed, otherwise use mouse
        if any([keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN]]):
            crosshair_pos = (crosshair_x, crosshair_y)
        else:
            crosshair_pos = (mouse_x, mouse_y)
            crosshair_x, crosshair_y = mouse_x, mouse_y

        # Draw crosshair at current position
        draw_crosshair(screen, crosshair_pos)
        
        # Draw control instructions
        controls_text = font.render('Mouse: Aim & Click | Arrow Keys: Move | Space: Fire | 1,2,3: Select Base', True, (150, 150, 150))
        screen.blit(controls_text, (10, HEIGHT - 30))

        # Draw missile bases
        for i, base in enumerate(MISSILE_BASES):
            draw_enhanced_missile_base(screen, base, i == selected_base)
        
        # Draw base selection info
        base_names = ['Left (1)', 'Center (2)', 'Right (3)']
        selection_text = font.render(f'Selected: {base_names[selected_base]}', True, (255, 255, 255))
        screen.blit(selection_text, (10, 90))

        # Update and draw power-ups
        powerups_to_remove = []
        for powerup in powerups:
            # Move power-up
            powerup['pos'][0] += powerup['vel'][0]
            powerup['pos'][1] += powerup['vel'][1]
            
            # Remove if off screen
            if powerup['pos'][1] > HEIGHT:
                powerups_to_remove.append(powerup)
            else:
                draw_powerup(screen, powerup)
        
        for p in powerups_to_remove:
            powerups.remove(p)
        
        # Check power-up collection
        powerups_to_remove = []
        for powerup in powerups:
            # Check collision with crosshair
            dx = powerup['pos'][0] - crosshair_pos[0]
            dy = powerup['pos'][1] - crosshair_pos[1]
            if dx*dx + dy*dy < (powerup['radius'] + 10)**2:
                apply_powerup(powerup['type'])
                powerups_to_remove.append(powerup)
        
        for p in powerups_to_remove:
            powerups.remove(p)
        
        # Update power-up effects
        update_powerup_effects()

        # Draw power-up indicators
        draw_powerup_indicators(screen)
    
    elif game_state == GAME_OVER:
        # Draw game over screen
        draw_stars(screen)
        
        big_font = pygame.font.SysFont(None, 72)
        text = big_font.render('GAME OVER', True, (255, 0, 0))
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
        screen.blit(text, rect)
        score_text = font.render(f'Final Score: {score}', True, (255,255,255))
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
        screen.blit(score_text, score_rect)
        level_text = font.render(f'Level Reached: {current_level}', True, (0,255,255))
        level_rect = level_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        screen.blit(level_text, level_rect)
        high_score_text = font.render(f'High Score: {high_score}', True, (255,255,0))
        high_score_rect = high_score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 80))
        screen.blit(high_score_text, high_score_rect)
        instr_text = font.render('Press R to Restart or Q to Quit', True, (255,255,0))
        instr_rect = instr_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 120))
        screen.blit(instr_text, instr_rect)
        
        # Handle game over input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_state = PLAYING
                    reset_game()
                elif event.key == pygame.K_q:
                    running = False

    pygame.display.flip()

pygame.quit()
sys.exit() 