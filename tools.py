import pygame
from constants import BLOCK_SIZE, GameState


def draw_tetromino(screen, shape, color, position):
    outline_color = (0, 0, 139)  # Dark blue color
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    position[0] + x * BLOCK_SIZE,
                    position[1] + y * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                )
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, outline_color, rect, 1)  # Draw outline


def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]


def handle_events(event, game_state):
    if event.type == pygame.QUIT:
        return GameState.QUIT
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            return GameState.QUIT
        elif event.key == pygame.K_SPACE and game_state == GameState.TITLE_SCREEN:
            return GameState.PLAY
    return game_state
