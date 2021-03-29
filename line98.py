import pygame
import random, time

# Pygame initilize
pygame.init()
pygame.font.init()

# Window's Configuration
WIN_WIDTH = WIN_HEIGHT = 600                                # height and width of window
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_WIDTH))       # initilize win form
pygame.display.set_caption("LINE 98")                       # win caption
SCORE_TEXT_FONT = pygame.font.Font('./fonts/CursedTimerUlil-Aznm.ttf', 30)
SCORE_FONT = pygame.font.Font('./fonts/CursedTimerUlil-Aznm.ttf', 30, bold=True)
BUTTON_FONT = pygame.font.Font('./fonts/Poppins-Bold.ttf', 18)


# Grid Configuration
WIDTH = HEIGHT = 450                                        # width and height of the grid
GAP = 50                                                    # width of each square in a grid
ROWS = COLS = 9

# Color Variables
RED = (224, 62, 78)
BLUE = (62, 119, 224)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TURQUOISE = (64, 224, 208)
GREEN = (62, 224, 86)


ICON_IMAGES = pygame.image.load('./images/line98.png')
SCORE_DISPLAY = pygame.image.load('./images/scoreDisplay.png')
GAMEOVER_IMAGE = pygame.image.load('./images/gameOver5.png')
CLOSEICON = pygame.image.load('./images/cancel.png')

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


# $$$$$$$$$$$$********* Square contains 1 ball *********$$$$$$$$$$$$ #
class Spot():
    def __init__(self, row, column):
        self.row = row
        self.col = column
        self.x = self.col * GAP + 75
        self.y = self.row * GAP + 130
        self.width = GAP

        # Spot status
        self.bgColor = WHITE
        self.color = random.choice(list(IMAGES.keys()))

        # animation
        self.selected = False
        self.up = False
        self.offsetY = 0

        # Status
        self.baby = False
        self.alive = False

    def __str__(self):
        return f'Spot at {self.row}, {self.col}'
    
    # Get position of a square
    def getPosition(self):
        return self.row, self.col
    
    # Get the movable squares all round this square
    def getMovableSquare(self, grid):
        self.movableRoutes = []

        # Below square
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].alive:
            self.movableRoutes.append(grid[self.row + 1][self.col])

        # Upper square
        if self.row > 0 and not grid[self.row - 1][self.col].alive:
            self.movableRoutes.append(grid[self.row - 1][self.col])

        # Right square
        if self.col < COLS - 1 and not grid[self.row][self.col + 1].alive:
            self.movableRoutes.append(grid[self.row][self.col + 1])

        # Left square
        if self.col > 0 and not grid[self.row][self.col - 1].alive:
            self.movableRoutes.append(grid[self.row][self.col - 1])

        return self.movableRoutes
    
    # Check if 2 spots is the same type
    def isSame(self, otherSpot):
        if not self.alive or not otherSpot.alive:
            return False
        
        return self.color == otherSpot.color
    
    # Update new color
    def update(self, otherSpot):
        self.row = otherSpot.row
        self.col = otherSpot.col
        self.alive = otherSpot.alive
        self.baby = otherSpot.baby
        self.color = otherSpot.color
        self.selected = otherSpot.selected

    # Make spot became bigger
    def makeAlive(self):
        self.alive = True
        self.baby = False
    
    # Make spot became dead
    def makeDead(self):
        self.color = random.choice(list(IMAGES.keys()))
        self.alive = False
        self.baby = False
    
    # Draw a square
    def draw(self, win):
        pygame.draw.rect(win, self.bgColor, (self.x, self.y, self.width, self.width))

        if self.alive:
            # bouncing animation
            if self.selected:
                if not self.up:
                    self.offsetY += 1
            
                if self.offsetY == 10:
                    self.up = True
                
                if self.up:
                    self.offsetY -= 1
                
                if self.offsetY < 0:
                    self.offsetY = 0
                    self.up = False
            
            else:
                self.offsetY = 0
            
            newY = self.y - self.offsetY
            self.mainImg = win.blit(IMAGES[self.color].get('big'), (self.x, newY))
    
        elif self.baby:
            newX = self.x + 15
            newY = self.y + 15
            self.mainImg = win.blit(IMAGES[self.color].get('small'), (newX, newY))


