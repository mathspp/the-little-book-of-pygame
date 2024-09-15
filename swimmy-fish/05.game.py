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


fish = PlayerFish(FISH_X_POSITION, HEIGHT // 2)

clock = pygame.time.Clock()
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN and event.dict["key"] == pygame.K_SPACE:
            fish.vy = INITIAL_VY  # <-- Subtle change.

    fish.update()

    if fish.rect.bottom > HEIGHT or fish.rect.top < 0:
        break

    screen.fill(BACKGROUND_COLOUR)
    screen.blit(fish.image, fish.rect)
    pygame.display.flip()
