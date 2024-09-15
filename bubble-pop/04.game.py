import pygame
import random
import time

SIZE = 400

screen = pygame.display.set_mode((SIZE, SIZE))

next_bubble = time.time() + 2
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    now = time.time()
    if now >= next_bubble:
        x, y = random.randint(0, SIZE), random.randint(0, SIZE)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 30, 2)
        next_bubble = now + 2
    pygame.display.flip()
