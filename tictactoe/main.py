
import pygame
import sys
import random

# Scoreboard (move to top so it's always in scope)
score = {'X': 0, 'O': 0, 'Tie': 0}

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Load sound file
hit = pygame.mixer.Sound('sound_files/hit.wav')
end = pygame.mixer.Sound('sound_files/end.wav')

# Set the dimensions of the window
width = 300
height = 400  # Increased height to accommodate scoreboard and buttons
size = (width, height)

# Set the colors
black = (30, 30, 30)
white = (245, 245, 245)
gray = (200, 200, 200)
blue = (70, 130, 180)
hover_color = (220, 220, 255)
gold = (255, 215, 0)

# Set the font
font = pygame.font.SysFont('Arial', 100)
title_font = pygame.font.SysFont('Arial', 20, bold=True)
instruction_font = pygame.font.SysFont('Arial', 14)
score_font = pygame.font.SysFont('Arial', 16)

# Set the screen
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tic Tac Toe')

# Set the board
def create_board():
    """Create a new empty board."""
    return [['', '', ''], ['', '', ''], ['', '', '']]

board = create_board()

# Draw game mode selection menu
def select_game_mode():
    """Display game mode selection menu in the game window and return the selected mode."""
    menu_running = True
    selected_mode = None
    while menu_running:
        screen.fill(white)
        title = title_font.render("Select Game Mode", True, black)
        screen.blit(title, (50, 40))
        btn1 = pygame.Rect(50, 100, 200, 50)
        btn2 = pygame.Rect(50, 170, 200, 50)
        pygame.draw.rect(screen, gray, btn1, border_radius=10)
        pygame.draw.rect(screen, black, btn1, 2, border_radius=10)
        pygame.draw.rect(screen, gray, btn2, border_radius=10)
        pygame.draw.rect(screen, black, btn2, 2, border_radius=10)
        txt1 = instruction_font.render("1. Human vs Human", True, black)
        txt2 = instruction_font.render("2. Human vs Computer", True, black)
        screen.blit(txt1, (btn1.x + 20, btn1.y + 15))
        screen.blit(txt2, (btn2.x + 20, btn2.y + 15))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if btn1.collidepoint(mx, my):
                    selected_mode = 1
                    menu_running = False
                elif btn2.collidepoint(mx, my):
                    selected_mode = 2
                    menu_running = False
    return selected_mode

# Computer move logic (minimax algorithm)
def computer_move():
    def minimax(board, depth, is_maximizing):
        winner = check_win()[0]
        if winner == 'O':
            return 1
        elif winner == 'X':
            return -1
        elif winner == 'Tie':
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == '':
                        board[r][c] = 'O'
                        score = minimax(board, depth + 1, False)
                        board[r][c] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == '':
                        board[r][c] = 'X'
                        score = minimax(board, depth + 1, True)
                        board[r][c] = ''
                        best_score = min(score, best_score)
            return best_score

    best_score = -float('inf')
    move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == '':
                board[r][c] = 'O'
                score = minimax(board, 0, False)
                board[r][c] = ''
                if score > best_score:
                    best_score = score
                    move = (r, c)
    if move:
        row, col = move
        board[row][col] = 'O'
        hit.play()

# Draw the grid
def draw_grid():
    """Draw a rounded Tic Tac Toe grid on the screen."""
    for i in range(1, 3):
        pygame.draw.rect(screen, gray, pygame.Rect(i*100-2, 0, 4, 300), border_radius=2)
        pygame.draw.rect(screen, gray, pygame.Rect(0, i*100-2, 300, 4), border_radius=2)