# $$$$$$$$$$$$********* Grid contains all the balls *********$$$$$$$$$$$$ #
class Grid():
    def __init__(self):
        # Grid coordinate's config
        self.width = self.height = 450
        self.marginBottom = 20
        self.rows = self.cols = 9
        self.x = (WIN_WIDTH - self.width) / 2
        self.y = WIN_HEIGHT - self.height -  self.marginBottom
        
        # ...
        self.newBabies = 40
        self.freeSpots = []
        self.babies = []
        self.lastState = []
        self.lastScore = 0
        self.createNewGrid()
    
    # check if the mouse is clicked inside grid
    def isCliked(self, pos):
        mouseX, mouseY = pos

        if mouseX < self.x or mouseX > self.x + self.width:
            return False
        
        if mouseY < self.y or mouseY > self.y + self.height:
            return False

        return True
    
    # Return the row and col of the spot that was clicked
    def getPosition(self, pos):
        mouseX, mouseY = pos

        spotX = mouseX - self.x
        spotY = mouseY - (WIN_HEIGHT - self.height - self.marginBottom)

        spotRow = spotY // GAP
        spotCol = spotX // GAP
        
        return int(spotRow), int(spotCol)

    # Initialize a empty grid
    def createNewGrid(self):
        self.grid = []
        self.freeSpots = []

        for row in range(ROWS):
            self.grid.append([])

            for col in range(COLS):
                spot = Spot(row, col)
                self.grid[row].append(spot)
                self.freeSpots.append((row, col))
    
    # draw the lines
    def drawLine(self, win):
        gap = self.width // self.rows
        for row in range(self.rows):
            pygame.draw.line(win, BLACK, (self.x, self.y + row * gap), (self.x + self.width, self.y + row * gap))
            for col in range(self.rows):
                pygame.draw.line(win, BLACK, (self.x + col * gap, self.y), (self.x + col * gap, self.y + self.width))
            
            self.rectangle = pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.width), 2)

    # Draw the grid
    def draw(self, win):
        for row in self.grid:
            for spot in row:
                spot.draw(win)

        self.drawLine(win)
        
    # return a col and col of a random idle sqot
    def randomSquare(self):
        row, col = random.choice(self.freeSpots)

        return row, col

    # make 3 random babies
    def makeBabies(self):
        self.babies = []
        if len(self.freeSpots) < self.newBabies:
            return
        
        while len(self.babies) < self.newBabies:
            newRow, newCol = self.randomSquare()

            if self.grid[newRow][newCol].baby:
                continue
        
            self.grid[newRow][newCol].baby = True
            self.babies.append(self.grid[newRow][newCol])

    # Reset grid to start new round with 3 grown and 3 baby spots
    def resetNewRound(self):
        self.createNewGrid()
        newSquares = []

        while len(newSquares) < 3:
            newRow, newCol = self.randomSquare()

            if self.grid[newRow][newCol].baby:
                continue

            self.grid[newRow][newCol].makeAlive()
            self.freeSpots.remove((newRow, newCol))
            newSquares.append(self.grid[newRow][newCol])
        
        self.makeBabies()
        self.saveSate()
    
    # Make all babies bigger
    def grownUp(self):
        for spot in self.babies:
            if spot.baby:
                spot.makeAlive()
        
        self.babies = []
    
    # Save current state
    def saveSate(self, score=0):
        self.lastState = []
        self.lastBabies = []
        self.lastScore = score

        for row in range(self.rows):
            self.lastState.append([])
            for col in range(self.cols):
                spot = Spot(row, col)
                spot.update(self.grid[row][col])
                self.lastState[row].append(spot)

                if spot.baby:
                    self.lastBabies.append(spot)

    # Undo previous move
    def undo(self):
        self.grid = self.lastState
        self.babies = self.lastBabies

        return self.lastScore
        
    # checking grid conditions
    # Delete and increase score
    def checking(self, currentScore):
        point = 0
        deleteSpots = []

        # Check for 5 same spot in a row
        for row in range(self.rows):
            tempVList = [self.grid[row][0], ]
            for col in range(self.cols - 1):  
                if self.grid[row][col].isSame(self.grid[row][col + 1]):
                    tempVList.append(self.grid[row][col + 1])
                else:
        
                    tempVList = [self.grid[row][col + 1], ]
            
                if len(tempVList) >= 5:
                    print('There are 5 in a row')
                    for spot in tempVList:
                        if spot not in deleteSpots:
                            deleteSpots.append(spot)
        
        # Check for 5 same spot in a column
        for col in range(self.cols):
            tempHList = [self.grid[0][col], ]
            for row in range(self.rows - 1):
                if self.grid[row][col].isSame(self.grid[row + 1][col]):
                    tempHList.append(self.grid[row + 1][col])
                else:
                    tempHList = [self.grid[row + 1][col], ]
            
                if len(tempHList) >= 5:
                    print('There are 5 in a column')
                    for spot in tempHList:
                        if spot not in deleteSpots:
                            deleteSpots.append(spot)

        # Right to Left diaognal
        for col in range(5):
            for row in range(5):
                if (
                    self.grid[row][col].isSame(self.grid[row + 1][col + 1]) and 
                    self.grid[row + 1][col + 1].isSame(self.grid[row + 2][col + 2]) and 
                    self.grid[row + 2][col + 2].isSame(self.grid[row + 3][col + 3]) and 
                    self.grid[row + 3][col + 3].isSame(self.grid[row + 4][col + 4])
                ):
                    deleteSpots.append(self.grid[row][col]);
                    deleteSpots.append(self.grid[row + 1][col + 1]);
                    deleteSpots.append(self.grid[row + 2][col + 2]);
                    deleteSpots.append(self.grid[row + 3][col + 3]);
                    deleteSpots.append(self.grid[row + 4][col + 4]);
        
        # Left to Right diaognal
        for col in range(4, self.cols):
            for row in range(5):
                if (
                    self.grid[row][col].isSame(self.grid[row + 1][col - 1]) and 
                    self.grid[row + 1][col - 1].isSame(self.grid[row + 2][col - 2]) and 
                    self.grid[row + 2][col - 2].isSame(self.grid[row + 3][col - 3]) and 
                    self.grid[row + 3][col - 3].isSame(self.grid[row + 4][col - 4])
                ):
                    deleteSpots.append(self.grid[row][col]);
                    deleteSpots.append(self.grid[row + 1][col - 1]);
                    deleteSpots.append(self.grid[row + 2][col - 2]);
                    deleteSpots.append(self.grid[row + 3][col - 3]);
                    deleteSpots.append(self.grid[row + 4][col - 4]);


        # Delete spots
        for spot in deleteSpots:
            spot.makeDead()
            spot.draw(WIN)
            self.drawLine(WIN)
            pygame.time.delay(70)
            point += 1
            pygame.display.update()
        
        # Score animation
        newScore = currentScore + point

        while currentScore < newScore:
            currentScore += 1
            scoreText = SCORE_FONT.render(f"{currentScore}", True, WHITE)
            WIN.blit(SCORE_DISPLAY, (225, 70))
            WIN.blit(scoreText, (240, 80))
            pygame.time.delay(50)
            pygame.display.update()
        
        # Checking for available spots
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col].alive and (row, col) in self.freeSpots:
                    self.freeSpots.remove((row, col))
                
                if not self.grid[row][col].alive and (row, col) not in self.freeSpots:
                    self.freeSpots.append((row, col))
        
        # print(len(self.freeSpots))
        return point

    # ****************** BFS Algorithm ****************** #
    def findShortestPath(self, start, end):
        distance = [[-1 for spot in range(self.rows + 1)] for row in range(self.rows + 1)]
        prev = [[None for spot in range(self.rows + 1)] for row in range(self.rows + 1)]
        path = []

        from collections import deque

        rowQueue = deque()
        colQueue = deque()

        startRow, startCol = start.getPosition()
        endRow, endCol = end.getPosition()

        rowQueue.append(startRow)
        colQueue.append(startCol)
        distance[startRow][startCol] = 0

        while len(rowQueue) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            row = rowQueue.popleft()
            col = colQueue.popleft()
            square = self.grid[row][col]

            if row == endRow and col == endCol:
                path = self.reconstructPath(prev, end)
                path.reverse()


                orginalColor = start.color
                img = IMAGES[start.color].get('big')

                c_x, c_y = start.x, start.y
                start.makeDead()

                prevPath = []
                for spot in path:
                    prevPath.append(spot)
                    newX, newY = spot.x, spot.y
                    while c_x != newX or c_y != newY:
                        if newX > c_x:
                            c_x += 1
                        elif newX < c_x:
                            c_x -= 1

                        if newY > c_y:
                            c_y += 1
                        elif newY < c_y:
                            c_y -= 1

                        for spot in prevPath:
                            spot.draw(WIN)
                        self.drawLine(WIN)
                        WIN.blit(img, (c_x, c_y))

                        # pygame.time.delay(1)
                        pygame.display.update()

                        current = spot

                    c_x, c_y = spot.x, spot.y
                    if spot == path[-1]:
                        path[-1].makeDead()
                        path[-1].color = orginalColor
                        path[-1].makeAlive()

                return True

            if row != endRow and col != endCol:
                # print('Looking through movableRoutes!!!')
                pass

            for neighbour in square.movableRoutes:
                neighRow, neighCol = neighbour.getPosition()

                if distance[neighRow][neighCol] == -1:
                    distance[neighRow][neighCol] = distance[row][col] + 1
                    rowQueue.append(neighRow)
                    colQueue.append(neighCol)

                    prev[neighRow][neighCol] = (row, col)
        return False

    # Reconstruct the path found by algorithm
    def reconstructPath(self, prev, end):
        path = []
        endRow, endCol = end.getPosition()
        current = (endRow, endCol)

        while current is not None:
            path.append(self.grid[current[0]][current[1]])
            current = prev[current[0]][current[1]]

        return path


