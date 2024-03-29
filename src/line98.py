from .gameObjects import *
import random


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
        self.newBabies = 3
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
    def checking(self, win, currentScore):
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
                    for spot in tempHList:
                        if spot not in deleteSpots:
                            deleteSpots.append(spot)

        # Top Right to Bottom Left diaognal
        for col in range(5):
            tempDList = []
            for row in range(5):
                if (
                    self.grid[row][col].isSame(self.grid[row + 1][col + 1]) and 
                    self.grid[row + 1][col + 1].isSame(self.grid[row + 2][col + 2]) and 
                    self.grid[row + 2][col + 2].isSame(self.grid[row + 3][col + 3]) and 
                    self.grid[row + 3][col + 3].isSame(self.grid[row + 4][col + 4])
                ):
                    tempDList.append(self.grid[row][col]);
                    tempDList.append(self.grid[row + 1][col + 1]);
                    tempDList.append(self.grid[row + 2][col + 2]);
                    tempDList.append(self.grid[row + 3][col + 3]);
                    tempDList.append(self.grid[row + 4][col + 4]);
                
                if len(tempDList) >= 5:
                    for spot in tempDList:
                        if spot not in deleteSpots:
                            deleteSpots.append(spot)
        
        
        # Top Left to Right diaognal
        for col in range(4, self.cols):
            tempDList = []
            for row in range(5):
                if (
                    self.grid[row][col].isSame(self.grid[row + 1][col - 1]) and 
                    self.grid[row + 1][col - 1].isSame(self.grid[row + 2][col - 2]) and 
                    self.grid[row + 2][col - 2].isSame(self.grid[row + 3][col - 3]) and 
                    self.grid[row + 3][col - 3].isSame(self.grid[row + 4][col - 4])
                ):
                    tempDList.append(self.grid[row][col]);
                    tempDList.append(self.grid[row + 1][col - 1]);
                    tempDList.append(self.grid[row + 2][col - 2]);
                    tempDList.append(self.grid[row + 3][col - 3]);
                    tempDList.append(self.grid[row + 4][col - 4]);
                
                if len(tempDList) >= 5:
                    for spot in tempDList:
                        if spot not in deleteSpots:
                            deleteSpots.append(spot)


        # Delete spots
        for spot in deleteSpots:
            spot.makeDead()
            spot.draw(win)
            self.drawLine(win)
            pygame.time.delay(70)
            point += 1
            pygame.display.update()
        
        # Score animation
        newScore = currentScore + point

        if newScore > currentScore:
            SOUNDS_EFFECT.get('scored').play()
        
        while currentScore < newScore:
            currentScore += 1
            scoreText = SCORE_FONT.render(f"{currentScore}", True, WHITE)
            win.blit(SCORE_DISPLAY, (225, 40))
            win.blit(scoreText, (240, 50))
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
    def findShortestPath(self, win, start, end):
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
                            spot.draw(win)
                        self.drawLine(win)
                        win.blit(img, (c_x, c_y))

                        # pygame.time.delay(20)
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



# Update main win everey frame
def draw(win, grid, buttons, score=0, goBoard=None, hsBoard=None, msgBoard=None):
    win.fill(TURQUOISE)
    grid.draw(win)
    
    win.blit(ICON_IMAGES, (75, 10))

    # score text
    text = SCORE_TEXT_FONT.render("Score", True, RED)
    win.blit(text, (225, 10))

    scoreText = SCORE_FONT.render(f"{score}", True, WHITE)
    win.blit(SCORE_DISPLAY, (225, 40))
    win.blit(scoreText, (240, 50))

    # Buttons
    for btn in buttons:
        btn.draw(win)
    
    if goBoard:
        goBoard.draw(win)

    if hsBoard:
        hsBoard.draw(win)

    if msgBoard:
        msgBoard.draw(win)
    
    pygame.display.update()




