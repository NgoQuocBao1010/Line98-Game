import pygame
import random, time

# Pygame initilize
pygame.init()
pygame.font.init()

# Window's Configuration
WIN_WIDTH = WIN_HEIGHT = 600                                # height and width of window
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_WIDTH))       # initilize win form
pygame.display.set_caption("LINE 98")                       # win caption

# Grid Configuration
WIDTH = HEIGHT = 450                                        # width and height of the grid
GAP = 50                                                    # width of each square in a grid
ROWS = COLS = 9


# Fonts
SCORE_TEXT_FONT = pygame.font.Font('./fonts/CursedTimerUlil-Aznm.ttf', 30)
SCORE_FONT = pygame.font.Font('./fonts/CursedTimerUlil-Aznm.ttf', 30, bold=True)
BUTTON_FONT = pygame.font.Font('./fonts/Poppins-Bold.ttf', 18)


# Color Variables
RED = (224, 62, 78)
BLUE = (62, 119, 224)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TURQUOISE = (64, 224, 208)
GREEN = (62, 224, 86)
LIGHTYELLOW = (235, 235, 99)


# IMAGES
ICON_IMAGES = pygame.image.load('./images/line98.png')
SCORE_DISPLAY = pygame.image.load('./images/scoreDisplay.png')
GAMEOVER_IMAGE = pygame.image.load('./images/gameOver.png')
PODIUM = pygame.image.load('./images/podium.png')
HIGHSCOREICON = pygame.image.load('./images/highscoreIcon.png')

# Ball's Images
IMAGES = {
    'yellow': {
        'big': pygame.image.load('./images/big1.png'),
        'small': pygame.image.load('./images/small1.png'),
    },
    'pink': {
        'big': pygame.image.load('./images/big2.png'),
        'small': pygame.image.load('./images/small2.png'),
    },
    'blue': {
        'big': pygame.image.load('./images/big3.png'),
        'small': pygame.image.load('./images/small3.png'),
    },
    'green': {
        'big': pygame.image.load('./images/big4.png'),
        'small': pygame.image.load('./images/small4.png'),
    },
    'red': {
        'big': pygame.image.load('./images/big5.png'),
        'small': pygame.image.load('./images/small5.png'),
    },
}


# Sounds
SOUNDS_EFFECT = {
    'start': pygame.mixer.Sound('./sounds/ctcht.mp3'),
    'newgame': pygame.mixer.Sound('./sounds/newgame.wav'),
    'moved': pygame.mixer.Sound('./sounds/moved.wav'),
    'cantMoved': pygame.mixer.Sound('./sounds/cantMoved.mp3'),
    'undo': pygame.mixer.Sound('./sounds/undo.wav'),
    'scored': pygame.mixer.Sound('./sounds/scored.wav'),
    'gameover': pygame.mixer.Sound('./sounds/gameover.wav'),
    'highscore': pygame.mixer.Sound('./sounds/highscore.wav'),
}