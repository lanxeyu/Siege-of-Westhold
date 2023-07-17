import pygame

# Load frames to memory by splitting the sprite sheet accordingly then storing each frame in the 'frames' array
def load_frames(sprite_sheet, num_of_frames):
    frames = []  # List to store the animation frames
    # Split the sprite sheet into individual frames
    frame_width = sprite_sheet.get_width() // num_of_frames
    frame_height = sprite_sheet.get_height()
    for i in range(num_of_frames):
        frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    
    return frames


# Load static images
background_image = pygame.image.load("assets/graphics/background.png").convert()
heart_image = pygame.image.load("assets/graphics/heart.png").convert_alpha()

# Define a list of image paths and frame counts
frame_info = [
    ("assets/graphics/magefire.png", 4),
    ("assets/graphics/magefire_atk.png", 3),
    ("assets/graphics/magelight.png", 4),
    ("assets/graphics/magelight_atk.png", 3),
    ("assets/graphics/fireball.png", 4),
    ("assets/graphics/fireball_hit.png", 4),
    ("assets/graphics/laser.png", 4),
    ("assets/graphics/laser_hit.png", 4),
    ("assets/graphics/mob.png", 6),
    ("assets/graphics/charger.png", 5)
]

frames = [] # List to store the frames of each image

# Iterate over each image path and frame count
for image_path, frame_count in frame_info:
    # Load the image and generate the frames using load_frames() function
    image = pygame.image.load(image_path).convert_alpha()
    frames.append(load_frames(image, frame_count))

# Assign the frames to their respective variables using tuple unpacking
magefire_frames, magefire_atk_frames, magelight_frames, magelight_atk_frames, \
fireball_frames, fireball_hit_frames, laser_frames, laser_hit_frames, \
mob_frames, charger_frames = frames
