TILE_COLOUR = pygame.color.Color(98, 114, 164)
# ...


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # ...
        self.lerp_factor = 0

    def update(self):
        if self.lerp_factor == 100:
            self.kill()
            return

        self.lerp_factor += 1
        self.image.fill(TILE_COLOUR.lerp(BACKGROUND_COLOUR, self.lerp_factor / 100))
