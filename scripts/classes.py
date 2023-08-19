import pygame

from scripts.functions import *
from scripts.groups import *
from scripts.load_assets import *


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
    
    def find_2nd_nearest_enemy(self, start_pos, enemies):
        # Set initial distances comparators to infinite
        min_distance = float('inf')
        second_min_distance = float('inf')
        nearest_enemy = None
        second_nearest_enemy = None

        # Check the distance from the start position to every enemy
        for enemy in enemies:
            distance = (pygame.Vector2(enemy.rect.center) - pygame.Vector2(start_pos)).length()
            
            if distance < min_distance:
                second_min_distance = min_distance
                second_nearest_enemy = nearest_enemy
                min_distance = distance
                nearest_enemy = enemy
            elif distance < second_min_distance:
                second_min_distance = distance
                second_nearest_enemy = enemy

        return second_nearest_enemy.position if second_nearest_enemy else None
    
    def update(self):
        update_animation(self)
        update_position(self)

        # Check if the projectile is offscreen, if yes, kill it
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
            

class Fireball(Projectile):
    def __init__(self, start_pos):
        super().__init__()
        self.speed = 10.0
        self.damage = 4

        init_animation(self, fireball_frames)
        self.rect = self.image.get_rect()
        
        # self.start_pos = (70, 334)
        self.start_pos = start_pos
        self.target_pos = pygame.mouse.get_pos()
        init_position(self, self.start_pos, self.target_pos)

        # Apply changes to MageFire state
        magefire.frames = magefire_atk_frames
        magefire.is_attacking = True


class Laser(Projectile):
    def __init__(self, start_pos):
        super().__init__()
        self.speed = 15.0
        self.damage = 2

        init_animation(self, laser_frames)
        self.rect = self.image.get_rect()

        # self.start_pos = (90, 334)
        self.start_pos = start_pos
        self.target_pos = self.find_nearest_enemy(self.start_pos, enemies)
        init_position(self, self.start_pos, self.target_pos)

        # Apply changes to MageLight state
        magelight.frames = magelight_atk_frames
        magelight.is_attacking = True


class Tornado(Projectile):
    def __init__(self, start_pos):
        super().__init__()
        self.speed = 4.0
        self.damage = 0.1
        self.atk_range = 500

        init_animation(self, tornado_frames)
        self.rect = self.image.get_rect()

        # self.start_pos = (90, 350)
        self.start_pos = start_pos
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
    def __init__(self, start_pos):
        super().__init__()
        self.speed = 30.0
        self.damage = 3

        init_animation(self, energy_frames)
        self.rect = self.image.get_rect()

        # self.start_pos = (70, 350)
        self.start_pos = start_pos
        self.target_pos = self.find_nearest_enemy(self.start_pos, enemies)
        init_position(self, self.start_pos, self.target_pos)

        # Apply changes to MageLight state
        mageshock.frames = mageshock_atk_frames
        mageshock.is_attacking = True

class EnergyBounce(Projectile):
    def __init__(self, start_pos):#
        
        super().__init__()
        self.speed = 30.0
        self.damage = 3

        init_animation(self, energy_frames)
        self.rect = self.image.get_rect()        

        self.start_pos = start_pos

        self.target_pos = self.find_2nd_nearest_enemy(self.start_pos, enemies)
        init_position(self, self.start_pos, self.target_pos)
   


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

        self.is_alive = True

        # Add to enemies and all_sprites groups
        enemies.add(self)
        all_sprites.add(self)
 
    def update(self):
        if self.curr_health <= 0:
            self.is_alive = False
            self.kill()

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


# ============== Create tower object ==============
tower = Tower()

# ============== Create mage objects ==============
magefire = MageFire()
magelight = MageLight()
magewind = MageWind()
mageshock = MageShock()