from test import *

class Game():
    def __init__(self):
        self.grid = Grid()

        self.gameOverBoard = GameOverBoard()
        self.highscoreBoard = HighscoreBoard()
        self.msgBoard = MessageBoard()

        self.buttons = []
        
        self.selectedSquare = None
        self.gotoSquare = None

        self.score = 0
        self.gameOver = False
        self.overlay = False
    
    # Create ingame button
    def ingameButtons(self):
        y = 10
        for title in ['New Game', 'HighScores', 'Exit']:
            btn = Button(x=405, y=y, text=title, bgColor=(247, 245, 141), fontColor=(70, 73, 242))
            self.buttons.append(btn)
            y += 40

        btnX = 225
        for title in ['Save', 'Undo']:
            btn = Button(x=btnX, y=95, text=title, width=32, height=32)

            mainImgUrl = f'./images/{title.lower()}.png'
            pressedImgUrl = f'./images/{title.lower()}Pressed.png'
            btn.imageConfig(pygame.image.load(mainImgUrl), pygame.image.load(pressedImgUrl))
            self.buttons.append(btn)
            btnX += 90
    

    # Update main win everey frame
    def draw(self, win):
        win.fill(TURQUOISE)
        self.grid.draw(win)
        
        win.blit(ICON_IMAGES, (75, 10))

        # score text
        text = SCORE_TEXT_FONT.render("Score", True, RED)
        win.blit(text, (225, 10))

        scoreText = SCORE_FONT.render(f"{self.score}", True, WHITE)
        win.blit(SCORE_DISPLAY, (225, 40))
        win.blit(scoreText, (240, 50))

        # Buttons
        for btn in self.buttons:
            btn.draw(win)
        
        self.gameOverBoard.draw(win)
        self.highscoreBoard.draw(win)
        self.
        
        pygame.display.update()

    def play(self):
        pass
