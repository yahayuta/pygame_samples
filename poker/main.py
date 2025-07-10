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

# Add game state variables for betting and draw rounds
player_chips = 1000
computer_chips = 1000
pot = 0
# Add variable for current bet/raise amount
current_bet_amount = 10
player_in = True
computer_in = True
player_selected = [False] * 5  # For discards

game_phase = 'deal'  # 'deal', 'bet1', 'draw', 'bet2', 'showdown', 'gameover'
message = ''

# Add a variable to track last computer action
last_computer_action = ''

# Add action history log
action_history = []

# Add a variable to track game over state
game_over = False

# Add a variable to track help overlay state
show_help = False

# Add variables for stats/leaderboard
show_stats = False
stats = {
    'hands_played': 0,
    'player_wins': 0,
    'computer_wins': 0,
    'ties': 0,
    'biggest_pot': 0,
    'current_streak': 0,
    'longest_streak': 0,
    'last_winner': None
}

# --- Casino Poker Rule Enhancements ---
ANTE_AMOUNT = 10
MIN_BET = 10
MAX_BET = 100

dealer_is_player = True  # True = player is dealer, False = computer is dealer

# Scaffold for multiple players (for now, just player and computer)
players = [
    {'name': 'You', 'chips': 1000, 'is_human': True},
    {'name': 'Computer', 'chips': 1000, 'is_human': False}
]
# For compatibility, keep player_chips and computer_chips variables
player_chips = players[0]['chips']
computer_chips = players[1]['chips']


def log_action(action):
    global action_history
    action_history.append(action)
    if len(action_history) > 3:
        action_history = action_history[-3:]

# Helper to reset hands and state
def new_hand():
    global deck, player_hand, computer_hand, pot, player_in, computer_in, player_selected, game_phase, message, last_computer_action, action_history, game_over, dealer_is_player, player_chips, computer_chips
    deck = [(suit, rank) for suit in suits for rank in ranks]
    random.shuffle(deck)
    player_hand = [deck.pop(), deck.pop(), deck.pop(), deck.pop(), deck.pop()]
    computer_hand = [deck.pop(), deck.pop(), deck.pop(), deck.pop(), deck.pop()]
    pot = 0
    player_in = True
    computer_in = True
    player_selected = [False] * 5
    game_phase = 'bet1'
    message = 'First betting round: B=Bet, C=Call, R=Raise, F=Fold'
    last_computer_action = ''
    action_history = []
    game_over = False
    # Alternate dealer
    dealer_is_player = not dealer_is_player
    # Ante
    for p in players:
        if p['chips'] >= ANTE_AMOUNT:
            p['chips'] -= ANTE_AMOUNT
            pot += ANTE_AMOUNT
    # Sync chips
    player_chips = players[0]['chips']
    computer_chips = players[1]['chips']

new_hand()

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
    rank_values.sort()
    is_straight = False
    straight_high = None
    if len(rank_values) == 5:
        # Ace-low straight (A-2-3-4-5)
        if rank_values == [0, 1, 2, 3, 12]:
            is_straight = True
            straight_high = 3  # 5 is the high card (index 3)
        elif rank_values == list(range(min(rank_values), max(rank_values) + 1)):
            is_straight = True
            straight_high = max(rank_values)
    # Ensure straight_high is always an int for tie-breakers
    if is_straight and straight_high is None:
        straight_high = 0

    # Helper to get sorted values for tie-breakers
    def sorted_ranks_by_count():
        # Sort by count (desc), then by rank (desc)
        return sorted(rank_counts.keys(), key=lambda x: (rank_counts[x], x), reverse=True)

    # Determine hand rank and relevant cards for tie-breaker
    if is_flush and is_straight:
        return ("Straight Flush", 8, [straight_high])
    elif any(count == 4 for count in rank_counts.values()):
        four = [r for r, c in rank_counts.items() if c == 4][0]
        kicker = [r for r in rank_counts if r != four][0]
        return ("Four of a Kind", 7, [four, kicker])
    elif sorted(rank_counts.values()) == [2, 3]:
        three = [r for r, c in rank_counts.items() if c == 3][0]
        pair = [r for r, c in rank_counts.items() if c == 2][0]
        return ("Full House", 6, [three, pair])
    elif is_flush:
        return ("Flush", 5, sorted(rank_values, reverse=True))
    elif is_straight:
        return ("Straight", 4, [straight_high])
    elif any(count == 3 for count in rank_counts.values()):
        three = [r for r, c in rank_counts.items() if c == 3][0]
        kickers = sorted([r for r in rank_counts if r != three], reverse=True)
        return ("Three of a Kind", 3, [three] + kickers)
    elif sorted(rank_counts.values()) == [1, 2, 2]:
        pairs = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
        kicker = [r for r, c in rank_counts.items() if c == 1][0]
        return ("Two Pair", 2, pairs + [kicker])
    elif any(count == 2 for count in rank_counts.values()):
        pair = [r for r, c in rank_counts.items() if c == 2][0]
        kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
        return ("One Pair", 1, [pair] + kickers)
    else:
        return ("High Card", 0, sorted(rank_values, reverse=True))

