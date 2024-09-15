from itertools import product
import enum
import random

import pygame


class MazeCellTypes(enum.Enum):
    WALL = 0
    PATH = 1
    TARGET = 2


CELL_SIZE = 100
SCREEN_SIZE = 700
MAZE_COLOURS = {
    MazeCellTypes.WALL: (40, 42, 54),
    MazeCellTypes.PATH: (248, 248, 242),
    MazeCellTypes.TARGET: (255, 121, 198),
}
PLAYER_COLOUR = (189, 147, 249)
BASE_WIDTH = 15
BASE_HEIGHT = 7


def generate_maze(base_width, base_height):
    width = 2 * base_width - 1
    height = 2 * base_height - 1
    # Initialize the grid with walls
    maze = [[MazeCellTypes.WALL for _ in range(width)] for _ in range(height)]

    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def carve_passages(x, y):
        # Mark the current cell as part of the maze.
        maze[y][x] = MazeCellTypes.PATH

        for dx, dy in random.sample(DIRECTIONS, 4):
            nx, ny = x + 2 * dx, y + 2 * dy
            if (
                0 <= nx < width
                and 0 <= ny < height
                and maze[ny][nx] == MazeCellTypes.WALL
            ):
                # Carve through the wall between the current cell and the neighbor
                maze[y + dy][x + dx] = MazeCellTypes.PATH
                carve_passages(nx, ny)

    carve_passages(
        2 * random.randint(0, base_width - 1), 2 * random.randint(0, base_height - 1)
    )

    maze[-1][-1] = MazeCellTypes.TARGET
    return maze


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
            colour = MAZE_COLOURS[MazeCellTypes.WALL]
        pygame.draw.rect(
            screen, colour, (dx * CELL_SIZE, dy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )
    pygame.draw.circle(
        screen,
        PLAYER_COLOUR,
        (SCREEN_SIZE // 2, SCREEN_SIZE // 2),
        radius=CELL_SIZE // 3,
    )


pygame.font.init()
font = pygame.font.Font(size=CELL_SIZE // 2)


def show_message_and_wait(screen, message):
    screen.fill(MAZE_COLOURS[MazeCellTypes.WALL])
    rendered_text = font.render(message, 1, MAZE_COLOURS[MazeCellTypes.PATH])
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


def clamp(min_value, max_value, value):
    return max(min_value, min(max_value, value))


screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
show_message_and_wait(screen, "Press SPACE to start")

maze = generate_maze(BASE_WIDTH, BASE_HEIGHT)
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

            if maze[y][x] != MazeCellTypes.WALL:
                player_pos = (x, y)
            if maze[y][x] == MazeCellTypes.TARGET:
                playing = False
            repaint = x != old_x or y != old_y

    if repaint:
        draw_screen(player_pos, maze, screen)
        pygame.display.flip()


show_message_and_wait(screen, "You won!")