# MAIN
def main():
    grid = Grid()
    grid.resetNewRound()

    goBoard = GameOverBoard()
    hsBoard = HighscoreBoard()

    msgBoard = MessageBoard()

    buttons = []

    # Create button 
    y = 10
    for title in ['New Game', 'HighScores', 'Exit']:
        btn = Button(x=405, y=y, text=title, bgColor=(247, 245, 141), fontColor=(70, 73, 242))
        buttons.append(btn)
        y += 40

    # Create button 
    btnX = 225
    for title in ['Save', 'Undo']:
        btn = Button(x=btnX, y=95, text=title, width=32, height=32)

        mainImgUrl = getFullPath(f'./images/{title.lower()}.png')
        pressedImgUrl = getFullPath(f'./images/{title.lower()}Pressed.png')
        btn.imageConfig(pygame.image.load(mainImgUrl), pygame.image.load(pressedImgUrl))
        buttons.append(btn)
        btnX += 90

    selectedSquare = None
    gotoSquare = None

    score = 0
    gameOver = False
    overlay = False

    startSong = SOUNDS_EFFECT.get('start').play(-1)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        draw(WIN, grid, buttons, score, goBoard, hsBoard, msgBoard)

        if not gameOver:
            score += grid.checking(WIN, score)

        # Loop through all events in 1 frames
        for event in pygame.event.get():

            # Get mouse position
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                break

            # Event for left mouse click
            if pygame.mouse.get_pressed()[0]:
                if not gameOver and not overlay:
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
                                moved = grid.findShortestPath(WIN, selectedSquare, gotoSquare)

                                if moved:
                                    SOUNDS_EFFECT.get('moved').play()
                                    point = grid.checking(WIN, score)
                                    selectedSquare = None
                                    gotoSquare = None
                                    score += point

                                    if point == 0:
                                        grid.grownUp()
                                        grid.makeBabies()
                                
                                else:
                                    SOUNDS_EFFECT.get('cantMoved').play()
                                    selectedSquare.selected = True
                            
                            else:
                                selectedSquare.selected = False
                                spot.selected = True
                                selectedSquare = spot
                
                if gameOver:
                    # Gameover Button
                    for btn in goBoard.buttons:
                        if btn.isPointed(pos):
                            btn.isPressed = True
                
                if overlay:
                    if hsBoard.activated:
                        # Highscore Board Button
                        for btn in hsBoard.buttons:
                            if btn.isPointed(pos):
                                btn.isPressed = True
                    
                    if msgBoard.activated:
                        for btn in msgBoard.buttons:
                            if btn.isPointed(pos):
                                btn.isPressed = True

                # Ingame buttons
                for button in buttons:
                    if button.isPointed(pos):
                        button.isPressed = True
            
            # Detect release mouse after clicked
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:               # Left mouse click
                    # Ingame Buttons
                    for button in buttons:
                        if button.isPressed:
                            button.isPressed = False

                            if button.text == "New Game":
                                selectedSquare = None
                                gotoSquare = None
                                score = 0
                                grid.resetNewRound()
                                SOUNDS_EFFECT.get('newgame').play()
                                gameOver = False
                                overlay = False
                                goBoard.activated = False
                                hsBoard.activated = False
                                msgBoard.activated = False
                            
                            if button.text == "HighScores":
                                overlay = True
                                hsBoard.activated = True

                            if button.text == "Exit":
                                overlay = True
                                msgBoard.activated = True
                                msgBoard.invokeMessage('Exit Game', 'Your score wont be saved? Continue?')
                            
                            if button.text == "Save":
                                overlay = True
                                msgBoard.activated = True
                                msgBoard.invokeMessage('Save Game', 'Are you sure to stop playing?')
                            
                            if button.text == "Undo" and not gameOver:
                                SOUNDS_EFFECT.get('undo').play()
                                score = grid.undo()
                    
                    # Game Over Board buttons
                    if gameOver:
                        for btn in goBoard.buttons:
                            if btn.isPressed:
                                btn.isPressed = False
                                goBoard.activated = False

                                if btn.text == "Restart":
                                    selectedSquare = None
                                    gotoSquare = None
                                    score = 0
                                    SOUNDS_EFFECT.get('newgame').play()
                                    grid.resetNewRound()
                                    gameOver = False
                                
                                if btn.text == "HighScores":
                                    overlay = True
                                    hsBoard.activated = True

                    if overlay:
                        if hsBoard.activated:
                            for btn in hsBoard.buttons:
                                if btn.isPressed:
                                    btn.isPressed = False
                                    overlay = False
                                    hsBoard.activated = False

                                    if btn.text == "Restart":
                                        selectedSquare = None
                                        gotoSquare = None
                                        score = 0
                                        SOUNDS_EFFECT.get('newgame').play()
                                        grid.resetNewRound()
                                        gameOver = False
                                        goBoard.activated = False
                        
                        if msgBoard.activated:
                            for btn in msgBoard.buttons:
                                if btn.isPressed:
                                    btn.isPressed = False
                                    overlay = False
                                    msgBoard.activated = False

                                    if btn.text == "OK":
                                        if msgBoard.title == "Save Game":
                                            grid.freeSpots = []

                                        if msgBoard.title == "Exit Game":
                                            run = False
                                            break


        if len(grid.freeSpots) <= grid.newBabies:
            if not gameOver:
                goBoard.newHighscore = hsBoard.updateScore(score)

                if goBoard.newHighscore:
                    SOUNDS_EFFECT.get('highscore').play()
                else:
                    SOUNDS_EFFECT.get('gameover').play()
            
            selectedSquare = None
            gotoSquare = None
            gameOver = True
            goBoard.activated = True
            goBoard.score = score