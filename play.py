import pygame
import random
import time
from constants import OUTLINE_COLOR, GameState, TETROMINOES, BLOCK_SIZE
from tools import draw_tetromino, handle_events, rotate_shape

WELL_DEPTH = 20
WELL_WIDTH = 10
FALL_SPEED = 0.5


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


def run(screen):
    game_state = GameState.PLAY

    # Initialize the well
    well = [[0 for _ in range(WELL_WIDTH)] for _ in range(WELL_DEPTH)]

    current_tetromino = random.choice(TETROMINOES)
    tetromino_position = [0, 4]  # Starting position at the top center

    last_update_time = time.time()

    while game_state == GameState.PLAY:
        for event in pygame.event.get():
            game_state = handle_events(event, game_state)
            if game_state != GameState.PLAY:
                return game_state
            if event.type == pygame.KEYDOWN:
                new_position = list(tetromino_position)
                if event.key == pygame.K_a:
                    new_position[1] -= 1
                elif event.key == pygame.K_d:
                    new_position[1] += 1
                elif event.key == pygame.K_SPACE:
                    new_position = drop_tetromino(
                        well, current_tetromino, tetromino_position
                    )
                elif event.key == pygame.K_s:
                    new_position[0] += 1
                elif event.key == pygame.K_w:
                    rotated_tetromino = rotate_shape(current_tetromino[0])
                    if can_move(well, rotated_tetromino, tetromino_position):
                        current_tetromino = (rotated_tetromino, current_tetromino[1])
                        continue

                if can_move(well, current_tetromino[0], new_position):
                    tetromino_position = new_position

        current_time = time.time()
        if (
            current_time - last_update_time > FALL_SPEED
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

                # Choose the next tetromino
                current_tetromino = random.choice(TETROMINOES)
                tetromino_position = [0, 4]

            last_update_time = current_time

        screen.fill((0, 0, 0))

        draw_well(screen, well)

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
