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
    pygame.draw.circle(
        screen,
        PLAYER_COLOUR,
        (SCREEN_SIZE // 2, SCREEN_SIZE // 2),
        radius=CELL_SIZE // 3,
    )


pygame.font.init()
font = pygame.font.Font(size=CELL_SIZE // 2)  # <--


def show_message_and_wait(screen, message):
    screen.fill(MAZE_COLOURS[0])  # <--
    rendered_text = font.render(message, 1, MAZE_COLOURS[1])  # <--
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
            if maze[y][x] == 2:
                playing = False
            repaint = x != old_x or y != old_y

    if repaint:
        draw_screen(player_pos, maze, screen)
        pygame.display.flip()


show_message_and_wait(screen, "You won!")
