import pygame
import sys
from constants import Phase
from game_state import GameState
import play
import title_screen
import game_over


def quit_game():
    pygame.quit()
    sys.exit()


def main():
    pygame.init()
    pygame.display.set_caption("Snek Bloks")

    game_state = GameState()
    while True:
        match game_state.phase:
            case Phase.TITLE_SCREEN:
                game_state.phase = title_screen.run(game_state.phase)
            case Phase.PLAY:
                game_state.phase = play.run(game_state)
            case Phase.GAME_OVER:
                game_state.phase = game_over.run()
            case Phase.SCORE:
                # Placeholder for score state logic
                pass
            case Phase.QUIT:
                quit_game()


if __name__ == "__main__":
    main()
