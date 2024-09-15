import collections
import math
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

OBSTACLE_VERTICAL_GAP = 150
OBSTACLE_MIN_GAP = HEIGHT // 5
OBSTACLE_MAX_GAP = HEIGHT - OBSTACLE_MIN_GAP
OBSTACLE_INTERVAL = 3  # seconds
SCROLL_SPEED = 2

TOP_OBSTACLE = pygame.image.load("res/top_obstacle.png").convert_alpha()
BOTTOM_OBSTACLE = pygame.image.load("res/bottom_obstacle.png").convert_alpha()
OBSTACLE_WIDTH = TOP_OBSTACLE.get_width()
OBSTACLE_HEIGHT = TOP_OBSTACLE.get_height()

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


def rad2deg(x):
    return 360 * x / (2 * math.pi)  # `import math`


class PlayerFish(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self._image = pygame.image.load("res/fish.png").convert_alpha()
        self.image = self._image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vy = INITIAL_VY

    def update(self):
        self.rect.centery += self.vy
        self.vy += GRAVITY
        self.image = pygame.transform.rotate(
            self._image, rad2deg(math.atan(-self.vy / SCROLL_SPEED)) / 6
        )


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top, bottom):
        super().__init__()
        height = bottom - top
        self.image = pygame.Surface((OBSTACLE_WIDTH, height), flags=pygame.SRCALPHA)
        if top == 0:  # This obstacle hangs from the top of the screen.
            self.image.blit(
                TOP_OBSTACLE,
                (0, 0),
                (0, OBSTACLE_HEIGHT - height, OBSTACLE_WIDTH, height),
            )
        else:  # This obstacle is floored at the bottom of the screen.
            self.image.blit(
                BOTTOM_OBSTACLE,
                (0, 0),
                (0, 0, OBSTACLE_WIDTH, height),
            )
        self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.left = WIDTH

    def update(self):
        self.rect.left -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()


class ScrollingBackground:
    def __init__(self, filename, scroll_speed):
        self.surface = pygame.image.load(filename).convert_alpha()
        self.width = self.surface.get_width()
        self.right_margin = self.width
        self.scroll_speed = scroll_speed
        self.blit_height = HEIGHT - self.surface.get_height()

    def update(self):
        self.right_margin -= self.scroll_speed
        if self.right_margin < 0:
            self.right_margin += self.width

    def draw(self, screen):
        screen.blit(self.surface, (self.right_margin - self.width, self.blit_height))
        if self.right_margin < WIDTH:
            screen.blit(self.surface, (self.right_margin, self.blit_height))


pygame.mixer.init()
pygame.mixer.music.load("res/game-music-loop.mp3")
pygame.mixer.music.play(loops=-1)  # Loop indefinitely until you go crazy!

level_up_sound = pygame.mixer.Sound("res/level-up.mp3")

show_message_and_wait(screen, "Press SPACE to start")

fish = PlayerFish(FISH_X_POSITION, HEIGHT // 2)

obstacles = pygame.sprite.Group()
top_obstacles = collections.deque()
next_obstacle_at = pygame.time.get_ticks()
score = 0

sand_foreground = ScrollingBackground("res/sand_foreground.png", SCROLL_SPEED)
sand_background = ScrollingBackground("res/sand_background.png", SCROLL_SPEED // 2)

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
        level_up_sound.play()

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

    sand_background.update()
    sand_foreground.update()

    screen.fill(BACKGROUND_COLOUR)
    sand_background.draw(screen)
    obstacles.draw(screen)
    sand_foreground.draw(screen)
    screen.blit(fish.image, fish.rect)
    screen.blit(FONT.render(str(score), 1, FISH_COLOUR), (10, 10))
    pygame.display.flip()

pygame.mixer.music.load("res/game-over.mp3")
pygame.mixer.music.play()
show_message_and_wait(screen, f"Final score: {score}")
