import pygame
import random

# Initialize Pygame
pygame.init()


# Load background images
background = pygame.image.load("image_files/background.jpg")

# Set up the window
WIDTH = background.get_width() 
HEIGHT = background.get_height()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slot Machine")

# Load images
reel_images = [
    pygame.image.load("image_files/bell.jpg"),
    pygame.image.load("image_files/cherry.jpg"),
    pygame.image.load("image_files/plum.jpg"),
    pygame.image.load("image_files/seven.jpg"),
    pygame.image.load("image_files/wm.jpg"),
]
spin_button = pygame.image.load("image_files/spin.jpg")
spin_button_rect = spin_button.get_rect()
spin_button_rect.center = (WIDTH // 2, HEIGHT - 20)

# Define constants
REEL_WIDTH = reel_images[0].get_width()
REEL_HEIGHT = reel_images[0].get_height()
REEL_SPACING = 60
REEL_Y = HEIGHT // 2 - REEL_HEIGHT // 2

# Define the reel class
class Reel:
    def __init__(self, x):
        self.x = x
        self.y = REEL_Y
        self.images = reel_images
        self.num_images = len(self.images)
        self.speed = 0
        self.spin_time = 0
        self.spin_duration = 0
        self.stopped = False
        self.current_index = random.randint(0, self.num_images - 1)
    
    def start_spin(self):
        self.speed = random.randint(10, 20)
        self.spin_duration = random.randint(20, 40)
        self.spin_time = 0
        self.stopped = False
    
    def update(self):
        if not self.stopped:
            self.spin_time += 1
            if self.spin_time > self.spin_duration:
                self.speed = max(0, self.speed - 1)
                if self.speed == 0:
                    self.stopped = True
        self.current_index = (self.current_index + self.speed) % self.num_images
    
    def draw(self):
        image = self.images[self.current_index]
        rect = image.get_rect()
        rect.x = self.x
        rect.y = self.y
        screen.blit(image, rect)

# Create the reels
reels = [
    Reel(REEL_SPACING),
    Reel(20 + 2 * REEL_WIDTH),
    Reel(30 + 3 * REEL_WIDTH)
]

# Set up fonts
font = pygame.font.SysFont("Arial", 36)
BLACK = (0, 0, 0)

# Define the game loop
def game_loop():
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if spin_button_rect.collidepoint(pygame.mouse.get_pos()):
                    for reel in reels:
                        reel.start_spin()
        
        # Update the game state
        for reel in reels:
            reel.update()
        
        # Draw the game
        screen.blit(background, (0, 0))
        for reel in reels:
            reel.draw()
        screen.blit(spin_button, spin_button_rect)
        pygame.display.flip()

# Start the game loop
game_loop()

# Clean up Pygame
pygame.quit()
