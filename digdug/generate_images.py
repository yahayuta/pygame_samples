
import pygame
import os

# Constants
CELL_SIZE = 40

# Colors
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

ASSETS_DIR = "C:/Users/yasun/develop/pygame_samples/digdug/assets"

def generate_images():
    pygame.init()

    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)

    # Dirt tile
    dirt_tile = pygame.Surface((CELL_SIZE, CELL_SIZE))
    dirt_tile.fill(BROWN)
    pygame.image.save(dirt_tile, os.path.join(ASSETS_DIR, "dirt.png"))

    # Player (Dig Dug)
    player_img = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(player_img, WHITE, (10, 20, 20, 20)) # Body
    pygame.draw.rect(player_img, BLUE, (10, 10, 20, 10)) # Helmet
    pygame.image.save(player_img, os.path.join(ASSETS_DIR, "player.png"))

    # Enemy (Pooka)
    pooka_img = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(pooka_img, RED, (20, 20), 15) # Body
    pygame.draw.circle(pooka_img, YELLOW, (15, 15), 5) # Eye
    pygame.image.save(pooka_img, os.path.join(ASSETS_DIR, "pooka.png"))

    # Harpoon
    harpoon_img = pygame.Surface((CELL_SIZE, 5), pygame.SRCALPHA)
    harpoon_img.fill(WHITE)
    pygame.image.save(harpoon_img, os.path.join(ASSETS_DIR, "harpoon.png"))

    # Rock
    rock_img = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(rock_img, GRAY, (5, 5, 30, 30))
    pygame.draw.line(rock_img, BLACK, (5, 5), (35, 35), 2)
    pygame.draw.line(rock_img, BLACK, (5, 35), (35, 5), 2)
    pygame.image.save(rock_img, os.path.join(ASSETS_DIR, "rock.png"))

    pygame.quit()

if __name__ == "__main__":
    generate_images()
