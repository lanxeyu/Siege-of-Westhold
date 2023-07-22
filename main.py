import pygame, random

# ============== Sprite animation and position functions ==============
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
        self.atk_speed = 1000 # 1000
        init_animation(self, magefire_frames)
        self.rect = self.image.get_rect()
        self.rect.center = (70, 350)

    def update(self):
        super().update(magefire_frames)


class MageLight(Mage):
    def __init__(self):
        super().__init__()
        self.atk_speed = 2000 # 2000
        init_animation(self, magelight_frames)
        self.rect = self.image.get_rect()
        self.rect.center = (90, 350)

    def update(self):
        super().update(magelight_frames)


class MageWind(Mage):
    def __init__(self):
        super().__init__()
        self.atk_speed = 2500 # 2500
        init_animation(self, magewind_frames)
        self.rect = self.image.get_rect()
        self.rect.center = (90, 366)

    def update(self):
        super().update(magewind_frames)


class MageShock(Mage):
    def __init__(self):
        super().__init__()
        self.atk_speed = 1500 # 1500
        init_animation(self, mageshock_frames)
        self.rect = self.image.get_rect()
        self.rect.center = (70, 366)

    def update(self):
        super().update(mageshock_frames)


# ============== Projectile classes ==============
class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        # Add to projectiles, and all_sprite groups
        projectiles.add(self)
        all_sprites.add(self)

    def find_nearest_enemy(self, start_pos, enemies):
        # Set initial distance comparator to infinite
        min_distance = float('inf')
        nearest_enemy = None

        # Check the distance from the start position to every enemy
        for enemy in enemies:
            distance = (pygame.Vector2(enemy.rect.center) - pygame.Vector2(start_pos)).length()
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy

        return nearest_enemy.position
    
    def update(self):
        update_animation(self)
        update_position(self)

        # Check if the projectile is offscreen, if yes, kill it
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
            

class Fireball(Projectile):
    def __init__(self):
        super().__init__()
        self.speed = 10.0
        self.damage = 4

        init_animation(self, fireball_frames)
        self.rect = self.image.get_rect()
        
        self.start_pos = (70, 334)
        self.target_pos = pygame.mouse.get_pos()
        init_position(self, self.start_pos, self.target_pos)

        # Apply changes to MageFire state
        magefire.frames = magefire_atk_frames
        magefire.is_attacking = True


class Laser(Projectile):
    def __init__(self):
        super().__init__()
        self.speed = 15.0
        self.damage = 2

        init_animation(self, laser_frames)
        self.rect = self.image.get_rect()

        self.start_pos = (90, 334)
        self.target_pos = self.find_nearest_enemy(self.start_pos, enemies)
        init_position(self, self.start_pos, self.target_pos)

        # Apply changes to MageLight state
        magelight.frames = magelight_atk_frames
        magelight.is_attacking = True


class Tornado(Projectile):
    def __init__(self):
        super().__init__()
        self.speed = 4.0
        self.damage = 0.1
        self.atk_range = 500

        init_animation(self, tornado_frames)
        self.rect = self.image.get_rect()

        self.start_pos = (90, 350)
        self.target_pos = self.find_nearest_enemy(self.start_pos, enemies)
        init_position(self, self.start_pos, self.target_pos)

        # Apply changes to MageWind state
        magewind.frames = magewind_atk_frames
        magewind.is_attacking = True

    def update(self):
        update_animation(self)
        update_position(self)

        # Check if the projectile is offscreen or at a distance of 10 from start_pos, if yes, kill it
        if (self.rect.right < 0 or self.rect.left > WIDTH or
                self.rect.bottom < 0 or self.rect.top > HEIGHT or
                pygame.Vector2(self.rect.center).distance_to(self.start_pos) >= self.atk_range):
            self.kill()


class Energy(Projectile):
    def __init__(self):
        super().__init__()
        self.speed = 5.0
        self.damage = 3

        init_animation(self, energy_frames)
        self.rect = self.image.get_rect()

        self.start_pos = (90, 334)
        self.target_pos = self.find_nearest_enemy(self.start_pos, enemies)
        init_position(self, self.start_pos, self.target_pos)

        # Apply changes to MageLight state
        mageshock.frames = mageshock_atk_frames
        mageshock.is_attacking = True
# ============== HitMarker classes ==============
class HitMarker(pygame.sprite.Sprite):
    def __init__(self, collision_point, frames):
        pygame.sprite.Sprite.__init__(self)
        init_animation(self, frames)
        self.animation_delay = 100
        self.rect = self.image.get_rect(center=collision_point)

        # Add to hitmarkers and all_sprites groups
        hitmarkers.add(self)
        all_sprites.add(self)

    def update(self):
        if self.curr_frame_index < len(self.frames) - 1:
            update_animation(self)
        else:
            self.kill()


class FireballHitMarker(HitMarker):
    def __init__(self, collision_point):
        super().__init__(collision_point, fireball_hit_frames)


class LaserHitMarker(HitMarker):
    def __init__(self, collision_point):
        super().__init__(collision_point, laser_hit_frames)


