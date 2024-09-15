import pygame

WIDTH = 600
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

FISH_COLOUR = (252, 152, 3)
BACKGROUND_COLOUR = (18, 60, 99)

screen.fill(BACKGROUND_COLOUR)
pygame.draw.rect(screen, FISH_COLOUR, (180, HEIGHT // 2, 60, 50))
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
