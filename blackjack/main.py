import pygame
import random
import math
import os

# Define constants for the screen width and height
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Define constants for the card size
CARD_WIDTH = 60
CARD_HEIGHT = 90

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
GOLD = (255, 215, 0)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

# Define the ranks and suits
suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']

# Initialize Pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack - Casino Royale")

# Load the card images
card_images = {}
back_img = pygame.image.load('cards/back.png')
card_images['back'] = pygame.transform.scale(back_img, (CARD_WIDTH, CARD_HEIGHT))
for suit in suits:
    for rank in ranks:
        filename = 'cards/{}_of_{}.png'.format(rank, suit)
        card_image = pygame.image.load(filename)
        card_images['{}_{}'.format(rank, suit)] = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))

# Define fonts
title_font = pygame.font.SysFont('Arial', 48, bold=True)
large_font = pygame.font.SysFont('Arial', 36, bold=True)
font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)
button_font = pygame.font.SysFont('Arial', 20, bold=True)

# Button class for UI
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = button_font
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 3, border_radius=10)
        
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.color
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Chip class for betting
class Chip:
    def __init__(self, x, y, value, color):
        self.x = x
        self.y = y
        self.value = value
        self.color = color
        self.radius = 25
        self.selected = False
        
    def draw(self, surface):
        # Draw chip shadow
        pygame.draw.circle(surface, DARK_GRAY, (self.x + 2, self.y + 2), self.radius)
        
        # Draw chip
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, BLACK, (self.x, self.y), self.radius, 3)
        
        # Draw value text
        if self.value >= 1000:
            text = f"${self.value//1000}K"
        else:
            text = f"${self.value}"
        text_surface = small_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        surface.blit(text_surface, text_rect)
        
        # Draw selection indicator
        if self.selected:
            pygame.draw.circle(surface, GOLD, (self.x, self.y), self.radius + 5, 3)
    
    def is_clicked(self, pos):
        distance = math.sqrt((pos[0] - self.x)**2 + (pos[1] - self.y)**2)
        return distance <= self.radius

# Define a function to create a deck of cards
def create_deck():
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck

# Define a function to draw a card with shadow
def draw_card(screen, card, x, y, angle=0):
    image = card_images['{}_{}'.format(card[0], card[1])]
    
    # Draw shadow
    shadow = pygame.Surface((CARD_WIDTH + 4, CARD_HEIGHT + 4))
    shadow.fill(DARK_GRAY)
    screen.blit(shadow, (x + 2, y + 2))
    
    # Rotate image if angle is specified
    if angle != 0:
        image = pygame.transform.rotate(image, angle)
    
    screen.blit(image, (x, y))

# Define a function to calculate the value of a hand
def calculate_hand_value(hand):
    value = 0
    has_ace = False
    for card in hand:
        rank = card[0]
        if rank == 'ace':
            has_ace = True
            value += 11
        elif rank in ['jack', 'queen', 'king']:
            value += 10
        else:
            value += int(rank)
    if has_ace and value > 21:
        value -= 10
    return value

# Define a function to display the player's hand with better layout
def display_player_hand(screen, player_hand, player_value):
    # Player section background (move down, reduce height)
    player_bg = pygame.Rect(30, 250, SCREEN_WIDTH - 60, 120)
    pygame.draw.rect(screen, DARK_GREEN, player_bg, border_radius=15)
    pygame.draw.rect(screen, GOLD, player_bg, 3, border_radius=15)
    
    # Player title
    title_text = large_font.render("YOUR HAND", True, WHITE)
    screen.blit(title_text, (50, 260))
    
    # Player value
    value_text = font.render(f"Value: {player_value}", True, WHITE)
    screen.blit(value_text, (50, 290))
    
    # Draw cards
    start_x = 50
    y = 320
    for i, card in enumerate(player_hand):
        draw_card(screen, card, start_x + i * 70, y)

# Define a function to display the dealer's hand
def display_dealer_hand(screen, dealer_hand, dealer_value, reveal):
    # Dealer section background (move down, reduce height)
    dealer_bg = pygame.Rect(30, 70, SCREEN_WIDTH - 60, 120)
    pygame.draw.rect(screen, DARK_GREEN, dealer_bg, border_radius=15)
    pygame.draw.rect(screen, GOLD, dealer_bg, 3, border_radius=15)
    
    # Dealer title
    title_text = large_font.render("DEALER'S HAND", True, WHITE)
    screen.blit(title_text, (50, 80))
    
    # Dealer value (only show if revealed)
    if reveal:
        value_text = font.render(f"Value: {dealer_value}", True, WHITE)
    else:
        value_text = font.render("Value: ?", True, WHITE)
    screen.blit(value_text, (50, 110))
    
    # Draw cards
    start_x = 50
    y = 140
    for i, card in enumerate(dealer_hand):
        if i == 0 and not reveal:
            image = card_images['back']
            # Draw shadow
            shadow = pygame.Surface((CARD_WIDTH + 4, CARD_HEIGHT + 4))
            shadow.fill(DARK_GRAY)
            screen.blit(shadow, (start_x + i * 70 + 2, y + 2))
            screen.blit(image, (start_x + i * 70, y))
        else:
            draw_card(screen, card, start_x + i * 70, y)

