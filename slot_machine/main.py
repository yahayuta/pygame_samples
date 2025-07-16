import pygame
import random
import math
import time
import json
import os

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Load sound files
try:
    start_sound = pygame.mixer.Sound('sound_files/start.mp3')
    win_sound = pygame.mixer.Sound('sound_files/win.wav')
    # Add new sound effects
    coin_sound = pygame.mixer.Sound('sound_files/coin_drop.wav') if pygame.mixer.get_init() else None
    button_sound = pygame.mixer.Sound('sound_files/button_click.wav') if pygame.mixer.get_init() else None
    big_win_sound = pygame.mixer.Sound('sound_files/big_win.wav') if pygame.mixer.get_init() else None
    jackpot_sound = pygame.mixer.Sound('sound_files/jackpot.wav') if pygame.mixer.get_init() else None
    bonus_sound = pygame.mixer.Sound('sound_files/bonus.wav') if pygame.mixer.get_init() else None
except:
    # Create dummy sounds if files don't exist
    start_sound = None
    win_sound = None
    coin_sound = None
    button_sound = None
    big_win_sound = None
    jackpot_sound = None
    bonus_sound = None

# Load background images
# (delete or comment out these lines)
# background = pygame.image.load("image_files/background.jpg")

# Set up the window
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slot Machine")

# UI layout constants
TOP_BAR_HEIGHT = 70
BOTTOM_BAR_HEIGHT = 60
PADDING = 24

# --- Add paytable constants ---
PAYTABLE_WIDTH = 260
PAYTABLE_PADDING = 18

# Load images
reel_images = [
    pygame.image.load("image_files/seven.jpg"),
    pygame.image.load("image_files/cherry.jpg"),
    pygame.image.load("image_files/plum.jpg"),
    pygame.image.load("image_files/wm.jpg"),
    pygame.image.load("image_files/bell.jpg"),
]
# Remove background and spin button images
# (delete or comment out these lines)
# spin_button = pygame.image.load("image_files/spin.png")
# spin_button_rect = spin_button.get_rect()

# Reel layout
num_reels = 3
REEL_WIDTH = reel_images[0].get_width()
REEL_HEIGHT = reel_images[0].get_height()
REEL_SPACING = 30

game_area_height = HEIGHT - TOP_BAR_HEIGHT - BOTTOM_BAR_HEIGHT
reels_total_width = num_reels * REEL_WIDTH + (num_reels - 1) * REEL_SPACING
REEL_X_START = (WIDTH - reels_total_width) // 2
REEL_Y = TOP_BAR_HEIGHT + (game_area_height - REEL_HEIGHT) // 2

# Instead, define a rect for the spin button (after REEL_Y and REEL_HEIGHT are defined)
SPIN_BTN_WIDTH = 180
SPIN_BTN_HEIGHT = 60
SPIN_BTN_COLOR = (60, 180, 60)
SPIN_BTN_HOVER = (80, 220, 80)
SPIN_BTN_TEXT_COLOR = (255, 255, 255)
spin_btn_rect = pygame.Rect(0, 0, SPIN_BTN_WIDTH, SPIN_BTN_HEIGHT)
spin_btn_rect.centerx = WIDTH // 2
spin_btn_rect.top = REEL_Y + REEL_HEIGHT + 30

# Game state variables
credits = 1000
current_bet = 1
max_bet = 100
auto_play = False
auto_play_count = 0
show_paytable = False
game_mode = "classic"  # classic, practice, tournament
practice_mode = False

# Progressive jackpot system
progressive_jackpot = 5000
jackpot_contribution = 0.01  # 1% of each bet goes to jackpot
jackpot_trigger = 0.001  # 0.1% chance to trigger jackpot

# Bonus features
free_spins = 0
multiplier = 1
bonus_round_active = False
bonus_round_spins = 0
bonus_multiplier = 1

# Tournament mode
tournament_mode = False
tournament_score = 0
tournament_time = 60  # 60 seconds
tournament_start_time = 0

# Statistics and achievements
stats = {
    "total_spins": 0,
    "total_wins": 0,
    "total_credits_won": 0,
    "biggest_win": 0,
    "jackpots_hit": 0,
    "free_spins_triggered": 0,
    "bonus_rounds_triggered": 0,
    "highest_multiplier": 1,
    "longest_winning_streak": 0,
    "current_streak": 0,
    "total_play_time": 0,
    "games_played": 0
}

achievements = {
    "first_win": False,
    "big_winner": False,  # Win 500+ credits
    "jackpot_hunter": False,  # Hit jackpot
    "free_spin_master": False,  # Trigger 10 free spins
    "bonus_round_expert": False,  # Complete 5 bonus rounds
    "streak_master": False,  # 10+ win streak
    "high_roller": False,  # Bet max 10 times
    "persistent_player": False,  # Play 100 spins
    "lucky_seven": False,  # Get three sevens 5 times
    "cherry_picker": False  # Get three cherries 10 times
}

# Animation variables
win_animation_time = 0
win_animation_duration = 2.0  # seconds
particles = []
glow_alpha = 0
glow_increasing = True

# Symbol names for display
symbol_names = ["Seven", "Cherry", "Plum", "Watermelon", "Bell"]

# Ensure winning_symbols is always defined
going_symbols = []
winning_symbols = []

# Enhanced paytable with proper paylines and bonus features
paytable = {
    # 3 of a kind combinations
    (0, 0, 0): 100,  # Three sevens - can trigger jackpot
    (1, 1, 1): 50,   # Three cherries - can trigger free spins
    (2, 2, 2): 25,   # Three plums
    (3, 3, 3): 15,   # Three watermelons
    (4, 4, 4): 10,   # Three bells
    
    # 2 of a kind combinations (first two positions)
    (0, 0, -1): 20,  # Two sevens
    (1, 1, -1): 10,  # Two cherries
    (2, 2, -1): 5,   # Two plums
    (3, 3, -1): 3,   # Two watermelons
    (4, 4, -1): 2,   # Two bells
    
    # Single high symbols
    (0, -1, -1): 5,  # One seven
    (1, -1, -1): 2,  # One cherry
}

