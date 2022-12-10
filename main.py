import pygame
 
pygame.init()
screen = pygame.display.set_mode((600, 1080))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
 
def placePeg(x,y,colour):
    #                       Size
    surface = pygame.Surface((10,10))
    surface.fill(colour)
    #                   Position
    screen.blit(surface, (x,y))
    pygame.display.update()  

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
            colour = "white"

        elif peg < white+grey:
            colour = "grey"

        else:
            colour = "cyan"

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

    
class Button:
    """Create a button, then blit the surface in the while loop"""
 
    def __init__(self, text,  pos, listOfColours, font, bg="black", feedback="",submitButton = False, listOfButtons = []):

        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.currentColour = bg
        self.submit = submitButton

        if submitButton == True:
            text = "Submit ;P"
            self.text = self.font.render(text, 1, pygame.Color("White"))
            self.size = self.text.get_size()
            self.surface = pygame.Surface(self.size)
            self.surface.blit(self.text, (0, 0))




        elif feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        


        # hard bit
        bg = self.get_next_colour(listOfColours)

        self.change_colour(listOfColours)
 
    def get_next_colour(self, listOfColours):
        currentColour = self.currentColour
        # If the current colour is the last in the list
        if currentColour == listOfColours[-1]:
            # Sets colour to start of the list
            self.currentColour = listOfColours[0]
        else:
            # Sets the colour to the next in line ;)
            self.currentColour = listOfColours[listOfColours.index(currentColour)+1]

    def submit_answer(self):
        pass

    def change_colour(self, listOfColours):
        """Change the text when you click"""
        if self.submit == True:
            x,y = 110,50
        else:
            x,y = 50,50

        # Affects where the click is registered
        self.size = [x,y]
        # Affects where the button is visually drawn
        self.surface = pygame.Surface((x,y))
        self.get_next_colour(listOfColours)
        bg = self.currentColour
        self.surface.fill(bg)
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.show()
        pygame.display.update()     
 
    def show(self):
        screen.blit(self.surface, (self.x, self.y))
        if self.submit == True:
            self.surface.blit(self.text, (0, 0))

    def click(self, event, listOfColours):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    # If the button isn't submit ;)
                    if self.submit == False:
                        self.change_colour(listOfColours)
                        self.show()
                        pygame.display.update()  
                        wantAnswers = False
                        return wantAnswers                 
                    else:
                        wantAnswers = True
                        return wantAnswers

    def getCurrentColour(self):
        return self.currentColour

    def checkSubmitButton(self):
        return self.submit

def getAnswers(allButtons):
    answers = []
    for button in allButtons:
        if button.checkSubmitButton() == False:
            ans = button.getCurrentColour()
            answers.append(ans)

    return answers

def getPegColours(numCorrectColourAndPosition, numberCorrectColour, numberWrong):
    colouredPegs = {"white":numCorrectColourAndPosition, "grey":numberCorrectColour, "black":numberWrong}
    return colouredPegs

def displayGame(buttons, listOfColours, oldx, oldy, numberOfColumns, correctAnswer, numberOfRowsLeft, gameOn):
    # Display board and all that

    # Checks if the game is closed or not ;P

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # Checks if each button has been clicked yet ;)
        createNewRow = False
        for b in buttons:
            wantAns = b.click(event, listOfColours)
            if wantAns == True:
                answers = getAnswers(buttons)

                # ******************************* IMPORTANT ***********************************
                # Need to display new row

                # Ends the loop
                b = buttons[-1]
                # Initiate creation of new row
                createNewRow = True
                countOfEachCorrectColour = countNumberOfEachColour(colours, board)
                print(f"countOfEachCorrectColour = {countOfEachCorrectColour}")
                corrections =  checkUsersGuess (answers, correctAnswer, countOfEachCorrectColour, listOfColours)
                print(f"answers = {answers}")
                right, kindaRight, wrong = corrections["Number Correct"], corrections["Number Correct Colour"], corrections["Number Wrong"]
                print(f"right, kindaRight, wrong = {right, kindaRight, wrong}")
                pegColours = getPegColours(right, kindaRight, wrong)
                if pegColours["white"] ==  pegColours["white"] +  pegColours["grey"] +  pegColours["black"]:
                    gameOn = False
                getPegsPositioned(pegColours, oldx, oldy)
                numberOfRowsLeft -=1



        if createNewRow == True:
            buttons, oldx, oldy = makeButtons(oldx, oldy, numberOfColumns)
    
    # Displays the button
    for button in buttons:
        button.show()
        clock.tick(75)
        pygame.display.update()

    return buttons, oldx, oldy, numberOfRowsLeft, gameOn
    
colours = ["Yellow", "Blue", "Red", "Purple", "Orange", "Green"]



def makeButtons(oldx, oldy, numOfColumns):
    buttons = []
    # Regular buttons
    yChange = 70
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

    return buttons, newx, newy

# Create the buttons for the initial row
numberOfColumns = 4
buttons, oldx, oldy = makeButtons(100, 30, numberOfColumns)
board = generateRandomBoard(colours, numberOfColumns)

print(f"Board = {board}")
gameOn = True
numberOfRowsLeft = 10
while gameOn:
    buttons, oldx, oldy, numberOfRowsLeft, gameOn =  displayGame(buttons, colours, oldx, oldy, numberOfColumns, board, numberOfRowsLeft, gameOn)
    if gameOn == False:
        print("You won!!")
    elif numberOfRowsLeft == 0:
        print("Loser!! :P")
        gameOn = False













