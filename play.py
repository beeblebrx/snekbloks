import pygame
import random
import time
from constants import OUTLINE_COLOR, TETROMINOES, BLOCK_SIZE, Phase
from tools import draw_tetromino, handle_events, rotate_shape
from screen import Screen

WELL_DEPTH = 20
WELL_WIDTH = 10
INTERVAL = 0.1

next_tetrominoes = []


def draw_well(well):
    screen = Screen.getScreen()
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


def draw_score(score):
    screen = Screen.getScreen()
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, ((WELL_WIDTH + 2) * BLOCK_SIZE + 10, 10))


def draw_combo_bonus(combo_count):
    screen = Screen.getScreen()
    if combo_count > 1:
        font = pygame.font.Font(None, 36)
        combo_text = font.render("COMBO BONUS!", True, (255, 0, 0))
        screen.blit(combo_text, ((WELL_WIDTH + 2) * BLOCK_SIZE + 10, 50))


def draw_next_tetromino():
    screen = Screen.getScreen()
    font = pygame.font.Font(None, 36)
    next_text = font.render("Next:", True, (255, 255, 255))
    screen.blit(next_text, ((WELL_WIDTH + 2) * BLOCK_SIZE + 10, 90))

    incoming_tetromino = next_tetrominoes[0]
    draw_tetromino(
        screen,
        incoming_tetromino[0],
        incoming_tetromino[1],
        ((WELL_WIDTH + 2) * BLOCK_SIZE + 10, 130),
    )


def draw_level(well, game_state, combo_count):
    screen = Screen.getScreen()
    screen.fill((0, 0, 0))
    draw_well(well)
    draw_score(game_state.score)
    draw_combo_bonus(combo_count)
    draw_next_tetromino()


def clear_full_rows(well, full_rows, game_state, combo_count):
    draw_level(well, game_state, combo_count)
    pygame.display.flip()
    pygame.time.wait(300)
    remove_full_rows(well, full_rows)


def remove_full_rows(well, full_rows):
    for row_index in full_rows:
        del well[row_index]
        well.insert(0, [0] * WELL_WIDTH)


def check_rows(well, combo_count, game_state):
    full_rows = find_full_rows(well)
    if full_rows:
        clear_full_rows(well, full_rows, game_state, combo_count)
        combo_count += 1  # Increment combo count
        score_multiplier = 2 if combo_count > 1 else 1
        game_state.add_score_by_lines(len(full_rows) * score_multiplier)
    else:
        combo_count = 0  # Reset combo count if no rows are cleared

    return combo_count


def fill_tetromino_buffer(buffer):
    """
    Pick a random tetromino and append it to the buffer until the buffer is three elements long.
    If there would be three of the same tetromino in a row, pick a different one.
    """
    while len(buffer) < 3:
        tetromino = random.choice(TETROMINOES)
        if len(buffer) > 0 and buffer[-1] == tetromino:
            continue
        buffer.append(tetromino)
    return buffer


def start_new_round(
    well, current_tetromino, tetromino_position, game_state, combo_count
):
    global next_tetrominoes
    # Place the tetromino in the well
    for y, row in enumerate(current_tetromino[0]):
        for x, cell in enumerate(row):
            if cell:
                well[tetromino_position[0] + y][tetromino_position[1] + x] = (
                    current_tetromino[1]
                )

    # Check for full row and award points
    combo_count = check_rows(well, combo_count, game_state)

    # Choose the next tetromino
    current_tetromino = next_tetrominoes.pop(0)
    tetromino_position = [0, 4]

    # Check if the new tetromino can fit in the well
    if not can_move(well, current_tetromino[0], tetromino_position):
        return Phase.GAME_OVER, current_tetromino, tetromino_position, combo_count

    next_tetrominoes = fill_tetromino_buffer(next_tetrominoes)
    return None, current_tetromino, tetromino_position, combo_count


def run(game_state):
    screen = Screen.getScreen()
    global next_tetrominoes
    # Initialize the well
    well = [[0] * WELL_WIDTH for _ in range(WELL_DEPTH)]

    # Initialize a buffer of tetrominoes
    next_tetrominoes = fill_tetromino_buffer(next_tetrominoes)

    current_tetromino = next_tetrominoes.pop(0)
    tetromino_position = [0, 4]  # Starting position at the top center

    last_update_time = time.time()  # Initialize to current time
    combo_count = 0  # Initialize combo count
    level = 10  # Difficulty level
    frame = 0  # Frame counter

    tetromino_dropped = True  # Tracks if the tetromino was dropped. Set to true to prevent dropping on the first frame.
    tetromino_rotated = False  # Tracks if the tetromino was rotated

    while True:
        event = pygame.event.poll()
        game_phase = handle_events(event, game_state.phase)
        if game_phase != Phase.PLAY:
            return game_phase

        pressed_keys = pygame.key.get_pressed()

        # Handle key events that should happen immediately between intervals.
        if pressed_keys[pygame.K_SPACE]:
            if not tetromino_dropped:
                new_position = drop_tetromino(
                    well, current_tetromino, tetromino_position
                )
                game_phase, current_tetromino, tetromino_position, combo_count = (
                    start_new_round(
                        well, current_tetromino, new_position, game_state, combo_count
                    )
                )
                if game_phase == Phase.GAME_OVER:
                    return game_phase
                tetromino_dropped = True
                continue

        if pressed_keys[pygame.K_UP] and not tetromino_rotated:
            rotated_tetromino = rotate_shape(current_tetromino[0])
            if can_move(well, rotated_tetromino, tetromino_position):
                current_tetromino = (rotated_tetromino, current_tetromino[1])
                tetromino_rotated = True
        if not pressed_keys[pygame.K_UP]:
            tetromino_rotated = False
        if not pressed_keys[pygame.K_SPACE]:
            tetromino_dropped = False

        current_time = time.time()
        if current_time - last_update_time > INTERVAL:
            new_position = list(tetromino_position)

            # Handle key events that should happen at intervals.
            if pressed_keys[pygame.K_LEFT]:
                if can_move(
                    well, current_tetromino[0], [new_position[0], new_position[1] - 1]
                ):
                    new_position[1] -= 1
            elif pressed_keys[pygame.K_RIGHT]:
                if can_move(
                    well, current_tetromino[0], [new_position[0], new_position[1] + 1]
                ):
                    new_position[1] += 1
            elif pressed_keys[pygame.K_DOWN]:
                if can_move(
                    well, current_tetromino[0], [new_position[0] + 1, new_position[1]]
                ):
                    new_position[0] += 1

            frame = (frame + 1) % 100

            if frame % level == 0:
                new_position[0] += 1

            if can_move(well, current_tetromino[0], new_position):
                tetromino_position = new_position
            else:
                game_phase, current_tetromino, tetromino_position, combo_count = (
                    start_new_round(
                        well,
                        current_tetromino,
                        tetromino_position,
                        game_state,
                        combo_count,
                    )
                )
                if game_phase == Phase.GAME_OVER:
                    return game_phase

            last_update_time = current_time  # Update last_update_time here

        draw_level(well, game_state, combo_count)

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