# Draw the X's and O's
def draw_marks():
    """Draw X and O marks on the board with color and centering."""
    for row in range(3):
        for col in range(3):
            rect = pygame.Rect(col*100, row*100, 100, 100)
            if board[row][col] == 'X':
                text = font.render('X', True, blue)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            elif board[row][col] == 'O':
                text = font.render('O', True, black)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def check_win():
    """Check for a win or tie. Returns (result, winning_line)"""
    # Check rows, columns, diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0], [(i, 0), (i, 1), (i, 2)]
        if board[0][i] == board[1][i] == board[2][i] != '':
            return board[0][i], [(0, i), (1, i), (2, i)]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2], [(0, 2), (1, 1), (2, 0)]
    # Check for tie
    if all(board[r][c] != '' for r in range(3) for c in range(3)):
        return 'Tie', []
    return None, []

def draw_instructions():
    """Draw game instructions at the bottom of the screen."""
    instruction_text = instruction_font.render("Click to place your mark", True, black)
    screen.blit(instruction_text, (10, 320))

def draw_scoreboard():
    """Draw the scoreboard showing wins for X, O, and ties."""
    score_text = score_font.render(f"X: {score['X']}  O: {score['O']}  Tie: {score['Tie']}", True, black)
    screen.blit(score_text, (10, 340))

def draw_restart_button():
    """Draw the restart button and return its rectangle."""
    restart_rect = pygame.Rect(200, 320, 80, 30)
    pygame.draw.rect(screen, gray, restart_rect, border_radius=5)
    pygame.draw.rect(screen, black, restart_rect, 2, border_radius=5)
    restart_text = instruction_font.render("Restart", True, black)
    text_rect = restart_text.get_rect(center=restart_rect.center)
    screen.blit(restart_text, text_rect)
    return restart_rect

def draw_message_box(message):
    """Draw a message box with the given message."""
    # Create a semi-transparent overlay
    overlay = pygame.Surface((300, 300))
    overlay.set_alpha(128)
    overlay.fill(black)
    screen.blit(overlay, (0, 0))
    
    # Draw message box
    box_rect = pygame.Rect(50, 100, 200, 100)
    pygame.draw.rect(screen, white, box_rect, border_radius=10)
    pygame.draw.rect(screen, black, box_rect, 2, border_radius=10)
    
    # Draw message text
    message_text = title_font.render(message, True, black)
    text_rect = message_text.get_rect(center=box_rect.center)
    screen.blit(message_text, text_rect)

def main():
    player = 'X'
    game_mode = select_game_mode()
    winning_line = []
    restart_rect = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check restart button click
                if restart_rect and restart_rect.collidepoint(mouse_x, mouse_y):
                    board[:] = create_board()
                    player = 'X'
                    winning_line = []
                    continue
                # Check board click (only if within board area)
                if mouse_y < 300 and game_mode == 1 or (game_mode == 2 and player == 'X'):
                    row = mouse_y // 100
                    col = mouse_x // 100
                    if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == '':
                        board[row][col] = player
                        hit.play()
                        player = 'O' if player == 'X' else 'X'

        # Computer move if needed
        if game_mode == 2 and player == 'O':
            pygame.time.wait(500)
            computer_move()
            player = 'X'

        screen.fill(white)
        
        # Draw hover effect
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 0 <= mouse_x < 300 and 0 <= mouse_y < 300:
            row = mouse_y // 100
            col = mouse_x // 100
            if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == '':
                pygame.draw.rect(screen, hover_color, (col*100, row*100, 100, 100), border_radius=15)
        
        draw_grid()
        draw_marks()
        draw_instructions()
        draw_scoreboard()
        restart_rect = draw_restart_button()
        
        result, winning_line = check_win()
        
        # Highlight winning line
        if winning_line:
            for (r, c) in winning_line:
                pygame.draw.rect(screen, gold, (c*100, r*100, 100, 100), 5, border_radius=15)
        
        if result is not None:
            end.play()
            score[result] += 1
            if result == 'Tie':
                draw_message_box('Tie!')
            else:
                draw_message_box(result + ' wins!')
            pygame.display.update()
            pygame.time.wait(2000)
            board[:] = create_board()
            player = 'X'
            winning_line = []
        
        pygame.display.update()

if __name__ == "__main__":
    main()
