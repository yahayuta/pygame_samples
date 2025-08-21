
import pygame
import random

# Constants
GRID_WIDTH = 20
GRID_HEIGHT = 20
CELL_SIZE = 30
NUM_MINES = 40
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)

# Load images
HIDDEN_TILE = pygame.image.load("assets/hidden.png")
REVEALED_TILE = pygame.image.load("assets/revealed.png")
FLAG_TILE = pygame.image.load("assets/flag.png")
MINE_TILE = pygame.image.load("assets/mine.png")

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.mine_neighbors = 0

    def draw(self, screen):
        if self.is_revealed:
            screen.blit(REVEALED_TILE, (self.x * CELL_SIZE, self.y * CELL_SIZE))
            if self.is_mine:
                screen.blit(MINE_TILE, (self.x * CELL_SIZE, self.y * CELL_SIZE))
            elif self.mine_neighbors > 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(self.mine_neighbors), True, BLACK)
                screen.blit(text, (self.x * CELL_SIZE + 5, self.y * CELL_SIZE + 5))
        elif self.is_flagged:
            screen.blit(FLAG_TILE, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        else:
            screen.blit(HIDDEN_TILE, (self.x * CELL_SIZE, self.y * CELL_SIZE))

def create_grid():
    grid = [[Cell(x, y) for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
    # Place mines
    mines_placed = 0
    while mines_placed < NUM_MINES:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if not grid[x][y].is_mine:
            grid[x][y].is_mine = True
            mines_placed += 1
    # Calculate mine neighbors
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if not grid[x][y].is_mine:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= x + i < GRID_WIDTH and 0 <= y + j < GRID_HEIGHT:
                            if grid[x + i][y + j].is_mine:
                                grid[x][y].mine_neighbors += 1
    return grid

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()

    grid = create_grid()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                grid_x = x // CELL_SIZE
                grid_y = y // CELL_SIZE
                if event.button == 1:  # Left click
                    grid[grid_x][grid_y].is_revealed = True
                elif event.button == 3:  # Right click
                    grid[grid_x][grid_y].is_flagged = not grid[grid_x][grid_y].is_flagged

        screen.fill(BLACK)
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                grid[x][y].draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
