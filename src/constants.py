import pygame
import os

def getFullPath(relativePath, ignoreNonExist=False) -> str:
    """ Return full absolute path of a relative path """

    filePath = os.path.abspath(__file__)
    folderPath = os.path.dirname(filePath)

    absolutePath = os.path.join(folderPath, relativePath)

    if ignoreNonExist: return absolutePath

    return absolutePath if os.path.exists(absolutePath) else None


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
SCORE_TEXT_FONT = pygame.font.Font(getFullPath('./fonts/CursedTimerUlil-Aznm.ttf'), 30)
SCORE_FONT = pygame.font.Font(getFullPath('./fonts/CursedTimerUlil-Aznm.ttf'), 30, bold=True)
BUTTON_FONT = pygame.font.Font(getFullPath('./fonts/Poppins-Bold.ttf'), 18)


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
ICON_IMAGES = pygame.image.load(getFullPath('./images/line98.png'))
SCORE_DISPLAY = pygame.image.load(getFullPath('./images/scoreDisplay.png'))
GAMEOVER_IMAGE = pygame.image.load(getFullPath('./images/gameOver.png'))
PODIUM = pygame.image.load(getFullPath('./images/podium.png'))
HIGHSCOREICON = pygame.image.load(getFullPath('./images/highscoreIcon.png'))

# Ball's Images
IMAGES = {
    'yellow': {
        'big': pygame.image.load(getFullPath('./images/big1.png')),
        'small': pygame.image.load(getFullPath('./images/small1.png')),
    },
    'pink': {
        'big': pygame.image.load(getFullPath('./images/big2.png')),
        'small': pygame.image.load(getFullPath('./images/small2.png')),
    },
    'blue': {
        'big': pygame.image.load(getFullPath('./images/big3.png')),
        'small': pygame.image.load(getFullPath('./images/small3.png')),
    },
    'green': {
        'big': pygame.image.load(getFullPath('./images/big4.png')),
        'small': pygame.image.load(getFullPath('./images/small4.png')),
    },
    'red': {
        'big': pygame.image.load(getFullPath('./images/big5.png')),
        'small': pygame.image.load(getFullPath('./images/small5.png')),
    },
}

# Remove song because of license
backgroundMusic = getFullPath('./sounds/ctcht.mp3') if getFullPath('./sounds/ctcht.mp3') else getFullPath('./sounds/Makani – Scandinavianz & AXM (No Copyright Music) (64 kbps).mp3')

# Sounds
SOUNDS_EFFECT = {
    'start': pygame.mixer.Sound(backgroundMusic),
    'newgame': pygame.mixer.Sound(getFullPath('./sounds/newgame.wav')),
    'moved': pygame.mixer.Sound(getFullPath('./sounds/moved.wav')),
    'cantMoved': pygame.mixer.Sound(getFullPath('./sounds/cantMoved.mp3')),
    'undo': pygame.mixer.Sound(getFullPath('./sounds/undo.wav')),
    'scored': pygame.mixer.Sound(getFullPath('./sounds/scored.wav')),
    'gameover': pygame.mixer.Sound(getFullPath('./sounds/gameover.wav')),
    'highscore': pygame.mixer.Sound(getFullPath('./sounds/highscore.wav')),
}