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
