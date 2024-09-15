import random
import time

import pygame

BACKGROUND_COLOUR = (40, 42, 54)
TILE_SIZE = 100
TILE_COLOUR = (98, 114, 164)
SECRET_TILE_COLOUR = (255, 121, 198)
TILE_GAP = 10
TILES_X = 5
TILES_Y = 5
HIDDEN_TILES = 7
PATTERN_DURATION = 3  # seconds


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(TILE_COLOUR)
        self.rect = self.image.get_rect()
        self.rect.x = x * (TILE_SIZE + TILE_GAP)
        self.rect.y = y * (TILE_SIZE + TILE_GAP)


screen = pygame.display.set_mode(
    (
        TILES_X * TILE_SIZE + (TILES_X - 1) * TILE_GAP,
        TILES_Y * TILE_SIZE + (TILES_Y - 1) * TILE_GAP,
    )
)
screen.fill(BACKGROUND_COLOUR)

all_tiles = [Tile(x, y) for x in range(TILES_X) for y in range(TILES_Y)]
random.shuffle(all_tiles)  # `import random`
secret_tiles = pygame.sprite.Group(all_tiles[:HIDDEN_TILES])  # `HIDDEN_TILES = 7`
for tile in secret_tiles:
    tile.image.fill(SECRET_TILE_COLOUR)  # `SECRET_TILE_COLOUR = (255, 121, 198)`
secret_tiles.draw(screen)  # Draw the secret tiles with the new colour.
tiles = pygame.sprite.Group(all_tiles[HIDDEN_TILES:])
tiles.draw(screen)  # Draw the non-secret tiles.
pygame.display.flip()

showing_pattern = True
show_until = time.time() + PATTERN_DURATION
playing = False
while showing_pattern or playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    if showing_pattern and time.time() > show_until:
        showing_pattern = False
        playing = True
        for tile in secret_tiles:
            tile.image.fill(TILE_COLOUR)
        secret_tiles.draw(screen)
        pygame.display.flip()
