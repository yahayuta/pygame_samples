import pygame
import math
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Asteroids')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ship settings
SHIP_SIZE = 30
SHIP_TURN_SPEED = 5
SHIP_ACCELERATION = 0.2
SHIP_FRICTION = 0.99

# Bullet settings
BULLET_SPEED = 7
BULLET_LIFETIME = 60

# Asteroid settings
ASTEROID_MIN_SIZE = 20
ASTEROID_MAX_SIZE = 60
ASTEROID_MIN_SPEED = 1
ASTEROID_MAX_SPEED = 3
ASTEROID_SPLIT_COUNT = 2

clock = pygame.time.Clock()

# Load sounds
sound_path = os.path.join(os.path.dirname(__file__), 'sound_files')
shoot_sound = pygame.mixer.Sound(os.path.join(sound_path, 'shoot.wav'))
explosion_sound = pygame.mixer.Sound(os.path.join(sound_path, 'explosion.wav'))
hit_sound = pygame.mixer.Sound(os.path.join(sound_path, 'hit.wav'))
game_over_sound = pygame.mixer.Sound(os.path.join(sound_path, 'game_over.wav'))

# Starfield with parallax and twinkle
class Star:
    def __init__(self, width, height):
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.layer = random.choice([1, 2, 3])  # 1=slowest, 3=fastest
        self.base_brightness = random.randint(100, 200)
        self.brightness = self.base_brightness
        self.twinkle_speed = random.uniform(0.01, 0.05)
        self.twinkle_phase = random.uniform(0, 2 * math.pi)
    def update(self, dx, dy):
        # Parallax: move opposite to ship's movement, faster for higher layers
        self.x = (self.x - dx * 0.1 * self.layer) % WIDTH
        self.y = (self.y - dy * 0.1 * self.layer) % HEIGHT
        # Twinkle
        self.brightness = int(self.base_brightness + 55 * math.sin(pygame.time.get_ticks() * self.twinkle_speed + self.twinkle_phase))
        self.brightness = max(80, min(255, self.brightness))
    def draw(self, surface):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.layer)

