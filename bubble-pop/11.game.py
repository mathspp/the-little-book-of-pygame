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


clock = pygame.time.Clock()
next_bubble = time.time() + 2
bubbles = []
stop_at = time.time() + 60
popped = 0
failed = 0
while time.time() < stop_at:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.dict["button"] == pygame.BUTTON_LEFT:
                click_x, click_y = event.dict["pos"]
                bubbles_on_screen = len(bubbles)
                bubbles = [
                    bubble
                    for bubble in bubbles
                    if not bubble.is_popped(click_x, click_y)
                ]
                popped += bubbles_on_screen - len(bubbles)

    bubbles_on_screen = len(bubbles)
    bubbles = [bubble for bubble in bubbles if bubble.update() > 0]
    failed += bubbles_on_screen - len(bubbles)

    now = time.time()
    if now >= next_bubble or not bubbles:
        bubbles.append(Bubble(30))
        next_bubble = now + 2

    screen.fill((0, 0, 0))
    for bubble in bubbles:
        bubble.draw(screen)
    pygame.display.flip()

# Print the final score.
score = f"popped: {popped}; missed: {failed}"
print(score)

screen.fill((0, 0, 0))
pygame.font.init()  # Initialise the font submodule.
font = pygame.font.Font(size=SIZE // 20)  # Create a font.
# Render text into a surface that Pygame can display.
score_text = font.render(score, True, (255, 255, 255))
text_width, text_height = score_text.get_size()
screen.blit(
    score_text,
    (
        SIZE // 2 - text_width // 2,
        SIZE // 2 - text_height // 2,
    ),
)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
