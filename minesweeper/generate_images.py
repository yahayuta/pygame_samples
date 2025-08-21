
import pygame

# Constants
CELL_SIZE = 30

# Colors
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

def generate_images():
    pygame.init()

    # Hidden tile
    hidden_tile = pygame.Surface((CELL_SIZE, CELL_SIZE))
    hidden_tile.fill(GRAY)
    pygame.draw.rect(hidden_tile, DARK_GRAY, (0, 0, CELL_SIZE, CELL_SIZE), 3)
    pygame.image.save(hidden_tile, "assets/hidden.png")

    # Revealed tile
    revealed_tile = pygame.Surface((CELL_SIZE, CELL_SIZE))
    revealed_tile.fill(DARK_GRAY)
    pygame.draw.rect(revealed_tile, GRAY, (0, 0, CELL_SIZE, CELL_SIZE), 3)
    pygame.image.save(revealed_tile, "assets/revealed.png")

    # Flag tile
    flag_tile = pygame.Surface((CELL_SIZE, CELL_SIZE))
    flag_tile.fill(GRAY)
    pygame.draw.rect(flag_tile, DARK_GRAY, (0, 0, CELL_SIZE, CELL_SIZE), 3)
    pygame.draw.polygon(flag_tile, RED, ((5, 5), (25, 15), (5, 25)))
    pygame.image.save(flag_tile, "assets/flag.png")

    # Mine tile
    mine_tile = pygame.Surface((CELL_SIZE, CELL_SIZE))
    mine_tile.fill(DARK_GRAY)
    pygame.draw.rect(mine_tile, GRAY, (0, 0, CELL_SIZE, CELL_SIZE), 3)
    pygame.draw.circle(mine_tile, BLACK, (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 3)
    pygame.image.save(mine_tile, "assets/mine.png")

    pygame.quit()

if __name__ == "__main__":
    generate_images()
