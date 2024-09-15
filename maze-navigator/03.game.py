from itertools import product

import pygame


CELL_SIZE = 100
SCREEN_SIZE = 700
MAZE_COLOURS = {
    0: (40, 42, 54),
    1: (248, 248, 242),
    2: (255, 121, 198),
}
PLAYER_COLOUR = (189, 147, 249)


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
    pygame.draw.circle(  # <--
        screen,
        PLAYER_COLOUR,
        (SCREEN_SIZE // 2, SCREEN_SIZE // 2),
        radius=CELL_SIZE // 3,
    )


def clamp(min_value, max_value, value):
    return max(min_value, min(max_value, value))


screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

player_pos = (0, 0)
maze_height = len(maze)
maze_width = len(maze[0])
draw_screen(player_pos, maze, screen)
pygame.display.flip()

playing = True
repaint = False
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            old_x, old_y = x, y = player_pos
            if event.dict["key"] == pygame.K_UP:
                y = clamp(0, maze_height - 1, y - 1)
            elif event.dict["key"] == pygame.K_DOWN:
                y = clamp(0, maze_height - 1, y + 1)
            elif event.dict["key"] == pygame.K_RIGHT:
                x = clamp(0, maze_width - 1, x + 1)
            elif event.dict["key"] == pygame.K_LEFT:
                x = clamp(0, maze_width - 1, x - 1)

            if maze[y][x]:
                player_pos = (x, y)
            repaint = x != old_x or y != old_y

    if repaint:
        draw_screen(player_pos, maze, screen)
        pygame.display.flip()
