if True:
    import pygame
    from network import Network
    pygame.init()
    width = 1200
    height = 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('MasterMind By Tom Campbell-Oulton') 
    clock = pygame.time.Clock()

    def placePeg(x,y,colour):
        #                       Size
        surface = pygame.Surface((10,10))
        surface.fill(colour)
        #                   Position
        screen.blit(surface, (x,y))
    #    pygame.display.update()  

    def generateRandomBoard(coloursAvailable, numberOfColumns):
        from random import randint
        board = []
        for column in range(numberOfColumns):
            randomColour = randint(0, len(coloursAvailable)-1)
            board.append(coloursAvailable[randomColour])

        return board

    def countNumberOfEachColour(availableColours, chosenColours):
        countOfColours = {}
        for colour in availableColours:
            countOfColours[colour] = chosenColours.count(colour)
        
        return countOfColours

    def checkUsersGuess(guessedColours, correctAnswer, countOfEachCorrectColour, availableColours):
        row = guessedColours
        numberOfColumns = len(correctAnswer)
        corrections = {"Number Correct": 0, "Number Correct Colour": 0, "Number Wrong": 0}

        # Checks if the correct colour is in the correct tile
        count = 0
        for colour in correctAnswer:

            usersGuess = row[count]

            if colour == usersGuess:
                corrections["Number Correct"] += 1
                row[count] = ""
                countOfEachCorrectColour[colour] -= 1
            count += 1

        numberOfEachColourGuessed = countNumberOfEachColour(availableColours, row)  
        for colour in numberOfEachColourGuessed:
            # Number of correct colours in wrong places
            numOfRealColour = countOfEachCorrectColour[colour]
            numOfGuessedColour = numberOfEachColourGuessed[colour] 
            # If the result is zero then they guessed the correct number of that colour
            # Checks the number guessed isn't 0 either
            if numOfRealColour == numOfGuessedColour:
                corrections["Number Correct Colour"] += numOfGuessedColour
                
            # If the result is negative and they didn't guess 0
            # number correct = real - guess
            elif numOfGuessedColour < numOfRealColour and numOfGuessedColour != 0 and numOfRealColour != 0:
                corrections["Number Correct Colour"] += numOfGuessedColour

            # If the result is positive and they didn't guess 0
            # number correct = guess - real 
            elif numOfGuessedColour > numOfRealColour and numOfGuessedColour != 0 and numOfRealColour != 0:
                corrections["Number Correct Colour"] += numOfRealColour

            countOfEachCorrectColour[colour], numberOfEachColourGuessed[colour]  = 0,0

        corrections["Number Wrong"] += numberOfColumns - corrections["Number Correct Colour"] - corrections["Number Correct"]

        return corrections

    def getPegsPositioned(pegColours, x, y):

        white, grey, black = pegColours["white"], pegColours["grey"], pegColours["black"]
        totalPlaced = 0
        for peg in range( white+grey+black):
            if peg < white:
                colour = "green"

            elif peg < white+grey:
                colour = "orange"

            else:
                colour = "red"

            # If odd
            if totalPlaced % 2 == 1:
                newY =  y + 13
                newX = x - (totalPlaced//2 +1)*13
                placePeg(newX,newY,colour)
                
            else:
                newX = x - (totalPlaced//2 + 1)*13
                newY =  y
                placePeg(newX,newY,colour)
            totalPlaced += 1

    def getXCoord(text):
        font = pygame.font.SysFont("Arial", 30)
        renderedText = font.render(text, 1, pygame.Color("White"))
        size = renderedText.get_size()
        xCoord = int((width - size[0])/2)
        return xCoord

    def giveXCoord(longestMessage, width):
        font = pygame.font.SysFont("Arial", 30)
        renderedText = font.render(longestMessage, 1, pygame.Color("White"))
        size = renderedText.get_size()
        xCoord = int((width - size[0])/2)   
        return xCoord

    class Button:
        """Create a button, then blit the surface in the while loop"""
    
        def __init__(self, text,  pos, listOfColours=[], font=0, bg="black", feedback="",submitButton = False, displayLeaderBoardButton = False, newGameButton = False, saveGameButton = False, loadGameButton = False, mainMenu = False, numberButton = False, settingsPageButton = False, plusButton = False, minusButton = False, rangeOfNumbers = 25, currentNumber = 0, listOfButtons = [], loadingGame = False, helpPageButton=False, rulesPageButton = False, multiPlayerButton=False, singlePlayerButton=False, localButton=False, onlineButton=False):

            self.x, self.y = pos
            self.font = pygame.font.SysFont("Arial", font)
            self.currentColour = bg
            self.submit = submitButton
            self.showLeaderboard = displayLeaderBoardButton
            self.newGame = newGameButton
            self.saveGame = saveGameButton 
            self.loadGame = loadGameButton
            self.mainMenu = mainMenu
            self.numberButton = numberButton
            self.currentNumber = currentNumber
            self.rangeOfNumbers = rangeOfNumbers
            self.settingsButton = settingsPageButton
            self.plusButton = plusButton
            self.minusButton = minusButton
            self.loadingGame = loadingGame
            self.helpPage = helpPageButton
            self.rulesPage = rulesPageButton
            self.multiplayer = multiPlayerButton
            self.singleplayer = singlePlayerButton
            self.localGame = localButton
            self.online = onlineButton



            if submitButton:
                text = "Submit ;P"
                self.text = self.font.render(text, 1, pygame.Color("White"))
                self.size = self.text.get_size()
                self.surface = pygame.Surface(self.size)
                self.surface.blit(self.text, (0,0))
            elif displayLeaderBoardButton:
                text = "Display Leaderboards"
                self.text = self.font.render(text, 1, pygame.Color("White"))
                self.size = self.text.get_size()
                self.surface = pygame.Surface(self.size)
                self.surface.blit(self.text, (0,0))
            elif saveGameButton:
                text = "Save Game"
                self.text = self.font.render(text, 1, pygame.Color("White"))
                self.size = self.text.get_size()
                self.surface = pygame.Surface(self.size)
                self.surface.blit(self.text, (0,0))
            elif newGameButton:
                text = "New Game"
                self.text = self.font.render(text, 1, pygame.Color("White"))
                self.size = self.text.get_size()
                self.surface = pygame.Surface(self.size)
                self.surface.blit(self.text, (0,0))
            elif loadGameButton:
                text = "Load Game"
                self.text = self.font.render(text, 1, pygame.Color("White"))
                self.size = self.text.get_size()
                self.surface = pygame.Surface(self.size)
                self.surface.blit(self.text, (self.x, self.y))
            elif mainMenu:
                text = "Main Menu"
                self.text = self.font.render(text, 1, pygame.Color("White"))
                self.size = self.text.get_size()
                self.surface = pygame.Surface(self.size)
                self.surface.blit(self.text, (self.x, self.y))
            elif settingsPageButton:
                text = "Settings Page"
                self.text = self.font.render(text, 1, pygame.Color("White"))
                self.size = self.text.get_size()
                self.surface = pygame.Surface(self.size)
                self.surface.blit(self.text, (self.x, self.y))
            elif plusButton:
                text = "+"
                self.text = self.font.render(text, 1, pygame.Color("White"))
                self.size = self.text.get_size()
                self.surface = pygame.Surface(self.size)
                self.surface.blit(self.text, (self.x, self.y))
            elif minusButton:
                text = "-"
                self.text = self.font.render(text, 1, pygame.Color("White"))
                self.size = self.text.get_size()
                self.surface = pygame.Surface(self.size)
                self.surface.blit(self.text, (self.x, self.y))
            elif helpPageButton:
                text = "Help Page"
                self.text = self.font.render(text, 1, pygame.Color("White"))
                self.size = self.text.get_size()
                self.surface = pygame.Surface(self.size)
                self.surface.blit(self.text, (self.x, self.y))
            elif rulesPageButton:
                text = "Rules Page"
                self.text = self.font.render(text, 1, pygame.Color("White"))
                self.size = self.text.get_size()
                self.surface = pygame.Surface(self.size)
                self.surface.blit(self.text, (self.x, self.y))
            elif singlePlayerButton:
                text = "Single Player"
                self.text = self.font.render(text, 1, pygame.Color("White"))
                self.size = self.text.get_size()
                self.surface = pygame.Surface(self.size)
                self.surface.blit(self.text, (self.x, self.y))
            elif multiPlayerButton:
                text = "Multi Player"
                self.text = self.font.render(text, 1, pygame.Color("White"))
                self.size = self.text.get_size()
                self.surface = pygame.Surface(self.size)
                self.surface.blit(self.text, (self.x, self.y))
            elif localButton:
                text = "Local"
                self.text = self.font.render(text, 1, pygame.Color("White"))
                self.size = self.text.get_size()
                self.surface = pygame.Surface(self.size)
                self.surface.blit(self.text, (self.x, self.y))
            elif onlineButton:
                text = "Online"
                self.text = self.font.render(text, 1, pygame.Color("White"))
                self.size = self.text.get_size()
                self.surface = pygame.Surface(self.size)
                self.surface.blit(self.text, (self.x, self.y))

            elif feedback == "":
                self.feedback = "text"
            else:
                self.feedback = feedback       
            change = 1
            # hard bit
            if  submitButton or displayLeaderBoardButton or newGameButton or saveGameButton or loadGameButton or mainMenu or settingsPageButton or plusButton or minusButton or helpPageButton or rulesPageButton or singlePlayerButton or multiPlayerButton or localButton or onlineButton:
                change = 0
            if self.numberButton:
                bg = self.get_next_number(change, rangeOfNumbers)
                self.change_number(change, rangeOfNumbers)
            else:
                if self.loadingGame == False:
                    bg = self.get_next_colour(listOfColours, change)
                    self.change_colour(listOfColours, change)       
    
        def get_next_number(self, change, rangeOfNumbers):
            if int(self.currentNumber) + change > rangeOfNumbers:
                self.currentNumber = 1
            elif int(self.currentNumber) + change < 1:
                self.currentNumber = rangeOfNumbers
            else:
                self.currentNumber = change + int(self.currentNumber)

        def change_number(self, change, rangeOfNumbers):
            x,y = 50, 50
            self.size = [x,y]
            self.surface = pygame.Surface((x,y))
            self.get_next_number(change, rangeOfNumbers)
            text = str(self.currentNumber)

            clearScreen(50,50, self.x, self.y)

            self.font = pygame.font.SysFont("Arial", 30)
            self.text = self.font.render(text, 1, pygame.Color("White"))
            self.size = self.text.get_size()
            self.surface = pygame.Surface(self.size)
            self.surface.blit(self.text, (self.x, self.y))

            self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
            self.show()
            #pygame.display.update() 

        def get_next_colour(self, listOfColours, direction):
            currentColour = self.currentColour
            if direction == 1:
                # If the current colour is the last in the list
                if currentColour == listOfColours[-1]:
                    # Sets colour to start of the list
                    self.currentColour = listOfColours[0]
                else:
                    # Sets the colour to the next in line ;)
                    self.currentColour = listOfColours[listOfColours.index(currentColour)+1]
            elif direction == -1:
                # If the current colour is the first in the list
                if currentColour == listOfColours[0]:
                    # Sets colour to start of the list
                    self.currentColour = listOfColours[-1]
                else:
                    # Sets the colour to the previous in line ;)
                    self.currentColour = listOfColours[listOfColours.index(currentColour)-1]

        def submit_answer(self):
            pass

        def change_colour(self, listOfColours, direction):
            """Change the text when you click"""
            if self.submit or self.showLeaderboard or self.newGame or self.loadGame or self.mainMenu or self.settingsButton or self.plusButton or self.minusButton or self.saveGame or self.helpPage or self.rulesPage or self.singleplayer or self.multiplayer or self.localGame or self.online:
                x,y = self.size
            else:
                x,y = 50,50

            # Affects where the click is registered
            self.size = [x,y]
            # Affects where the button is visually drawn
            self.surface = pygame.Surface((x,y))
            self.get_next_colour(listOfColours, direction)
            bg = self.currentColour

            self.surface.fill(bg)
            self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
            self.show()
            #pygame.display.update()   
    
        def show(self):
            screen.blit(self.surface, (self.x, self.y))
            if self.submit:
                self.surface.blit(self.text, (0, 0))
            elif self.showLeaderboard:
                self.surface.blit(self.text, (0, 0))
            elif self.loadGame:
                self.surface.blit(self.text, (0, 0))
            elif self.saveGame:
                self.surface.blit(self.text, (0, 0))
            elif self.newGame:
                self.surface.blit(self.text, (0, 0))
            elif self.mainMenu:
                self.surface.blit(self.text, (0, 0))
            elif self.numberButton:
                self.surface.blit(self.text, (0,0))
            elif self.settingsButton:
                self.surface.blit(self.text, (0,0))
            elif self.plusButton:
                self.surface.blit(self.text, (0,0))
            elif self.minusButton:
                self.surface.blit(self.text, (0,0))
            elif self.helpPage:
                self.surface.blit(self.text, (0,0))
            elif self.rulesPage:
                self.surface.blit(self.text, (0,0))
            elif self.singleplayer:
                self.surface.blit(self.text, (0,0))
            elif self.multiplayer:
                self.surface.blit(self.text, (0,0))
            elif self.localGame:
                self.surface.blit(self.text, (0,0))
            elif self.online:
                self.surface.blit(self.text, (0,0))

            pygame.display.update()
    
        def getSize(self):
            return self.size

        def click(self, event, listOfColours=[]):
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed():
                    if self.rect.collidepoint(x, y):
                        
                        # event.button:
                        # 1 = Left click
                        # 2 = Middle Click
                        # 3 = Right Click
                        # 4 = Scroll Up
                        # 5 = Scroll Down

                        if event.button == 1 or event.button == 4:
                            direction = 1

                        elif event.button == 3 or event.button == 5:
                            direction = -1

                        if event.button in [1,3,4,5]:
                            # If the button isn't submit ;)
                            wants = "Nothing"
                            if  not (self.submit or self.showLeaderboard or self.newGame or self.loadGame or self.saveGame or self.mainMenu or self.settingsButton or self.plusButton or self.minusButton or self.helpPage or self.rulesPage or self.singleplayer or self.multiplayer or self.localGame or self.online):
                                if self.numberButton:
                                    self.change_number(direction, self.rangeOfNumbers)
                                    self.show()
                                else:
                                    self.change_colour(listOfColours, direction)
                                    self.show()
                                #pygame.display.update()  
                            
                            

                            elif event.button in [1,3]:   
                                if self.showLeaderboard:
                                    wants = "Leaderboard"

                                elif self.newGame:
                                    wants = "NewGame"

                                elif self.saveGame:
                                    wants = "SaveGame"

                                elif self.loadGame:
                                    wants = "LoadGame"

                                elif self.submit:
                                    wants = "Submit"

                                elif self.mainMenu:
                                    wants = "MainMenu"

                                elif self.settingsButton:
                                    wants = "SettingsPage"

                                elif self.minusButton:
                                    wants = "-"

                                elif self.plusButton:
                                    wants = "+"

                                elif self.helpPage:
                                    wants = "Help"

                                elif self.rulesPage:
                                    wants = "Rules"

                                elif self.multiplayer:
                                    wants = "MultiPlayer"
                                
                                elif self.singleplayer:
                                    wants = "SinglePlayer"

                                elif self.localGame:
                                    wants = "Local"
                                
                                elif self.online:
                                    wants = "Online"

                                else:
                                    wants = "Glitch"

                            return wants 
                
        def getCurrentColour(self):
            return self.currentColour

        def checkSubmitButton(self):
            return self.submit

        def checkLeaderboardButton(self):
            return self.showLeaderboard
        
        def checkNewGameButton(self):
            return self.newGame

        def checkSaveGameButton(self):
            return self.saveGame
        
        def checkLoadGameButton(self):
            return self.loadGame

        def checkMainMenu(self):
            return self.mainMenu

        def checkSettingsButton(self):
            return self.settingsButton

    def getAnswers(allButtons, specialCase = False):
        answers = []
        if specialCase:
            legalButtons = allButtons[:-1]
        else:
            legalButtons = allButtons[:-2]
        for button in legalButtons:
            if button.checkSubmitButton() == False:
                ans = button.getCurrentColour()
                answers.append(ans)

        return answers

    def getPegColours(numCorrectColourAndPosition, numberCorrectColour, numberWrong):
        colouredPegs = {"white":numCorrectColourAndPosition, "grey":numberCorrectColour, "black":numberWrong}
        return colouredPegs
    
    def leaderboardPage(width, height, currentNumber, colours, numberOfColumns, numberOfRows):
        clearScreen(width, height)

        font = pygame.font.SysFont(None,60)
        img = font.render("Leaderboards!", True, "White")
        screen.blit(img,(giveXCoord("Leaderboards!", width)-50,50))

        font = pygame.font.SysFont(None,70)
        img = font.render("Score", True, "White")
        screen.blit(img,(100,80))
            
        font = pygame.font.SysFont(None,70)
        img = font.render("Date", True, "White")
        screen.blit(img,(300,80))

        font = pygame.font.SysFont(None,40)
        for i in range(15):
            img = font.render(f"{i+1}. ", True, "White")
            screen.blit(img,(75, 150 + i*55))


        mainMenuButton = Button("Main Menu", (width-127, 5), colours, font=30, bg="Red", mainMenu=True)


        buttons = [mainMenuButton]
        for button in buttons:
            button.show()
            clock.tick(75)


        pygame.display.update()
        leaderPage = True


        doLeaderboardStuff()

        while leaderPage:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  
                for b in buttons:
                    buttonPressed = b.click(event, colours)
                    if buttonPressed == "MainMenu":
                        openGame(width, height, numberOfColumns, numberOfRows, colours)
                        leaderPage = False
                        
    def getLeaderBoardPeople(numberOfColumns, numberOfColours):
        from os import getcwd
        basePath = getcwd()
        fileName = f"{numberOfColumns}-{numberOfColours}"
        filePath = f"{basePath}\\{fileName}.txt"
        file = open(filePath)
        data = file.readlines()
        info = []
        for line in data:
            date = line[2:14]
            name = line[14:]
            numberOfMoves = line[:2]
            info.append([numberOfMoves, name, date])
        file.close()
        return info

    def displayLeaderboardData(data):
        # Format:
        # Number Of Moves
        # Player name?
        # Date



        for i in range(len(data)):
            text = f"{data[i]}"
            x = 115
            y = 150 + 55*i
            if "\n" in text:
                text = text.replace("\n","")
            font = pygame.font.SysFont(None,40)
            img = font.render(text, True, "White")
            screen.blit(img,(x,y))


        pygame.display.update()

    def makeNewFile(numOfColumns, numOfColours):
        from os import getcwd
        basePath = getcwd()
        fileName = f"{numOfColumns}-{numOfColours}.txt"
        path = f"{basePath}\\{fileName}"
        f = open(path, "w")
        f.close()

    def writeToFile(filePath, numOfMovesUsed, name="Tom"):
        try:
            file = open(filePath, "r")
            data = file.read()
            file.close()
        except:
            data = "\n"
        alreadyAdded = False
        newData = ""
        oldData = data.split("\n")
        from datetime import datetime
        date = datetime.now().strftime("%y%m%d%H%M%S")
        stringOfData = f"{numOfMovesUsed}{date}{name}"
        for i in range(len(oldData)):
            # Check if old is better than new?
            if len(oldData[i]) > 0:
                numberOfMoves = int(oldData[i][:2])
                if numberOfMoves > numOfMovesUsed and alreadyAdded == False:
                    newData += f"{stringOfData}\n"
                    alreadyAdded = True
            newData += f"{oldData[i]}\n"
        file = open(filePath, "w")
        file.write(newData)
        file.close()

    def doLeaderboardStuff():
        from os import getcwd
        path = getcwd()

        # New Scoring System
        # Score = Number Of Colours * Number Of Columns / Number Of Turns
        

        leaderBoardFile = open(f"{path}/leaderboards.txt", "r")
        leaderBoardData = leaderBoardFile.readlines()
        leaderBoardFile.close()

        displayLeaderboardData(leaderBoardData)

    def updateLeaderboards(numberOfColours, numberOfColumns, numberOfTurns, won=True):
        from os import getcwd
        path = getcwd()
        from datetime import datetime
        date = datetime.now().strftime("          %d.%m.%y - %H:%M:%S")

        if won:
            score = int((numberOfColours * numberOfColumns) ** ((1/(numberOfTurns)))*1000)
            
            scoreString = str(score).replace(" ","")
            listOfScore = list(scoreString)
            print(listOfScore)
            print(f"Length = {len(scoreString)}")
            if len(scoreString) < 6:
                listOfScore.insert(len(scoreString)-3, ",")
                scoreString = "".join(listOfScore)
                numOfCharactersShort = 7-len(scoreString)
                tempString = "  " * numOfCharactersShort
                scoreString = tempString + scoreString
            print(scoreString)
            leaderBoardFile = open(f"{path}/leaderboards.txt", "r")
            leaderBoardData = leaderBoardFile.readlines()
            leaderBoardFile.close()
            count = 0
            for data in leaderBoardData:
                data=data.replace(",","")

            added = False
            while count < len(leaderBoardData):
                if len(leaderBoardData[count]) > 6:
                    d = leaderBoardData[count].replace(" ","").replace(",","")[:-18]
                    value = int(d)
                    if score > value :
                        leaderBoardData.insert(count, str(scoreString)+date+"\n")
                        count = len(leaderBoardData)
                        added = True
                count += 1
            if added == False:
                leaderBoardData.append(str(scoreString+date+"\n"))
            s1 = ""
            for line in leaderBoardData:
                s1 += line

            leaderBoardFile = open(f"{path}/leaderboards.txt", "w")
            leaderBoardFile.write(s1)

            leaderBoardFile.close() 

    def makeButtons(oldx, oldy, numOfColumns, colours):
        buttons = []
        # Regular buttons
        yChange = 70
        mainMenuButton = Button("Main Menu", (width-320, 50), font=30, bg="Red", mainMenu=True)
        saveGameButton = Button("Save Game", (width-170, 50), font=30, bg="Red", saveGameButton = True)
        for i in range(numOfColumns):
            xChange = 60*i
            x = oldx + xChange
            y = oldy + yChange

            button = Button(
            "Click here",
            (x, y),
            colours,
            font=30,
            bg=colours[0],
            feedback="You clicked me")


            buttons.append(button)
        # Submit button
        button = Button(
        "Submit",
        (x+60, y),
        colours,
        font=30,
        bg="Blue",
        feedback="Submitted",
        submitButton=True)
        buttons.append(button)
        newx, newy = oldx, oldy + yChange
        buttons.append(mainMenuButton)
        buttons.append(saveGameButton)
    
        return buttons, newx, newy

    def displayGameOver(gameStatus, screenWidth, screenHeight, listOfColours, numberOfTurns, numberOfColumns, playerName=999, playerScore=0, losersName=999, losersScore=0):
        # gameStatus = True or False
        # True = won
        # False = lost


        # Make the screen blank
        if gameStatus:
            surface = pygame.Surface((screenWidth,screenHeight))
            surface.fill((0,0,0))  
            screen.blit(surface, (0,0))


        # If game won
        if gameStatus:
            # Write a message on the blank screen ;)
            font = pygame.font.SysFont(None,60)
            if playerName == 999:
                img = font.render("You won!", True, "White")
                screen.blit(img,(180,300))
                text = font.render(f"The number of turns you used: {numberOfTurns}", 1, "White")
                screen.blit(text,(180,400))
                text = font.render(f"The number of columns: {numberOfColumns}", 1, "White")
                screen.blit(text,(180,500))
                text = font.render(f"The number of colours: {len(listOfColours)}", 1, "White")
                screen.blit(text,(180,600))
                score = int((len(listOfColours) * numberOfColumns) ** ((1/(numberOfTurns)))*1000)


                font = pygame.font.SysFont(None,60)
                img = font.render(f"Your Score:      {score}", True, "White")

                screen.blit(img,(180,450))       
    
            else:
                img = font.render(f"Player {playerName} won!", True, "White")
                score = playerScore    
                screen.blit(img,(180,300))
                font = pygame.font.SysFont(None,60)
                img = font.render(f"Player {playerName}'s Score:      {score}", True, "White")
                img2 = font.render(f"Player {losersName}'s Score:      {losersScore}", True, "White")
                screen.blit(img,(180,450))
                screen.blit(img2,(180,550))
        pygame.display.update()
        # Now add the buttons :3
        buttons = []
        mainMenuButton = Button("Main Menu", (1000, 30), listOfColours, font=30, bg="Red", mainMenu=True)

        buttons.append(mainMenuButton)


        for button in buttons:
            button.show()
            clock.tick(75)

        return buttons

    def clearScreen(width,height,x=0,y=0):
        pygame.draw.rect(screen, "Black", pygame.Rect(x,y,width,height))
      
    def runGame(n, numberOfColumns, width, height, listOfColours, allPegs = [], allUsersAnswers = [], numberOfTurnsUsed = 0, board=[], answers=[]):
        numberOfRowsLeft = n
        # Create the buttons for the initial row
        
        if numberOfTurnsUsed == 0:

            buttons, oldx, oldy = makeButtons(100, 30, numberOfColumns, listOfColours)
            if len(answers) == 0:
                board = generateRandomBoard(listOfColours, numberOfColumns)
            else:
                board = answers
            print(f"Board = {board}")
            gameOn = True

            clearScreen(width, height)
            pygame.font.init()
            myFont = pygame.font.SysFont("Comic Sans MS", 30)
            textSurface = myFont.render(f"Number Of Rows Remaining: {numberOfRowsLeft}", False, (100,100,100))
            size = textSurface.get_size()
            surface = pygame.Surface(size)
            surface.blit(textSurface, (0, 0))
            screen.blit(textSurface, (50,10))

        else:
            buttons, oldx, oldy = makeButtons(100, 30+70*numberOfTurnsUsed, numberOfColumns, listOfColours)

        gameOn = True
        lost = False
        while gameOn:
            # Start the game
            buttons, oldx, oldy, numberOfRowsLeft, gameOn =  displayGame(buttons, listOfColours, oldx, oldy, numberOfColumns, board, numberOfRowsLeft, gameOn, board, width, height, allPegs, allUsersAnswers, numberOfRows=n)

            won = False
            # If the game is over
            if gameOn == False:
                won = True
                pygame.time.delay(1000)


            # If the game isn't over :(
            elif numberOfRowsLeft == 0:
                print("You failed as a human being T_T")
                clearScreen(width, height)
                # Show their final input
                # Show the real answer XD

                writeText("You lost... You disappoint me. :(", 130, 200, fontColour="Red", fontSize=75)

                writeText("Answer: ",200,400)
                x,y = 350,400
                for ans in board:
                    surface = pygame.Surface((50,50))
                    surface.fill(ans)
                    screen.blit(surface, (x, y)) 
                    x += 60
                
                writeText("Your Input: ",200,600)
                x,y = 350,600
                for colour in allUsersAnswers[-1][:-2]:
                    surface = pygame.Surface((50,50))
                    surface.fill(colour)
                    screen.blit(surface, (x, y)) 
                    x += 60

                pygame.display.update()
                pygame.time.delay(2000)
                gameOn = False
                lost = True

        numberOfTurnsUsed = n-numberOfRowsLeft
        updateLeaderboards(len(listOfColours), numberOfColumns, numberOfTurnsUsed, not lost)
        return won, numberOfTurnsUsed

    def displayGame(buttons, listOfColours, oldx, oldy, numberOfColumns, correctAnswer, numberOfRowsLeft, gameOn, board, screenWidth, screenHeight, allPegs = [], allUsersAnswers = [], numberOfRows=10):
        # Display board and all that
        # Checks if the game is closed or not ;P
        # Draw all the coloured Boxes

        showColoursForPage(len(listOfColours), listOfColours, screenWidth, screenHeight)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Checks if each button has been clicked yet ;)
            createNewRow = False
            for b in buttons:
                wantAns = b.click(event, listOfColours)
                if wantAns == "Submit":
                    answers = getAnswers(buttons)
                    answersToWrite = []
                    counterVariable = 0
                    for ans in answers:

                        if ans == "":
                            answersToWrite.append(correctAnswer[counterVariable])
                        else:
                            answersToWrite.append(ans)
                        counterVariable += 1
                    allUsersAnswers.append(answersToWrite)

                    # ******************************* IMPORTANT ***********************************
                    # Need to display new row

                    # Ends the loop
                    b = buttons[-1]
                    # Initiate creation of new row

                    countOfEachCorrectColour = countNumberOfEachColour(listOfColours, board)
                    corrections =  checkUsersGuess(answers, correctAnswer, countOfEachCorrectColour, listOfColours)
                    right, kindaRight, wrong = corrections["Number Correct"], corrections["Number Correct Colour"], corrections["Number Wrong"]
                    pegColours = getPegColours(right, kindaRight, wrong)
                    allPegs.append(pegColours)
                    if pegColours["white"] ==  pegColours["white"] +  pegColours["grey"] +  pegColours["black"]:
                        gameOn = False
                    allPegs.append(pegColours)
                    getPegsPositioned(pegColours, oldx, oldy)
                    numberOfRowsLeft -=1


                    if numberOfRowsLeft > 0:
                        createNewRow = True
                        clearScreen(screenWidth, 50)

                elif wantAns == "SaveGame":
                    saveGame(numberOfColumns, numberOfRows, listOfColours, correctAnswer, numberOfRowsLeft, allUsersAnswers, allPegs)

                elif wantAns == "MainMenu":
                    #numberOfColumns=5, numberOfRows=12, listOfColours=[], screenWidth=1200, screenHeight=900, allPegs = [], allUsersAnswers = []
                    mainMenu(numberOfColumns, numberOfRows, listOfColours,screenWidth,screenHeight)

            if createNewRow:
                buttons, oldx, oldy = makeButtons(oldx, oldy, numberOfColumns, listOfColours)
                mainMenuButton = Button("Main Menu", (screenWidth-320, 50), font=30, bg="Red", mainMenu = True)
                saveGameButton = Button("Save Game", (screenWidth-170, 50), font=30, bg="Red", saveGameButton = True)
                buttons.append(mainMenuButton)
                buttons.append(saveGameButton)

                mainMenuButton.show()
                saveGameButton.show()
                pygame.font.init()
                myFont = pygame.font.SysFont("Comic Sans MS", 30)
                textSurface = myFont.render(f"Number Of Rows Remaining: {numberOfRowsLeft}", False, (100,100,100))
                size = textSurface.get_size()
                surface = pygame.Surface(size)
                surface.blit(textSurface, (0, 0))
                screen.blit(textSurface, (50,10))

        # Displays the button
        for button in buttons:
            button.show()
            clock.tick(75)


        # Display how many turns left:


        return buttons, oldx, oldy, numberOfRowsLeft, gameOn

    def mainMenu(numberOfColumns=5, numberOfRows=12, listOfColours=[], screenWidth=1200, screenHeight=900, allPegs = [], allUsersAnswers = []):
        # Make the screen blank
        surface = pygame.Surface((screenWidth,screenHeight))
        surface.fill((0,0,0))  
        screen.blit(surface, (0,0))


        # Now add the buttons :3
        buttons = []
        longestLabel = "Show Leaderboard"
        #helpPage(numberOfColumns, numberOfRows, listOfColours, screenWidth, screenHeight)
        helpPageButton = Button("Help Page", (giveXCoord(longestLabel, screenWidth)+49, 580), listOfColours, font=30, bg="Salmon", helpPageButton=True)
        rulesPageButton = Button("Rules Page", (giveXCoord(longestLabel, screenWidth)+40, 650), listOfColours, font=30, bg="navyblue", rulesPageButton=True)
        showLeaderBoardButton = Button("Show Leaderboard", (giveXCoord(longestLabel, screenWidth), 300), listOfColours, font=30, bg="deeppink4", displayLeaderBoardButton=True)
        newGameButton = Button("New Game", (giveXCoord(longestLabel, screenWidth)+50, 370), listOfColours, font=30, bg="Red", newGameButton=True)
    # saveGameButton = Button("Save Game", (xCoord, 440), listOfColours, font=30, bg="Red", saveGameButton=True)
        loadGameButton = Button("Load Game", (giveXCoord(longestLabel, screenWidth)+47, 440), listOfColours, font=30, bg="Green", loadGameButton=True)
        settingsPageButton = Button("Settings", (giveXCoord(longestLabel, screenWidth)+34, 510), listOfColours, font=30, bg="darkgreen", settingsPageButton = True)

        buttons.append(helpPageButton)
        buttons.append(rulesPageButton)
        buttons.append(settingsPageButton)
        buttons.append(showLeaderBoardButton)
        buttons.append(newGameButton)
        buttons.append(loadGameButton)


    # writeText(text, x, y,fontsize, fontcolour)
        writeText("Master Mind", 350, 150, 120, "White")
        writeText("By Tom Campbell Oulton", 680, 220, 20, "White")

        for button in buttons:
            button.show()
            clock.tick(75)


        running = True
        numberOfTurns = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  
                for b in buttons:
                    buttonPressed = b.click(event, listOfColours)
                    if buttonPressed == "Leaderboard":
                        currentNumber = 1
                        running = False
                        leaderboardPage(screenWidth, screenHeight, currentNumber, listOfColours, numberOfColumns, numberOfRows)
                    
                    elif buttonPressed == "NewGame":
                        singleOrMultiPage(numberOfColumns, numberOfRows,screenWidth, screenHeight, listOfColours, allPegs, allUsersAnswers)


                    elif buttonPressed == "LoadGame":
                        loadGame(screenWidth, screenHeight)

                    elif buttonPressed == "SettingsPage":
                        clearScreen(screenWidth, screenHeight)
                        widthNum, heightNum, columnNum, rowNum, listOfColours = settingsPage(screenWidth,screenHeight, numberOfColumns, numberOfRows, len(listOfColours), ["Yellow", "Red", "Orange", "Blue", "Purple",  "Green", "Cyan", "darkblue", "darkgreen", "deeppink4", "pink", "Crimson", "Coral",  "darksalmon"])
                        mainMenu(columnNum, rowNum, listOfColours, widthNum, heightNum)
                    
                    elif buttonPressed == "Help":
                        clearScreen(screenWidth, screenHeight)
                        helpPage(numberOfColumns, numberOfRows, listOfColours, screenWidth, screenHeight)

                    elif buttonPressed == "Rules":
                        clearScreen(screenWidth, screenHeight)
                        rulesPage(numberOfColumns, numberOfRows, listOfColours, screenWidth, screenHeight)
        won = False
        return won, screenWidth,screenHeight, numberOfColumns, numberOfRows, listOfColours, numberOfTurns

    def changeListOfColours(newLength):
        colourList = ["Yellow", "Red", "Orange", "Blue", "Purple",  "Green", "Cyan", "darkblue", "darkgreen", "deeppink4", "pink", "Crimson", "Coral",  "darksalmon"]
        newColourList = colourList[:newLength]
        return newColourList

    def openGame(width, height, numberOfColumns, numberOfRows, colours, allPegs = [], allUsersAnswers = []):
                                                                                                
        won, screenWidth,screenHeight, numberOfColumns, numberOfRows, listOfColours, numberOfTurns = mainMenu(numberOfColumns, numberOfRows, listOfColours=colours, screenWidth=width, screenHeight=height, allPegs=allPegs, allUsersAnswers=allUsersAnswers)

        buttons = displayGameOver(won, screenWidth, screenHeight, listOfColours, numberOfTurns, numberOfColumns)
        

        return buttons, screenWidth,screenHeight, numberOfColumns, numberOfRows, listOfColours

    def showColoursForPage(numOfColours, listOfColours, screenWidth, screenHeight):
        clearScreen(210, screenHeight-200, x=screenWidth-210, y=200)
        writeText("Available Colours:",screenWidth-270,150, fontSize=35, fontName="Arial")
        for colourIndex in range(numOfColours):
            if colourIndex < 6:
                x = screenWidth-90
                y = 200+(colourIndex*55)
            elif colourIndex < 12:
                x = screenWidth-150
                y = 200+((colourIndex-6)*55)
            else:
                x = screenWidth-210
                y = 200+((colourIndex-12)*55)                
            currentColour = listOfColours[colourIndex]
            # Affects where the button is visually drawn
            surface = pygame.Surface((50,50))
            surface.fill(currentColour)
 
            screen.blit(surface, (x, y)) 


    def settingsPage(screenWidth,screenHeight, numberOfColumns, numberOfRows, numberOfColours, listOfColours):

        if True:
            columnNum = numberOfColumns
            rowNum = numberOfRows
            numOfColours = numberOfColours
            heightNum = screenHeight
            widthNum = screenWidth
            # Make the screen blank
            surface = pygame.Surface((screenWidth,screenHeight))
            surface.fill((0,0,0))  
            screen.blit(surface, (0,0))


            # Now add the buttons :3
            buttons = []
            longestLabel = "Show Leaderboard"
            resolution = (screenWidth,screenHeight)

            xTitle = screenWidth//2 -200
            x = screenWidth//4 -200
            fontSize = 40
            # Show titles:
            writeText ("Settings Page", xTitle,50, fontSize+10)
            writeText ("Resolution", x,120, fontSize)
            writeText ("Number Of Columns", x,160, fontSize)
            writeText ("Number Of Rows", x,200, fontSize)
            writeText ("Number Of Colours", x,240, fontSize)
            
            x2 = screenWidth//4 + 200
            x3 = screenWidth//4 + 600
            writeText (f"{screenWidth}", x2,120, fontSize)
            writeText (f"{screenHeight}", x3,120, fontSize)
            writeText (f"{numberOfColumns}", x2,160, fontSize)
            writeText (f"{numberOfRows}", x2,200, fontSize)
            writeText (f"{numOfColours}", x2,240, fontSize)
        
            #pb = plus button
            #mb = minues button

            mainMenuButton = Button("Main Menu", (screenWidth-320, 50), font=30, bg="Red", mainMenu=True)
            pb1 = Button("+", (x2-20, 110), font=30, plusButton=True)
            mb1 = Button("-", (x2+80, 110), font=30, minusButton=True)
            pb2 = Button("+", (x2-20, 150), font=30, plusButton=True)
            mb2 = Button("-", (x2+80, 150), font=30, minusButton=True)
            pb3 = Button("+", (x2-20, 190), font=30, plusButton=True)
            mb3 = Button("-", (x2+80, 190), font=30, minusButton=True)
            pb4 = Button("+", (x2-20, 230), font=30, plusButton=True)
            mb4 = Button("-", (x2+80, 230), font=30, minusButton=True)
            pb5 = Button("+", (x3-20, 110), font=30, plusButton=True)
            mb5 = Button("-", (x3+100, 110), font=30, minusButton=True)
            buttons.append(mainMenuButton)
            buttons.append(pb1)
            buttons.append(mb1)
            buttons.append(pb2)
            buttons.append(mb2)
            buttons.append(pb3)
            buttons.append(mb3)
            buttons.append(pb4)
            buttons.append(mb4)
            buttons.append(pb5)
            buttons.append(mb5)
            
        #+-
        for button in buttons:
            button.show()
            clock.tick(75)
        
        showColoursForPage(numOfColours, listOfColours, screenWidth, screenHeight)
        pygame.display.update()

        font = pygame.font.SysFont("Arial", fontSize)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  
                for b in buttons:
                    buttonPressed = b.click(event)
                    if buttonPressed == "MainMenu":

                        running = False
                        
                    elif buttonPressed == "-":
                        if b == mb1:
                            t = str("Width")
                            if widthNum > 600:
                                widthNum -= 10
                            n=widthNum
                            text = font.render(t, 1, pygame.Color("White"))
                            size = text.get_size()
                            clearScreen(size[0], size[1], x2, 110)
                            newX = x2
                            newY = 120
                        elif b == mb2:
                            t = str("Num")
                            if columnNum > 1:
                                columnNum -= 1
                            n=columnNum
                            text = font.render(t, 1, pygame.Color("White"))
                            size = text.get_size()
                            clearScreen(size[0], size[1], x2, 150)
                            newX = x2
                            newY = 160
                        elif b == mb3:  
                            t = str("Num")
                            if rowNum > 2:
                                rowNum -= 1
                            n=rowNum
                            text = font.render(t, 1, pygame.Color("White"))
                            size = text.get_size()
                            clearScreen(size[0], size[1], x2, 190)
                            newX = x2
                            newY = 200
                        elif b == mb4:
                            t = str("Num")
                            if numOfColours > 1:
                                numOfColours -= 1
                            n=numOfColours
                            text = font.render(t, 1, pygame.Color("White"))
                            size = text.get_size()
                            clearScreen(size[0], size[1], x2, 230)
                            showColoursForPage(numOfColours, listOfColours, screenWidth, screenHeight)
                            newX = x2
                            newY = 240
                        elif b == mb5:
                            t = str("Height")
                            if heightNum > 720:
                                heightNum -= 10
                            n=heightNum
                            text = font.render(t, 1, pygame.Color("White"))
                            size = text.get_size()
                            clearScreen(size[0], size[1], x3, 110)
                            newX = x3
                            newY = 120
                        writeText (f"{n}", newX,newY, fontSize)
                    elif buttonPressed == "+":
                        if b == pb1:
                            t = str("Width")
                            if widthNum < 1920:
                                widthNum += 10
                            n = widthNum
                            text = font.render(t, 1, pygame.Color("White"))
                            size = text.get_size()
                            clearScreen(size[0], size[1], x2, 110)
                            newX = x2
                            newY = 120
                        elif b == pb2:
                            t = str("Num")
                            if columnNum < 11:
                                columnNum += 1
                            n=columnNum
                            text = font.render(t, 1, pygame.Color("White"))
                            size = text.get_size()
                            clearScreen(size[0], size[1], x2, 150)
                            newX = x2
                            newY = 160
                        elif b == pb3:
                            t = str("Num")
                            if rowNum < 12:
                                rowNum += 1
                            n=rowNum
                            text = font.render(t, 1, pygame.Color("White"))
                            size = text.get_size()
                            clearScreen(size[0], size[1], x2, 190)
                            newX = x2
                            newY = 200
                        elif b == pb4:
                            t = str("Num")
                            if numOfColours < 14:
                                numOfColours += 1
                            n=numOfColours
                            text = font.render(t, 1, pygame.Color("White"))
                            size = text.get_size()
                            clearScreen(size[0], size[1], x2, 230)
                            showColoursForPage(numOfColours, listOfColours, screenWidth, screenHeight)
                            newX = x2
                            newY = 240
                        elif b == pb5:
                            t = str("Height")
                            if heightNum < 1080:
                                heightNum += 10
                            n=heightNum
                            text = font.render(t, 1, pygame.Color("White"))
                            size = text.get_size()
                            clearScreen(size[0], size[1], x3, 110)
                            newX = x3
                            newY = 120
                        writeText (f"{n}", newX,newY, fontSize)

                    pygame.display.update()
        listOfColours = changeListOfColours(numOfColours)
        return widthNum, heightNum, columnNum, rowNum, listOfColours

    def saveGame(numberOfColumns, numberOfRows, colours, answer, numberOfTurnsLeft, listOfUsersAnswers, listOfColouredPegs):
        # saving format
        """
        numberOfColumns
        numberOfRows
        listOfColours
        NumberOfTurnsLeft
        answer
        previous guesses... with pegs
        (e.g. ["red", "green", "blue"]_[white, white, blue]
        ["blue", "orange", "green"]_[white, white, blue]) 

        """
        stringToWrite = ""
        stringToWrite += f"{numberOfColumns}\n"
        stringToWrite += f"{numberOfRows}\n"
        stringToWrite += f"{colours}\n"
        stringToWrite += f"{numberOfTurnsLeft}\n"
        stringToWrite += f"{answer}\n"
        # Write previously written answers
        numberOfAnswersInputted = numberOfRows - numberOfTurnsLeft
        for i in range(numberOfAnswersInputted):
            usersAnswer = listOfUsersAnswers[i]
            colouredPeg = listOfColouredPegs[i]
            # Seperator between answers and coloured pegs is a _
            stringToWrite += f"{usersAnswer}_{colouredPeg}\n"
        # File name will be the time
        from os import getcwd
        basePath = getcwd()
        from datetime import datetime
        date = datetime.now().strftime("%y%m%d%H%M%S")

        filesPath = f"{basePath}/SavedGames/{date}.txt"

        file = open(filesPath, "w")
        file.write(stringToWrite)
        file.close()


    def loadGame(screenWidth=1200, screenHeight= 900):
        # saving format
        """
        numberOfColumns
        numberOfRows
        listOfColours
        NumberOfTurnsLeft
        answer
        previous guesses... with pegs
        (e.g. ["red", "green", "blue"]_[white, white, blue]
        ["blue", "orange", "green"]_[white, white, blue]) 

        """

        from os import getcwd
        basePath = getcwd()
        from os import listdir

        clearScreen(screenWidth, screenHeight)

        filesPath = f"{basePath}/SavedGames/"
        allFiles = listdir(filesPath)
        textFiles = []
        for file in allFiles:
            if file[-3:] == "txt":
                textFiles.append(file)

        newestFile = textFiles[-1]

        file = open(f"{filesPath}{newestFile}", "r")
        data = file.readlines()
        file.close()

        numberOfColumns = int(data[0])
        numberOfRows = int(data[1])
        listOfColours = data[2]
        listOfColours = listOfColours.replace("[","").replace("]","").replace("'","").replace(" ","").replace("\n","").split(",")

        numberOfTurnsRemaining = int(data[3])
        answer = data[4]
        answer = answer.replace("[","").replace("]","").replace("'","").replace(" ","").replace("\n","").split(",")
        previousGuesses = []
        previousPegs = []
        for i in range(len(data) - 5):
            line = data[i+5].split("_")
            line[0] = line[0].replace("[", "").replace("]","").replace("'", "").split(",")
            line[1] = line[1].replace("{", "").replace("}","").replace("'", "").replace("\n","").replace("white","").replace("grey","").replace("black","").replace(":","").split(",")
            for i in range(len(line[1])):
                line[1][i] = int(line[1][i])
            previousGuesses.append(line[0])
            previousPegs.append(line[1])
            
        displayLoadedGame(numberOfColumns, numberOfRows,numberOfTurnsRemaining,previousPegs,previousGuesses, screenWidth, listOfColours, answer,screenWidth, screenHeight)




    def displayLoadedGame(numberOfColumns, numberOfRows, numberOfRowsRemaining, colouredPegs, usersChoices, screenWidth, listOfColours, board,width, height):
        oldx = 100
        oldy = 100
        surface = pygame.Surface((oldx,oldy))

        listOfDictionariesOfPegs = []
        for item in colouredPegs:
            d = {}
            d["white"] = item[0]
            d["grey"] = item[1]
            d["black"] = item[2]
            listOfDictionariesOfPegs.append(d)


        for i in range(numberOfRows-numberOfRowsRemaining):
            buttons = []
            yChange = 70

            for j in range(numberOfColumns):
                xChange = 60*j
                x = oldx + xChange
                size = [10,10]
                bg = usersChoices[i][j]
                surface = pygame.Surface((50,50))
                surface.fill(bg)
                screen.blit(surface, (x,oldy))

            pegColours = listOfDictionariesOfPegs[i]
            getPegsPositioned(pegColours, oldx, oldy)
            oldy += yChange     

        pygame.font.init()
        myFont = pygame.font.SysFont("Comic Sans MS", 30)
        textSurface = myFont.render(f"Number Of Rows Remaining: {numberOfRowsRemaining}", False, (100,100,100))
        size = textSurface.get_size()
        surface = pygame.Surface(size)
        surface.blit(textSurface, (0, 0))
        screen.blit(textSurface, (50,10))
        pygame.display.update()



        won, numberOfTurnsUsed = runGame(numberOfRowsRemaining, numberOfColumns, width, height, listOfColours, allPegs = [], allUsersAnswers = [], numberOfTurnsUsed=numberOfRows-numberOfRowsRemaining, board=board)
        buttons = displayGameOver(won, screenWidth, height, listOfColours, numberOfTurnsUsed, numberOfColumns)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                for b in buttons:
                    buttonPressed = b.click(event, listOfColours)
                    if buttonPressed == "MainMenu":
                        mainMenu(numberOfColumns, numberOfRows, listOfColours, screenWidth, height)


    def writeText(text, x, y, fontSize=30, fontColour="White", fontName = None):
        font = pygame.font.SysFont(fontName,fontSize)
        img = font.render(text, True, fontColour)
        screen.blit(img,(x,y))

    def helpPage(numberOfColumns, numberOfRows, listOfColours, screenWidth, screenHeight):
        writeText("Help Page:",450,30, fontSize=50)

        writeText("Scoring:",100,90, fontSize=40)
        writeText("Score = (Number of colours chosen X number of columns) ^ (1 ÷ number of turns taken)  X 1,000",50,130, fontSize=30, fontColour="Grey")

        writeText("Colours:",100,190, fontSize=40)
        writeText("You can use between 1 and 14 colours, depending on the difficulty you desire.",50,230, fontSize=30, fontColour="Grey")
        writeText("These colours are: yellow, red, orange, blue, purple, green, crimson, coral, cyan,",50,270, fontSize=30, fontColour="Grey")
        writeText("                   dark blue, dark green, dark salmon, deep pink and pink.",50,310, fontSize=30, fontColour="Grey")

        writeText("Saving:",100,410, fontSize=40)
        writeText("You can only save 1 game. Once you save a new game, the old game that you saved is ",50,450, fontSize=30, fontColour="Grey")
        writeText("overridden. When you choose 'Load Game', the newest save will be loaded automatically.",50,490, fontSize=30, fontColour="Grey")

        writeText("Leaderboards:",100,590, fontSize=40)
        writeText("The order on the leaderboards are determined by the higher the score, the higher tha placement.",50,630, fontSize=30, fontColour="Grey")
        writeText("if you were to tie with a previous attempt, the older attempt will be ranked higher. All games played",50,670, fontSize=30, fontColour="Grey")
        writeText("are recorded.",100,710, fontSize=30, fontColour="Grey")

        writeText("How To Change Colours:",100,790, fontSize=40)
        writeText("Left click or scroll up changes the colours in one direction, right click or scroll down changes them in",50,830, fontSize=30, fontColour="Grey")
        writeText(" the opposite direction.",50,870, fontSize=30, fontColour="Grey")


        mainMenuButton = Button("Main Menu", (screenWidth-320, 50), font=30, bg="Red", mainMenu = True)
        mainMenuButton.show()

        buttons = [mainMenuButton]
        while True:   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                for b in buttons:
                    buttonPressed = b.click(event, listOfColours)
                    if buttonPressed == "MainMenu":
                        mainMenu(numberOfColumns, numberOfRows, listOfColours, screenWidth, screenHeight)

    def rulesPage(numberOfColumns, numberOfRows, listOfColours, screenWidth, screenHeight):
        writeText("Rules Page:",450,30, fontSize=50)

        writeText("Scoring:",100,90, fontSize=40)
        writeText("Score = (Number of colours chosen X number of columns) ^ (1 ÷ number of turns taken)  X 1,000",50,130, fontSize=30, fontColour="Grey")

        writeText("Coloured Pegs",100,190, fontSize=40)
        writeText("After each row that you submit, a coloured peg for each coloured tile will appear. If the coloured peg is green, it",50,230, fontSize=30, fontColour="Grey")
        writeText("means that the tile is in the correct place and the correct colour. If the tile is orange, it means you got the right",50,270, fontSize=30, fontColour="Grey")
        writeText("colour just in the wrong position and if it's red, it means it's completely wrong.",50,310, fontSize=30, fontColour="Grey")

        writeText("Goal:",100,410, fontSize=40)
        writeText("You have a limited number of turns to guess the combination of colours in the correct order that the computer",50,450, fontSize=30, fontColour="Grey")
        writeText("generated. the faster you do this, the higher your score.",50,490, fontSize=30, fontColour="Grey")

        mainMenuButton = Button("Main Menu", (screenWidth-320, 50), font=30, bg="Red", mainMenu = True)
        mainMenuButton.show()

        buttons = [mainMenuButton]
        while True:   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                for b in buttons:
                    buttonPressed = b.click(event, listOfColours)
                    if buttonPressed == "MainMenu":
                        mainMenu(numberOfColumns, numberOfRows, listOfColours, screenWidth, screenHeight)


    def singleOrMultiPage(numberOfColumns, numberOfRows,screenWidth, screenHeight, listOfColours, allPegs=[], allUsersAnswers=[]):
        clearScreen(screenWidth, screenHeight)
        # 3 Buttons
        # SinglePlayer, Multiplayer, Main Menu

        writeText("Single Player or", 350, 150, fontSize=90, fontColour="White")
        writeText("Multi Player?", 380, 250, fontSize=90, fontColour="White")
        singePlayerButton = Button("Single Player", (400, 450), font=70, bg="Red", singlePlayerButton = True)
        singePlayerButton.show()
        multiPlayerButton = Button("Multi Player", (420, 550), font=70, bg="Red", multiPlayerButton = True)
        multiPlayerButton.show()
        mainMenuButton = Button("Main Menu", (screenWidth-320, 50), font=30, bg="Red", mainMenu = True)
        mainMenuButton.show()
        pygame.display.update()

        buttons = [mainMenuButton, singePlayerButton, multiPlayerButton]
        while True:   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                for b in buttons:
                    buttonPressed = b.click(event, listOfColours)
                    if buttonPressed == "MainMenu":
                        mainMenu(numberOfColumns, numberOfRows, listOfColours, screenWidth, screenHeight)
                    elif buttonPressed == "SinglePlayer":
                        clearScreen(screenWidth, screenHeight)
                        #running = False
                        won, numberOfTurns = runGame(numberOfRows, numberOfColumns, screenWidth, screenHeight, listOfColours, allPegs, allUsersAnswers)
                        buttons = displayGameOver(won, screenWidth, screenHeight, listOfColours, numberOfTurns, numberOfColumns)
                        onGameOverScreen = True
                        while onGameOverScreen:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                for b in buttons:
                                    buttonPressed = b.click(event, listOfColours)
                                    if buttonPressed == "MainMenu":
                                        mainMenu(numberOfColumns, numberOfRows, listOfColours, screenWidth, screenHeight)
                    elif buttonPressed == "MultiPlayer":
                        localOrNetworked(numberOfColumns, numberOfRows, screenWidth, screenHeight, listOfColours, allPegs, allUsersAnswers)


    def localOrNetworked(numberOfColumns, numberOfRows, screenWidth, screenHeight, listOfColours, allPegs=[], allUsersAnswers=[]):
        clearScreen(screenWidth, screenHeight)
        onlineButton = Button("Online", (400, 450), font=70, bg="Red", onlineButton=True)
        onlineButton.show()
        writeText("Online Multiplayer or ",300,200, fontSize=90)        
        writeText("Local Multiplayer?",350,280, fontSize=90)
        writeText("Online: Not Currently In Game",600,450)
        writeText("Local: One player on your computer chooses the ",600,550)
        writeText("combination of colours for you to geuss.",600,580)
        localButton = Button("Local", (420, 550), font=70, bg="Red", localButton= True)
        localButton.show()
        mainMenuButton = Button("Main Menu", (screenWidth-320, 50), font=30, bg="Red", mainMenu = True)
        mainMenuButton.show()
        pygame.display.update()


        buttons = [mainMenuButton, onlineButton, localButton]
        while True:   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                for b in buttons:
                    buttonPressed = b.click(event, listOfColours)
                    if buttonPressed == "MainMenu":
                        mainMenu(numberOfColumns, numberOfRows, listOfColours, screenWidth, screenHeight)

                    elif buttonPressed == "Local":
                        stillPlaying = True
                        gamesData = []
                        playersScores = [0,0]
                        while stillPlaying:
                            for i in range(2):
                                playerNumber = i + 1
                                clearScreen(screenWidth, screenHeight)
                                answers = getUsersChoiceOfColours(numberOfColumns, listOfColours, numberOfRows,screenWidth,screenHeight,playerNumber)
                                clearScreen(screenWidth, screenHeight)
                                #running = False
                                won, numberOfTurns = runGame(numberOfRows, numberOfColumns, screenWidth, screenHeight, listOfColours, allPegs, allUsersAnswers, answers=answers)
                                gamesData.append([won, numberOfTurns])
                                score = int((len(listOfColours) * numberOfColumns) ** ((1/(numberOfTurns)))*1000)
                                playersScores[i] += score
                                clearScreen(screenWidth, screenHeight)
                                writeText(f"Player 1's Score: {playersScores[0]}",300,400, fontSize=70)
                                writeText(f"Player 2's Score: {playersScores[1]}",300,500, fontSize=70)
                                pygame.display.update()
                                pygame.time.delay(2000)
                            if playersScores[0] != playersScores[1]:
                                stillPlaying = False
                                if playersScores[1] < playersScores[0]:
                                    playerName, playersScore = 1, playersScores[0]
                                    losersName, losersScore = 2, playersScores[1]
                                else:
                                    playerName, playersScore = 2, playersScores[1]
                                    losersName, losersScore = 1, playersScores[0]






                        buttons = displayGameOver(won, screenWidth, screenHeight, listOfColours, numberOfTurns, numberOfColumns, playerName, playersScore, losersName, losersScore)
                        onGameOverScreen = True
                        while onGameOverScreen:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                for b in buttons:
                                    buttonPressed = b.click(event, listOfColours)
                                    if buttonPressed == "MainMenu":
                                        mainMenu(numberOfColumns, numberOfRows, listOfColours, screenWidth, screenHeight)


                    elif buttonPressed == "Online":
                        print("To Be Added")
                        #clearScreen(screenWidth, screenHeight)
                        #pygame.display.update()
                        #goOnline(screen, numberOfColumns, numberOfRows, screenWidth, screenHeight, listOfColours)



    def goOnline(screen, numberOfColumns, numberOfRows, screenWidth, screenHeight, listOfColours):
        run = True
        clock = pygame.time.Clock()
        n = Network()
        player = int(n.getP())
        print("You are player", player)

        while run:
            clock.tick(60)

            try:
                game = n.send("get")
            except:
                run = False
                break
                
            if game.bothWent():
                try:
                    game = n.send("reset")
                except:
                    run = False
                    break


                # Now users have given their board for their opponent to try, they need to try and beat that board

                findingWinner = True
                while findingWinner:
                    findingWinner = getOnlineInputs(screen, game, player, numberOfColumns, listOfColours, numberOfRows,screenWidth,screenHeight, n)


                font = pygame.font.SysFont("comicsans", 90)
                if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                    text = font.render("You Won!", 1, (255,0,0))
                    screen.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
                    text = font.render("The number of turns you used: {}", 1, (255,0,0))
                    screen.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
                    text = font.render(f"The number of columns: {numberOfColumns}", 1, (255,0,0))
                    screen.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
                    text = font.render(f"The number of colours: {len(listOfColours)}", 1, (255,0,0))
                    screen.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
                elif game.winner() == -1:
                    text = font.render("Tie Game!", 1, (255,0,0))
                else:
                    text = font.render("You Lost...", 1, (255, 0, 0))
                screen.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(2000)
                

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()


            redrawWindow(screen, game, player, numberOfColumns, listOfColours, numberOfRows,screenWidth,screenHeight, n)
           

    def getOnlineInputs(screen, game, player, numberOfColumns, listOfColours, numberOfRows,screenWidth,screenHeight, n):
        if player == 0 and game.getScore(player) == 0:
            print("Score is 0 T_T")
            answers = game.get_player_move(1)
            if game.p1Finished:
                clearScreen(screenWidth, screenHeight)
        elif player == 1 and game.getScore(player) == 0:
            answers = game.get_player_move(0)
            if game.p2Finished:
                clearScreen(screenWidth, screenHeight)
        x = str(showUsersTheirOptions(screen, game, player, numberOfColumns, listOfColours, numberOfRows,screenWidth,screenHeight, n, answers))
        game = n.send(x)
        print(f"x = {x}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  
        findingWinner = True
        if game.bothFinished():
            findingWinner = False
            winner = game.winner()
            print(f"The winner is {winner}")
        return findingWinner


    def showUsersTheirOptions(screen, game, player, numberOfColumns, listOfColours, numberOfRows,screenWidth,screenHeight, n, answers):
        clearScreen(screenWidth,screenHeight)
        ans = answers.split(":")[:-1]
        if n == 0:
            writeText("Welcome Player 1. Your guessing begins now :D", 100,140)

        elif n == 1:
            writeText("Welcome Player 2. Your guessing begins now :D", 100,140)

        else:
            writeText("T_T", 100,140)


        numberOfRowsLeft = numberOfRows
        numberOfTurnsUsed = 0
        # Create the buttons for the initial row
        
        if numberOfTurnsUsed == 0:

            buttons, oldx, oldy = makeButtons(100, 30, numberOfColumns, listOfColours)

            print(f"Board = {ans}")
            gameOn = True

            clearScreen(width, height)
            pygame.font.init()
            myFont = pygame.font.SysFont("Comic Sans MS", 30)
            textSurface = myFont.render(f"Number Of Rows Remaining: {numberOfRowsLeft}", False, (100,100,100))
            size = textSurface.get_size()
            surface = pygame.Surface(size)
            surface.blit(textSurface, (0, 0))
            screen.blit(textSurface, (50,10))

        else:
            buttons, oldx, oldy = makeButtons(100, 30+70*numberOfTurnsUsed, numberOfColumns, listOfColours)

        gameOn = True
        while gameOn:
            # Start the game
            buttons, oldx, oldy, numberOfRowsLeft, gameOn =  displayGame(buttons, listOfColours, oldx, oldy, numberOfColumns, ans, numberOfRowsLeft, gameOn, ans, width, height,numberOfRows=numberOfRows)

            if gameOn == False:
                score = int((len(listOfColours) * numberOfColumns) ** ((1/(numberOfRows - numberOfRowsLeft )))*1000)
                
                print(f"Score is = {score}")

            # If the game isn't over :(
            if numberOfRowsLeft == 0:
                gameOn = False


        numberOfTurnsUsed = numberOfRows-numberOfRowsLeft
        updateLeaderboards(len(listOfColours), numberOfColumns, numberOfTurnsUsed)
        return score



















    def redrawWindow(screen, game, p, numberOfColumns, listOfColours, numberOfRows,screenWidth,screenHeight, n):
        screen.fill((0,0,0))

        if not(game.connected()):
            font = pygame.font.SysFont("comicsans", 80)
            text = font.render("Waiting for Player...", 1, (255,0,0), True)
            screen.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        elif game.connected():
            font = pygame.font.SysFont("comicsans", 60)
            """
            text = font.render("Your Move", 1, (0, 255,255))
            screen.blit(text, (80, 200))

            text = font.render("Opponents Move", 1, (0, 255, 255))
            screen.blit(text, (380, 250))
            """
            if not game.bothWent():
                if p == 0 and game.getNewBoard(0)==[""]:
                    answers1 = getAnswersForMultiplayer(numberOfColumns, listOfColours, numberOfRows,screenWidth,screenHeight,p)

                    print(answers1)
                    ans = ""
                    for x in answers1:
                        ans += f"{x}:"
                    if not game.p1Went:
                        n.send(ans)

                elif p == 1 and game.getNewBoard(1)==[""]:
                    answers2 = getAnswersForMultiplayer(numberOfColumns, listOfColours, numberOfRows,screenWidth,screenHeight,p)

                    print(answers2)
                    ans = ""
                    for x in answers2:
                        ans += f"{x}:"
                    if not game.p2Went:
                        n.send(ans)
                    
            else:
                print("We have our inputs :D")

        else:
            print("Sad Times")
        

        pygame.display.update()
            

    def getAnswersForMultiplayer(numberOfColumns, listOfColours, numberOfRows,screenWidth,screenHeight,p):
        buttons = []
        x,y = 150,250
        xChange = 60
        for i in range(numberOfColumns):
            button = Button("Click here", (x, y), listOfColours, font=30, bg=listOfColours[0], feedback="You clicked me")
            x += xChange
            buttons.append(button)
        submitButton = Button("Submit",(x+10, y),listOfColours,font=30,bg="Blue",feedback="Submitted",submitButton=True)
        buttons.append(submitButton)
        for b in buttons:
            b.show()

        numOfColours = len(listOfColours)
        clearScreen(210, screenHeight-200, x=screenWidth-210, y=200)
        writeText("Available Colours:",screenWidth-270,150, fontSize=35, fontName="Arial")
        for colourIndex in range(numOfColours):
            if colourIndex < 6:
                x = screenWidth-90
                y = 200+(colourIndex*55)
            elif colourIndex < 12:
                x = screenWidth-150
                y = 200+((colourIndex-6)*55)
            else:
                x = screenWidth-210
                y = 200+((colourIndex-12)*55)                
            currentColour = listOfColours[colourIndex]
            # Affects where the button is visually drawn
            surface = pygame.Surface((50,50))
            surface.fill(currentColour)
 
            screen.blit(surface, (x, y)) 

        writeText(f"User {p}: Enter Your Choice", 80,90,fontSize=60,fontName="Arial")
        pygame.display.update()
        coloursNotFound = True
        while coloursNotFound:   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                for b in buttons:
                    buttonPressed = b.click(event, listOfColours)
                    if buttonPressed == "MainMenu":
                        mainMenu(numberOfColumns, numberOfRows, listOfColours,screenWidth,screenHeight)
                    elif buttonPressed == "Submit":
                        answersForBoard = getAnswers(buttons, specialCase=True)
                        coloursNotFound = False


        pygame.display.update()
        return answersForBoard

    def getUsersChoiceOfColours(numberOfColumns, listOfColours, numberOfRows,screenWidth,screenHeight,playerNumber):
        mainMenuButton = Button("Main Menu", (880, 50), font=30, bg="Red", mainMenu=True)
        buttons = []
        x,y = 150,250
        xChange = 60
        
        for i in range(numberOfColumns):
            button = Button("Click here", (x, y), listOfColours, font=30, bg=listOfColours[0], feedback="You clicked me")
            x += xChange
            buttons.append(button)

        submitButton = Button("Submit",(x+10, y),listOfColours,font=30,bg="Blue",feedback="Submitted",submitButton=True)
        buttons.append(submitButton)
        buttons.append(mainMenuButton)

        for b in buttons:
            b.show()
        showColoursForPage(len(listOfColours), listOfColours, screenWidth, screenHeight)
        writeText(f"User {playerNumber}: Enter Your Choice", 80,90,fontSize=60,fontName="Arial")
        pygame.display.update()
        coloursNotFound = True
        while coloursNotFound:   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                for b in buttons:
                    buttonPressed = b.click(event, listOfColours)
                    if buttonPressed == "MainMenu":
                        mainMenu(numberOfColumns, numberOfRows, listOfColours,screenWidth,screenHeight)
                    elif buttonPressed == "Submit":
                        answersForBoard = getAnswers(buttons)
                        coloursNotFound = False
        return answersForBoard
   




    #, "Blue", "Red", "Purple", "Orange", "Green", "Crimson", "Coral", "Cyan", "darkblue", "darkgreen", "darksalmon", "deeppink4", "pink"
    colourListLength = 4
    colours = changeListOfColours(colourListLength)
    numberOfColumns, numberOfRows = 4, 10
    buttons, screenWidth,screenHeight, numberOfColumns, numberOfRows, listOfColours = openGame(width, height, numberOfColumns, numberOfRows, colours)
    while True:   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            for b in buttons:
                buttonPressed = b.click(event, listOfColours)
                if buttonPressed == "MainMenu":

                    buttons, screenWidth,screenHeight, numberOfColumns, numberOfRows, listOfColours = openGame(screenWidth, screenHeight, numberOfColumns, numberOfRows, listOfColours, allPegs = ["Red"], allUsersAnswers = ["Blue"])
                