# Determine the winner with tie-breaker logic
def determine_winner(player_hand, computer_hand):
    player_rank, player_score, player_tiebreak = get_hand_rank(player_hand)
    computer_rank, computer_score, computer_tiebreak = get_hand_rank(computer_hand)

    if player_score > computer_score:
        return f"Player wins! {player_rank} vs {computer_rank}"
    elif player_score < computer_score:
        return f"Computer wins! {computer_rank} vs {player_rank}"
    else:
        # Tie-breaker: compare tiebreaker lists, filter out None
        player_tiebreak = [v for v in player_tiebreak if v is not None]
        computer_tiebreak = [v for v in computer_tiebreak if v is not None]
        for p, c in zip(player_tiebreak, computer_tiebreak):
            if p > c:
                return f"Player wins by high card! {player_rank} vs {computer_rank}"
            elif p < c:
                return f"Computer wins by high card! {computer_rank} vs {player_rank}"
        return f"It's a tie! Both have {player_rank}"

# Simple computer AI for betting (random for now)
def computer_bet():
    if not computer_in:
        return 'fold', 0
    # Evaluate hand strength
    rank_name, rank_score, _ = get_hand_rank(computer_hand)
    # Strong hands: raise big
    if rank_score >= 4:  # Straight or better
        amount = min(MAX_BET, max(MIN_BET, computer_chips))
        return 'raise', amount
    # Medium hands: call or raise medium
    elif rank_score >= 2:  # Two pair or three of a kind
        import random
        if random.random() < 0.4:
            amount = min(60, max(MIN_BET, computer_chips, MIN_BET))
            amount = min(amount, MAX_BET)
            return 'raise', amount
        else:
            amount = min(30, max(MIN_BET, computer_chips, MIN_BET))
            amount = min(amount, MAX_BET)
            return 'call', amount
    # One pair: mostly call, sometimes fold
    elif rank_score == 1:
        import random
        if random.random() < 0.8:
            amount = min(20, max(MIN_BET, computer_chips, MIN_BET))
            amount = min(amount, MAX_BET)
            return 'call', amount
        else:
            return 'fold', 0
    # High card: mostly fold, sometimes call small
    else:
        import random
        if random.random() < 0.7:
            return 'fold', 0
        else:
            amount = min(10, max(MIN_BET, computer_chips, MIN_BET))
            amount = min(amount, MAX_BET)
            return 'call', amount

# Helper to get rank name from index
rank_names = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