# Define constants
REEL_WIDTH = reel_images[0].get_width()
REEL_HEIGHT = reel_images[0].get_height()
REEL_SPACING = 60

# Particle system
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
        self.life = 1.0
        self.decay = random.uniform(0.02, 0.05)
        self.color = color
        self.size = random.randint(2, 6)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # gravity
        self.life -= self.decay
        return self.life > 0
    
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * self.life)
            color = (int(self.color[0]), int(self.color[1]), int(self.color[2]), alpha)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)

def create_particles(x, y, count=20, color=(255, 215, 0)):
    """Create particle burst effect"""
    global particles
    for _ in range(count):
        particles.append(Particle(x, y, color))

def update_particles():
    """Update all particles"""
    global particles
    particles = [p for p in particles if p.update()]

def draw_particles(screen):
    """Draw all particles"""
    for particle in particles:
        particle.draw(screen)

# Define the reel class with enhanced animations
class Reel:
    def __init__(self, x):
        self.x = x
        self.y = REEL_Y
        self.images = reel_images
        self.num_images = len(self.images)
        self.speed = 0
        self.spin_time = 0
        self.spin_duration = 0
        self.stopped = True
        self.current_index = random.randint(0, self.num_images - 1)
        self.target_index = self.current_index
        self.easing_factor = 0
        self.stop_delay = 0  # For sequential stopping
    
    def start_spin(self, delay=0):
        self.speed = random.randint(8000, 15000)
        self.spin_duration = random.randint(30, 50)
        self.spin_time = 0
        self.stopped = False
        self.easing_factor = 0
        self.stop_delay = delay
        # Do not play start_sound here (will play once per spin in game loop)
    
    def update(self):
        if not self.stopped:
            self.spin_time += 1
            if self.spin_time > self.spin_duration + self.stop_delay:
                # Easing deceleration
                self.easing_factor += 0.05
                self.speed = max(0, self.speed - (self.speed * self.easing_factor * 0.1))
                if self.speed < 100:
                    self.stopped = True
                    self.speed = 0
                    # Pick a random final index for realism
                    self.current_index = random.randint(0, self.num_images - 1)
        if not self.stopped:
            self.current_index = int((self.current_index + self.speed) % self.num_images)
    
    def draw(self, glow=False):
        image = self.images[self.current_index]
        rect = image.get_rect()
        rect.x = self.x
        rect.y = self.y
        
        # Add glow effect for winning symbols
        if glow:
            glow_surface = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
            glow_color = (255, 215, 0, int(50 + 30 * math.sin(time.time() * 3)))
            pygame.draw.rect(glow_surface, glow_color, (0, 0, rect.width + 20, rect.height + 20), border_radius=10)
            screen.blit(glow_surface, (rect.x - 10, rect.y - 10))
        
        screen.blit(image, rect)

# Create the reels
reels = [
    Reel(REEL_X_START + i * (REEL_WIDTH + REEL_SPACING)) for i in range(num_reels)
]

# Set up fonts
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)
large_font = pygame.font.SysFont("Arial", 32)
led_font = pygame.font.SysFont("Courier", 28, bold=True)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
PURPLE = (255, 0, 255)

def play_sound(sound_name):
    """Play sound with error handling and fallback beep if sound fails."""
    try:
        if sound_name == "win" and win_sound:
            win_sound.play()
        elif sound_name == "coin" and coin_sound:
            coin_sound.play()
        elif sound_name == "button" and button_sound:
            button_sound.play()
        elif sound_name == "big_win" and big_win_sound:
            big_win_sound.play()
        elif sound_name == "jackpot" and jackpot_sound:
            jackpot_sound.play()
        elif sound_name == "bonus" and bonus_sound:
            bonus_sound.play()
        elif sound_name == "beep":
            import sys
            if sys.platform == "win32":
                import winsound
                winsound.Beep(1000, 150)
            else:
                print("\a", end="")
    except Exception as e:
        print("Sound error:", e)
        if sound_name == "beep":
            print("\a", end="")

def save_game_state():
    """Save game state to file"""
    game_state = {
        "credits": credits,
        "stats": stats,
        "achievements": achievements,
        "progressive_jackpot": progressive_jackpot
    }
    try:
        with open("slot_machine_save.json", "w") as f:
            json.dump(game_state, f)
    except:
        pass

def load_game_state():
    """Load game state from file"""
    global credits, stats, achievements, progressive_jackpot
    try:
        if os.path.exists("slot_machine_save.json"):
            with open("slot_machine_save.json", "r") as f:
                game_state = json.load(f)
                credits = game_state.get("credits", 1000)
                stats.update(game_state.get("stats", {}))
                achievements.update(game_state.get("achievements", {}))
                progressive_jackpot = game_state.get("progressive_jackpot", 5000)
    except:
        pass

