import pygame
import time

from constants import TETROMINOES, Phase
from tools import draw_tetromino, rotate_shape, handle_events

TITLE_SCREEN_BLOCK_SIZE = 16
GAP_SIZE = 20


def run(screen, game_phase):
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
            game_phase = handle_events(event, game_phase)
            if game_phase != Phase.TITLE_SCREEN:
                return game_phase

        screen.fill((0, 0, 0))
        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)

        total_width = len(tetrominoes) * (TITLE_SCREEN_BLOCK_SIZE + GAP_SIZE * 3)
        x_offset = title_rect.centerx - total_width // 2
        y_offset = title_rect.bottom + GAP_SIZE
        for shape, color in tetrominoes:
            draw_tetromino(
                screen, shape, color, (x_offset, y_offset), TITLE_SCREEN_BLOCK_SIZE
            )
            x_offset += TITLE_SCREEN_BLOCK_SIZE + GAP_SIZE * 3

        current_time = time.time()
        if current_time - last_update_time > 0.1:
            tetrominoes[current_tetromino] = (
                rotate_shape(tetrominoes[current_tetromino][0]),
                tetrominoes[current_tetromino][1],
            )
            current_tetromino = (current_tetromino + 1) % len(tetrominoes)
            last_update_time = current_time

        pygame.display.flip()
