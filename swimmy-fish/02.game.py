import pygame

WIDTH = 600
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
FISH_COLOUR = (252, 152, 3)
BACKGROUND_COLOUR = (18, 60, 99)

fish_y = HEIGHT // 2  # The y position.
fish_vy = 2  # y (vertical) velocity.

clock = pygame.time.Clock()
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    fish_y += fish_vy  # Update the position by its velocity.

    if fish_y > HEIGHT:
        break

    screen.fill(BACKGROUND_COLOUR)
    pygame.draw.rect(screen, FISH_COLOUR, (180, fish_y, 60, 50))
    pygame.display.flip()
