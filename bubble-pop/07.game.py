import pygame
import random
import time

SIZE = 400

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


next_bubble = time.time() + 2
bubbles = []  # store all bubbles here.
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # The event is a mouse click:
            if event.dict["button"] == pygame.BUTTON_LEFT:  # Left mouse button:
                click_x, click_y = event.dict["pos"]  # Click screen position.
                bubbles = [  # Drop the bubbles that have been clicked.
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
