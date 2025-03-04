import pygame
from constants import BLOCK_SIZE, OUTLINE_COLOR, GameState


def draw_tetromino(screen, shape, color, position, block_size=BLOCK_SIZE):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    position[0] + x * block_size,
                    position[1] + y * block_size,
                    block_size,
                    block_size,
                )
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, OUTLINE_COLOR, rect, 1)  # Draw outline


def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]


def handle_events(event, game_state):
    if event.type == pygame.QUIT:
        return GameState.QUIT
    elif event.type == pygame.KEYDOWN:
        if game_state == GameState.GAME_OVER:
            return GameState.QUIT
        if event.key == pygame.K_q:
            return GameState.QUIT
        elif event.key == pygame.K_SPACE and game_state == GameState.TITLE_SCREEN:
            return GameState.PLAY
    return game_state
