import pygame
import random
from math import sqrt

# Game constants
WIDTH = 1920
HEIGHT = 1080
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player constants
PLAYER_SIZE = 50
PLAYER_SPEED = 5

# Enemy constants
ENEMY_SIZE = 30
ENEMY_SPEED = 3

# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survival Game by Lanxe Yu")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]  or keys[pygame.K_w]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED

        # Keep the player inside the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        # Set the initial position of the enemy offscreen
        spawn_side = random.choice(['left', 'right', 'top', 'bottom'])
        if spawn_side == 'left':
            self.rect.x = random.randint(-ENEMY_SIZE, -1)
            self.rect.y = random.randint(0, HEIGHT - ENEMY_SIZE)
        elif spawn_side == 'right':
            self.rect.x = random.randint(WIDTH, WIDTH + ENEMY_SIZE)
            self.rect.y = random.randint(0, HEIGHT - ENEMY_SIZE)
        elif spawn_side == 'top':
            self.rect.x = random.randint(0, WIDTH - ENEMY_SIZE)
            self.rect.y = random.randint(-ENEMY_SIZE, -1)
        elif spawn_side == 'bottom':
            self.rect.x = random.randint(0, WIDTH - ENEMY_SIZE)
            self.rect.y = random.randint(HEIGHT, HEIGHT + ENEMY_SIZE)

        self.speed = ENEMY_SPEED
        self.player = player

    def update(self):
        # Calculate the direction towards the player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
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

        # Move the enemy towards the player
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

# Pojectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0))  # Yellow color for the projectile
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.speed = 15

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


# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Create player object and add it to sprite groups
player = Player()
all_sprites.add(player)

# Initialize score
score = 0

# Game loop
running = True
spawn_timer = 0
spawn_delay = 3000  # Time delay in milliseconds for spawning a new enemy
enemy_count = 1  # Initial number of enemies

while running:
    # Keep the loop running at the right speed
    clock.tick(FPS)

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Get the mouse position
                mouse_pos = pygame.mouse.get_pos()

                # Create a projectile
                projectile = Projectile(player.rect.center, mouse_pos)
                all_sprites.add(projectile)
                projectiles.add(projectile)

    # Update
    all_sprites.update()

    # Spawn a new enemy if the timer exceeds the spawn delay
    spawn_timer += clock.get_time()
    if spawn_timer >= spawn_delay:
        for _ in range(round(enemy_count)):
            new_enemy = Enemy(player)
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)
        spawn_timer = 0

        # Increase the number of enemies over time
        enemy_count += 0.5

        score += 1 # Increment score by 1 for each enemy spawned


    # Check for collisions between player and enemies
    hits = pygame.sprite.spritecollide(player, enemies, True)
    if hits:
        # Game over logic
        running = False
    
    hits = pygame.sprite.groupcollide(projectiles, enemies, True, True)
    for projectile, enemy_list in hits.items():
        # Increment the score for each enemy destroyed
        score += len(enemy_list)

    # Render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    

    # Display the score on the screen
    score_text = font.render("Score: {}".format(score), True, WHITE)
    screen.blit(score_text, (50, 50))
    
    pygame.display.flip()

# Quit the game
pygame.quit()
