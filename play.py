import pygame
import random
import time
from constants import OUTLINE_COLOR, TETROMINOES, BLOCK_SIZE, Phase
from tools import draw_tetromino, handle_events, rotate_shape

WELL_DEPTH = 20
WELL_WIDTH = 10
INTERVAL = 0.5


def draw_well(screen, well):
    well_color = (173, 216, 230)  # Light blue color
    # Draw the well boundaries
    for y in range(WELL_DEPTH):
        pygame.draw.rect(
            screen,
            well_color,
            pygame.Rect(0, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
        )
        pygame.draw.rect(
            screen,
            well_color,
            pygame.Rect(
                (WELL_WIDTH + 1) * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
            ),
        )

    # Draw the well bottom
    for x in range(WELL_WIDTH + 2):
        pygame.draw.rect(
            screen,
            well_color,
            pygame.Rect(x * BLOCK_SIZE, 19 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
        )

    # Draw the well contents
    for y, row in enumerate(well):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.draw.rect(
                    screen,
                    cell,
                    pygame.Rect(
                        (x + 1) * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
                    ),
                )
                pygame.draw.rect(screen, OUTLINE_COLOR, rect, 1)  # Draw outline


def drop_tetromino(well, tetromino, position):
    while can_move(well, tetromino[0], [position[0] + 1, position[1]]):
        position[0] += 1
    return position


def can_move(well, tetromino, position):
    for y, row in enumerate(tetromino):
        for x, cell in enumerate(row):
            if cell:
                new_y = position[0] + y
                new_x = position[1] + x
                if (
                    new_y >= WELL_DEPTH - 1
                    or new_x < 0
                    or new_x >= WELL_WIDTH
                    or well[new_y][new_x]
                ):
                    return False
    return True


def find_full_rows(well):
    full_rows = [index for index, row in enumerate(well) if all(row)]
    for row_index in full_rows:
        # Paint the row in white for one update
        well[row_index] = [(255, 255, 255)] * WELL_WIDTH
    return full_rows  # Return the full rows to be cleared

def draw_score(screen, score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, ((WELL_WIDTH + 2) * BLOCK_SIZE + 10, 10))

def draw_level(screen, well, game_state):
    screen.fill((0, 0, 0))
    draw_well(screen, well)
    draw_score(screen, game_state.score)

def clear_full_rows(screen, well, full_rows, game_state):
    draw_level(screen, well, game_state)
    pygame.display.flip()
    pygame.time.wait(300)
    remove_full_rows(well, full_rows)


def remove_full_rows(well, full_rows):
    for row_index in full_rows:
        del well[row_index]
        well.insert(0, [0] * WELL_WIDTH)


def handle_controls(event, tetromino_position, current_tetromino, well):
    new_position = list(tetromino_position)
    restart_loop = False
    if event.key == pygame.K_LEFT:
        new_position[1] -= 1
    elif event.key == pygame.K_RIGHT:
        new_position[1] += 1
    elif event.key == pygame.K_SPACE:
        new_position = drop_tetromino(well, current_tetromino, tetromino_position)
    elif event.key == pygame.K_DOWN:
        new_position[0] += 1
    elif event.key == pygame.K_UP:
        rotated_tetromino = rotate_shape(current_tetromino[0])
        if can_move(well, rotated_tetromino, tetromino_position):
            current_tetromino = (rotated_tetromino, current_tetromino[1])
            restart_loop = True

    if can_move(well, current_tetromino[0], new_position):
        tetromino_position = new_position

    return {
        "new_position": new_position,
        "tetromino_position": tetromino_position,
        "current_tetromino": current_tetromino,
        "restart_loop": restart_loop,
    }

def run(screen, game_state):
    # Initialize the well
    well = [[0] * WELL_WIDTH for _ in range(WELL_DEPTH)]

    current_tetromino = random.choice(TETROMINOES)
    tetromino_position = [0, 4]  # Starting position at the top center

    last_update_time = time.time()

    while True:
        for event in pygame.event.get():
            game_phase = handle_events(event, game_state.phase)
            if game_phase != Phase.PLAY:
                return game_phase
            if event.type == pygame.KEYDOWN:
                result = handle_controls(
                    event, tetromino_position, current_tetromino, well
                )
                new_position = result["new_position"]
                tetromino_position = result["tetromino_position"]
                current_tetromino = result["current_tetromino"]
                restart_loop = result["restart_loop"]
                if restart_loop:
                    continue

        current_time = time.time()
        if (
            current_time - last_update_time > INTERVAL
        ):  # Move tetromino down after interval
            new_position = list(tetromino_position)
            new_position[0] += 1
            if can_move(well, current_tetromino[0], new_position):
                tetromino_position = new_position
            else:
                # Place the tetromino in the well
                for y, row in enumerate(current_tetromino[0]):
                    for x, cell in enumerate(row):
                        if cell:
                            well[tetromino_position[0] + y][
                                tetromino_position[1] + x
                            ] = current_tetromino[1]

                # Check for full rows
                full_rows = find_full_rows(well)
                if full_rows:
                    clear_full_rows(screen, well, full_rows, game_state)
                    game_state.add_score_by_lines(len(full_rows))

                # Choose the next tetromino
                current_tetromino = random.choice(TETROMINOES)
                tetromino_position = [0, 4]

                # Check if the new tetromino can fit in the well
                if not can_move(well, current_tetromino[0], tetromino_position):
                    return Phase.GAME_OVER

            last_update_time = current_time

        draw_level(screen, well, game_state)

        # Draw the current tetromino
        draw_tetromino(
            screen,
            current_tetromino[0],
            current_tetromino[1],
            (
                (tetromino_position[1] + 1) * BLOCK_SIZE,
                tetromino_position[0] * BLOCK_SIZE,
            ),
        )

        pygame.display.flip()
