import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("rock-paper-scissors Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Game variables
choices = ["Rock", "Paper", "Scissors"]
player_choice = None
computer_choice = None
result = None

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Count variables
win_count = 0
lose_count = 0
draw_count = 0

def draw_counts():
    draw_text(f"Wins: {win_count}", BLACK, WIDTH // 4, 500)
    draw_text(f"Loses: {lose_count}", BLACK, WIDTH // 2, 500)
    draw_text(f"Draws: {draw_count}", BLACK, 3 * WIDTH // 4, 500)

def main():
    global player_choice, computer_choice, result, win_count, lose_count, draw_count

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player_choice = "Rock"
                elif event.key == pygame.K_p:
                    player_choice = "Paper"
                elif event.key == pygame.K_s:
                    player_choice = "Scissors"

        if player_choice:
            computer_choice = random.choice(choices)
            if player_choice == computer_choice:
                result = "It's a draw!"
                draw_count += 1
            elif (
                (player_choice == "Rock" and computer_choice == "Scissors")
                or (player_choice == "Paper" and computer_choice == "Rock")
                or (player_choice == "Scissors" and computer_choice == "Paper")
            ):
                result = "You win!"
                win_count += 1
            else:
                result = "You lose!"
                lose_count += 1

            # Display result and counts
            draw_text("rock-paper-scissors Game", BLACK, WIDTH // 2, 50)
            draw_text(f"You chose: {player_choice}", BLACK, WIDTH // 2, 150)
            draw_text(f"Computer chose: {computer_choice}", BLACK, WIDTH // 2, 200)
            draw_text(result, BLACK, WIDTH // 2, 250)
            draw_counts()
            draw_text("Press 'R' for Rock, 'P' for Paper, 'S' for Scissors", BLACK, WIDTH // 2, 400)

            # Reset variables for the next round
            player_choice = None
            computer_choice = None
            result = None

            pygame.display.flip()

if __name__ == "__main__":
    main()
