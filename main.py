import pygame
import random

# Game constants
WIDTH = 1280
HEIGHT = 720
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Siege of Westhold")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Initialize sprite animation values
def init_animation(self, sprite_sheet, num_of_frames):
    self.frames = []  # List to store the animation frames
    self.curr_frame_index = 0  # Index of the current animation frame
    self.animation_delay = 200  # Delay between frame changes in milliseconds
    self.last_frame_change = pygame.time.get_ticks()  # Time of the last frame change

    # Split the sprite sheet into individual frames
    frame_width = sprite_sheet.get_width() // num_of_frames
    frame_height = sprite_sheet.get_height()
    for i in range(num_of_frames):
        frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        self.frames.append(frame)

    # Set the initial image as the first frame
    self.image = self.frames[0]

    self.rect = self.image.get_rect()

def update_animation(self):
    # Animation: check if it's time to change to the next frame
    current_time = pygame.time.get_ticks()
    if current_time - self.last_frame_change >= self.animation_delay:
        # Update the animation frame index
        self.curr_frame_index = (self.curr_frame_index + 1) % len(self.frames)

        # Update the sprite's image with the current frame
        self.image = self.frames[self.curr_frame_index]

        # Update the time of the last frame change
        self.last_frame_change = current_time

def init_position(self, start_pos, target_pos):
    # Set the initial position using the start_pos passed in
    self.position = pygame.Vector2(start_pos)
    self.rect = self.image.get_rect(center=start_pos)

    # Calculate the self.velocity vector from start_pos to target_pos
    self.velocity = pygame.Vector2(target_pos) - self.position

    # Normalize the direction vector
    self.velocity.scale_to_length(self.speed)

def update_position(self):
    # Move the sprite based on the velocity vector
    self.position += self.velocity

    # Update the rect's position using float values
    self.rect.centerx = self.position.x
    self.rect.centery = self.position.y

def select_spawn(self):
    # Set the initial position of the enemy offscreen
    spawn_side = random.choice(['right', 'top', 'bottom'])
    if spawn_side == 'right':
        self.rect.x = random.randint(WIDTH, WIDTH + self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
    elif spawn_side == 'top':
        self.rect.x = random.randint(WIDTH / 2, WIDTH - self.rect.width)
        self.rect.y = random.randint(-self.rect.height, -1)
    elif spawn_side == 'bottom':
        self.rect.x = random.randint(WIDTH / 2, WIDTH - self.rect.width)
        self.rect.y = random.randint(HEIGHT, HEIGHT + self.rect.height)

# Tower class
class Tower(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/graphics/tower.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = 80
        self.rect.centery = 368

        self.max_health = 100
        self.curr_health = 100

class Mage(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
class FireMage(Mage):
    def __init__(self):
        self.attack_speed = 1

# Enemy classes
class Enemy(pygame.sprite.Sprite):
    def __init__(self, tower):
        pygame.sprite.Sprite.__init__(self)
        self.tower = tower
 
    def update(self):
        update_animation(self)
        update_position(self)

class Mob(Enemy):
    def __init__(self, tower):
        super().__init__(tower)
        self.max_health = 2
        self.curr_health = 2
        self.speed = 0.5
        
        init_animation(self, mob_sheet, 6)
        select_spawn(self)
        init_position(self, self.rect.center, tower.rect.center)

    def update(self):
        super().update()

class Charger(Enemy):
    def __init__(self, tower):
        super().__init__(tower)
        self.max_health = 3
        self.curr_health = 3
        self.speed = 1
        self.dash_distance = 400  # Distance from the tower to pause and dash
        self.dash_timer = 0
        self.pause_duration = 2500  # Pause duration in milliseconds
        self.dash_speed = 8
        
        init_animation(self, charger_sheet, 5)
        select_spawn(self)
        init_position(self, self.rect.center, tower.rect.center)

    def update(self):

        update_animation(self)

        # Once the Charger gets to a certain distance to the tower, pause movement to being charging
        if (self.position - tower.rect.center).length() <= self.dash_distance:
            self.dash_timer += clock.get_time()

            # After charge time elapses, move towards the tower at a higher speed
            if self.dash_timer >= self.pause_duration:
                
                # Normalize the direction vector using a higher speed value
                self.velocity.scale_to_length(self.dash_speed)

                # Move the sprite based on the velocity vector
                self.position += self.velocity

                # Update the rect's position using float values
                self.rect.centerx = self.position.x
                self.rect.centery = self.position.y

        else:
            super().update()

# Fireball class
class Fireball(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        pygame.sprite.Sprite.__init__(self)
        
        self.speed = 10.0
        self.damage = 1

        init_animation(self, fireball_sheet, 4)
        init_position(self, start_pos, target_pos)

    def update(self):
        update_animation(self)
        update_position(self)

# Load the Background image
background_image = pygame.image.load("assets/graphics/background.png").convert()

# Load sprite sheets containing the animation frames
fireball_sheet = pygame.image.load("assets/graphics/fireball.png").convert_alpha()
mob_sheet = pygame.image.load("assets/graphics/mob.png").convert_alpha()
charger_sheet = pygame.image.load("assets/graphics/charger.png").convert_alpha()

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
fireballs = pygame.sprite.Group()

# Create tower object and add it to sprite groups
tower = Tower()
all_sprites.add(tower)

# Game loop
running = True
spawn_timer = 0
spawn_delay = 3000  # Time delay in milliseconds for spawning a new enemy
enemy_count = 1  # Initial number of enemies
fireball_timer = 0

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
    spawn_timer += clock.get_time()
    if spawn_timer >= spawn_delay:
        for _ in range(round(enemy_count)):
            enemy_type = random.choice(['Mob', 'Charger',])

            if enemy_type == 'Mob':
                new_enemy = Mob(tower)
            elif enemy_type == 'Charger':
                new_enemy = Charger(tower)
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)
            spawn_timer = 0

            # Increase the number of enemies spawned over time
            enemy_count += 0.1

    # Increase the fireball timer
    fireball_timer += clock.get_time()

    # Check if the fireball timer exceeds the desired interval (0.5 seconds)
    if fireball_timer >= 500:
        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()
        # Spawn a new fireball
        fireball = Fireball(tower.rect.center, mouse_pos)
        all_sprites.add(fireball)
        fireballs.add(fireball)
        fireball_timer = 0

    # Check for collisions between tower and enemies
    tower_hits = pygame.sprite.spritecollide(tower, enemies, True)
    if tower_hits:
        tower.curr_health -= 1
        # Game over logic
        if tower.curr_health <= 0:
            running = False
    
    # Check for fireball collision with enemies
    fireball_hits = pygame.sprite.groupcollide(fireballs, enemies, True, False)
    for fireball, enemy_list in fireball_hits.items():
        for enemy in enemy_list:
            enemy.curr_health -= fireball.damage
            if enemy.curr_health <= 0:
                enemy.kill()

    # Draw/render
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    
    # Display the Tower health on the screen
    health_text = font.render("Health: {}".format(tower.curr_health), True, WHITE)
    screen.blit(health_text, (50, 50))
    
    pygame.display.flip()

# Quit the game
pygame.quit()
