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

# ============== Initialize Pygame ==============
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Siege of Westhold")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# ============== Sprite animation and position functions ==============
# Split sprite sheet into frames and return an array containing the frames
def load_frames(sprite_sheet, num_of_frames):
    frames = []  # List to store the animation frames
    # Split the sprite sheet into individual frames
    frame_width = sprite_sheet.get_width() // num_of_frames
    frame_height = sprite_sheet.get_height()
    for i in range(num_of_frames):
        frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    
    return frames

# Initialize sprite animation values
def init_animation(self, frames):
    self.frames = frames
    self.curr_frame_index = 0  # Index of the current animation frame
    self.animation_delay = 200  # Delay between frame changes in milliseconds
    self.last_frame_change = pygame.time.get_ticks()  # Time of the last frame change

    # Set the initial image as the first frame
    self.image = self.frames[0]

# Update animation according to the frames in the sprite sheet
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

# Hit marker animation when projectiles collide with enemies
def hit_animation(self):
    # Animation: check if it's time to change to the next frame
    current_time = pygame.time.get_ticks()
    if current_time - self.last_frame_change >= 100:
        # Check if the current frame index is not the last frame index
        if self.curr_frame_index < len(self.frames) - 1:
            # Update the animation frame index
            self.curr_frame_index += 1

            # Update the sprite's image with the current frame
            self.image = self.frames[self.curr_frame_index]

            # Update the time of the last frame change
            self.last_frame_change = current_time
        else:
            self.kill()

# Initialize position of the sprite
def init_position(self, start_pos, target_pos):
    # Set the initial position using the start_pos passed in
    self.position = pygame.Vector2(start_pos)
    self.rect = self.image.get_rect(center=start_pos)

    # Calculate the self.velocity vector from start_pos to target_pos
    self.velocity = pygame.Vector2(target_pos) - self.position

    # Normalize the direction vector
    self.velocity.scale_to_length(self.speed)

# Update position of the sprite
def update_position(self):
    # Move the sprite based on the velocity vector
    self.position += self.velocity

    # Update the rect's position using float values
    self.rect.centerx = self.position.x
    self.rect.centery = self.position.y

# Select the spawn point of the enemy sprite
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


# ============== Tower class ==============
class Tower(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/graphics/tower.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = 80
        self.rect.centery = 368

        self.max_health = 100
        self.curr_health = 100

        # Add to all_sprites group
        all_sprites.add(self)

# ============== Mage classes ==============
class Mage(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.is_attacking = False

        # Add to mages and all_sprites groups
        mages.add(self)
        all_sprites.add(self)

    def update(self, frames):
        if self.is_attacking:
            # Check if the current frame index is not the last frame index
            if self.curr_frame_index < len(self.frames) - 1:
                update_animation(self)
            else:
                self.is_attacking = False
                self.image = self.frames[0]  # Reset to the idle frame
                self.curr_frame_index = 0
                self.frames = frames
        else:
            update_animation(self)
        
class MageFire(Mage):
    def __init__(self):
        super().__init__()
        self.atk_speed = 1000
        init_animation(self, magefire_frames)
        self.rect = self.image.get_rect()
        self.rect.center = (70, 350)

    def update(self):
        super().update(magefire_frames)

class MageLight(Mage):
    def __init__(self):
        super().__init__()
        self.atk_speed = 1500
        init_animation(self, magelight_frames)
        self.rect = self.image.get_rect()
        self.rect.center = (90, 350)

    def update(self):
        super().update(magelight_frames)

# ============== Auto-firing Projectile classes ==============
class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))  # Adjust the size of the projectile
        self.image.fill((255, 0, 0))  # Set the color of the projectile

        self.speed = 5  # Adjust the speed of the projectile
        self.rect = self.image.get_rect()


        self.start_pos = (71, 334)
        # self.target_pos = self.find_nearest_enemy(self.start_pos, enemies)
        self.target_pos = pygame.mouse.get_pos() ######################## testing 
        init_position(self, self.start_pos, self.target_pos)

        self.direction = self.calculate_direction()

        # Apply changes to MageLight state
        magelight.frames = magelight_atk_frames
        magelight.is_attacking = True

        # Add to auto-projectiles, projectiles, and all_sprite groups
        autoprojectiles.add(self)
        projectiles.add(self)
        all_sprites.add(self)

    def find_nearest_enemy(self, start_pos, enemies):
        min_distance = float('inf')
        nearest_enemy = None

        for enemy in enemies:
            distance = (enemy.rect.center - start_pos).length()
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy

        return nearest_enemy

    def calculate_direction(self):
        direction = pygame.Vector2(self.target_pos) - pygame.Vector2(self.rect.center)
        return direction.normalize()
    
    def update(self):
        update_position(self)

class Laser(Projectile):
    pass


# ============== Player-controlled Fireball class ==============
class Fireball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10.0
        self.damage = 1

        init_animation(self, fireball_frames)
        self.rect = self.image.get_rect()
        
        self.start_pos = (71, 334)
        self.target_pos = pygame.mouse.get_pos()
        init_position(self, self.start_pos, self.target_pos)

        # Apply changes to MageFire state
        magefire.frames = magefire_atk_frames
        magefire.is_attacking = True

        # Add to fireballs, projectiles, and all_sprite groups
        fireballs.add(self)
        projectiles.add(self)
        all_sprites.add(self)

    def update(self):
        update_animation(self)
        update_position(self)

        # Check if the fireball is offscreen, if yes, kill it
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
            
