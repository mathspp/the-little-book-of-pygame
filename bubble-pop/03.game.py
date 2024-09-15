import pygame

SIZE = 400

screen = pygame.display.set_mode((SIZE, SIZE))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
