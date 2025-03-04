import pygame
from constants import GameState
from tools import handle_events

def run(screen):
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))

    # Create a background box slightly larger than the text
    background_rect = text_rect.inflate(20, 20)

    while True:
        for event in pygame.event.get():
            if handle_events(event, GameState.GAME_OVER) != GameState.GAME_OVER:
                return GameState.TITLE_SCREEN

        # Draw the background box
        pygame.draw.rect(screen, (0, 0, 0), background_rect)
        # Draw the text
        screen.blit(text, text_rect)
        pygame.display.flip()

