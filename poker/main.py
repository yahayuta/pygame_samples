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
    for card in hand:
        _, rank = card
        rank = ranks.index(rank)  # Convert rank from string to integer
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
        suit_counts[card[0]] = suit_counts.get(card[0], 0) + 1

    is_flush = any(count == 5 for count in suit_counts.values())
    is_straight = sorted(rank_counts.keys()) in (
        [0, 1, 2, 3, 12],  # Ace-2-3-4-5 straight
        list(range(min(rank_counts), max(rank_counts) + 1)),  # Normal straight
    )

    if is_flush and is_straight:
        return "Straight Flush"
    elif any(count == 4 for count in rank_counts.values()):
        return "Four of a Kind"
    elif sorted(rank_counts.values()) == [2, 3]:
        return "Full House"
    elif is_flush:
        return "Flush"
    elif is_straight:
        return "Straight"
    elif any(count == 3 for count in rank_counts.values()):
        return "Three of a Kind"
    elif sorted(rank_counts.values()) == [1, 2, 2]:
        return "Two Pair"
    elif any(count == 2 for count in rank_counts.values()):
        return "One Pair"
    else:
        return "High Card"

# Determine the winner
def determine_winner(player_hand, computer_hand):
    player_rank = get_hand_rank(player_hand)
    computer_rank = get_hand_rank(computer_hand)

    if player_rank == computer_rank:
        return f"It's a tie! you:{player_rank} cpu:{computer_rank}"
    elif player_rank > computer_rank:
        return f"Player wins! you:{player_rank} cpu:{computer_rank}"
    else:
        return f"Computer wins! you:{player_rank} cpu:{computer_rank}"

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
