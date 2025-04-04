from enum import Enum


class Phase(Enum):
    TITLE_SCREEN = 1
    PLAY = 2
    GAME_OVER = 3
    SCORE = 4
    QUIT = 5


BLOCK_SIZE = 28
OUTLINE_COLOR = (0, 0, 139)  # Dark blue

TETROMINOES = [
    ([[1, 1, 1], [0, 1, 0]], (255, 165, 0)),  # T
    ([[1, 1, 0], [0, 1, 1]], (0, 0, 255)),  # Z
    ([[0, 1, 1], [1, 1, 0]], (0, 255, 0)),  # S
    ([[1, 1, 1], [1, 0, 0]], (255, 0, 0)),  # L
    ([[1, 1, 1], [0, 0, 1]], (128, 0, 128)),  # J
    ([[1, 1, 1, 1]], (0, 255, 255)),  # I
    ([[1, 1], [1, 1]], (255, 255, 0)),  # O
]

LEVEL_THRESHOLDS = [10, 20, 40, 60, 80, 100, 120, 140, 160, 200]
