import pygame
import sys

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

# create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Reversi')

# create the board
board = [[0 for x in range(COLUMN_COUNT)] for y in range(ROW_COUNT)]
board[3][3] = 1
board[4][4] = 1
board[3][4] = 2
board[4][3] = 2

# draw the board
def draw_board():
    for row in range(ROW_COUNT):
        for column in range(COLUMN_COUNT):
            pygame.draw.rect(screen, GREEN, (column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if board[row][column] == 1:
                pygame.draw.circle(screen, BLACK, (int(column*SQUARE_SIZE+SQUARE_SIZE/2), int(row*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
            elif board[row][column] == 2:
                pygame.draw.circle(screen, WHITE, (int(column*SQUARE_SIZE+SQUARE_SIZE/2), int(row*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)

            pygame.draw.line(screen, BLACK, [column*50, row*50], [(column+1)*50, row*50], 1)
            pygame.draw.line(screen, BLACK, [(column+1)*50, row*50], [(column+1)*50, (row+1)*50], 1)
            pygame.draw.line(screen, BLACK, [(column+1)*50, (row+1)*50], [column*50, (row+1)*50], 1)
            pygame.draw.line(screen, BLACK, [column*50, (row+1)*50], [column*50, row*50], 1)


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

# draw the score
def draw_score(score):
    font = pygame.font.Font(None, 30)
    score_text = font.render("Black: " + str(score[1]) + "  White: " + str(score[2]), True, BLACK)
    screen.blit(score_text, (10, HEIGHT-30))

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
