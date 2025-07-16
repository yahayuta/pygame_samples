import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
GOLD = (255, 215, 0)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
PURPLE = (128, 0, 128)

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Game variables
choices = ["Rock", "Paper", "Scissors"]
player_choice = None
computer_choice = None
result = None
result_color = BLACK
showing_result = False
result_start_time = 0

# Count variables
win_count = 0
lose_count = 0
draw_count = 0

def draw_text(text, color, x, y, font_obj=font_medium):
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_button(text, color, x, y, width, height, hover_color=None):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x - width//2, y - height//2, width, height)
    
    # Check if mouse is hovering over button
    if button_rect.collidepoint(mouse_pos) and hover_color:
        pygame.draw.rect(screen, hover_color, button_rect)
    else:
        pygame.draw.rect(screen, color, button_rect)
    
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    draw_text(text, BLACK, x, y, font_small)

def draw_counts():
    # Draw background for counts
    count_bg = pygame.Rect(50, 450, WIDTH - 100, 100)
    pygame.draw.rect(screen, LIGHT_BLUE, count_bg)
    pygame.draw.rect(screen, BLACK, count_bg, 2)
    
    draw_text(f"Wins: {win_count}", GREEN, WIDTH // 4, 500)
    draw_text(f"Losses: {lose_count}", RED, WIDTH // 2, 500)
    draw_text(f"Draws: {draw_count}", GRAY, 3 * WIDTH // 4, 500)

def get_result_color(result_text):
    if "win" in result_text.lower():
        return GREEN
    elif "lose" in result_text.lower():
        return RED
    else:
        return GOLD

def main():
    global player_choice, computer_choice, result, win_count, lose_count, draw_count, result_color
    global showing_result, result_start_time

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not showing_result:
                    if event.key == pygame.K_r:
                        player_choice = "Rock"
                    elif event.key == pygame.K_p:
                        player_choice = "Paper"
                    elif event.key == pygame.K_s:
                        player_choice = "Scissors"
                else:
                    # Any key to continue to next round
                    showing_result = False
                    player_choice = None
                    computer_choice = None
                    result = None

        # Draw title
        draw_text("Rock Paper Scissors Game", BLUE, WIDTH // 2, 50, font_large)
        
        if not showing_result:
            # Draw instruction box
            instruction_bg = pygame.Rect(100, 80, WIDTH - 200, 80)
            pygame.draw.rect(screen, LIGHT_BLUE, instruction_bg)
            pygame.draw.rect(screen, BLACK, instruction_bg, 2)
            draw_text("Press 'R' for Rock, 'P' for Paper, 'S' for Scissors", BLACK, WIDTH // 2, 120)

            if player_choice:
                computer_choice = random.choice(choices)
                if player_choice == computer_choice:
                    result = "It's a Draw!"
                    draw_count += 1
                elif (
                    (player_choice == "Rock" and computer_choice == "Scissors")
                    or (player_choice == "Paper" and computer_choice == "Rock")
                    or (player_choice == "Scissors" and computer_choice == "Paper")
                ):
                    result = "You Win!"
                    win_count += 1
                else:
                    result = "You Lose!"
                    lose_count += 1
                
                result_color = get_result_color(result)
                showing_result = True
                result_start_time = time.time()

        if showing_result:
            # Draw result box
            result_bg = pygame.Rect(150, 200, WIDTH - 300, 200)
            pygame.draw.rect(screen, LIGHT_BLUE, result_bg)
            pygame.draw.rect(screen, BLACK, result_bg, 3)
            
            # Display choices and result with better formatting
            draw_text("RESULT", PURPLE, WIDTH // 2, 220, font_large)
            draw_text(f"Your choice: {player_choice}", BLACK, WIDTH // 2, 270)
            draw_text(f"Computer choice: {computer_choice}", BLACK, WIDTH // 2, 320)
            draw_text(result, result_color, WIDTH // 2, 370, font_large)
            
            # Draw play again instruction
            draw_text("Press any key to play again", BLACK, WIDTH // 2, 420)

        # Always draw counts
        draw_counts()

        pygame.display.flip()

if __name__ == "__main__":
    main()