def describe_hand(hand):
    rank_counts = {}
    suit_counts = {}
    rank_values = []
    for card in hand:
        suit, rank = card
        rank_idx = ranks.index(rank)
        rank_values.append(rank_idx)
        rank_counts[rank_idx] = rank_counts.get(rank_idx, 0) + 1
        suit_counts[suit] = suit_counts.get(suit, 0) + 1
    is_flush = any(count == 5 for count in suit_counts.values())
    rank_values.sort()
    is_straight = False
    straight_high = None
    if len(rank_values) == 5:
        if rank_values == [0, 1, 2, 3, 12]:
            is_straight = True
            straight_high = 3
        elif rank_values == list(range(min(rank_values), max(rank_values) + 1)):
            is_straight = True
            straight_high = max(rank_values)
    if is_flush and is_straight:
        flush_suit = [suit for suit, count in suit_counts.items() if count == 5][0]
        return f'Straight Flush: {rank_names[min(rank_values)]} to {rank_names[max(rank_values)]} of {flush_suit.capitalize()}'
    elif 4 in rank_counts.values():
        four = [r for r, c in rank_counts.items() if c == 4][0]
        return f'Four of a Kind: {rank_names[four]}s'
    elif sorted(rank_counts.values()) == [2, 3]:
        three = [r for r, c in rank_counts.items() if c == 3][0]
        pair = [r for r, c in rank_counts.items() if c == 2][0]
        return f'Full House: {rank_names[three]}s over {rank_names[pair]}s'
    elif is_flush:
        flush_suit = [suit for suit, count in suit_counts.items() if count == 5][0]
        return f'Flush: {flush_suit.capitalize()}'
    elif is_straight:
        return f'Straight: {rank_names[min(rank_values)]} to {rank_names[max(rank_values)]}'
    elif 3 in rank_counts.values():
        three = [r for r, c in rank_counts.items() if c == 3][0]
        return f'Three of a Kind: {rank_names[three]}s'
    elif list(rank_counts.values()).count(2) == 2:
        pairs = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
        return f'Two Pair: {rank_names[pairs[0]]}s and {rank_names[pairs[1]]}s'
    elif 2 in rank_counts.values():
        pair = [r for r, c in rank_counts.items() if c == 2][0]
        return f'Pair of {rank_names[pair]}s'
    else:
        high = max(rank_values)
        return f'High Card: {rank_names[high]}'

