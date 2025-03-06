import pygame
from constants import BLOCK_SIZE, OUTLINE_COLOR, Phase


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


def handle_events(event, game_phase):
    if event.type == pygame.QUIT:
        return Phase.QUIT
    elif event.type == pygame.KEYDOWN:
        if game_phase == Phase.GAME_OVER:
            return Phase.QUIT
        if event.key == pygame.K_q:
            return Phase.QUIT
        elif event.key == pygame.K_SPACE and game_phase == Phase.TITLE_SCREEN:
            return Phase.PLAY
    return game_phase