# Function to draw the game title and background
def draw_background():
    # Create gradient background
    for y in range(SCREEN_HEIGHT):
        color_ratio = y / SCREEN_HEIGHT
        r = int(0 + (34 - 0) * color_ratio)
        g = int(50 + (139 - 50) * color_ratio)
        b = int(0 + (34 - 0) * color_ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    # Draw title with shadow
    title_text = title_font.render("BLACKJACK", True, BLACK)
    title_shadow = title_font.render("BLACKJACK", True, DARK_GRAY)
    screen.blit(title_shadow, (SCREEN_WIDTH//2 - title_text.get_width()//2 + 2, 15))
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 13))

# Function to draw game status
def draw_game_status(screen, game_state, player_value, dealer_value, current_bet=0, bankroll=1000):
    # Move status box lower to avoid overlap
    status_bg = pygame.Rect(SCREEN_WIDTH//2 - 200, 420, 400, 60)
    pygame.draw.rect(screen, BLACK, status_bg, border_radius=15)
    pygame.draw.rect(screen, GOLD, status_bg, 3, border_radius=15)
    
    if game_state == "betting":
        status_text = font.render(f"Place your bet! Bankroll: ${bankroll}", True, WHITE)
    elif game_state == "playing":
        status_text = font.render(f"Your turn - Hit or Stand? Bet: ${current_bet}", True, WHITE)
    elif game_state == "dealer_turn":
        status_text = font.render("Dealer's turn...", True, WHITE)
    elif game_state == "player_bust":
        status_text = large_font.render(f"BUST! You lose ${current_bet}!", True, RED)
    elif game_state == "dealer_bust":
        status_text = large_font.render(f"Dealer busts! You win ${current_bet}!", True, GOLD)
    elif game_state == "player_win":
        status_text = large_font.render(f"You win ${current_bet}!", True, GOLD)
    elif game_state == "dealer_win":
        status_text = large_font.render(f"Dealer wins! You lose ${current_bet}!", True, RED)
    elif game_state == "tie":
        status_text = large_font.render(f"Push! Bet returned.", True, WHITE)
    
    screen.blit(status_text, (SCREEN_WIDTH//2 - status_text.get_width()//2, 440))

# Function to draw betting interface
def draw_betting_interface(screen, chips, current_bet, bankroll):
    # Betting area background
    betting_bg = pygame.Rect(SCREEN_WIDTH//2 - 200, 150, 400, 180)
    pygame.draw.rect(screen, BLACK, betting_bg, border_radius=15)
    pygame.draw.rect(screen, GOLD, betting_bg, 3, border_radius=15)
    
    # Title
    title_text = large_font.render("PLACE YOUR BET", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 170))
    
    # Bankroll display
    bankroll_text = font.render(f"Bankroll: ${bankroll}", True, GOLD)
    screen.blit(bankroll_text, (SCREEN_WIDTH//2 - bankroll_text.get_width()//2, 200))
    
    # Current bet display
    bet_text = font.render(f"Current Bet: ${current_bet}", True, WHITE)
    screen.blit(bet_text, (SCREEN_WIDTH//2 - bet_text.get_width()//2, 230))
    
    # Draw chips (move up a bit)
    for chip in chips:
        chip.draw(screen)
    
    # Draw bet area and DEAL button further down, outside the black box
    bet_area = pygame.Rect(SCREEN_WIDTH//2 - 60, 350, 120, 50)
    pygame.draw.rect(screen, DARK_GREEN, bet_area, border_radius=10)
    pygame.draw.rect(screen, GOLD, bet_area, 3, border_radius=10)
    
    if current_bet > 0:
        bet_chip_text = font.render(f"${current_bet}", True, WHITE)
        screen.blit(bet_chip_text, (SCREEN_WIDTH//2 - bet_chip_text.get_width()//2, 365))

# Define the main function for the game
def main():
    # Initialize game variables
    bankroll = 1000
    current_bet = 0
    selected_chip = None
    
    # Create chips
    chips = [
        Chip(SCREEN_WIDTH//2 - 150, 270, 5, RED),
        Chip(SCREEN_WIDTH//2 - 100, 270, 25, BLUE),
        Chip(SCREEN_WIDTH//2 - 50, 270, 100, GREEN),
        Chip(SCREEN_WIDTH//2, 270, 500, PURPLE),
        Chip(SCREEN_WIDTH//2 + 50, 270, 1000, GOLD),
        Chip(SCREEN_WIDTH//2 + 100, 270, 5000, ORANGE)
    ]
    
    # Create buttons
    hit_button = Button(SCREEN_WIDTH//2 - 200, 520, 120, 50, "HIT", GREEN, DARK_GREEN)
    stand_button = Button(SCREEN_WIDTH//2 - 60, 520, 120, 50, "STAND", BLUE, DARK_GRAY)
    deal_button = Button(SCREEN_WIDTH//2 - 60, 420, 120, 50, "DEAL", GOLD, ORANGE)
    new_game_button = Button(SCREEN_WIDTH//2 + 80, 520, 120, 50, "NEW GAME", GOLD, RED)
    
    # Create a deck of cards
    deck = create_deck()

    # Initialize the player's hand and the dealer's hand
    player_hand = []
    dealer_hand = []

    # Initialize the game state variables
    game_state = "betting"
    player_value = 0
    dealer_value = 0
    
    # Start the game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_state == "playing":
                    if event.key == pygame.K_h:
                        player_hand.append(deck.pop())
                        player_value = calculate_hand_value(player_hand)
                        if player_value > 21:
                            game_state = "player_bust"
                            bankroll -= current_bet
                        elif len(player_hand) == 5:
                            game_state = "player_win"
                            bankroll += current_bet
                    elif event.key == pygame.K_s:
                        game_state = "dealer_turn"
                        # Dealer's turn logic
                        while calculate_hand_value(dealer_hand) < 17:
                            dealer_hand.append(deck.pop())
                        dealer_value = calculate_hand_value(dealer_hand)
                        
                        if dealer_value > 21:
                            game_state = "dealer_bust"
                            bankroll += current_bet
                        elif dealer_value >= player_value:
                            game_state = "dealer_win"
                            bankroll -= current_bet
                        else:
                            game_state = "player_win"
                            bankroll += current_bet
                elif event.key == pygame.K_n:
                    # Start new game
                    deck = create_deck()
                    player_hand = []
                    dealer_hand = []
                    current_bet = 0
                    game_state = "betting"
            
            # Handle chip clicks for betting
            if game_state == "betting":
                for chip in chips:
                    if event.type == pygame.MOUSEBUTTONDOWN and chip.is_clicked(event.pos):
                        if bankroll >= chip.value:
                            current_bet += chip.value
                            bankroll -= chip.value
                            # Reset chip selection
                            for c in chips:
                                c.selected = False
                            chip.selected = True
            
            # Handle button clicks
            if deal_button.handle_event(event) and game_state == "betting" and current_bet > 0:
                # Deal cards
                player_hand = [deck.pop(), deck.pop()]
                dealer_hand = [deck.pop(), deck.pop()]
                player_value = calculate_hand_value(player_hand)
                dealer_value = calculate_hand_value(dealer_hand)
                game_state = "playing"
            elif hit_button.handle_event(event) and game_state == "playing":
                player_hand.append(deck.pop())
                player_value = calculate_hand_value(player_hand)
                if player_value > 21:
                    game_state = "player_bust"
                    bankroll -= current_bet
                elif len(player_hand) == 5:
                    game_state = "player_win"
                    bankroll += current_bet
            elif stand_button.handle_event(event) and game_state == "playing":
                game_state = "dealer_turn"
                # Dealer's turn logic
                while calculate_hand_value(dealer_hand) < 17:
                    dealer_hand.append(deck.pop())
                dealer_value = calculate_hand_value(dealer_hand)
                
                if dealer_value > 21:
                    game_state = "dealer_bust"
                    bankroll += current_bet
                elif dealer_value >= player_value:
                    game_state = "dealer_win"
                    bankroll -= current_bet
                else:
                    game_state = "player_win"
                    bankroll += current_bet
            elif new_game_button.handle_event(event):
                # Start new game
                deck = create_deck()
                player_hand = []
                dealer_hand = []
                current_bet = 0
                game_state = "betting"

        # Draw the screen
        draw_background()
        
        if game_state == "betting":
            # Draw betting interface
            draw_betting_interface(screen, chips, current_bet, bankroll)
            deal_button.draw(screen)
        else:
            # Display hands
            display_dealer_hand(screen, dealer_hand, dealer_value, game_state != "playing")
            display_player_hand(screen, player_hand, player_value)
            
            # Draw game status
            draw_game_status(screen, game_state, player_value, dealer_value, current_bet, bankroll)
            
            # Draw buttons
            if game_state == "playing":
                hit_button.draw(screen)
                stand_button.draw(screen)
            else:
                new_game_button.draw(screen)
        
        # Draw instructions
        if game_state == "betting":
            instructions = [
                "Click chips to place your bet",
                "Click DEAL to start the game",
                "Press N or click NEW GAME to reset"
            ]
        else:
            instructions = [
                "Press H or click HIT to draw a card",
                "Press S or click STAND to end your turn",
                "Press N or click NEW GAME to start over"
            ]
        
        for i, instruction in enumerate(instructions):
            text = small_font.render(instruction, True, WHITE)
            screen.blit(text, (10, SCREEN_HEIGHT - 60 + i * 20))
        
        pygame.display.flip()

    pygame.quit()

# Start the game
if __name__ == "__main__":
    main()
