import pygame


class Screen:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Screen, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, width=800, height=600):
        if not self._initialized:
            pygame.init()
            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption("Tetris")
            self._initialized = True

    @classmethod
    def getScreen(cls):
        return cls().screen
