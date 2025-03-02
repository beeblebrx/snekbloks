import pygame
import sys
import title_screen
from constants import GameState
import play


def quit_game():
    pygame.quit()
    sys.exit()


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snek Bloks")

    game_state = GameState.TITLE_SCREEN

    while True:
        match game_state:
            case GameState.TITLE_SCREEN:
                game_state = title_screen.run(screen)
            case GameState.PLAY:
                game_state = play.run(screen)
            case GameState.GAME_OVER:
                # Placeholder for game over state logic
                pass
            case GameState.SCORE:
                # Placeholder for score state logic
                pass
            case GameState.QUIT:
                quit_game()


if __name__ == "__main__":
    main()
