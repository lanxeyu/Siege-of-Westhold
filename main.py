import pygame
import random
from math import sqrt

# Game constants
WIDTH = 800
HEIGHT = 800
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Tower constants
TOWER_SIZE = 32

# Enemy constants
ENEMY_SIZE = 30

# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Mage Tower by Lanxe Yu")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Tower class
class Tower(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/graphics/tower.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2

# Enemy classes
class Enemy(pygame.sprite.Sprite):
    def __init__(self, tower):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.rect = self.image.get_rect()

        # Set the initial position of the enemy offscreen
        spawn_side = random.choice(['left', 'right', 'top'])
        if spawn_side == 'left':
            self.rect.x = random.randint(-ENEMY_SIZE, -1)
            self.rect.y = random.randint(0, HEIGHT - ENEMY_SIZE)
        elif spawn_side == 'right':
            self.rect.x = random.randint(WIDTH, WIDTH + ENEMY_SIZE)
            self.rect.y = random.randint(0, HEIGHT - ENEMY_SIZE)
        elif spawn_side == 'top':
            self.rect.x = random.randint(0, WIDTH - ENEMY_SIZE)
            self.rect.y = random.randint(-ENEMY_SIZE, -1)
           
        self.tower = tower

    def update(self):
        # Calculate the direction towards the tower
        dx = self.tower.rect.centerx - self.rect.centerx
        dy = self.tower.rect.centery - self.rect.centery
        distance = sqrt(dx ** 2 + dy ** 2)

        # Normalize the direction vector
        if distance != 0:
            direction_x = dx / distance
            direction_y = dy / distance
        else:
            direction_x = 0
            direction_y = 0

        # Set the velocity vector based on the direction and speed
        self.velocity_x = direction_x * self.speed
        self.velocity_y = direction_y * self.speed

        # Move the enemy towards the tower
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

class Mob(Enemy):
    def __init__(self, tower):
        super().__init__(tower)
        self.image.fill(RED)
        self.speed = 2

    def update(self):
        super().update()

class Charger(Enemy):
    def __init__(self, tower):
        super().__init__(tower)
        self.image.fill((0, 0, 255))
        self.speed = 2
        self.dash_distance = 750  # Distance from the tower to pause and dash
        self.dash_timer = 0
        self.pause_duration = 2500  # Pause duration in milliseconds
        self.dash_speed = 4

    def update(self):
        dx = self.tower.rect.centerx - self.rect.centerx
        dy = self.tower.rect.centery - self.rect.centery
        distance = sqrt(dx ** 2 + dy ** 2)

        if distance <= self.dash_distance:
            self.dash_timer += clock.get_time()
            if self.dash_timer >= self.pause_duration:
                direction_x = dx / distance
                direction_y = dy / distance
                self.rect.x += direction_x * self.dash_speed
                self.rect.y += direction_y * self.dash_speed
        else:
            super().update()

# Pojectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.speed = 30

        # Calculate the direction vector from start_pos to target_pos
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = sqrt(dx ** 2 + dy ** 2)

        # Normalize the direction vector
        if distance != 0:
            direction_x = dx / distance
            direction_y = dy / distance
        else:
            direction_x = 0
            direction_y = 0

        # Set the velocity vector based on the direction and speed
        self.velocity_x = direction_x * self.speed
        self.velocity_y = direction_y * self.speed

    def update(self):
        # Move the projectile based on the velocity vector
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

# Load the Background image
background_image = pygame.image.load("assets/graphics/background.png").convert()
# Calculate the position to center the background image
background_x = (WIDTH - background_image.get_width()) // 2
background_y = (HEIGHT - background_image.get_height()) // 2

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Create tower object and add it to sprite groups
tower = Tower()
all_sprites.add(tower)

# Initialize score
score = 0

# Game loop
running = True
spawn_timer = 0
spawn_delay = 3000  # Time delay in milliseconds for spawning a new enemy
enemy_count = 1  # Initial number of enemies
projectile_timer = 0

while running:
    # Keep the loop running at the right speed
    clock.tick(FPS)
    
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Increase the projectile timer
    projectile_timer += clock.get_time()

    # Spawn a new enemy if the timer exceeds the spawn delay
    spawn_timer += clock.get_time()
    if spawn_timer >= spawn_delay:
        for _ in range(round(enemy_count)):
            enemy_type = random.choice(['Mob', 'Mob', 'Mob', 'Charger'])

            if enemy_type == 'Mob':
                new_enemy = Mob(tower)
            elif enemy_type == 'Charger':
                new_enemy = Charger(tower)
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)
            spawn_timer = 0

            # Increase the number of enemies spawned over time
            enemy_count += 0.1

        score += 1 # Increment score by 1 for each enemy spawned

    # Check if the projectile timer exceeds the desired interval (0.5 seconds)
    if projectile_timer >= 500:
        # Spawn a new projectile
        mouse_pos = pygame.mouse.get_pos()
        projectile = Projectile(tower.rect.center, mouse_pos)
        all_sprites.add(projectile)
        projectiles.add(projectile)
        projectile_timer = 0

    # Check for collisions between tower and enemies
    hits = pygame.sprite.spritecollide(tower, enemies, True)
    if hits:
        # Game over logic
        running = False
    
    hits = pygame.sprite.groupcollide(projectiles, enemies, True, True)
    for projectile, enemy_list in hits.items():
        # Increment the score for each enemy destroyed
        score += len(enemy_list)

    # Draw/render
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    
    # Display the score on the screen
    score_text = font.render("Score: {}".format(score), True, WHITE)
    screen.blit(score_text, (50, 50))
    
    pygame.display.flip()

# Quit the game
pygame.quit()
