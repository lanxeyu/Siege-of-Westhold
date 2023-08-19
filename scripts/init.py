import pygame

# Screen constants
WIDTH = 1280
HEIGHT = 720
FPS = 60

clock = pygame.time.Clock()

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
health_font = pygame.font.Font(None, 24)
pygame.display.set_caption("Siege of Westhold")