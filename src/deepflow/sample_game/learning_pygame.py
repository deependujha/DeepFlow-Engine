# credits: https://github.com/deependujha
import pygame
from deepflow.game import DeepFlowGame


class SimplePyGame(DeepFlowGame):
    def __init__(self):
        super().__init__()
        # Initializing
        pygame.init()

        # Setting up FPS
        self.FPS = 60
        self.FramePerSec = pygame.time.Clock()

        # Creating colors
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        # Other Variables for use in the program
        self.SCREEN_WIDTH = 400
        self.SCREEN_HEIGHT = 600
        self.SPEED = 7
        self.SCORE = 0

        # Setting up Fonts
        self.font = pygame.font.SysFont("Verdana", 60)
        self.font_small = pygame.font.SysFont("Verdana", 20)
        self.game_over = self.font.render("Game Over", True, self.BLACK)

        self.background = pygame.image.load("AnimatedStreet.png")

        # Create a white screen
        self.DISPLAYSURF = pygame.display.set_mode((400, 600))
        self.DISPLAYSURF.fill(self.WHITE)
        pygame.display.set_caption("Game")