class Ship:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.angle = 0
        self.speed_x = 0
        self.speed_y = 0
        self.alive = True
        self.thrusting = False
        self.trail = []  # List of (x, y, alpha)
        self.shield_timer = 0  # Frames left for shield

    def respawn(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed_x = 0
        self.speed_y = 0
        self.shield_timer = 90  # 1.5 seconds of shield

    def update(self, keys):
        self.thrusting = False
        if keys[pygame.K_LEFT]:
            self.angle += SHIP_TURN_SPEED
        if keys[pygame.K_RIGHT]:
            self.angle -= SHIP_TURN_SPEED
        if keys[pygame.K_UP]:
            rad = math.radians(self.angle)
            self.speed_x += SHIP_ACCELERATION * math.sin(rad)
            self.speed_y += SHIP_ACCELERATION * math.cos(rad)
            self.thrusting = True
        self.x += self.speed_x
        self.y -= self.speed_y
        self.speed_x *= SHIP_FRICTION
        self.speed_y *= SHIP_FRICTION
        # Screen wrap
        self.x %= WIDTH
        self.y %= HEIGHT
        # Add to trail
        self.trail.append((self.x, self.y, 255))
        if len(self.trail) > 30:
            self.trail.pop(0)
        # Fade trail
        self.trail = [(x, y, max(0, a - 8)) for (x, y, a) in self.trail]
        # Shield timer
        if self.shield_timer > 0:
            self.shield_timer -= 1

    def draw(self, surface, offset_x=0, offset_y=0):
        # Draw trail
        for x, y, a in self.trail:
            if a > 0:
                s = pygame.Surface((8, 8), pygame.SRCALPHA)
                pygame.draw.circle(s, (100, 200, 255, a), (4, 4), 4)
                surface.blit(s, (x - 4 + offset_x, y - 4 + offset_y))
        rad = math.radians(self.angle)
        tip = (self.x + SHIP_SIZE * math.sin(rad) + offset_x, self.y - SHIP_SIZE * math.cos(rad) + offset_y)
        left = (self.x + SHIP_SIZE * math.sin(rad + 2.5) + offset_x, self.y - SHIP_SIZE * math.cos(rad + 2.5) + offset_y)
        right = (self.x + SHIP_SIZE * math.sin(rad - 2.5) + offset_x, self.y - SHIP_SIZE * math.cos(rad - 2.5) + offset_y)
        # Draw ship glow
        glow_surf = pygame.Surface((SHIP_SIZE * 2, SHIP_SIZE * 2), pygame.SRCALPHA)
        pygame.draw.polygon(glow_surf, (100, 200, 255, 60), [
            (tip[0] - self.x - offset_x + SHIP_SIZE, tip[1] - self.y - offset_y + SHIP_SIZE),
            (left[0] - self.x - offset_x + SHIP_SIZE, left[1] - self.y - offset_y + SHIP_SIZE),
            (right[0] - self.x - offset_x + SHIP_SIZE, right[1] - self.y - offset_y + SHIP_SIZE)
        ])
        pygame.draw.circle(glow_surf, (100, 200, 255, 40), (SHIP_SIZE, SHIP_SIZE), SHIP_SIZE // 1)
        surface.blit(glow_surf, (self.x - SHIP_SIZE + offset_x, self.y - SHIP_SIZE + offset_y), special_flags=pygame.BLEND_ADD)
        # Draw ship
        pygame.draw.polygon(surface, WHITE, [tip, left, right])
        # Draw animated flame if thrusting
        if self.thrusting:
            flame_rad = math.radians(self.angle + 180)
            flame_len = (SHIP_SIZE // 1.5) * random.uniform(0.8, 1.2)
            flame_color = (
                255,
                random.randint(100, 180),
                random.randint(0, 50)
            )
            flame_tip = (self.x + flame_len * math.sin(flame_rad) + offset_x, self.y - flame_len * math.cos(flame_rad) + offset_y)
            flame_left = (self.x + (SHIP_SIZE // 3) * math.sin(rad + 2.5) + offset_x, self.y - (SHIP_SIZE // 3) * math.cos(rad + 2.5) + offset_y)
            flame_right = (self.x + (SHIP_SIZE // 3) * math.sin(rad - 2.5) + offset_x, self.y - (SHIP_SIZE // 3) * math.cos(rad - 2.5) + offset_y)
            pygame.draw.polygon(surface, flame_color, [flame_tip, flame_left, flame_right])
        # Draw shield if active
        if self.shield_timer > 0:
            shield_alpha = int(120 + 80 * math.sin(pygame.time.get_ticks() * 0.02))
            shield_color = (100, 200, 255, shield_alpha)
            s = pygame.Surface((SHIP_SIZE * 2, SHIP_SIZE * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, shield_color, (SHIP_SIZE, SHIP_SIZE), SHIP_SIZE, 3)
            surface.blit(s, (self.x - SHIP_SIZE + offset_x, self.y - SHIP_SIZE + offset_y))

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.life = BULLET_LIFETIME
        rad = math.radians(angle)
        self.speed_x = BULLET_SPEED * math.sin(rad)
        self.speed_y = BULLET_SPEED * math.cos(rad)

    def update(self):
        self.x += self.speed_x
        self.y -= self.speed_y
        self.x %= WIDTH
        self.y %= HEIGHT
        self.life -= 1

    def draw(self, surface):
        # Draw bullet glow
        glow = pygame.Surface((14, 14), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 255, 100, 80), (7, 7), 7)
        surface.blit(glow, (int(self.x) - 7, int(self.y) - 7), special_flags=pygame.BLEND_ADD)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), 3)

class Asteroid:
    def __init__(self, x=None, y=None, size=None):
        self.size = size if size else random.randint(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
        self.x = x if x is not None else random.randint(0, WIDTH)
        self.y = y if y is not None else random.randint(0, HEIGHT)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
        self.speed_x = speed * math.cos(angle)
        self.speed_y = speed * math.sin(angle)
        self.rotation = random.uniform(-0.03, 0.03)
        self.angle = random.uniform(0, 2 * math.pi)
        # Jagged polygon
        self.base_points = []
        for i in range(12):
            theta = 2 * math.pi * i / 12
            radius = self.size * random.uniform(0.7, 1.2)
            self.base_points.append((radius, theta))
        # Texture: random lines
        self.texture_lines = []
        for _ in range(5):
            a = random.uniform(0, 2 * math.pi)
            b = random.uniform(0, 2 * math.pi)
            r1 = self.size * random.uniform(0.2, 0.8)
            r2 = self.size * random.uniform(0.2, 0.8)
            self.texture_lines.append(((r1, a), (r2, b)))

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.x %= WIDTH
        self.y %= HEIGHT
        self.angle += self.rotation

    def get_points(self):
        points = []
        for radius, theta in self.base_points:
            t = theta + self.angle
            px = self.x + radius * math.cos(t)
            py = self.y + radius * math.sin(t)
            points.append((px, py))
        return points

    def draw(self, surface, offset_x=0, offset_y=0):
        points = self.get_points()
        # Draw asteroid glow
        center_x = sum([p[0] for p in points]) / len(points) + offset_x
        center_y = sum([p[1] for p in points]) / len(points) + offset_y
        glow = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
        pygame.draw.circle(glow, (180, 180, 255, 40), (self.size * 3 // 2, self.size * 3 // 2), self.size)
        surface.blit(glow, (center_x - self.size * 1.5, center_y - self.size * 1.5), special_flags=pygame.BLEND_ADD)
        shifted_points = [(x + offset_x, y + offset_y) for (x, y) in points]
        pygame.draw.polygon(surface, WHITE, shifted_points, 2)
        # Draw texture lines
        for (r1, a1), (r2, a2) in self.texture_lines:
            x1 = self.x + r1 * math.cos(a1 + self.angle) + offset_x
            y1 = self.y + r1 * math.sin(a1 + self.angle) + offset_y
            x2 = self.x + r2 * math.cos(a2 + self.angle) + offset_x
            y2 = self.y + r2 * math.sin(a2 + self.angle) + offset_y
            pygame.draw.line(surface, (120, 120, 120), (x1, y1), (x2, y2), 1)

    def collide(self, x, y, radius):
        dist = math.hypot(self.x - x, self.y - y)
        return dist < self.size + radius

class Particle:
    def __init__(self, x, y, angle, speed, color, lifetime, size):
        self.x = x
        self.y = y
        self.speed_x = speed * math.cos(angle)
        self.speed_y = speed * math.sin(angle)
        self.color = color
        self.lifetime = lifetime
        self.size = size
        self.age = 0
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1
        self.size = max(0, self.size - 0.1)
    def draw(self, surface):
        if self.lifetime > 0 and self.size > 0:
            alpha = max(0, min(255, int(255 * (self.lifetime / 30))))
            s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, alpha), (int(self.size), int(self.size)), int(self.size))
            surface.blit(s, (self.x - self.size, self.y - self.size))

class ScorePopup:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.life = 40
        self.font = pygame.font.SysFont(None, 28)
    def update(self):
        self.y -= 1
        self.life -= 1
    def draw(self, surface):
        if self.life > 0:
            text = self.font.render(f'+{self.value}', True, (255, 255, 100))
            text.set_alpha(int(255 * (self.life / 40)))
            surface.blit(text, (self.x, self.y))

def main():
    ship = Ship()
    bullets = []
    asteroids = [Asteroid() for _ in range(5)]
    particles = []
    # Create parallax starfield
    starfield = [Star(WIDTH, HEIGHT) for _ in range(100)]
    score_popups = []
    score = 0
    lives = 3
    font = pygame.font.SysFont(None, 36)
    running = True
    last_ship_x, last_ship_y = ship.x, ship.y
    shake_timer = 0
    shake_intensity = 0
    flash_timer = 0
    while running:
        # Calculate ship movement delta for parallax
        dx = ship.x - last_ship_x
        dy = ship.y - last_ship_y
        last_ship_x, last_ship_y = ship.x, ship.y
        # Draw parallax starfield
        screen.fill(BLACK)
        for star in starfield:
            star.update(dx, dy)
            star.draw(screen)
        # Screen shake offset
        offset_x = offset_y = 0
        if shake_timer > 0:
            offset_x = random.randint(-shake_intensity, shake_intensity)
            offset_y = random.randint(-shake_intensity, shake_intensity)
            shake_timer -= 1
        # Flash effect overlay
        if flash_timer > 0:
            flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, int(180 * (flash_timer / 10))))
            screen.blit(flash_surf, (0, 0))
            flash_timer -= 1
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and ship.alive:
                    bullets.append(Bullet(ship.x, ship.y, ship.angle))
                    shoot_sound.play()
        if ship.alive:
            ship.update(keys)
            # Draw ship with shake
            ship.draw(screen, offset_x, offset_y)
            # Thrust particles
            if ship.thrusting:
                for _ in range(2):
                    angle = math.radians(ship.angle + 180 + random.uniform(-15, 15))
                    speed = random.uniform(1, 3)
                    color = (255, 180, 50)
                    lifetime = random.randint(15, 25)
                    size = random.uniform(2, 4)
                    px = ship.x + (SHIP_SIZE // 1.5) * math.sin(angle)
                    py = ship.y - (SHIP_SIZE // 1.5) * math.cos(angle)
                    particles.append(Particle(px, py, angle, speed, color, lifetime, size))
        # Update and draw asteroids
        for asteroid in asteroids[:]:
            asteroid.update()
            asteroid.draw(screen, offset_x, offset_y)
            # Check collision with ship
            if ship.alive and asteroid.collide(ship.x, ship.y, SHIP_SIZE // 2):
                if ship.shield_timer == 0:
                    lives -= 1
                    hit_sound.play()
                    ship.respawn()
                    shake_timer = 10
                    shake_intensity = 8
                    flash_timer = 8
                    if lives <= 0:
                        ship.alive = False
                        game_over_sound.play()
        # Update and draw bullets
        for bullet in bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if bullet.life <= 0:
                bullets.remove(bullet)
                continue
            # Check collision with asteroids
            for asteroid in asteroids[:]:
                if asteroid.collide(bullet.x, bullet.y, 3):
                    bullets.remove(bullet)
                    score += 10
                    explosion_sound.play()
                    # Score popup
                    score_popups.append(ScorePopup(asteroid.x, asteroid.y, 10))
                    # Screen shake
                    shake_timer = 6
                    shake_intensity = 5
                    # Explosion particles
                    for _ in range(25):
                        angle = random.uniform(0, 2 * math.pi)
                        speed = random.uniform(1, 4)
                        color = (255, random.randint(100,200), 0)
                        lifetime = random.randint(20, 35)
                        size = random.uniform(2, 5)
                        particles.append(Particle(asteroid.x, asteroid.y, angle, speed, color, lifetime, size))
                    # Asteroid fragments
                    for _ in range(10):
                        angle = random.uniform(0, 2 * math.pi)
                        speed = random.uniform(2, 5)
                        color = (180, 180, 180)
                        lifetime = random.randint(10, 20)
                        size = random.uniform(1, 2)
                        particles.append(Particle(asteroid.x, asteroid.y, angle, speed, color, lifetime, size))
                    if asteroid.size > ASTEROID_MIN_SIZE * 1.5:
                        for _ in range(ASTEROID_SPLIT_COUNT):
                            asteroids.append(Asteroid(asteroid.x, asteroid.y, asteroid.size // 2))
                    asteroids.remove(asteroid)
                    break
        # Update and draw particles
        for p in particles[:]:
            p.update()
            p.draw(screen)
            if p.lifetime <= 0 or p.size <= 0:
                particles.remove(p)
        # Update and draw score popups
        for popup in score_popups[:]:
            popup.update()
            popup.draw(screen)
            if popup.life <= 0:
                score_popups.remove(popup)
        # Respawn asteroids if all destroyed
        if not asteroids:
            asteroids.extend([Asteroid() for _ in range(5)])
        # Draw score and lives
        score_text = font.render(f'Score: {score}', True, WHITE)
        lives_text = font.render(f'Lives: {lives}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        if not ship.alive:
            over_text = font.render('GAME OVER - Press R to Restart', True, WHITE)
            screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))
            if keys[pygame.K_r]:
                ship = Ship()
                bullets.clear()
                asteroids = [Asteroid() for _ in range(5)]
                score = 0
                lives = 3
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main() 