import pygame

WIDTH = 600
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
FISH_COLOUR = (252, 152, 3)
BACKGROUND_COLOUR = (18, 60, 99)
GRAVITY = 0.3
INITIAL_VY = -5  # <--

fish_y = HEIGHT // 2
fish_vy = INITIAL_VY

clock = pygame.time.Clock()
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    fish_y += fish_vy  # The position changes based on the speed.
    fish_vy += GRAVITY  # The speed changes based on the acceleration.

    if fish_y > HEIGHT:
        break

    screen.fill(BACKGROUND_COLOUR)
    pygame.draw.rect(screen, FISH_COLOUR, (180, fish_y, 60, 50))
    pygame.display.flip()
