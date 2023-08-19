import pygame, random

from scripts.init import WIDTH, HEIGHT, clock

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

# Spawn projectiles based on set timer
def spawn_projectile(projectile_class, timer, atk_speed, start_pos):
    timer += clock.get_time()
    if timer >= atk_speed:
        projectile_class(start_pos)
        timer = 0
    return timer