class TornadoHitMarker(HitMarker):
    def __init__(self, collision_point):
        super().__init__(collision_point, tornado_hit_frames)


class EnergyHitMarker(HitMarker):
    def __init__(self, collision_point):
        super().__init__(collision_point, energy_hit_frames)
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
        self.max_health = 4
        self.curr_health = 4
        self.speed = 0.5
        
        init_animation(self, mob_frames)
        self.rect = self.image.get_rect()

        select_spawn(self)
        init_position(self, self.rect.center, tower.rect.center)


class Charger(Enemy):
    def __init__(self):
        super().__init__()
        self.max_health = 7
        self.curr_health = 7
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

        # Once the Charger gets to a certain distance to the tower, pause movement to being charging
        if (self.position - tower.rect.center).length() <= self.dash_distance:
            self.dash_timer += clock.get_time()

            # After charge time elapses, move towards the tower at a higher speed
            if self.dash_timer >= self.pause_duration:
                
                # Normalize the direction vector using a higher speed value
                self.velocity.scale_to_length(self.dash_speed)
                super().update()

        else:
            super().update()


# ============== Screen constants ==============
WIDTH = 1280
HEIGHT = 720
FPS = 60

# ============== Initialize Pygame ==============
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Siege of Westhold")
clock = pygame.time.Clock()
health_font = pygame.font.Font(None, 24)

# Load graphics assets
from load_assets import *

# ============== Create sprite groups ==============
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
mages = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
hitmarkers = pygame.sprite.Group()

# ============== Create tower object ==============
tower = Tower()

# ============== Create mage objects ==============
magefire = MageFire()
magelight = MageLight()
magewind = MageWind()
mageshock = MageShock()

# ============== GAME LOOP INITIALIZE ==============
running = True
spawn_timer = 2500
spawn_delay = 3000  # Time delay in milliseconds for spawning a new enemy
enemy_count = 1  # Initial number of enemies
fireball_timer = 0
laser_timer = 0
tornado_timer = 0
energy_timer = 0
hit_cd_duration = 50  # Hit cooldown duration in milliseconds
cooldowns = {}  # Dictionary to store cooldown timestamps for each projectile-enemy pair


# ============== GAME LOOP ==============
while running:
    # Keep the loop running at the right speed
    clock.tick(FPS)
    

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Update the animations and positions of all existing sprites
    all_sprites.update()

    # ===================== ENEMY SPAWN =====================
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

    # ===================== PROJECTILE SPAWN =====================
    if len(enemies) > 0:
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
            Laser()
            laser_timer = 0


        # Increase the tornado timer
        tornado_timer += clock.get_time()
        # Check if the fireball timer exceeds the desired interval which is equal to the fire mage's attack speed
        if tornado_timer >= magewind.atk_speed:
                    
            # Spawn a new laser
            Tornado()
            tornado_timer = 0

        # Increase the tornado timer
        energy_timer += clock.get_time()
        # Check if the fireball timer exceeds the desired interval which is equal to the fire mage's attack speed
        if energy_timer >= mageshock.atk_speed:
                    
            # Spawn a new laser
            Energy()
            energy_timer = 0


    # ===================== PROJECTILE-ENEMY COLLISION =====================
    # Detect collisions between projectile group and enemies group
    projectile_hits = pygame.sprite.groupcollide(projectiles, enemies, False, False)
    for projectile, enemy_list in projectile_hits.items():
        for enemy in enemy_list:
            # Create a unique key for the projectile-enemy pair
            pair_key = (projectile, enemy)

            # Check if the cooldown for this pair has expired
            if pair_key not in cooldowns or pygame.time.get_ticks() - cooldowns[pair_key] >= hit_cd_duration:
                # Update the cooldown timestamp for this pair
                cooldowns[pair_key] = pygame.time.get_ticks()

                # Based on the type of projectile, create the appropriate hitmarker and kill projectile if necessary
                if isinstance(projectile, Laser):
                    # Create hitmarker at collision point
                    LaserHitMarker(enemy.rect.center)
                elif isinstance(projectile, Fireball): 
                    projectile.kill()
                    FireballHitMarker(projectile.rect.center)
                elif isinstance(projectile, Tornado):
                    enemy.position = projectile.position
                    TornadoHitMarker(enemy.rect.center)
                elif isinstance(projectile, Energy):
                    projectile.kill()
                    EnergyHitMarker(projectile.rect.center)

                # Lower enemy's current health by the projectile damage
                enemy.curr_health -= projectile.damage
                if enemy.curr_health <= 0:
                    enemy.kill()


    # ===================== TOWER-ENEMY COLLISION =====================
    # Detect collisions between tower group and enemies group
    tower_hits = pygame.sprite.spritecollide(tower, enemies, True)
    if tower_hits:
        tower.curr_health -= 1
        # Game over logic
        if tower.curr_health <= 0:
            running = False
    

    #  ===================== RENDER =====================
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    
    # Display the Tower health on the screen
    health_text = health_font.render("{}".format(tower.curr_health), True, (200, 30, 30))
    screen.blit(health_text, (75, 391))
    screen.blit(heart_image, (57, 390))
    
    pygame.display.flip()

# Quit the game
pygame.quit()