class FireballHitAnim(pygame.sprite.Sprite):
        def __init__(self, fireball_collision_point):
            pygame.sprite.Sprite.__init__(self)
            init_animation(self, fireball_hit_frames)
            self.rect = self.image.get_rect()
            self.rect.center = fireball_collision_point

            # Add to hitmarkers and all_sprites groups
            hitmarkers.add(self)
            all_sprites.add(self)
        
        def update(self):
            hit_animation(self)

# ============== Enemy classes ==============
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Add to enemies and all_sprites groups
        enemies.add(self)
        all_sprites.add(self)
 
    def update(self):
        update_animation(self)
        update_position(self)

class Mob(Enemy):
    def __init__(self):
        super().__init__()
        self.max_health = 2
        self.curr_health = 2
        self.speed = 0.5
        
        init_animation(self, mob_frames)
        self.rect = self.image.get_rect()

        select_spawn(self)
        init_position(self, self.rect.center, tower.rect.center)

    def update(self):
        super().update()

class Charger(Enemy):
    def __init__(self):
        super().__init__()
        self.max_health = 3
        self.curr_health = 3
        self.speed = 1
        self.dash_distance = 400  # Distance from the tower to pause and dash
        self.dash_timer = 0
        self.pause_duration = 2500  # Pause duration in milliseconds
        self.dash_speed = 8
        
        init_animation(self, charger_frames)
        self.rect = self.image.get_rect()

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

# ============== Load graphics assets ==============
background_image = pygame.image.load("assets/graphics/background.png").convert()
magefire_sheet = pygame.image.load("assets/graphics/magefire.png").convert_alpha()
magefire_frames = load_frames(magefire_sheet, 4)
magefire_atk_sheet = pygame.image.load("assets/graphics/magefire_atk.png").convert_alpha()
magefire_atk_frames = load_frames(magefire_atk_sheet, 3)

magelight_sheet = pygame.image.load("assets/graphics/magelight.png").convert_alpha()
magelight_frames = load_frames(magelight_sheet, 4)
magelight_atk_sheet = pygame.image.load("assets/graphics/magelight_atk.png").convert_alpha()
magelight_atk_frames = load_frames(magelight_atk_sheet, 3)

fireball_sheet = pygame.image.load("assets/graphics/fireball.png").convert_alpha()
fireball_frames = load_frames(fireball_sheet, 4)
fireball_hit_sheet = pygame.image.load("assets/graphics/fireball_hit.png").convert_alpha()
fireball_hit_frames = load_frames(fireball_hit_sheet, 4)

mob_sheet = pygame.image.load("assets/graphics/mob.png").convert_alpha()
mob_frames = load_frames(mob_sheet, 6)

charger_sheet = pygame.image.load("assets/graphics/charger.png").convert_alpha()
charger_frames = load_frames(charger_sheet, 5)

# ============== Create sprite groups ==============
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
mages = pygame.sprite.Group()
fireballs = pygame.sprite.Group()
autoprojectiles = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
hitmarkers = pygame.sprite.Group()

# ============== Create tower object ==============
tower = Tower()

# ============== Create mage objects ==============
magefire = MageFire()
magelight = MageLight()

# ============== Game loop ==============
running = True
spawn_timer = 0
spawn_delay = 3000  # Time delay in milliseconds for spawning a new enemy
enemy_count = 1  # Initial number of enemies
fireball_timer = 0
laser_timer = 0

while running:
    # Keep the loop running at the right speed
    clock.tick(FPS)
    
    # print(magefire.is_attacking)

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
                new_enemy = Mob()
            elif enemy_type == 'Charger':
                new_enemy = Charger()
            spawn_timer = 0

            # Increase the number of enemies spawned over time
            enemy_count += 0.1

    # Increase the fireball timer
    fireball_timer += clock.get_time()
    # Check if the fireball timer exceeds the desired interval which is equal to the fire mage's attack speed
    if fireball_timer >= magefire.atk_speed:

        # Spawn a new fireball
        Fireball()
        fireball_timer = 0

    # Increase the laser timer
    laser_timer += clock.get_time()
    # Check if the fireball timer exceeds the desired interval which is equal to the fire mage's attack speed
    if laser_timer >= magelight.atk_speed:
      
        # Spawn a new laser
        Projectile()
        laser_timer = 0

    # Check for fireball collision with enemies
    fireball_hits = pygame.sprite.groupcollide(fireballs, enemies, True, False)
    for fireball, enemy_list in fireball_hits.items():
        for enemy in enemy_list:
            
            # Create fireball hit marker at the last position of the fireball
            FireballHitAnim(fireball.rect.center)

            # Lower enemy's current health by the projectile damage
            enemy.curr_health -= fireball.damage
            if enemy.curr_health <= 0:
                enemy.kill()

    # Check for collisions between tower and enemies
    tower_hits = pygame.sprite.spritecollide(tower, enemies, True)
    if tower_hits:
        tower.curr_health -= 1
        # Game over logic
        if tower.curr_health <= 0:
            running = False
    

    # Draw/render
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    
    # Display the Tower health on the screen
    health_text = font.render("Health: {}".format(tower.curr_health), True, WHITE)
    screen.blit(health_text, (50, 50))
    
    pygame.display.flip()

# Quit the game
pygame.quit()
