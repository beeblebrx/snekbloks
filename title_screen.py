import pygame
import time

from constants import (
    BLOCK_SIZE,
    GAP_SIZE,
    TETROMINOES,
    GameState
)

from tools import draw_tetromino, rotate_shape, handle_events


def run(screen):
    game_state = GameState.TITLE_SCREEN

    font = pygame.font.Font(None, 36)
    title = font.render("SNEK BLOKS", True, (255, 255, 255))
    title_rect = title.get_rect(center=(400, 300))

    small_font = pygame.font.Font(None, 24)
    subtitle = small_font.render(
        "Press space to start, 'Q' to quit", True, (255, 255, 255)
    )
    subtitle_rect = subtitle.get_rect(center=(400, 500))

    last_update_time = time.time()
    current_tetromino = 0
    tetrominoes = [list(t) for t in TETROMINOES]  # Copy the constant array

    while True:
        for event in pygame.event.get():
            game_state = handle_events(event, game_state)
            if game_state != GameState.TITLE_SCREEN:
                return game_state

        screen.fill((0, 0, 0))
        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)

        total_width = len(tetrominoes) * (BLOCK_SIZE + GAP_SIZE * 3)
        x_offset = title_rect.centerx - total_width // 2
        y_offset = title_rect.bottom + 20
        for shape, color in tetrominoes:
            draw_tetromino(screen, shape, color, (x_offset, y_offset))
            x_offset += BLOCK_SIZE + GAP_SIZE * 3

        current_time = time.time()
        if current_time - last_update_time > 0.1:
            tetrominoes[current_tetromino] = (
                rotate_shape(tetrominoes[current_tetromino][0]),
                tetrominoes[current_tetromino][1],
            )
            current_tetromino = (current_tetromino + 1) % len(tetrominoes)
            last_update_time = current_time

        screen.fill((0, 0, 0))
        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)

        total_width = len(tetrominoes) * (BLOCK_SIZE + GAP_SIZE * 3)
        x_offset = title_rect.centerx - total_width // 2
        y_offset = title_rect.bottom + 20
        for shape, color in tetrominoes:
            draw_tetromino(screen, shape, color, (x_offset, y_offset))
            x_offset += BLOCK_SIZE + GAP_SIZE * 3

        pygame.display.flip()
