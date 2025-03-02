import pygame
import random
import time
from constants import GameState, TETROMINOES, BLOCK_SIZE
from tools import draw_tetromino, handle_events

WELL_DEPTH = 20
WELL_WIDTH = 10

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

        current_time = time.time()
        if current_time - last_update_time > 0.2:  # Move tetromino down every 0.5 seconds
            tetromino_position[0] += 1
            last_update_time = current_time

            # Check if tetromino has reached the bottom or collided with another block
            if tetromino_position[0] + len(current_tetromino[0]) > WELL_DEPTH - 1 or any(
                well[tetromino_position[0] + y][tetromino_position[1] + x]
                for y, row in enumerate(current_tetromino[0])
                for x, cell in enumerate(row)
                if cell
            ):
                # Place the tetromino in the well
                for y, row in enumerate(current_tetromino[0]):
                    for x, cell in enumerate(row):
                        if cell:
                            well[tetromino_position[0] + y - 1][tetromino_position[1] + x] = current_tetromino[1]

                # Choose the next tetromino
                current_tetromino = random.choice(TETROMINOES)
                tetromino_position = [0, 4]

        screen.fill((0, 0, 0))

        # Draw the well borders
        well_color = (173, 216, 230)  # Light blue color
        for y in range(WELL_DEPTH):
            pygame.draw.rect(
                screen,
                well_color,
                pygame.Rect(0, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
            )
            pygame.draw.rect(
                screen,
                well_color,
                pygame.Rect(11 * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
            )
        for x in range(WELL_WIDTH + 2):
            pygame.draw.rect(
                screen,
                well_color,
                pygame.Rect(x * BLOCK_SIZE, 19 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
            )

        # Draw the well
        for y, row in enumerate(well):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        cell,
                        pygame.Rect(
                            (x + 1) * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
                        ),
                    )

        # Draw the current tetromino
        draw_tetromino(
            screen,
            current_tetromino[0],
            current_tetromino[1],
            ((tetromino_position[1] + 1) * BLOCK_SIZE, tetromino_position[0] * BLOCK_SIZE),
        )

        pygame.display.flip()
