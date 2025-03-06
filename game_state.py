from constants import Phase


class GameState:
    def __init__(self):
        self.phase = Phase.TITLE_SCREEN
        self.score = 0

    def add_score_by_lines(self, lines):
        self.score += 10 * 2 ** (lines - 1)
