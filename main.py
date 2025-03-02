import pygame
import sys
import time

BLOCK_SIZE = 16
GAP_SIZE = 20

def quit_game():
    pygame.quit()
    sys.exit()

def draw_tetromino(screen, shape, color, position):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color, pygame.Rect(
                    position[0] + x * BLOCK_SIZE,
                    position[1] + y * BLOCK_SIZE,
                    BLOCK_SIZE, BLOCK_SIZE
                ))

def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snek Bloks")

    font = pygame.font.Font(None, 36)
    text = font.render("Hello! Press Q to quit.", True, (255, 255, 255))
    text_rect = text.get_rect(center=(400, 300))

    tetrominoes = [
        ([[1, 1, 1], [0, 1, 0]], (255, 165, 0)),  # T
        ([[1, 1, 0], [0, 1, 1]], (0, 0, 255)),  # Z
        ([[0, 1, 1], [1, 1, 0]], (0, 255, 0)),  # S
        ([[1, 1, 1], [1, 0, 0]], (255, 0, 0)),  # L
        ([[1, 1, 1], [0, 0, 1]], (128, 0, 128)),  # J
        ([[1, 1, 1, 1]], (0, 255, 255)),  # I
        ([[1, 1], [1, 1]], (255, 255, 0)),  # O
    ]

    last_update_time = time.time()
    current_tetromino = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit_game()

        current_time = time.time()
        if current_time - last_update_time > 0.1:
            tetrominoes[current_tetromino] = (rotate_shape(tetrominoes[current_tetromino][0]), tetrominoes[current_tetromino][1])
            current_tetromino = (current_tetromino + 1) % len(tetrominoes)
            last_update_time = current_time

        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)

        total_width = len(tetrominoes) * (BLOCK_SIZE + GAP_SIZE * 3)
        x_offset = text_rect.centerx - total_width // 2
        y_offset = text_rect.bottom + 20
        for shape, color in tetrominoes:
            draw_tetromino(screen, shape, color, (x_offset, y_offset))
            x_offset += BLOCK_SIZE + GAP_SIZE * 3

        pygame.display.flip()

if __name__ == "__main__":
    main()