def check_achievements():
    """Check and update achievements"""
    global achievements
    
    # First win
    if stats["total_wins"] > 0 and not achievements["first_win"]:
        achievements["first_win"] = True
    
    # Big winner
    if stats["biggest_win"] >= 500 and not achievements["big_winner"]:
        achievements["big_winner"] = True
    
    # Jackpot hunter
    if stats["jackpots_hit"] > 0 and not achievements["jackpot_hunter"]:
        achievements["jackpot_hunter"] = True
    
    # Free spin master
    if stats["free_spins_triggered"] >= 10 and not achievements["free_spin_master"]:
        achievements["free_spin_master"] = True
    
    # Bonus round expert
    if stats["bonus_rounds_triggered"] >= 5 and not achievements["bonus_round_expert"]:
        achievements["bonus_round_expert"] = True
    
    # Streak master
    if stats["longest_winning_streak"] >= 10 and not achievements["streak_master"]:
        achievements["streak_master"] = True
    
    # High roller
    if stats.get("max_bets", 0) >= 10 and not achievements["high_roller"]:
        achievements["high_roller"] = True
    
    # Persistent player
    if stats["total_spins"] >= 100 and not achievements["persistent_player"]:
        achievements["persistent_player"] = True

def check_win():
    """Enhanced win detection with progressive jackpot and bonus features"""
    global credits, current_bet, win_animation_time, progressive_jackpot, free_spins, multiplier, bonus_round_active, stats
    
    # Get current symbols
    symbols = [reels[i].current_index for i in range(3)]
    
    # Check for progressive jackpot (three sevens)
    if symbols[0] == symbols[1] == symbols[2] == 0:  # Three sevens
        jackpot_win = progressive_jackpot
        progressive_jackpot = 5000  # Reset jackpot
        credits += jackpot_win
        stats["jackpots_hit"] += 1
        stats["biggest_win"] = max(stats["biggest_win"], jackpot_win)
        play_sound("jackpot")
        return jackpot_win, f"JACKPOT! {jackpot_win} Credits!", [0, 1, 2]
    
    # Check for free spins (three cherries)
    if symbols[0] == symbols[1] == symbols[2] == 1:  # Three cherries
        free_spins += 10
        stats["free_spins_triggered"] += 10
        play_sound("bonus")
        return 0, f"FREE SPINS! +10 Free Spins!", [0, 1, 2]
    
    # Check for bonus round (three bells)
    if symbols[0] == symbols[1] == symbols[2] == 4:  # Three bells
        bonus_round_active = True
        bonus_round_spins = 5
        bonus_multiplier = 3
        stats["bonus_rounds_triggered"] += 1
        play_sound("bonus")
        return 0, f"BONUS ROUND! 5x Multiplier!", [0, 1, 2]
    
    # Check for regular wins
    win_amount = 0
    win_message = ""
    winning_symbols = []
    
    # Check 3 of a kind
    if symbols[0] == symbols[1] == symbols[2]:
        for combo, payout in paytable.items():
            if combo[0] == symbols[0] and combo[1] == symbols[1] and combo[2] == symbols[2]:
                win_amount = payout * current_bet * multiplier
                win_message = f"Three {symbol_names[symbols[0]]}s! Win: {win_amount}"
                winning_symbols = [0, 1, 2]
                break
    
    # Check 2 of a kind (first two positions)
    elif symbols[0] == symbols[1]:
        for combo, payout in paytable.items():
            if combo[0] == symbols[0] and combo[1] == symbols[1] and combo[2] == -1:
                win_amount = payout * current_bet * multiplier
                win_message = f"Two {symbol_names[symbols[0]]}s! Win: {win_amount}"
                winning_symbols = [0, 1]
                break
    
    # Check single high symbols
    else:
        for combo, payout in paytable.items():
            if combo[0] == symbols[0] and combo[1] == -1 and combo[2] == -1:
                win_amount = payout * current_bet * multiplier
                win_message = f"One {symbol_names[symbols[0]]}! Win: {win_amount}"
                winning_symbols = [0]
                break
    
    if win_amount > 0:
        credits += win_amount
        win_animation_time = time.time()
        stats["total_wins"] += 1
        stats["total_credits_won"] += win_amount
        stats["biggest_win"] = max(stats["biggest_win"], win_amount)
        stats["current_streak"] += 1
        stats["longest_winning_streak"] = max(stats["longest_winning_streak"], stats["current_streak"])
        
        # Play appropriate sound
        if win_amount >= 100:
            play_sound("big_win")
        else:
            play_sound("win")
        
        # Create particle effects
        for i in winning_symbols:
            x = reels[i].x + REEL_WIDTH // 2
            y = reels[i].y + REEL_HEIGHT // 2
            create_particles(x, y, 15, GOLD)
        
        return win_amount, win_message, winning_symbols
    
    # No win
    stats["current_streak"] = 0
    return 0, "", []

def draw_led_display(text, x, y, color=GOLD, size=28):
    """Draw LED-style display"""
    led_font = pygame.font.SysFont("Courier", size, bold=True)
    text_surface = led_font.render(text, True, color)
    # Add LED glow effect
    glow_surface = pygame.Surface((text_surface.get_width() + 4, text_surface.get_height() + 4), pygame.SRCALPHA)
    glow_color = (int(color[0]), int(color[1]), int(color[2]), 50)
    pygame.draw.rect(glow_surface, glow_color, (0, 0, text_surface.get_width() + 4, text_surface.get_height() + 4), border_radius=2)
    screen.blit(glow_surface, (x - 2, y - 2))
    screen.blit(text_surface, (x, y))

