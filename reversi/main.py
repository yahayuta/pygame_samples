import pygame
import sys
import time

# initialize pygame
pygame.init()

# board parameters
ROW_COUNT = 8
COLUMN_COUNT = 8
SQUARE_SIZE = 50
WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = ROW_COUNT * SQUARE_SIZE
RADIUS = int(SQUARE_SIZE/2 - 5)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

# Modern colors and theme
BG_COLOR1 = (34, 139, 34)
BG_COLOR2 = (0, 100, 0)
GRID_COLOR = (40, 40, 40)
HIGHLIGHT_COLOR = (255, 215, 0)
PIECE_SHADOW = (60, 60, 60)
PIECE_HIGHLIGHT = (220, 220, 220)

# create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT+50))
pygame.display.set_caption('Reversi')

# create the board
board = [[0 for x in range(COLUMN_COUNT)] for y in range(ROW_COUNT)]
board[3][3] = 1
board[4][4] = 1
board[3][4] = 2
board[4][3] = 2

# draw the board
def draw_board():
    # Gradient background
    for row in range(ROW_COUNT):
        color = [BG_COLOR1[i] + (BG_COLOR2[i] - BG_COLOR1[i]) * row // ROW_COUNT for i in range(3)]
        pygame.draw.rect(screen, color, (0, row*SQUARE_SIZE, WIDTH, SQUARE_SIZE))
    
    # Draw grid
    for i in range(ROW_COUNT+1):
        pygame.draw.line(screen, GRID_COLOR, (0, i*SQUARE_SIZE), (WIDTH, i*SQUARE_SIZE), 2)
    for i in range(COLUMN_COUNT+1):
        pygame.draw.line(screen, GRID_COLOR, (i*SQUARE_SIZE, 0), (i*SQUARE_SIZE, HEIGHT), 2)
    
    # Highlight valid moves
    legal_moves = get_legal_moves(player)
    for (row, column) in legal_moves:
        pygame.draw.ellipse(screen, HIGHLIGHT_COLOR, (column*SQUARE_SIZE+10, row*SQUARE_SIZE+10, SQUARE_SIZE-20, SQUARE_SIZE-20), 3)
    
    # Draw pieces with 3D effect
    for row in range(ROW_COUNT):
        for column in range(COLUMN_COUNT):
            cx = int(column*SQUARE_SIZE+SQUARE_SIZE/2)
            cy = int(row*SQUARE_SIZE+SQUARE_SIZE/2)
            if board[row][column] == 1:
                # Black piece with shadow and highlight
                pygame.draw.circle(screen, PIECE_SHADOW, (cx+3, cy+3), RADIUS)
                pygame.draw.circle(screen, BLACK, (cx, cy), RADIUS)
                pygame.draw.circle(screen, PIECE_HIGHLIGHT, (cx-8, cy-8), RADIUS//3)
            elif board[row][column] == 2:
                # White piece with shadow and highlight
                pygame.draw.circle(screen, PIECE_SHADOW, (cx+3, cy+3), RADIUS)
                pygame.draw.circle(screen, WHITE, (cx, cy), RADIUS)
                pygame.draw.circle(screen, (200, 200, 255), (cx-8, cy-8), RADIUS//3)


# get the position of the mouse click
def get_click_position(position):
    x, y = position
    row = y // SQUARE_SIZE
    column = x // SQUARE_SIZE
    return row, column

# get the legal moves for a player
def get_legal_moves(player):
    legal_moves = []
    for row in range(ROW_COUNT):
        for column in range(COLUMN_COUNT):
            if board[row][column] == 0:
                for r, c in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                    temp_row, temp_column = row+r, column+c
                    if 0 <= temp_row < ROW_COUNT and 0 <= temp_column < COLUMN_COUNT and board[temp_row][temp_column] == 3-player:
                        while 0 <= temp_row < ROW_COUNT and 0 <= temp_column < COLUMN_COUNT and board[temp_row][temp_column] == 3-player:
                            temp_row += r
                            temp_column += c
                        if 0 <= temp_row < ROW_COUNT and 0 <= temp_column < COLUMN_COUNT and board[temp_row][temp_column] == player:
                            legal_moves.append((row, column))
                            break
    return legal_moves

# make a move
def make_move(player, row, column):
    board[row][column] = player
    for r, c in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
        temp_row, temp_column = row+r, column+c
        if 0 <= temp_row < ROW_COUNT and 0 <= temp_column < COLUMN_COUNT and board[temp_row][temp_column] == 3-player:
            while 0 <= temp_row < ROW_COUNT and 0 <= temp_column < COLUMN_COUNT and board[temp_row][temp_column] == 3-player:
                temp_row += r
                temp_column += c
            if 0 <= temp_row < ROW_COUNT and 0 <= temp_column < COLUMN_COUNT and board[temp_row][temp_column] == player:
                while temp_row != row+r or temp_column != column+c:
                    temp_row -= r
                    temp_column -= c
                    # Animate flip
                    from_color = BLACK if player == 2 else WHITE
                    to_color = BLACK if player == 1 else WHITE
                    flipping_pieces.append((temp_row, temp_column, from_color, to_color, time.time()))
                    board[temp_row][temp_column] = player

# get the score
def get_score():
    score = {1: 0, 2: 0}
    for row in range(ROW_COUNT):
        for column in range(COLUMN_COUNT):
            if board[row][column] == 1:
                score[1] += 1
            elif board[row][column] == 2:
                score[2] += 1
    return score

# Modern font
INFO_FONT = pygame.font.SysFont('Segoe UI', 28)

# Draw modern score/status panel
def draw_score(score):
    # Draw rounded rectangle panel below the board
    panel_rect = pygame.Rect(0, HEIGHT, WIDTH, 50)
    pygame.draw.rect(screen, (30, 30, 30), panel_rect, border_radius=18)
    pygame.draw.rect(screen, (80, 80, 80), panel_rect, 3, border_radius=18)
    # Draw score text
    score_text = INFO_FONT.render(f"Black: {score[1]}   White: {score[2]}", True, (255,255,255))
    screen.blit(score_text, (20, HEIGHT+10))

# Track flipping pieces for animation
flipping_pieces = []  # Each: (row, col, from_color, to_color, start_time)
FLIP_DURATION = 0.25  # seconds

# Animate flipping pieces
def animate_flips():
    now = time.time()
    still_flipping = []
    for (row, col, from_color, to_color, start_time) in flipping_pieces:
        t = (now - start_time) / FLIP_DURATION
        if t >= 1:
            continue  # Animation done
        # Interpolate color
        color = tuple(int(from_color[i] + (to_color[i] - from_color[i]) * t) for i in range(3))
        cx = int(col*SQUARE_SIZE+SQUARE_SIZE/2)
        cy = int(row*SQUARE_SIZE+SQUARE_SIZE/2)
        pygame.draw.circle(screen, PIECE_SHADOW, (cx+3, cy+3), RADIUS)
        pygame.draw.circle(screen, color, (cx, cy), RADIUS)
        pygame.draw.circle(screen, PIECE_HIGHLIGHT, (cx-8, cy-8), RADIUS//3)
        still_flipping.append((row, col, from_color, to_color, start_time))
    return still_flipping

# initialize the player
player = 1

# main game loop
while True:

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if player == 1:
                legal_moves = get_legal_moves(1)
                if legal_moves:
                    row, column = get_click_position(event.pos)
                    if (row, column) in legal_moves:
                        make_move(1, row, column)
                        player = 2
            else:
                legal_moves = get_legal_moves(2)
                if legal_moves:
                    row, column = get_click_position(event.pos)
                    if (row, column) in legal_moves:
                        make_move(2, row, column)
                        player = 1

    # draw the board and the score
    draw_board()
    # Animate flips
    flipping_pieces = animate_flips()
    score = get_score()
    draw_score(score)

    pygame.display.update()

    # check if the game is over
    if not get_legal_moves(1) and not get_legal_moves(2):
        if score[1] > score[2]:
            print("Black wins!")
        elif score[2] > score[1]:
            print("White wins!")
        else:
            print("Draw!")
        pygame.time.wait(5000)
        sys.exit()
