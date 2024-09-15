from itertools import product

import pygame


CELL_SIZE = 100
SCREEN_SIZE = 700
MAZE_COLOURS = {
    0: (40, 42, 54),
    1: (248, 248, 242),
    2: (255, 121, 198),
}


maze = [
    [1, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 0, 2],
]


def draw_screen(pos, maze, screen):
    px, py = pos
    cells = SCREEN_SIZE // CELL_SIZE
    offset = cells // 2
    maze_height = len(maze)
    maze_width = len(maze[0])
    for dx, dy in product(range(cells), repeat=2):
        x = px + (dx - offset)
        y = py + (dy - offset)
        if 0 <= x < maze_width and 0 <= y < maze_height:
            colour = MAZE_COLOURS[maze[y][x]]
        else:
            colour = MAZE_COLOURS[0]
        pygame.draw.rect(
            screen, colour, (dx * CELL_SIZE, dy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )


screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
draw_screen((0, 0), maze, screen)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