# Define fonts for use in the drawing section
sel_font = pygame.font.SysFont(None, 12)
phase_font = pygame.font.SysFont(None, 18)
font = pygame.font.SysFont(None, 16)
status_font = pygame.font.SysFont(None, 12)
hist_font = pygame.font.SysFont(None, 14)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                show_help = not show_help
                continue
            if show_help:
                continue
            if event.key == pygame.K_s:
                show_stats = not show_stats
                continue
            if show_stats:
                continue
            # Set bet amount with number keys
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                key_map = {
                    pygame.K_1: 10, pygame.K_2: 20, pygame.K_3: 30, pygame.K_4: 40, pygame.K_5: 50,
                    pygame.K_6: 60, pygame.K_7: 70, pygame.K_8: 80, pygame.K_9: 90, pygame.K_0: 100
                }
                amt = key_map[event.key]
                if amt < MIN_BET:
                    amt = MIN_BET
                if amt > MAX_BET:
                    amt = MAX_BET
                current_bet_amount = amt
            if game_phase == 'bet1' or game_phase == 'bet2':
                if event.key == pygame.K_b and player_in:
                    # Player bets
                    if player_chips >= current_bet_amount and MIN_BET <= current_bet_amount <= MAX_BET:
                        player_chips -= current_bet_amount
                        players[0]['chips'] = player_chips
                        pot += current_bet_amount
                        log_action(f'You bet {current_bet_amount}')
                        # Computer responds
                        ai_action, ai_amount = computer_bet()
                        if ai_action == 'fold':
                            computer_in = False
                            game_phase = 'showdown'
                            message = 'Computer folds! You win the pot.'
                            last_computer_action = 'Computer folded'
                            log_action('Computer folded')
                        elif ai_action == 'raise' and computer_chips >= ai_amount:
                            computer_chips -= ai_amount
                            players[1]['chips'] = computer_chips
                            pot += ai_amount
                            message = f'Computer raises {ai_amount}! Press C to call, F to fold.'
                            last_computer_action = f'Computer raised {ai_amount}'
                            log_action(f'Computer raised {ai_amount}')
                        else:
                            computer_chips -= ai_amount
                            players[1]['chips'] = computer_chips
                            pot += ai_amount
                            game_phase = 'draw' if game_phase == 'bet1' else 'showdown'
                            message = 'Both called. Proceed.'
                            last_computer_action = f'Computer called {ai_amount}'
                            log_action(f'Computer called {ai_amount}')
                elif event.key == pygame.K_c and player_in:
                    # Player calls
                    if player_chips >= current_bet_amount:
                        player_chips -= current_bet_amount
                        players[0]['chips'] = player_chips
                        pot += current_bet_amount
                        log_action(f'You called {current_bet_amount}')
                        game_phase = 'draw' if game_phase == 'bet1' else 'showdown'
                        message = 'Both called. Proceed.'
                        last_computer_action = f'Computer called {current_bet_amount}'
                        log_action(f'Computer called {current_bet_amount}')
                elif event.key == pygame.K_r and player_in:
                    # Player raises
                    if player_chips >= current_bet_amount:
                        player_chips -= current_bet_amount
                        players[0]['chips'] = player_chips
                        pot += current_bet_amount
                        log_action(f'You raised {current_bet_amount}')
                        # Computer responds
                        ai_action, ai_amount = computer_bet()
                        if ai_action == 'fold':
                            computer_in = False
                            game_phase = 'showdown'
                            message = 'Computer folds! You win the pot.'
                            last_computer_action = 'Computer folded'
                            log_action('Computer folded')
                        else:
                            computer_chips -= ai_amount
                            players[1]['chips'] = computer_chips
                            pot += ai_amount
                            game_phase = 'draw' if game_phase == 'bet1' else 'showdown'
                            message = f'Both raised. Proceed.'
                            last_computer_action = f'Computer raised {ai_amount}'
                            log_action(f'Computer raised {ai_amount}')
                elif event.key == pygame.K_f and player_in:
                    # Player folds
                    player_in = False
                    game_phase = 'showdown'
                    message = 'You folded! Computer wins the pot.'
                    last_computer_action = ''
                    log_action('You folded')
            elif game_phase == 'draw' and player_in:
                # 1-5 to select cards
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    idx = event.key - pygame.K_1
                    player_selected[idx] = not player_selected[idx]
                elif event.key == pygame.K_d:
                    # Discard selected and draw new
                    num_discards = sum(player_selected)
                    for i in range(5):
                        if player_selected[i]:
                            player_hand[i] = deck.pop()
                    log_action(f'You drew {num_discards} card(s)')
                    # Improved computer discarding
                    # Keep pairs, three/four of a kind, try to complete flush/straight
                    comp_ranks = [ranks.index(card[1]) for card in computer_hand]
                    comp_suits = [card[0] for card in computer_hand]
                    from collections import Counter
                    rank_counts = Counter(comp_ranks)
                    suit_counts = Counter(comp_suits)
                    # Find which cards to keep
                    keep = [False]*5
                    # Keep all cards that are part of a pair or better
                    for i, r in enumerate(comp_ranks):
                        if rank_counts[r] > 1:
                            keep[i] = True
                    # If close to flush (4 of same suit), keep those
                    for suit, count in suit_counts.items():
                        if count == 4:
                            for i, s in enumerate(comp_suits):
                                if s == suit:
                                    keep[i] = True
                    # If close to straight (4 in sequence), keep those
                    sorted_r = sorted(comp_ranks)
                    for i in range(2):
                        window = sorted_r[i:i+4]
                        if window == list(range(window[0], window[0]+4)):
                            for j, r in enumerate(comp_ranks):
                                if r in window:
                                    keep[j] = True
                    # Discard all others
                    comp_discards = 0
                    for i in range(5):
                        if not keep[i]:
                            computer_hand[i] = deck.pop()
                            comp_discards += 1
                    if comp_discards:
                        log_action(f'Computer drew {comp_discards} card(s)')
                    game_phase = 'bet2'
                    message = 'Second betting round: B=Bet, C=Call, R=Raise, F=Fold'
            elif game_phase == 'showdown':
                if event.key == pygame.K_SPACE:
                    # Award pot
                    if player_in and not computer_in:
                        player_chips += pot
                        players[0]['chips'] = player_chips
                    elif computer_in and not player_in:
                        computer_chips += pot
                        players[1]['chips'] = computer_chips
                    else:
                        # Both in, determine winner
                        winner = determine_winner(player_hand, computer_hand)
                        if winner.startswith('Player'):
                            player_chips += pot
                            players[0]['chips'] = player_chips
                        elif winner.startswith('Computer'):
                            computer_chips += pot
                            players[1]['chips'] = computer_chips
                        else:
                            # Tie
                            player_chips += pot // 2
                            players[0]['chips'] = player_chips
                            computer_chips += pot // 2
                            players[1]['chips'] = computer_chips
                    # Check for game over
                    if player_chips <= 0 or computer_chips <= 0:
                        game_over = True
                        game_phase = 'gameover'
                        if player_chips <= 0 and computer_chips <= 0:
                            message = 'Game Over! Both players are out of chips. Press SPACE to restart.'
                        elif player_chips <= 0:
                            message = 'Game Over! You are out of chips. Press SPACE to restart.'
                        else:
                            message = 'Game Over! Computer is out of chips. Press SPACE to restart.'
                    else:
                        new_hand()

    # Clear the screen
    screen.fill((0, 128, 0))  # Green background color

    # In the drawing section, before drawing cards, draw the always-visible top bar UI
    # Draw top bar background
    bar_height = 60
    bar_color = (20, 20, 60)
    pygame.draw.rect(screen, bar_color, (0, 0, WIDTH, bar_height))
    # Draw player chips (left)
    chips_font = pygame.font.SysFont(None, 32, bold=True)
    player_chips_text = chips_font.render(f'Your Chips: {player_chips}', True, (255,255,0))
    screen.blit(player_chips_text, (30, 15))
    # Draw computer chips (right)
    computer_chips_text = chips_font.render(f'Computer Chips: {computer_chips}', True, (255,255,0))
    screen.blit(computer_chips_text, (WIDTH - computer_chips_text.get_width() - 30, 15))
    # Draw pot (center)
    pot_font = pygame.font.SysFont(None, 36, bold=True)
    pot_text = pot_font.render(f'POT: {pot}', True, (0,255,255))
    screen.blit(pot_text, (WIDTH//2 - pot_text.get_width()//2, 12))
    # Draw dealer indicator at top center above the pot
    dealer_font = pygame.font.SysFont(None, 22, bold=True)
    dealer_name = 'You' if dealer_is_player else 'Computer'
    dealer_text = dealer_font.render(f'Dealer: {dealer_name}', True, (255,200,0))
    screen.blit(dealer_text, (WIDTH//2 - dealer_text.get_width()//2, 0))

    # Draw phase/action prompt as a colored bar below the top bar
    prompt_bar_height = 38
    prompt_bar_color = (40, 40, 120)
    prompt_y = bar_height
    pygame.draw.rect(screen, prompt_bar_color, (0, prompt_y, WIDTH, prompt_bar_height))
    prompt_font = pygame.font.SysFont(None, 26, bold=True)
    if game_phase == 'bet1':
        prompt_msg = f'First Betting Round: B=Bet, C=Call, R=Raise, F=Fold, 1-9/0 to set bet'
    elif game_phase == 'draw':
        prompt_msg = 'Draw: 1-5 to select cards, D=Draw'
    elif game_phase == 'bet2':
        prompt_msg = f'Second Betting Round: B=Bet, C=Call, R=Raise, F=Fold, 1-9/0 to set bet'
    else:
        prompt_msg = ''
    prompt_text = prompt_font.render(prompt_msg, True, (255,255,255))
    screen.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, prompt_y + 7))

    # Show current bet/raise amount in a colored box near the action prompt
    bet_box_w, bet_box_h = 120, 36
    bet_box_x = WIDTH//2 - bet_box_w//2
    bet_box_y = prompt_y + prompt_bar_height + 8
    bet_box_color = (0, 180, 0)
    pygame.draw.rect(screen, bet_box_color, (bet_box_x, bet_box_y, bet_box_w, bet_box_h), border_radius=10)
    bet_font = pygame.font.SysFont(None, 28, bold=True)
    bet_text = bet_font.render(f'Bet: {current_bet_amount}', True, (255,255,255))
    screen.blit(bet_text, (bet_box_x + bet_box_w//2 - bet_text.get_width()//2, bet_box_y + bet_box_h//2 - bet_text.get_height()//2))

    # Calculate vertical offset for cards to avoid UI overlap
    card_area_offset = 60 + 38 + 36 + 20  # bar_height + prompt_bar_height + bet_box_h + extra spacing
    # Draw player's hand
    for i, card in enumerate(player_hand):
        x = i * CARD_WIDTH + 50
        y = HEIGHT - CARD_HEIGHT - 50
        y = max(y, card_area_offset + 180)  # Ensure player's cards are well below computer's
        screen.blit(card_images[card], (x, y))
        # Highlight selected for discard
        if game_phase == 'draw' and player_selected[i]:
            pygame.draw.rect(screen, (255, 255, 0), (x, y, CARD_WIDTH, CARD_HEIGHT), 6)
            # Draw 'Selected' label above card
            sel_text = sel_font.render('Selected', True, (255,255,0))
            screen.blit(sel_text, (x + CARD_WIDTH//2 - sel_text.get_width()//2, y - 12))

    # Draw computer's hand (showing only the back of the cards unless showdown)
    for i, card in enumerate(computer_hand):
        x = i * CARD_WIDTH + 50
        y = card_area_offset
        if game_phase == 'showdown':
            screen.blit(card_images[card], (x, y))
        else:
            screen.blit(card_back_image, (x, y))

    # Calculate a y offset below the player's cards for UI text
    ui_y = HEIGHT - CARD_HEIGHT - 50 + CARD_HEIGHT + 20

    # Display phase and message
    phase_text = phase_font.render(f'Phase: {game_phase.upper()}', True, (0,255,255))
    screen.blit(phase_text, (50, ui_y))

    # Before drawing chips_text, define player_status and computer_status
    player_status = 'In' if player_in else 'Folded'
    computer_status = 'In' if computer_in else 'Folded'
    chips_text = font.render(f'Player Chips: {player_chips} ({player_status})   Computer Chips: {computer_chips} ({computer_status})   Pot: {pot}', True, (255,255,255))
    screen.blit(chips_text, (50, ui_y + 30))

    msg_text = font.render(message, True, (255,255,0))
    screen.blit(msg_text, (50, ui_y + 55))

    # Show last computer action
    if last_computer_action:
        last_action_text = status_font.render(last_computer_action, True, (0,255,0))
        screen.blit(last_action_text, (50, ui_y + 75))

    # Show winner at showdown and hand rank results
    if game_phase == 'showdown' and player_in and computer_in:
        # Draw a full-screen, nearly opaque overlay
        overlay_box = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay_box.fill((0, 0, 0, 235))
        screen.blit(overlay_box, (0, 0))
        # Use very large, bold font for status
        result_font = pygame.font.SysFont(None, 64, bold=True)
        chips_font = pygame.font.SysFont(None, 40, bold=True)
        winner = determine_winner(player_hand, computer_hand)
        # Show who won the hand
        if winner.startswith('Player'):
            hand_result = 'You win this hand!'
            result_color = (0,255,0)
        elif winner.startswith('Computer'):
            hand_result = 'Computer wins this hand!'
            result_color = (255,0,0)
        else:
            hand_result = 'It’s a tie!'
            result_color = (255,255,0)
        hand_result_text = result_font.render(hand_result, True, result_color)
        screen.blit(hand_result_text, (WIDTH//2 - hand_result_text.get_width()//2, HEIGHT//2 - 120))
        winner_text = chips_font.render(winner, True, (255,255,255))
        screen.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 - 60))
        # Show both hands summary with enhanced description
        p_desc = describe_hand(player_hand)
        c_desc = describe_hand(computer_hand)
        p_hand_text = chips_font.render(f'Player: {p_desc}', True, (255,255,255))
        c_hand_text = chips_font.render(f'Computer: {c_desc}', True, (255,255,255))
        screen.blit(p_hand_text, (WIDTH//2 - p_hand_text.get_width()//2, HEIGHT//2))
        screen.blit(c_hand_text, (WIDTH//2 - c_hand_text.get_width()//2, HEIGHT//2 + 50))
        # Show chip counts
        chips_text = chips_font.render(f'Your Chips: {player_chips}   Computer Chips: {computer_chips}', True, (255,255,0))
        screen.blit(chips_text, (WIDTH//2 - chips_text.get_width()//2, HEIGHT//2 + 110))

    # Draw action history log below the main UI text
    for i, action in enumerate(reversed(action_history)):
        hist_text = hist_font.render(action, True, (255,200,200))
        screen.blit(hist_text, (50, ui_y + 100 + i*18))

    # If game_over, show a big Game Over message and block other UI
    if game_over:
        # Draw a full-screen, nearly opaque overlay
        overlay_box = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay_box.fill((0, 0, 0, 245))
        screen.blit(overlay_box, (0, 0))
        # Use very large, bold font for status
        over_font = pygame.font.SysFont(None, 80, bold=True)
        chips_font = pygame.font.SysFont(None, 48, bold=True)
        # Determine winner/loser/draw
        if player_chips > computer_chips:
            result_msg = 'YOU WIN!'
            result_color = (0,255,0)
        elif player_chips < computer_chips:
            result_msg = 'YOU LOSE!'
            result_color = (255,0,0)
        else:
            result_msg = 'DRAW!'
            result_color = (255,255,0)
        over_text = over_font.render(result_msg, True, result_color)
        screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 120))
        chips_text = chips_font.render(f'Your Chips: {player_chips}   Computer Chips: {computer_chips}', True, (255,255,0))
        screen.blit(chips_text, (WIDTH//2 - chips_text.get_width()//2, HEIGHT//2 - 30))
        prompt_text = chips_font.render('Press SPACE to restart', True, (255,255,255))
        screen.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, HEIGHT//2 + 60))
        pygame.display.flip()
        continue

    # Draw help overlay if show_help is True
    if show_help:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))
        help_font = pygame.font.Font(None, 22)
        y = 40
        lines = [
            'POKER HELP',
            '',
            'Controls:',
            '  H: Show/Hide this help',
            '  1-9,0: Set bet/raise amount (10-100 chips)',
            '  B: Bet   C: Call   R: Raise   F: Fold',
            '  1-5: Select cards to discard   D: Draw',
            '  SPACE: Continue after showdown or game over',
            '',
            'Game Phases:',
            '  - First Betting Round: Place your bet, call, raise, or fold.',
            '  - Draw: Select cards to discard, then press D to draw new cards.',
            '  - Second Betting Round: Bet, call, raise, or fold again.',
            '  - Showdown: Best hand wins the pot.',
            '',
            'Hand Rankings (Best to Worst):',
            '  Straight Flush: Five cards in sequence, same suit',
            '  Four of a Kind: Four cards of same rank',
            '  Full House: Three of a kind + a pair',
            '  Flush: Five cards, same suit',
            '  Straight: Five cards in sequence',
            '  Three of a Kind: Three cards of same rank',
            '  Two Pair: Two pairs',
            '  Pair: Two cards of same rank',
            '  High Card: None of the above',
            '',
            'How to Win:',
            '  Win chips by having the best hand or making your opponent fold.',
            '  Game over when either player runs out of chips.',
            '',
            'Press H to close this help.'
        ]
        for line in lines:
            text = help_font.render(line, True, (255,255,200))
            screen.blit(text, (60, y))
            y += 26
        pygame.display.flip()
        continue

    # Draw stats overlay if show_stats is True
    if show_stats:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))
        stats_font = pygame.font.Font(None, 22)
        y = 60
        lines = [
            'POKER STATS',
            '',
            f'Total Hands Played: {stats["hands_played"]}',
            f'Player Wins: {stats["player_wins"]}',
            f'Computer Wins: {stats["computer_wins"]}',
            f'Ties: {stats["ties"]}',
            f'Biggest Pot Won: {stats["biggest_pot"]}',
            f'Longest Win Streak: {stats["longest_streak"]}',
            '',
            'Press S to close this stats screen.'
        ]
        for line in lines:
            text = stats_font.render(line, True, (200,255,255))
            screen.blit(text, (60, y))
            y += 28
        pygame.display.flip()
        continue

    pygame.display.flip()

# Quit the game
pygame.quit()