def draw_ui():
    """Draw a modern, clear UI with top bar, centered reels, and bottom bar."""
    # --- Top Bar ---
    top_bar = pygame.Surface((WIDTH, TOP_BAR_HEIGHT))
    top_bar.fill((25, 25, 40))
    screen.blit(top_bar, (0, 0))
    
    # CREDITS (left) - adjusted position to avoid overlap
    draw_led_display(f"CREDITS: {credits:06d}", 24, TOP_BAR_HEIGHT//2 - 18, GOLD, 24)
    
    # FREE SPINS (center, smaller font) - only show if active
    if free_spins > 0:
        draw_led_display(f"FREE SPINS: {free_spins:02d}", WIDTH//2 - 70, TOP_BAR_HEIGHT//2 - 16, GREEN, 18)
    
    # JACKPOT (right) - adjusted position to avoid overlap
    jackpot_text = f"JACKPOT: {progressive_jackpot:06d}"
    jackpot_width = len(jackpot_text) * 12  # Approximate width
    jackpot_x = WIDTH - jackpot_width - 24
    draw_led_display(jackpot_text, jackpot_x, TOP_BAR_HEIGHT//2 - 18, PURPLE, 24)
    
    # Draw a line below top bar
    pygame.draw.line(screen, (80, 80, 120), (0, TOP_BAR_HEIGHT), (WIDTH, TOP_BAR_HEIGHT), 3)

    # --- Bottom Bar ---
    bottom_bar = pygame.Surface((WIDTH, BOTTOM_BAR_HEIGHT))
    bottom_bar.fill((25, 25, 40))
    screen.blit(bottom_bar, (0, HEIGHT - BOTTOM_BAR_HEIGHT))
    
    # Split controls text to avoid overlap
    controls_text1 = small_font.render("B: Bet 1   N: Bet 10   M: Bet Max   A: Auto Play", True, WHITE)
    controls_text2 = small_font.render("P: Paytable   S: Stats   SPACE: Spin", True, WHITE)
    
    screen.blit(controls_text1, (WIDTH//2 - controls_text1.get_width()//2, HEIGHT - BOTTOM_BAR_HEIGHT + 12))
    screen.blit(controls_text2, (WIDTH//2 - controls_text2.get_width()//2, HEIGHT - BOTTOM_BAR_HEIGHT + 32))
    
    pygame.draw.line(screen, (80, 80, 120), (0, HEIGHT - BOTTOM_BAR_HEIGHT), (WIDTH, HEIGHT - BOTTOM_BAR_HEIGHT), 3)
    
    if auto_play:
        auto_text = font.render(f"AUTO: {auto_play_count}", True, GREEN)
        screen.blit(auto_text, (WIDTH - 180, HEIGHT - BOTTOM_BAR_HEIGHT - 30))
    if tournament_mode:
        remaining_time = max(0, tournament_time - (time.time() - tournament_start_time))
        draw_led_display(f"TIME: {int(remaining_time):02d}s", WIDTH - 200, HEIGHT - BOTTOM_BAR_HEIGHT - 40, BLUE, 20)
        draw_led_display(f"SCORE: {tournament_score:06d}", WIDTH - 200, HEIGHT - BOTTOM_BAR_HEIGHT - 20, GOLD, 20)

def draw_win_line():
    """Draw winning line animation"""
    global glow_alpha, glow_increasing
    
    if glow_increasing:
        glow_alpha += 5
        if glow_alpha >= 100:
            glow_increasing = False
    else:
        glow_alpha -= 5
        if glow_alpha <= 30:
            glow_increasing = True
    
    # Draw animated line connecting winning symbols
    line_color = (255, 215, 0, glow_alpha)
    line_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.line(line_surface, line_color, (reels[0].x + REEL_WIDTH//2, reels[0].y + REEL_HEIGHT//2), 
                    (reels[2].x + REEL_WIDTH//2, reels[2].y + REEL_HEIGHT//2), 8)
    screen.blit(line_surface, (0, 0))

def draw_paytable():
    """Draw the paytable overlay with enhanced styling"""
    # Create semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Draw paytable box with gradient effect
    paytable_rect = pygame.Rect(WIDTH//2 - 320, HEIGHT//2 - 280, 640, 560)
    
    # Create gradient background
    gradient_surface = pygame.Surface((640, 560))
    for y in range(560):
        alpha = 200 - int(y * 0.3)
        color = (50, 50, 80, alpha)
        pygame.draw.line(gradient_surface, color, (0, y), (640, y))
    screen.blit(gradient_surface, (WIDTH//2 - 320, HEIGHT//2 - 280))
    
    pygame.draw.rect(screen, GOLD, paytable_rect, 3)
    
    # Draw title with minimum font size
    title_text = small_font.render("PRIZE LIST", True, GOLD)
    title_glow = small_font.render("PRIZE LIST", True, (255, 255, 0))
    screen.blit(title_glow, (WIDTH//2 - title_text.get_width()//2 + 2, HEIGHT//2 - 260 + 2))
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 260))
    
    # Draw paytable entries with minimum formatting and organization
    y_offset = HEIGHT//2 - 200
    section_spacing = 25  # Minimum spacing
    
    # JACKPOT SECTION
    section_title = pygame.font.SysFont("Arial", 16).render("JACKPOT COMBINATIONS", True, PURPLE)
    screen.blit(section_title, (WIDTH//2 - section_title.get_width()//2, y_offset))
    y_offset += 20
    
    entries = [
        ("Three Sevens (JACKPOT)", f"{progressive_jackpot} Credits", PURPLE),
    ]
    
    for symbol, payout, color in entries:
        symbol_text = pygame.font.SysFont("Arial", 16).render(symbol, True, color)
        payout_text = pygame.font.SysFont("Arial", 16).render(payout, True, WHITE)
        screen.blit(symbol_text, (WIDTH//2 - 280, y_offset))
        screen.blit(payout_text, (WIDTH//2 + 80, y_offset))
        y_offset += 20
    
    y_offset += section_spacing
    
    # HIGH VALUE SECTION
    section_title = pygame.font.SysFont("Arial", 16).render("HIGH VALUE COMBINATIONS", True, GOLD)
    screen.blit(section_title, (WIDTH//2 - section_title.get_width()//2, y_offset))
    y_offset += 20
    
    entries = [
        ("Three Cherries", "50x bet + 10 Free Spins", RED),
        ("Three Bells", "10x bet + Bonus Round", BLUE),
        ("Three Plums", "25x bet", (255, 0, 255)),
        ("Three Watermelons", "15x bet", GREEN),
    ]
    
    for symbol, payout, color in entries:
        symbol_text = pygame.font.SysFont("Arial", 16).render(symbol, True, color)
        payout_text = pygame.font.SysFont("Arial", 16).render(payout, True, WHITE)
        screen.blit(symbol_text, (WIDTH//2 - 280, y_offset))
        screen.blit(payout_text, (WIDTH//2 + 80, y_offset))
        y_offset += 20
    
    y_offset += section_spacing
    
    # MEDIUM VALUE SECTION
    section_title = pygame.font.SysFont("Arial", 16).render("MEDIUM VALUE COMBINATIONS", True, GOLD)
    screen.blit(section_title, (WIDTH//2 - section_title.get_width()//2, y_offset))
    y_offset += 20
    
    entries = [
        ("Two Sevens", "20x bet", GOLD),
        ("Two Cherries", "10x bet", RED),
        ("Two Plums", "5x bet", (255, 0, 255)),
        ("Two Watermelons", "3x bet", GREEN),
        ("Two Bells", "2x bet", BLUE),
    ]
    
    for symbol, payout, color in entries:
        symbol_text = pygame.font.SysFont("Arial", 16).render(symbol, True, color)
        payout_text = pygame.font.SysFont("Arial", 16).render(payout, True, WHITE)
        screen.blit(symbol_text, (WIDTH//2 - 280, y_offset))
        screen.blit(payout_text, (WIDTH//2 + 80, y_offset))
        y_offset += 20
    
    y_offset += section_spacing
    
    # LOW VALUE SECTION
    section_title = pygame.font.SysFont("Arial", 16).render("LOW VALUE COMBINATIONS", True, GOLD)
    screen.blit(section_title, (WIDTH//2 - section_title.get_width()//2, y_offset))
    y_offset += 20
    
    entries = [
        ("One Seven", "5x bet", GOLD),
        ("One Cherry", "2x bet", RED),
    ]
    
    for symbol, payout, color in entries:
        symbol_text = pygame.font.SysFont("Arial", 16).render(symbol, True, color)
        payout_text = pygame.font.SysFont("Arial", 16).render(payout, True, WHITE)
        screen.blit(symbol_text, (WIDTH//2 - 280, y_offset))
        screen.blit(payout_text, (WIDTH//2 + 80, y_offset))
        y_offset += 20
    
    # Draw close instruction with minimum font size
    close_text = pygame.font.SysFont("Arial", 16).render("Press P to close paytable", True, GOLD)
    close_glow = pygame.font.SysFont("Arial", 16).render("Press P to close paytable", True, (255, 255, 0))
    screen.blit(close_glow, (WIDTH//2 - close_text.get_width()//2 + 1, HEIGHT//2 + 240 + 1))
    screen.blit(close_text, (WIDTH//2 - close_text.get_width()//2, HEIGHT//2 + 240))

def draw_stats():
    """Draw statistics overlay"""
    # Create semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Draw stats box with better sizing
    stats_rect = pygame.Rect(WIDTH//2 - 320, HEIGHT//2 - 280, 640, 560)
    pygame.draw.rect(screen, (50, 50, 80), stats_rect)
    pygame.draw.rect(screen, GOLD, stats_rect, 3)
    
    # Draw title with minimum font size
    title_text = small_font.render("STATISTICS", True, GOLD)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 260))
    
    # Draw stats with minimum organization
    y_offset = HEIGHT//2 - 200
    section_spacing = 25  # Minimum spacing
    
    # GAME STATS SECTION
    section_title = pygame.font.SysFont("Arial", 16).render("GAME STATISTICS", True, GOLD)
    screen.blit(section_title, (WIDTH//2 - section_title.get_width()//2, y_offset))
    y_offset += 20
    
    stat_entries = [
        f"Total Spins: {stats['total_spins']}",
        f"Total Wins: {stats['total_wins']}",
        f"Total Credits Won: {stats['total_credits_won']}",
        f"Biggest Win: {stats['biggest_win']}",
    ]
    
    for entry in stat_entries:
        entry_text = pygame.font.SysFont("Arial", 16).render(entry, True, WHITE)
        screen.blit(entry_text, (WIDTH//2 - 280, y_offset))
        y_offset += 20
    
    y_offset += section_spacing
    
    # SPECIAL EVENTS SECTION
    section_title = pygame.font.SysFont("Arial", 16).render("SPECIAL EVENTS", True, GOLD)
    screen.blit(section_title, (WIDTH//2 - section_title.get_width()//2, y_offset))
    y_offset += 20
    
    stat_entries = [
        f"Jackpots Hit: {stats['jackpots_hit']}",
        f"Free Spins Triggered: {stats['free_spins_triggered']}",
        f"Bonus Rounds: {stats['bonus_rounds_triggered']}",
        f"Highest Multiplier: {stats['highest_multiplier']}x",
    ]
    
    for entry in stat_entries:
        entry_text = pygame.font.SysFont("Arial", 16).render(entry, True, WHITE)
        screen.blit(entry_text, (WIDTH//2 - 280, y_offset))
        y_offset += 20
    
    y_offset += section_spacing
    
    # STREAKS SECTION
    section_title = pygame.font.SysFont("Arial", 16).render("WINNING STREAKS", True, GOLD)
    screen.blit(section_title, (WIDTH//2 - section_title.get_width()//2, y_offset))
    y_offset += 20
    
    stat_entries = [
        f"Longest Win Streak: {stats['longest_winning_streak']}",
        f"Current Streak: {stats['current_streak']}",
    ]
    
    for entry in stat_entries:
        entry_text = pygame.font.SysFont("Arial", 16).render(entry, True, WHITE)
        screen.blit(entry_text, (WIDTH//2 - 280, y_offset))
        y_offset += 20
    
    # Draw close instruction with minimum font size
    close_text = pygame.font.SysFont("Arial", 16).render("Press S to close stats", True, GOLD)
    screen.blit(close_text, (WIDTH//2 - close_text.get_width()//2, HEIGHT//2 + 240))

def change_bet(amount):
    """Change the current bet amount with sound feedback"""
    global current_bet, stats
    if amount == "max":
        new_bet = min(max_bet, credits)
        if new_bet != current_bet:
            current_bet = new_bet
            stats["max_bets"] = stats.get("max_bets", 0) + 1
            play_sound("button")
    else:
        new_bet = current_bet + amount
        if 1 <= new_bet <= max_bet and new_bet <= credits:
            current_bet = new_bet
            play_sound("button")

def start_auto_play(count=10):
    """Start auto play mode"""
    global auto_play, auto_play_count
    auto_play = True
    auto_play_count = count
    play_sound("button")

def start_tournament():
    """Start tournament mode"""
    global tournament_mode, tournament_score, tournament_start_time
    tournament_mode = True
    tournament_score = 0
    tournament_start_time = time.time()

def end_tournament():
    """End tournament mode and save score"""
    global tournament_mode, tournament_score
    tournament_mode = False
    # Save tournament score to high scores
    try:
        high_scores = []
        if os.path.exists("high_scores.json"):
            with open("high_scores.json", "r") as f:
                high_scores = json.load(f)
        
        high_scores.append({"score": tournament_score, "date": time.strftime("%Y-%m-%d %H:%M")})
        high_scores.sort(key=lambda x: x["score"], reverse=True)
        high_scores = high_scores[:10]  # Keep top 10
        
        with open("high_scores.json", "w") as f:
            json.dump(high_scores, f)
    except:
        pass

# Load game state on startup
load_game_state()

# Add persistent result message timer variables BEFORE game_loop is defined
result_display_time = 2.5  # seconds
result_time = 0

def draw_slot_machine_frame():
    global frame_x, frame_y, frame_width, frame_height
    # Add drop shadow under the frame
    frame_width = REEL_WIDTH * num_reels + REEL_SPACING * (num_reels - 1) + 100
    frame_height = REEL_HEIGHT + 120
    # Adjust slot machine frame and reels to be centered in the remaining space to the right of the paytable
    frame_x = (WIDTH - frame_width) // 2
    frame_y = (HEIGHT - frame_height) // 2 - 30
    shadow = pygame.Surface((frame_width+32, frame_height+32), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0,0,0,60), (0, frame_height//2, frame_width+32, frame_height//2+16))
    screen.blit(shadow, (frame_x-16, frame_y+32))
    # Softer gold gradient
    for i in range(frame_height):
        color = (
            min(255, 200 - i // 10),
            min(215, 180 - i // 16),
            min(120, 80 - i // 32)
        )
        pygame.draw.rect(screen, color, (frame_x, frame_y + i, frame_width, 1), border_radius=48)
    # Outer border
    pygame.draw.rect(screen, (180, 140, 40), (frame_x, frame_y, frame_width, frame_height), 10, border_radius=48)
    # Glass reflection overlay
    glass = pygame.Surface((frame_width-20, frame_height-20), pygame.SRCALPHA)
    pygame.draw.ellipse(glass, (255,255,255,36), (0, 0, frame_width-20, (frame_height-20)//2))
    screen.blit(glass, (frame_x+10, frame_y+10))
    # Lever (smaller, moved up/right)
    lever_x = frame_x + frame_width - 18
    lever_y = frame_y + 40
    pygame.draw.rect(screen, (120,120,120), (lever_x, lever_y, 10, 60), border_radius=5)
    pygame.draw.circle(screen, (200,0,0), (lever_x+5, lever_y), 12)
    pygame.draw.circle(screen, (255,255,255), (lever_x+5, lever_y), 12, 2)

def draw_reels():
    global winning_symbols, win_animation_time, win_animation_duration, frame_x, frame_y, frame_width, frame_height
    # Padding from left/right inside the frame
    left_pad = 40
    right_pad = 40
    top_pad = 40
    reel_spacing = REEL_SPACING + 16
    reel_height = REEL_HEIGHT + 24
    # Calculate total width of all reels + spacing
    reels_total_width = num_reels * REEL_WIDTH + (num_reels - 1) * reel_spacing
    # Center reels horizontally in the frame
    reels_x_start = frame_x + left_pad + (frame_width - left_pad - right_pad - reels_total_width) // 2
    # Center reels vertically in the frame
    reel_y = frame_y + top_pad + (frame_height - top_pad - 40 - reel_height) // 2
    for i, reel in enumerate(reels):
        rx = reels_x_start + i * (REEL_WIDTH + reel_spacing)
        ry = reel_y
        # Shadow
        shadow = pygame.Surface((REEL_WIDTH+18, reel_height+18), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0,0,0,50), (0, 8, REEL_WIDTH+18, reel_height))
        screen.blit(shadow, (rx-9, ry-9))
        # Reel window
        pygame.draw.rect(screen, (240,240,240), (rx, ry, REEL_WIDTH, reel_height), border_radius=28)
        pygame.draw.rect(screen, (0,0,0), (rx, ry, REEL_WIDTH, reel_height), 2, border_radius=28)
        # Highlight
        highlight = pygame.Surface((REEL_WIDTH, reel_height//2), pygame.SRCALPHA)
        pygame.draw.ellipse(highlight, (255,255,255,32), (0,0,REEL_WIDTH,reel_height//2))
        screen.blit(highlight, (rx, ry))
        # Draw the symbol, vertically centered
        symbol_y = ry + (reel_height - REEL_HEIGHT)//2
        reel.y = symbol_y
        reel.x = rx
        reel.draw(glow=(i in winning_symbols and time.time() - win_animation_time < win_animation_duration))

def draw_paytable_board():
    # Draw the paytable board on the left side
    board_x = 10
    board_y = TOP_BAR_HEIGHT + 10
    board_width = PAYTABLE_WIDTH
    board_height = HEIGHT - TOP_BAR_HEIGHT - BOTTOM_BAR_HEIGHT - 20
    
    # Background with better styling
    board_bg = pygame.Surface((board_width, board_height), pygame.SRCALPHA)
    # Create gradient background
    for y in range(board_height):
        alpha = 230 - int(y * 0.1)
        color = (30, 30, 30, alpha)
        pygame.draw.line(board_bg, color, (0, y), (board_width, y))
    
    # Add border with rounded corners
    pygame.draw.rect(board_bg, (255, 215, 0), (0, 0, board_width, board_height), 4, border_radius=12)
    screen.blit(board_bg, (board_x, board_y))
    
    # Title with minimum font size
    title_font = pygame.font.SysFont("Arial", 20, bold=True)
    title = title_font.render("PRIZE LIST", True, (255, 215, 0))
    title_rect = title.get_rect(centerx=board_x + board_width//2, y=board_y + 10)
    screen.blit(title, title_rect)
    
    # Add a separator line below title
    pygame.draw.line(screen, (255, 215, 0), 
                    (board_x + 20, board_y + 35), 
                    (board_x + board_width - 20, board_y + 35), 2)
    
    # List entries with minimum font sizes
    y = board_y + 45  # Start below title and separator
    entry_font = pygame.font.SysFont("Arial", 14, bold=True)
    small_font2 = pygame.font.SysFont("Arial", 12)
    bonus_font = pygame.font.SysFont("Arial", 10)
    symbol_y_pad = 4
    symbol_size = 20  # Minimum symbol size
    
    # Define paytable entries with better organization
    entries = [
        # JACKPOT SECTION
        ((0,0,0), "Three Sevens", f"{progressive_jackpot}", (255,0,255), "JACKPOT"),
        # HIGH VALUE SECTION
        ((1,1,1), "Three Cherries", "50x", (255,0,0), "+10 FS"),
        ((4,4,4), "Three Bells", "10x", (0,100,255), "Bonus"),
        ((2,2,2), "Three Plums", "25x", (255,0,255), ""),
        ((3,3,3), "Three Watermelons", "15x", (0,200,0), ""),
        # SPACER
        (None, "", "", (0,0,0), ""),
        # MEDIUM VALUE SECTION
        ((0,0,-1), "Two Sevens", "20x", (255,215,0), ""),
        ((1,1,-1), "Two Cherries", "10x", (255,0,0), ""),
        ((2,2,-1), "Two Plums", "5x", (255,0,255), ""),
        ((3,3,-1), "Two Watermelons", "3x", (0,200,0), ""),
        ((4,4,-1), "Two Bells", "2x", (0,100,255), ""),
        # SPACER
        (None, "", "", (0,0,0), ""),
        # LOW VALUE SECTION
        ((0,-1,-1), "One Seven", "5x", (255,215,0), ""),
        ((1,-1,-1), "One Cherry", "2x", (255,0,0), ""),
    ]
    
    for combo, desc, payout, color, bonus in entries:
        if desc == "":
            y += 12  # Minimum space between sections
            continue
            
        # Draw symbol(s) with better positioning
        if combo:
            symbol_x = board_x + 12
            for i, idx in enumerate(combo):
                if idx != -1:
                    img = reel_images[idx]
                    img_s = pygame.transform.smoothscale(img, (symbol_size, symbol_size))
                    screen.blit(img_s, (symbol_x + i*(symbol_size + 3), y + symbol_y_pad))
        
        # Draw description with minimum font and better positioning
        desc_text = entry_font.render(desc, True, color)
        desc_x = board_x + 95  # Moved closer to symbols
        screen.blit(desc_text, (desc_x, y + 4))
        
        # Draw payout with better positioning
        payout_text = small_font2.render(payout, True, (0,255,0) if "x" in payout else (255,0,255))
        payout_x = board_x + board_width - payout_text.get_width() - 12
        screen.blit(payout_text, (payout_x, y + 6))
        
        # Draw bonus text if present with minimum font
        if bonus:
            bonus_text = bonus_font.render(bonus, True, (255, 255, 0))
            bonus_x = board_x + 95
            screen.blit(bonus_text, (bonus_x, y + 20))
            y += 28  # Minimum space for entries with bonus text
        else:
            y += 24  # Minimum standard spacing

# Define the game loop
def game_loop():
    global credits, auto_play, auto_play_count, show_paytable, win_animation_time
    global free_spins, multiplier, bonus_round_active, progressive_jackpot
    global tournament_mode, tournament_score, stats, show_stats
    global result_time, result_display_time  # add result_display_time here
    all_stop = True
    win_amount = 0
    win_message = ""
    winning_symbols = []
    running = True
    show_stats = False
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game_state()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not show_stats:
                    show_paytable = not show_paytable
                    play_sound("button")
                elif event.key == pygame.K_s and not show_paytable:
                    show_stats = not show_stats
                    play_sound("button")
                elif event.key == pygame.K_b and all_stop:
                    change_bet(1)
                elif event.key == pygame.K_n and all_stop:
                    change_bet(10)
                elif event.key == pygame.K_m and all_stop:
                    change_bet("max")
                elif event.key == pygame.K_a and all_stop:
                    start_auto_play(10)
                elif event.key == pygame.K_t and all_stop:
                    start_tournament()
                elif event.key == pygame.K_r and credits < current_bet:
                    # Restart game
                    credits = 1000
                    progressive_jackpot = 5000
                    free_spins = 0
                    multiplier = 1
                    bonus_round_active = False
                elif event.key == pygame.K_SPACE and all_stop and all(reel.stopped for reel in reels):
                    if credits >= current_bet or free_spins > 0:
                        if free_spins > 0:
                            free_spins -= 1
                        else:
                            credits -= current_bet
                            progressive_jackpot += int(current_bet * jackpot_contribution)
                        # Play start sound only once per spin
                        if start_sound:
                            start_sound.play()
                        else:
                            play_sound("beep")
                        for i, reel in enumerate(reels):
                            reel.start_spin(delay=i * 5)
                        all_stop = False
                        win_amount = 0
                        win_message = ""
                        winning_symbols = []
                        play_sound("button")
                        stats["total_spins"] += 1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if spin_btn_rect.collidepoint(event.pos) and all_stop and all(reel.stopped for reel in reels):
                    if credits >= current_bet or free_spins > 0:
                        if free_spins > 0:
                            free_spins -= 1
                        else:
                            credits -= current_bet
                            progressive_jackpot += int(current_bet * jackpot_contribution)
                        if start_sound:
                            start_sound.play()
                        else:
                            play_sound("beep")
                        for i, reel in enumerate(reels):
                            reel.start_spin(delay=i * 5)
                        all_stop = False
                        win_amount = 0
                        win_message = ""
                        winning_symbols = []
                        play_sound("button")
                        stats["total_spins"] += 1
        
        # Update the game state
        for reel in reels:
            reel.update()
        
        # Update particles
        update_particles()

        # Check for auto play
        if auto_play and all_stop and auto_play_count > 0:
            if credits >= current_bet or free_spins > 0:
                if free_spins > 0:
                    free_spins -= 1
                else:
                    credits -= current_bet
                    progressive_jackpot += int(current_bet * jackpot_contribution)
                
                for i, reel in enumerate(reels):
                    reel.start_spin(delay=i * 5)
                all_stop = False
                win_amount = 0
                win_message = ""
                winning_symbols = []
                auto_play_count -= 1
                stats["total_spins"] += 1
            else:
                auto_play = False

        # Check tournament time
        if tournament_mode:
            if time.time() - tournament_start_time >= tournament_time:
                end_tournament()

        # Draw the game
        screen.fill((0, 0, 0))  # Use solid black background
        
        # Draw always-visible paytable board
        draw_paytable_board()
        # Draw slot machine frame and reels
        draw_slot_machine_frame()
        draw_reels()
        
        # Draw the new SPIN button
        mouse_pos = pygame.mouse.get_pos()
        if spin_btn_rect.collidepoint(mouse_pos) and all_stop and all(reel.stopped for reel in reels):
            btn_color = SPIN_BTN_HOVER
        else:
            btn_color = SPIN_BTN_COLOR
        pygame.draw.rect(screen, btn_color, spin_btn_rect, border_radius=16)
        spin_text = large_font.render("SPIN", True, SPIN_BTN_TEXT_COLOR)
        screen.blit(spin_text, (spin_btn_rect.centerx - spin_text.get_width() // 2, spin_btn_rect.centery - spin_text.get_height() // 2))
        
        # Draw win line if there's a win
        if win_amount > 0 and time.time() - win_animation_time < win_animation_duration:
            draw_win_line()
        
        # Draw particles
        draw_particles(screen)
        
        # Draw UI
        draw_ui()

        # Check for a win
        if not all_stop and all(reel.stopped for reel in reels):
            start_sound.stop() if start_sound else None
            all_stop = True
            win_amount, win_message, winning_symbols = check_win()
            result_time = time.time()  # Only set here!
            if tournament_mode:
                tournament_score += win_amount

        # Game result message display logic
        # When a result is set (after all reels stop):
        if all_stop and win_amount > 0 and (time.time() - result_time < result_display_time):
            # Draw result message in a dedicated area between the top bar and the slot machine frame
            display_height = 54
            display_width = WIDTH - 80
            display_x = 40
            display_y = TOP_BAR_HEIGHT + 10  # Just below the top bar
            # Draw display window background
            display_bg = pygame.Surface((display_width, display_height), pygame.SRCALPHA)
            display_bg.fill((30, 30, 30, 220))
            pygame.draw.rect(display_bg, (200, 180, 60, 180), (0, 0, display_width, display_height), border_radius=18)
            pygame.draw.rect(display_bg, (255, 215, 0), (0, 0, display_width, display_height), 3, border_radius=18)
            screen.blit(display_bg, (display_x, display_y))
            # Draw the win message, centered
            win_text = large_font.render(win_message, True, GOLD)
            screen.blit(win_text, (display_x + display_width//2 - win_text.get_width()//2, display_y + 4))
            # Draw credit text below (if space)
            credit_text = font.render(f"+{win_amount} Credits!", True, GREEN)
            screen.blit(credit_text, (display_x + display_width//2 - credit_text.get_width()//2, display_y + 28))

        # Draw paytable if requested
        if show_paytable:
            draw_paytable()

        # Draw stats if requested
        if show_stats:
            draw_stats()

        # Check for game over
        if credits < current_bet and free_spins == 0 and not auto_play:
            game_over_bg = pygame.Surface((WIDTH, 80))
            game_over_bg.set_alpha(200)
            game_over_bg.fill((100, 0, 0))
            screen.blit(game_over_bg, (0, HEIGHT//2 - 40))
            
            game_over_text = large_font.render("GAME OVER - No more credits!", True, RED)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 20))
            
            restart_text = font.render("Press R to restart", True, WHITE)
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))

        # Check achievements
        check_achievements()

        pygame.display.flip()

# Start the game loop
game_loop()

# Clean up Pygame
pygame.quit()
