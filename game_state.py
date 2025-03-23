from constants import LEVEL_THRESHOLDS, Phase


class GameState:
    def __init__(self):
        self.phase = Phase.TITLE_SCREEN
        self.score = 0
        self.level = 1
        self.lines_cleared = 0

    def add_score_by_lines(self, lines):
        self.score += 10 * 2 ** (lines - 1)

    def add_cleared_lines(self, lines):
        self.lines_cleared += lines
        # Set level to the index of the first element in LEVEL_THRESHOLDS that is greater than or equal to lines_cleared
        self.level = (
            next(
                i
                for i, threshold in enumerate(LEVEL_THRESHOLDS)
                if threshold >= self.lines_cleared
            )
            + 1
        )

    def reset(self):
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
