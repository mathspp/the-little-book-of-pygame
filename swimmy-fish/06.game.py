import random

import pygame

WIDTH = 600
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
FISH_COLOUR = (252, 152, 3)
BACKGROUND_COLOUR = (18, 60, 99)
GRAVITY = 0.3
INITIAL_VY = -5
FISH_X_POSITION = 180

OBSTACLE_WIDTH = 50
OBSTACLE_VERTICAL_GAP = 150
OBSTACLE_MIN_GAP = HEIGHT // 5
OBSTACLE_MAX_GAP = HEIGHT - OBSTACLE_MIN_GAP
OBSTACLE_INTERVAL = 3  # seconds
SCROLL_SPEED = 2


class PlayerFish(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 50))
        self.image.fill(FISH_COLOUR)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vy = INITIAL_VY

    def update(self):
        self.rect.centery += self.vy
        self.vy += GRAVITY


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top, bottom):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, bottom - top))
        self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.left = WIDTH  # Place the obstacle at the left edge of the screen.

    def update(self):
        self.rect.left -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()


fish = PlayerFish(FISH_X_POSITION, HEIGHT // 2)

obstacles = pygame.sprite.Group()
next_obstacle_at = pygame.time.get_ticks()

clock = pygame.time.Clock()
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN and event.dict["key"] == pygame.K_SPACE:
            fish.vy = INITIAL_VY

    fish.update()
    obstacles.update()

    if fish.rect.bottom > HEIGHT or fish.rect.top < 0:
        break

    if next_obstacle_at <= pygame.time.get_ticks():
        # Don't forget to `import random`!
        top_stop = random.randint(
            OBSTACLE_MIN_GAP, OBSTACLE_MAX_GAP - OBSTACLE_VERTICAL_GAP
        )
        bottom_start = top_stop + OBSTACLE_VERTICAL_GAP
        obstacles.add(Obstacle(0, top_stop))
        obstacles.add(Obstacle(bottom_start, HEIGHT))
        next_obstacle_at = pygame.time.get_ticks() + OBSTACLE_INTERVAL * 1000

    screen.fill(BACKGROUND_COLOUR)
    obstacles.draw(screen)
    screen.blit(fish.image, fish.rect)
    pygame.display.flip()
