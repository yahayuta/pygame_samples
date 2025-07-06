import pygame
import random

# Define constants
WIDTH = 800
HEIGHT = 600
CARD_WIDTH = 100
CARD_HEIGHT = 150

# Define the ranks and suits
suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Poker Game")

card_back_image = pygame.image.load("images/back.png")  # Adjust the path to your card back image
image_width, image_height = card_back_image.get_size()
card_back_image = pygame.transform.scale(card_back_image, (image_width * 0.2, image_height * 0.2))

# Load card images
card_images = {}
for suit in suits:
    for rank in ranks:
        image_path = f"images/{rank}_of_{suit}.png"  # Adjust the path to your card images directory
        card_image = pygame.image.load(image_path)
        card_images[(suit, rank)] = pygame.transform.scale(card_image, (image_width * 0.2, image_height * 0.2))


# Create a deck of cards
deck = [(suit, rank) for suit in suits for rank in ranks]
random.shuffle(deck)

# Deal initial hands
player_hand = [deck.pop(), deck.pop(), deck.pop(), deck.pop(), deck.pop()]
computer_hand = [deck.pop(), deck.pop(), deck.pop(), deck.pop(), deck.pop()]

# Helper function to determine the poker hand rank
def get_hand_rank(hand):
    rank_counts = {}
    suit_counts = {}
    rank_values = []
    
    for card in hand:
        _, rank = card
        rank_idx = ranks.index(rank)
        rank_values.append(rank_idx)
        rank_counts[rank_idx] = rank_counts.get(rank_idx, 0) + 1
        suit_counts[card[0]] = suit_counts.get(card[0], 0) + 1

    is_flush = any(count == 5 for count in suit_counts.values())
    
    # Check for straight
    rank_values.sort()
    is_straight = False
    if len(rank_values) == 5:
        # Check for Ace-low straight (A-2-3-4-5)
        if rank_values == [0, 1, 2, 3, 12]:  # Ace, 2, 3, 4, 5
            is_straight = True
        # Check for normal straight
        elif rank_values == list(range(min(rank_values), max(rank_values) + 1)):
            is_straight = True

    # Determine hand rank
    if is_flush and is_straight:
        return ("Straight Flush", 8)
    elif any(count == 4 for count in rank_counts.values()):
        return ("Four of a Kind", 7)
    elif sorted(rank_counts.values()) == [2, 3]:
        return ("Full House", 6)
    elif is_flush:
        return ("Flush", 5)
    elif is_straight:
        return ("Straight", 4)
    elif any(count == 3 for count in rank_counts.values()):
        return ("Three of a Kind", 3)
    elif sorted(rank_counts.values()) == [1, 2, 2]:
        return ("Two Pair", 2)
    elif any(count == 2 for count in rank_counts.values()):
        return ("One Pair", 1)
    else:
        return ("High Card", 0)

# Determine the winner
def determine_winner(player_hand, computer_hand):
    player_rank, player_score = get_hand_rank(player_hand)
    computer_rank, computer_score = get_hand_rank(computer_hand)

    if player_score == computer_score:
        return f"It's a tie! Both have {player_rank}"
    elif player_score > computer_score:
        return f"Player wins! {player_rank} vs {computer_rank}"
    else:
        return f"Computer wins! {computer_rank} vs {player_rank}"

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a deck of cards
                deck = [(suit, rank) for suit in suits for rank in ranks]
                random.shuffle(deck)

                # Deal initial hands
                player_hand = [deck.pop(), deck.pop(), deck.pop(), deck.pop(), deck.pop()]
                computer_hand = [deck.pop(), deck.pop(), deck.pop(), deck.pop(), deck.pop()]

    # Clear the screen
    screen.fill((0, 128, 0))  # Green background color

    # Draw player's hand
    for i, card in enumerate(player_hand):
        x = i * CARD_WIDTH + 50
        y = HEIGHT - CARD_HEIGHT - 50
        screen.blit(card_images[card], (x, y))

    # Draw computer's hand (showing only the back of the cards)
    for i, card in enumerate(computer_hand):
        x = i * CARD_WIDTH + 50
        y = 50
        screen.blit(card_images[card], (x, y))

    # Determine the winner
    winner = determine_winner(player_hand, computer_hand)

    # Display the winner on the screen
    font = pygame.font.Font(None, 36)
    text = font.render(winner, True, (255, 255, 255))  # White text color
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    pygame.display.flip()

# Quit the game
pygame.quit()
