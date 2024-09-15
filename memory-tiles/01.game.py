import pygame

BACKGROUND_COLOUR = (40, 42, 54)
TILE_SIZE = 100
TILE_COLOUR = (98, 114, 164)
TILE_GAP = 10
TILES_X = 5
TILES_Y = 5


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(TILE_COLOUR)
        self.rect = self.image.get_rect()  # Get a Rect with the correct size.
        # Move the rect to the correct place:
        self.rect.x = x * (TILE_SIZE + TILE_GAP)  # x coordinate
        self.rect.y = y * (TILE_SIZE + TILE_GAP)  # y coordinate


screen = pygame.display.set_mode(
    (
        TILES_X * TILE_SIZE + (TILES_X - 1) * TILE_GAP,
        TILES_Y * TILE_SIZE + (TILES_Y - 1) * TILE_GAP,
    )
)
screen.fill(BACKGROUND_COLOUR)
tiles = pygame.sprite.Group(Tile(x, y) for x in range(TILES_X) for y in range(TILES_Y))
tiles.draw(screen)  # Draw all tiles on the screen...
pygame.display.flip()  # ... and update the screen to show them!

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
