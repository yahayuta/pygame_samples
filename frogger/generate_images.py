from PIL import Image

# Create a green square for the player
player_image = Image.new("RGB", (20, 20), (0, 255, 0))
player_image.save("frogger/assets/player.png")

# Create a red square for the enemy
enemy_image = Image.new("RGB", (20, 20), (255, 0, 0))
enemy_image.save("frogger/assets/enemy.png")

print("Images generated successfully!")
