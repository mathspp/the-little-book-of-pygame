import itertools
import random
import time
import pygame

BACKGROUND_COLOUR = (40, 42, 54)
TILE_SIZE = 100
TILE_COLOUR = pygame.color.Color(98, 114, 164)
SECRET_TILE_COLOUR = (255, 121, 198)
TILE_GAP = 10
PATTERN_DURATION = 3  # seconds
FPS = 60
TEXT_COLOUR = (248, 248, 242)


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(TILE_COLOUR)
        self.rect = self.image.get_rect()
        self.rect.x = x * (TILE_SIZE + TILE_GAP)
        self.rect.y = y * (TILE_SIZE + TILE_GAP)
        self.lerp_factor = 0

    def update(self):
        if self.lerp_factor == 100:
            self.kill()
            return

        self.lerp_factor += 2
        self.image.fill(TILE_COLOUR.lerp(BACKGROUND_COLOUR, self.lerp_factor / 100))


pygame.font.init()
font = pygame.font.Font(size=TILE_SIZE // 2)


def show_message_and_wait(screen, message):
    screen.fill(BACKGROUND_COLOUR)
    rendered_text = font.render(message, 1, TEXT_COLOUR)
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
                quit()
            elif event.type == pygame.KEYDOWN and event.dict["key"] == pygame.K_SPACE:
                running = False


def play(tiles_x, tiles_y, hidden_tiles):
    screen = pygame.display.set_mode(
        (
            tiles_x * TILE_SIZE + (tiles_x - 1) * TILE_GAP,
            tiles_y * TILE_SIZE + (tiles_y - 1) * TILE_GAP,
        )
    )
    show_message_and_wait(screen, "Press SPACE to start")

    screen.fill(BACKGROUND_COLOUR)
    all_tiles = [Tile(x, y) for x in range(tiles_x) for y in range(tiles_y)]
    random.shuffle(all_tiles)
    secret_tiles = pygame.sprite.Group(all_tiles[:hidden_tiles])
    for tile in secret_tiles:
        tile.image.fill(SECRET_TILE_COLOUR)
    secret_tiles.draw(screen)
    tiles = pygame.sprite.Group(all_tiles[hidden_tiles:])
    tiles.draw(screen)
    pygame.display.flip()

    animating_tiles = pygame.sprite.RenderUpdates()
    clock = pygame.time.Clock()

    showing_pattern = True
    show_until = time.time() + PATTERN_DURATION
    playing = False
    while showing_pattern or playing:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif (
                playing
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.dict["button"] == pygame.BUTTON_LEFT
            ):
                pos = event.dict["pos"]
                for tile in secret_tiles:
                    if tile.rect.collidepoint(pos):
                        animating_tiles.add(tile)
                        secret_tiles.remove(tile)
                        break
                else:
                    for tile in tiles:
                        if tile.rect.collidepoint(pos):
                            playing = False
                            won = False  # <--

        animating_tiles.update()
        updated = animating_tiles.draw(screen)
        pygame.display.update(updated)

        if not secret_tiles:
            playing = False
            won = True  # <--

        if showing_pattern and time.time() > show_until:
            showing_pattern = False
            playing = True
            for tile in secret_tiles:
                tile.image.fill(TILE_COLOUR)
            secret_tiles.draw(screen)
            pygame.display.flip()

    return won


games_lost = 0
level = 1
for tiles_y in itertools.count(4):
    for tiles_x in range(tiles_y, tiles_y + 3):
        for hidden_tiles in range(tiles_y, tiles_x + 3):
            pygame.display.set_caption(f"Level {level}")
            while not (won := play(tiles_x, tiles_y, hidden_tiles)):
                games_lost += 1
                if games_lost == 3:
                    screen = pygame.display.set_mode((4 * TILE_SIZE, TILE_SIZE))
                    show_message_and_wait(screen, f"You lost on level {level}.")
                    exit()
            level += 1
