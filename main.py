import pygame, random

# ============== Initialize Pygame ==============
from scripts.init import *

# ============== Initialize Objects ==============
from scripts.classes import *

# ============== GAME LOOP INITIALIZE ==============
running = True
start_screen = True
paused = False

spawn_timer = 2500
spawn_delay = 3000  # Time delay in milliseconds for spawning a new enemy
enemy_count = 1  # Initial number of enemies
fireball_timer = 0
laser_timer = 0
tornado_timer = 0
energy_timer = 0
hit_cd_duration = 50  # Hit cooldown duration in milliseconds
cooldowns = {}  # Dictionary to store cooldown timestamps for each projectile-enemy pair


# reset_game()

# ============== GAME LOOP ==============
while running:
    # Keep the loop running at the right speed
    clock.tick(FPS)
    

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Start screen events
            if start_screen:
                if event.key == pygame.K_SPACE:
                    start_screen = False  # Transition to the game loop when Spacebar is pressed


            # Game running events
            else:
                # Pause functionality
                if event.key == pygame.K_SPACE:
                    paused = not paused

    if not start_screen:
        # ===================== GAMEPLAY START =====================
        if not paused: 
        
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
                fireball_timer = spawn_projectile(Fireball, fireball_timer, magefire.atk_speed, (70, 334))
                laser_timer = spawn_projectile(Laser, laser_timer, magelight.atk_speed, (90, 334))
                tornado_timer = spawn_projectile(Tornado, tornado_timer, magewind.atk_speed, (90, 350))
                energy_timer = spawn_projectile(Energy, energy_timer, mageshock.atk_speed, (70, 350))


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
                            if len(enemies) > 1:
                                EnergyBounce(projectile.rect.center)
                        elif isinstance(projectile, EnergyBounce):
                            EnergyHitMarker(projectile.rect.center)
                            projectile.kill()

                        # Lower enemy's current health by the projectile damage
                        enemy.curr_health -= projectile.damage
                        

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
            health_text = health_font.render("{}".format(tower.curr_health), True, (BLACK))
            screen.blit(health_text, (75, 391))
            screen.blit(heart_image, (57, 390))

            # Display the Level and XP on the screen
            lvl_text = health_font.render("lvl {}".format(tower.lvl), True, (BLACK))
            screen.blit(lvl_text, (60, 410))
            
            xp_text = health_font.render("xp: {} / {}".format(tower.xp, tower.max_xp), True, (BLACK))
            screen.blit(xp_text, (60, 425))

            
            pygame.display.flip()
        # ===================== GAMEPLAY END =====================
           

    # Draw pause screen if paused
    if paused:
        pygame.draw.rect(screen, (0, 0, 0), (0, (HEIGHT // 2) - 15, WIDTH, 30))
        pause_text = health_font.render("PAUSED - press SPACE to unpause", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))
        pygame.display.flip()

    # Draw the start screen
    if start_screen:
        screen.fill(BLACK)
        start_text = health_font.render("Press SPACE to Start", True, WHITE)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))
        pygame.display.flip()


# Quit the game
pygame.quit()
