import pygame
import random

# Game constants
WIDTH = 800
HEIGHT = 600
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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - ENEMY_SIZE)
        self.rect.y = random.randrange(HEIGHT - ENEMY_SIZE)
        self.speedx = random.choice([-1, 1]) * ENEMY_SPEED
        self.speedy = random.choice([-1, 1]) * ENEMY_SPEED

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Bounce the enemy off the edges of the screen
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speedx = -self.speedx
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speedy = -self.speedy

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create player object and add it to sprite groups
player = Player()
all_sprites.add(player)

score = 0

# Create initial enemy object and add it to sprite groups
# enemy = Enemy()
# all_sprites.add(enemy)
# enemies.add(enemy)

# Game loop
running = True
spawn_timer = 0
spawn_delay = 3000  # Time delay in milliseconds for spawning a new enemy

while running:
    # Keep the loop running at the right speed
    clock.tick(FPS)

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Spawn a new enemy if the timer exceeds the spawn delay
    spawn_timer += clock.get_time()  # Use clock.get_time() instead of clock.get_rawtime()
    if spawn_timer >= spawn_delay:
        new_enemy = Enemy()
        all_sprites.add(new_enemy)
        enemies.add(new_enemy)
        spawn_timer = 0

        score += 1


    # Check for collisions between player and enemies
    hits = pygame.sprite.spritecollide(player, enemies, True)
    if hits:
        # Game over logic
        running = False

    # Render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    

    # Display the score on the screen
    score_text = font.render("Score: {}".format(score), True, WHITE)
    screen.blit(score_text, (50, 50))
    
    pygame.display.flip()

# Quit the game
pygame.quit()
