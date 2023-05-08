import pygame
import sys

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Load sound file
hit = pygame.mixer.Sound('sound_files/hit.mp3')
end = pygame.mixer.Sound('sound_files/end.mp3')

# Set the dimensions of the window
width = 300
height = 300
size = (width, height)

# Set the colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

# Set the font
font = pygame.font.SysFont('Arial', 100)

# Set the screen
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tic Tac Toe')

# Set the board
board = [['', '', ''],
         ['', '', ''],
         ['', '', '']]

# Draw the grid
def draw_grid():
    # Vertical lines
    pygame.draw.line(screen, black, (100, 0), (100, 300), 2)
    pygame.draw.line(screen, black, (200, 0), (200, 300), 2)

    # Horizontal lines
    pygame.draw.line(screen, black, (0, 100), (300, 100), 2)
    pygame.draw.line(screen, black, (0, 200), (300, 200), 2)

# Draw the X's and O's
def draw_marks():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                text = font.render('X', True, black)
                screen.blit(text, ((col * 100) + 10, (row * 100) + 0))
            elif board[row][col] == 'O':
                text = font.render('O', True, black)
                screen.blit(text, ((col * 100) + 10, (row * 100) + 0))

# Check for a win or tie
def check_win():
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != '':
            return board[row][0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]

    # Check for a tie
    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                return None

    return 'Tie'

# Main game loop
def main():
    # Set the initial player
    player = 'X'

    # Game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Play the sound
                hit.play()

                # Get the coordinates of the mouse click
                x, y = pygame.mouse.get_pos()

                # Convert the coordinates to the board indices
                row = y // 100
                col = x // 100

                # Check if the spot is available
                if board[row][col] == '':
                    # Place the mark
                    board[row][col] = player

                    # Switch players
                    if player == 'X':
                        player = 'O'
                    else:
                        player = 'X'

        # Clear the screen
        screen.fill(white)

        # Draw the grid
        draw_grid()

        # Draw the marks
        draw_marks()

        # Check for a win or tie
        result = check_win()
        if result is not None:
            # Play the sound
            end.play()

            # Display the result
            if result == 'Tie':
                draw_message_box('Tie')
            else:
                draw_message_box(result + ' wins!')
            
            # Pause for 2 seconds
            pygame.display.update()
            pygame.time.wait(2000)

            # Reset the board
            for row in range(3):
                for col in range(3):
                    board[row][col] = ''

        # Update the screen
        pygame.display.update()

# Draw the message box
def draw_message_box(message):
    # Draw the background
    pygame.draw.rect(screen, black, (0, 0, 300, 300))

    # Draw the message
    text = font.render(message, True, white)
    screen.blit(text, (0, 0))
                
# Call the main function
main()
