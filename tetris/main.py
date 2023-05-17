import pygame
import os
import random

# Game settings
cell_size = 25
columns = 10
rows = 20
screen_size = (cell_size * columns, cell_size * rows)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)
tetromino_colors = [RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE]
tetromino_shapes = [
    [['.....',
      '.....',
      '..O..',
      '.OOO.',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '...O.',
      '.....'],
     ['.....',
      '.....',
      '.OOO.',
      '..O..',
      '.....'],
     ['.....',
      '.O...',
      '.OO..',
      '..O..',
      '.....']],
    [['.....',
      '.....',
      '..OO.',
      '..OO.',
      '.....']],
    [['.....',
      '.....',
      '.OO..',
      '..OO.',
      '.....'],
     ['.....',
      '...O.',
      '..OO.',
      '.O...',
      '.....']],
    [['.....',
      '.....',
      '..OO.',
      '.OO..',
      '.....'],
     ['.....',
      '.O...',
      "..OO.',
      '..O..',
      '.....']],
    [['.....',
      '.....',
      '..O..',
      '.....',
      '.....'],
     ['.....',
      '.O...',
      '.O...',
      '.O...',
      '.O...'],
     ['.....',
      '...O.',
      '...O.']],
//Add more tetromino shapes
def new_board():
    return [[0 for in range(columns)] for in range(rows)]
def new_tetromino():
    shape = random.choice(tetromino_shapes)
    color = random.choice(tetromino_colors)
    x = columns // 2 - 2
    y = 0
    rotation = 0
    return {'shape': shape, 'color': color, 'x': x, 'y': y, 'rotation': rotation}
def rotate_tetromino(tetromino, rotation=None):
    if rotation is None:
        rotation = (tetromino['rotation'] + 1) % len(tetromino['shape'])
    return {'shape': tetromino['shape'], 'color': tetromino['color'], 'x': tetromino['x'], 'y': tetromino['y'], 'rotation': rotation}
  
def get_tetromino_cells(tetromino):
    shape = tetromino['shape'][tetromino['rotation']]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell == 'O':
                yield x + tetromino['x'], y + tetromino['y']

def tetromino_fits(board, tetromino):
    for x, y in get_tetromino_cells(tetromino):
        if x < 0 or x >= columns or y < 0 or y >= rows:
            return False
        if board[y][x] != 0:
            return False
    return True

def merge_tetromino(board, tetromino):
    for x, y in get_tetromino_cells(tetromino):
        board[y][x] = tetromino['color']
    return board

def remove_full_lines(board):
    new_board = [line for line in board if not all(cell != 0 for cell in line)]
    return new_board + [[0 for _ in range(columns)] for _ in range(rows - len(new_board))]

def draw_rect(screen, x, y, color):
    pygame.draw.rect(screen, color, (x * cell_size + 1, y * cell_size + 1, cell_size - 2, cell_size - 2))

def draw_board(screen, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell != 0:
                draw_rect(screen, x, y, cell)

def draw_tetromino(screen, tetromino):
    for x, y in get_tetromino_cells(tetromino):
        draw_rect(screen, x, y, tetromino['color'])

def main():
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Pygame Tetris')
    clock = pygame.time.Clock()

    board = new_board()
    current_tetromino = new_tetromino()
    falling_time = 0
    fall_speed = 500

    running = True
    while running:
        start_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                new_tetromino = current_tetromino.copy()
                if event.key == pygame.K_LEFT:
                    new_tetromino['x'] -= 1
                elif event.key == pygame.K_RIGHT:
                    new_tetromino['x'] += 1
                elif event.key == pygame.K_DOWN:
                    new_tetromino['y'] += 1
                elif event.key == pygame.K_UP:
                    new_tetromino = rotate_tetromino(current_tetromino)
                if tetromino_fits(board, new_tetromino):
                    current_tetromino = new_tetromino

        falling_time += pygame.time.get_ticks() - start_time
        if falling_time >= fall_speed:
            falling_time = 0
            new_tetromino = current_tetromino.copy()
            new_tetromino['y'] += 1
            if tetromino_fits(board, new_tetromino):
                current_tetromino = new_tetromino
            else:
                board = merge_tetromino(board, current_tetromino)
                current_tetromino = new_tetromino()
                if not tetromino_fits(board, current_tetromino):
                    break
                board = remove_full_lines(board)

        screen.fill(BLACK)
        draw_board(screen, board)
        draw_tetromino(screen, current_tetromino)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