# $$$$$$$$$$$$********* Button *********$$$$$$$$$$$$ #
class Button():
    def __init__(self, x, y, width=120, height=30, text="A button", font=BUTTON_FONT, fontColor=WHITE, bgColor=BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.fontColor = fontColor
        self.bgColor = bgColor

        self.isPressed = False

    def draw(self, win):
        backGroundColor = BLACK if self.isPressed else self.bgColor
        fontColor = WHITE if self.isPressed else self.fontColor

        pygame.draw.rect(win, backGroundColor, (self.x, self.y, self.width, self.height))

        # Center the text
        text = self.font.render(self.text, True, fontColor)
        textWidth, textHeight = text.get_size()
        textX = self.x + (self.width - textWidth) // 2
        textY = self.y + (self.height - textHeight) // 2
        
        win.blit(text, (textX, textY))
    
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
        self.x = 150
        self.y = 200
        self.width = 250
        self.height = 250

        self.score = 0

        self.activated = False
        self.buttons = []

        self.createButton()
    
    def createButton(self):
        font = pygame.font.Font('./fonts/Poppins-Bold.ttf', 12)

        btnX = self.x + 50
        btnY = self.y + self.height - 40
        restartBtn = Button(btnX, btnY, text="Restart", width=90, font=font, fontColor=(247, 245, 141), bgColor=(70, 73, 242))

        btnX = self.x + self.width - 90
        btnY = self.y + self.height - 40
        highScore = Button(btnX, btnY, text="HighScores", width=90, font=font, fontColor=(247, 245, 141), bgColor=(70, 73, 242))

        self.buttons.append(restartBtn)
        self.buttons.append(highScore)

    def draw(self, win):
        if self.activated:
            win.blit(GAMEOVER_IMAGE, (175, 200))

            # pygame.font.Font('./fonts/CursedTimerUlil-Aznm.ttf', 30, bold=True)
            scoreText = SCORE_FONT.render(f"{self.score}", True, RED)
            textWidth, _ = scoreText.get_size()
            textX = self.x + (self.width - textWidth) // 2
            textY = self.y + 20
            win.blit(scoreText, (textX, textY))


            for btn in self.buttons:
                btn.draw(win)
    
    def isClose(self):
        pass


# Update main win everey frame
def draw(win, grid, buttons, score=0, goBoard=None):
    win.fill(TURQUOISE)
    grid.draw(win)
    
    win.blit(ICON_IMAGES, (75, 10))

    # score text
    text = SCORE_TEXT_FONT.render("Score", True, RED)
    win.blit(text, (225, 40))

    scoreText = SCORE_FONT.render(f"{score}", True, WHITE)
    win.blit(SCORE_DISPLAY, (225, 70))
    win.blit(scoreText, (240, 80))

    # Buttons
    for btn in buttons:
        btn.draw(win)
    
    if goBoard:
        goBoard.draw(win)
    
    pygame.display.update()



def main():
    grid = Grid()
    grid.resetNewRound()

    goBoard = GameOverBoard()

    buttons = []

    # Create button 
    y = 10
    for title in ['New Game', 'Undo', 'HighScores']:
        btn = Button(x=405, y=y, text=title, bgColor=(247, 245, 141), fontColor=(70, 73, 242))
        buttons.append(btn)
        y += 40

    selectedSquare = None
    gotoSquare = None

    score = 0
    gameOver = False

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        draw(WIN, grid, buttons, score, goBoard)
        score += grid.checking(score)

        # Loop through all events in 1 frames
        for event in pygame.event.get():

            # Get mouse position
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                break

            # Event for left mouse click
            if pygame.mouse.get_pressed()[0]:
                if not gameOver:
                    if grid.isCliked(pos):
                        row, col = grid.getPosition(pos)
                        spot = grid.grid[row][col]

                        if not selectedSquare:
                            if spot.alive:
                                if not spot.selected:
                                    spot.selected = True
                                    selectedSquare = spot
                        
                        elif selectedSquare == spot:
                            spot.selected = False
                            selectedSquare = None

                        elif selectedSquare and spot != selectedSquare:
                            if not spot.alive:
                                selectedSquare.selected = False
                                gotoSquare = spot

                                for row in grid.grid:
                                    for square in row:
                                        square.getMovableSquare(grid.grid)
                                
                                grid.saveSate(score)
                                moved = grid.findShortestPath(selectedSquare, gotoSquare)

                                if moved:
                                    point = grid.checking(score)
                                    selectedSquare = None
                                    gotoSquare = None
                                    score += point

                                    if point == 0:
                                        grid.grownUp()
                                        grid.makeBabies()
                                
                                else:
                                    selectedSquare.selected = True
                            
                            else:
                                selectedSquare.selected = False
                                spot.selected = True
                                selectedSquare = spot
                
                else:
                    # Gameover Button
                    for btn in goBoard.buttons:
                        if btn.isPointed(pos):
                            btn.isPressed = True

                # Ingame buttons
                for button in buttons:
                    if button.isPointed(pos):
                        button.isPressed = True
            
            # Detect release mouse after clicked
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:               # Left mouse click
                    for button in buttons:
                        if button.isPressed:
                            button.isPressed = False

                            if button.text == "New Game":
                                selectedSquare = None
                                gotoSquare = None
                                score = 0
                                grid.resetNewRound()
                                gameOver = False
                                goBoard.activated = False
                            
                            if button.text == "Undo" and not gameOver:
                                score = grid.undo()
                    
                    if gameOver:
                        for btn in goBoard.buttons:
                            if btn.isPressed:
                                btn.isPressed = False
                                if btn.text == "Restart":
                                    selectedSquare = None
                                    gotoSquare = None
                                    score = 0
                                    grid.resetNewRound()
                                    gameOver = False
                                    goBoard.activated = False

        if len(grid.freeSpots) <= grid.newBabies:
            gameOver = True
            goBoard.activated = True
            goBoard.score = score
main()