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
        elif event.type == pygame.KEYDOWN and event.dict["key"] == pygame.K_SPACE:
            fish_vy = INITIAL_VY  # Reset the y velocity when the space is pressed.

    fish_y += fish_vy
    fish_vy += GRAVITY

    if fish_y > HEIGHT:
        break

    screen.fill(BACKGROUND_COLOUR)
    pygame.draw.rect(screen, FISH_COLOUR, (180, fish_y, 60, 50))
    pygame.display.flip()
