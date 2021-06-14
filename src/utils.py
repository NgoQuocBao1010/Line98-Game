from globals import *

# $$$$$$$$$$$$********* Button *********$$$$$$$$$$$$ #
class Button():
    def __init__(self, x, y, width=120, height=30, text="Button", font=BUTTON_FONT, fontPressedColor=None, fontColor=WHITE, bgColor=BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.fontColor = fontColor
        self.fontPressedColor = fontPressedColor
        self.bgColor = bgColor

        self.isPressed = False

        self.useImage = False
        self.mainImg = None
        self.pressedImg = None
    
    def imageConfig(self, mainImg, pressedImg):
        self.useImage = True
        self.mainImg = mainImg
        self.pressedImg = pressedImg

    def draw(self, win):
        if not self.useImage:
            backGroundColor = self.bgColor

            if self.fontPressedColor:
                fontColor = self.fontPressedColor if self.isPressed else self.fontColor
            else:
                fontColor = self.fontColor

            if self.isPressed:
                pygame.draw.rect(win, backGroundColor, (self.x, self.y, self.width, self.height))
            else:
                pygame.draw.rect(win, backGroundColor, (self.x, self.y, self.width, self.height), 3)

            # Center the text
            text = self.font.render(self.text, True, fontColor)
            textWidth, textHeight = text.get_size()
            textX = self.x + (self.width - textWidth) // 2
            textY = self.y + (self.height - textHeight) // 2
            
            win.blit(text, (textX, textY))
        
        else:
            # pygame.draw.rect(win, WHITE, (self.x, self.y, self.width, self.height))
            if self.isPressed:
                win.blit(self.pressedImg, (self.x, self.y))
            else:
                win.blit(self.mainImg, (self.x, self.y))
    
    def isPointed(self, pos):
        mouseX, mouseY = pos

        if mouseX < self.x or mouseX > self.x + self.width:
            return False
        
        if mouseY < self.y or mouseY > self.y + self.height:
            return False

        return True
    
    def __str__(self):
        return f"Button {self.text}"


# $$$$$$$$$$$$********* GameOver Board *********$$$$$$$$$$$$ #
class GameOverBoard():
    def __init__(self):
        self.x = 175
        self.y = 200
        self.width = 250
        self.height = 250

        self.score = 0

        self.activated = False
        self.buttons = []
        self.newHighscore = False

        self.createButton()
    
    def createButton(self):
        font = pygame.font.Font('./fonts/Poppins-Bold.ttf', 12)

        btnX = self.x + 20
        btnY = self.y + self.height - 40
        restartBtn = Button(btnX, btnY, text="Restart", width=90, font=font, fontPressedColor=WHITE, bgColor=(70, 73, 242), fontColor=(70, 73, 242))

        btnX = self.x + self.width - 110
        btnY = self.y + self.height - 40
        highScore = Button(btnX, btnY, text="HighScores", width=90, font=font, fontPressedColor=WHITE, bgColor=(70, 73, 242), fontColor=(70, 73, 242))

        self.buttons.append(restartBtn)
        self.buttons.append(highScore)

    def draw(self, win):
        if self.activated:
            win.blit(GAMEOVER_IMAGE, (self.x, self.y))

            scoreText = SCORE_FONT.render(f"{self.score}", True, RED)
            textWidth, _ = scoreText.get_size()
            textX = self.x + (self.width - textWidth) // 2
            textY = self.y + 20
            win.blit(scoreText, (textX, textY))

            if self.newHighscore:
                win.blit(HIGHSCOREICON, (textX + textWidth + 25, textY - 10))


            for btn in self.buttons:
                btn.draw(win)


# $$$$$$$$$$$$********* GameOver Board *********$$$$$$$$$$$$ #
class HighscoreBoard():
    def __init__(self):
        self.x = 175
        self.y = 200
        self.width = 250
        self.height = 250

        self.headerFont = pygame.font.Font('./fonts/Poppins-Bold.ttf', 21)
        self.scoreFont = pygame.font.Font('./fonts/Poppins-Bold.ttf', 17)
        self.firstPlace = pygame.font.Font('./fonts/Poppins-Bold.ttf', 22)
        self.newHSFont = pygame.font.Font('./fonts/TopSecret.ttf', 22)

        self.activated = False
        self.scores = []
        self.newHighScore = False
        self.buttons = []

        self.createButton()
        self.getHighscore()
    
    def createButton(self):
        font = pygame.font.Font('./fonts/Poppins-Bold.ttf', 12)

        btnX = self.x + 20
        btnY = self.y + self.height - 40
        restartBtn = Button(btnX, btnY, text="Restart", width=90, font=font, fontPressedColor=WHITE, bgColor=(70, 73, 242), fontColor=(70, 73, 242))

        btnX = self.x + self.width - 110
        btnY = self.y + self.height - 40
        closeBtn = Button(btnX, btnY, text="Close", width=90, font=font, fontPressedColor=WHITE, bgColor=(70, 73, 242), fontColor=(70, 73, 242))

        self.buttons.append(restartBtn)
        self.buttons.append(closeBtn)
    
    def getHighscore(self):
        with open("highscores.txt") as f:
            data = f.readlines()

            # Removes 'break line'
            for i in range(len(data)):
                data[i] = int(data[i].replace('\n', ''))
        
        self.scores = data
    
    def updateScore(self, newScore):
        self.newHighScore = True if newScore > self.scores[0] else False

        if newScore in self.scores:
            return self.newHighScore
        
        self.scores.append(newScore)
        self.scores.sort(reverse=True)

        # Remove bottom score
        self.scores = self.scores[0:-1]

        with open("highscores.txt", "w+") as f:
            for score in self.scores:
                f.write(f"{score}\n")
        
        return self.newHighScore

    def draw(self, win):
        if self.activated:
            pygame.draw.rect(win, LIGHTYELLOW, (self.x, self.y, self.width, self.height))

            headerText = self.headerFont.render(f"LEADERBOARD", True, BLUE)
            textWidth, _ = headerText.get_size()
            textX = self.x + (self.width - textWidth) // 2
            textY = self.y + 20
            win.blit(headerText, (textX, textY))

            imgX = self.x + 10
            imgY = self.y + 10
            win.blit(PODIUM, (imgX, imgY))


            img2X = self.x + self.width - 32 - 10
            img2Y = self.y + 10
            win.blit(PODIUM, (img2X, img2Y))

            # Display score
            scoreY = self.y + 60
            
            if self.newHighScore:
                text = self.newHSFont.render("New High Score", True, RED)
                win.blit(text, (self.x + 100, scoreY + 10))
            
            for index, score in enumerate(self.scores):
                pos = index + 1

                posText = self.scoreFont.render(f"{pos}.", True, BLUE) if pos !=  1 else self.firstPlace.render(f"{pos}.", True, RED)
                win.blit(posText, (self.x + 30, scoreY))


                score = self.scoreFont.render(f"{score}", True, BLUE) if pos != 1 else self.firstPlace.render(f"{score}", True, RED)
                win.blit(score, (self.x + 50, scoreY))
                scoreY += 50
            
            # Display button
            for btn in self.buttons:
                btn.draw(win)


# $$$$$$$$$$$$********* Message Board *********$$$$$$$$$$$$ #
class MessageBoard():
    def __init__(self):
        self.x = 150
        self.y = 200
        self.width = 300
        self.height = 250

        self.title = ""
        self.message = ""
        self.buttons = []

        self.headerFont = pygame.font.Font('./fonts/Poppins-Bold.ttf', 30)
        self.msgFont = pygame.font.Font('./fonts/Poppins-Bold.ttf', 15)

        self.activated = False

        self.createButton()
    
    def createButton(self):
        font = pygame.font.Font('./fonts/Poppins-Bold.ttf', 12)

        btnX = self.x + 20
        btnY = self.y + self.height - 40
        restartBtn = Button(btnX, btnY, text="OK", width=90, font=font, fontPressedColor=WHITE, bgColor=(70, 73, 242), fontColor=(70, 73, 242))

        btnX = self.x + self.width - 110
        btnY = self.y + self.height - 40
        closeBtn = Button(btnX, btnY, text="Cancel", width=90, font=font, fontPressedColor=WHITE, bgColor=(70, 73, 242), fontColor=(70, 73, 242))

        self.buttons.append(restartBtn)
        self.buttons.append(closeBtn)
    
    def invokeMessage(self, title, message):
        self.title = title
        self.message = message
    
    def draw(self, win):
        if self.activated:
            pygame.draw.rect(win, LIGHTYELLOW, (self.x, self.y, self.width, self.height))

            headerText = self.headerFont.render(f"{self.title}", True, RED)
            textWidth, _ = headerText.get_size()
            textX = self.x + (self.width - textWidth) // 2
            textY = self.y + 20
            win.blit(headerText, (textX, textY))

            msgText = self.msgFont.render(f"{self.message}", True, BLUE)
            textWidth, _ = msgText.get_size()
            textX = self.x + (self.width - textWidth) // 2
            textY = self.y + 100
            win.blit(msgText, (textX, textY))

            for btn in self.buttons:
                btn.draw(win)

