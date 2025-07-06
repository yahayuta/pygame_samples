import pygame
import random

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define constants for the card size
CARD_WIDTH = 71
CARD_HEIGHT = 96

# Define the ranks and suits
suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']

# Initialize Pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the card images
card_images = {}
back_img = pygame.image.load('cards/back.png')
image_width, image_height = back_img.get_size()
card_images['back'] = pygame.transform.scale(back_img, (image_width * 0.2, image_height * 0.2))
for suit in suits:
    for rank in ranks:
        filename = 'cards/{}_of_{}.png'.format(rank, suit)
        card_image = pygame.image.load(filename)
        card_images['{}_{}'.format(rank, suit)] = pygame.transform.scale(card_image, (image_width * 0.2, image_height * 0.2))

# Define the font for displaying text on the screen
font = pygame.font.SysFont('Arial', 24)
title_font = pygame.font.SysFont('Arial', 28, bold=True)
instruction_font = pygame.font.SysFont('Arial', 18)

# Define a function to create a deck of cards
def create_deck():
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck

# Define a function to draw a card
def draw_card(screen, card, x, y):
    image = card_images['{}_{}'.format(card[0], card[1])]
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

# Define a function to display the player's hand
def display_player_hand(screen, player_hand):
    x = 50
    y = 400
    for card in player_hand:
        draw_card(screen, card, x, y)
        x += 100

# Define a function to display the dealer's hand
def display_dealer_hand(screen, dealer_hand, reveal):
    x = 50
    y = 100
    for i, card in enumerate(dealer_hand):
        if i == 0 and not reveal:
            image = card_images['back']
        else:
            image = card_images['{}_{}'.format(card[0], card[1])]
        screen.blit(image, (x, y))
        x += 100

# Function to draw instructions
def draw_instructions():
    # Title
    title_text = title_font.render("BLACKJACK", True, (255, 255, 255))
    screen.blit(title_text, (10, 10))
    
    # Instructions
    instructions = [
        "OBJECTIVE: Beat dealer without going over 21",
        "CONTROLS:",
        "  H - Hit (draw card)",
        "  S - Stay (end turn)",
        "SCORING: Closest to 21 wins",
        "GAME OVER: Over 21 = bust"
    ]
    
    for i, instruction in enumerate(instructions):
        text = instruction_font.render(instruction, True, (255, 255, 255))
        screen.blit(text, (10, 50 + i * 25))

# Define the main function for the game
def main():
    # Create a deck of cards
    deck = create_deck()

    # Initialize the player's hand and the dealer's hand
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    # Initialize the game state variables
    game_over = False
    player_turn = True
    dealer_turn = False
    player_wins = False
    dealer_wins = False
    tie = False
    quit_game = False
    
    # Start the game loop
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                quit_game = True
                # Quit Pygame
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                # Player's turn
                if player_turn:
                    if event.key == pygame.K_h:
                        player_hand.append(deck.pop())
                        if calculate_hand_value(player_hand) > 21:
                            player_wins = False
                            dealer_wins = True
                            game_over = True
                        elif len(player_hand) == 5:
                            player_wins = True
                            dealer_wins = False
                            game_over = True
                    elif event.key == pygame.K_s:
                        player_turn = False
                        dealer_turn = True

                # Dealer's turn
                elif dealer_turn:
                    while calculate_hand_value(dealer_hand) < 17:
                        dealer_hand.append(deck.pop())
                    if calculate_hand_value(dealer_hand) > 21:
                        player_wins = True
                        dealer_wins = False
                        game_over = True
                    elif calculate_hand_value(dealer_hand) >= calculate_hand_value(player_hand):
                        player_wins = False
                        dealer_wins = True
                        game_over = True
                    else:
                        player_wins = True
                        dealer_wins = False
                        game_over = True

        if quit_game:
            break

        # Draw the screen
        screen.fill((0, 128, 0))
        display_player_hand(screen, player_hand)
        display_dealer_hand(screen, dealer_hand, not player_turn)
        
        # Draw instructions
        draw_instructions()
        
        if player_wins:
            text = font.render('Player wins!', True, (255, 255, 255))
            screen.blit(text, (350, 300))
        elif dealer_wins:
            text = font.render('Dealer wins!', True, (255, 255, 255))
            screen.blit(text, (350, 300))
        elif tie:
            text = font.render('It\'s a tie!', True, (255, 255, 255))
            screen.blit(text, (350, 300))

        if game_over:
            text = font.render('Press any key to play again', True, (255, 255, 255))
            screen.blit(text, (300, 350))
            
        pygame.display.flip()

    if not quit_game:
        # Wait for a key press before starting a new game
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    main()

# Start the game
main()
