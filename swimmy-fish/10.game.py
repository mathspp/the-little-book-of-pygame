import collections
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

pygame.font.init()
FONT = pygame.font.Font(size=70)


def show_message_and_wait(screen, message):
    screen.fill(BACKGROUND_COLOUR)
    rendered_text = FONT.render(message, 1, FISH_COLOUR)
    text_width, text_height = rendered_text.get_size()
    screen_width, screen_height = screen.get_size()
    screen.blit(
        rendered_text,
        (
            screen_width // 2 - text_width // 2,
            screen_height // 2 - text_height // 2,
        ),
    )
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN and event.dict["key"] == pygame.K_SPACE:
                running = False


class PlayerFish(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("res/fish.png").convert_alpha()
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
        self.rect.left = WIDTH

    def update(self):
        self.rect.left -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()


show_message_and_wait(screen, "Press SPACE to start")

fish = PlayerFish(FISH_X_POSITION, HEIGHT // 2)

obstacles = pygame.sprite.Group()
top_obstacles = collections.deque()
next_obstacle_at = pygame.time.get_ticks()
score = 0

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

    if (
        pygame.sprite.spritecollideany(fish, obstacles)
        or fish.rect.bottom > HEIGHT
        or fish.rect.top < 0
    ):
        break

    if top_obstacles and top_obstacles[0].rect.right < fish.rect.left:
        top_obstacles.popleft()
        score += 1

    if next_obstacle_at <= pygame.time.get_ticks():
        top_stop = random.randint(
            OBSTACLE_MIN_GAP, OBSTACLE_MAX_GAP - OBSTACLE_VERTICAL_GAP
        )
        bottom_start = top_stop + OBSTACLE_VERTICAL_GAP
        top_obstacle = Obstacle(0, top_stop)
        obstacles.add(top_obstacle)
        top_obstacles.append(top_obstacle)
        obstacles.add(Obstacle(bottom_start, HEIGHT))
        next_obstacle_at = pygame.time.get_ticks() + OBSTACLE_INTERVAL * 1000

    screen.fill(BACKGROUND_COLOUR)
    obstacles.draw(screen)
    screen.blit(fish.image, fish.rect)
    screen.blit(FONT.render(str(score), 1, FISH_COLOUR), (10, 10))
    pygame.display.flip()

show_message_and_wait(screen, f"Final score: {score}")
