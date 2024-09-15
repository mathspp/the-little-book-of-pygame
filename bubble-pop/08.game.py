import pygame
import random
import time

SIZE = 400
FPS = 60

screen = pygame.display.set_mode((SIZE, SIZE))


class Bubble:
    def __init__(self, radius):
        self.x = random.randint(0, SIZE)
        self.y = random.randint(0, SIZE)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius, 2)

    def is_popped(self, click_x, click_y):
        dx = click_x - self.x
        dy = click_y - self.y
        return dx**2 + dy**2 <= self.radius**2

    def update(self):
        self.radius -= 0.1
        return self.radius


clock = pygame.time.Clock()  # Create a clock.
next_bubble = time.time() + 2
bubbles = []
while True:
    clock.tick(FPS)  # Limit the framerate at 60 frames per second.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.dict["button"] == pygame.BUTTON_LEFT:
                click_x, click_y = event.dict["pos"]
                bubbles = [
                    bubble
                    for bubble in bubbles
                    if not bubble.is_popped(click_x, click_y)
                ]

    bubbles = [bubble for bubble in bubbles if bubble.update() > 0]

    now = time.time()
    if now >= next_bubble or not bubbles:
        bubbles.append(Bubble(30))
        next_bubble = now + 2

    screen.fill((0, 0, 0))
    for bubble in bubbles:
        bubble.draw(screen)
    pygame.display.flip()
