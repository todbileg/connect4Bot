import time

cornerSymbol = "+"
horizontalSymbol = "-"
verticalSymbol = "|"
placeholderSymbol = "_"
space = " "
horizontalLength = 3
verticalLength = 1
numRows = 6
numCols = 7
board = ""
welcomeSymbol = "^"
message = "Play Connect 4!"
P1Char = "X"
P2Char = "T"
minInput = 2
maxInput = 4
yCoordsIndicator = (verticalLength - 1) //2
numberToLetterMap = {i: chr(65 + i) for i in range(26)}
letterToNumberMap = {value: key for key, value in numberToLetterMap.items()}

#for the top row... im doing too much for this stupid thing
def get_label(n):
    label = ""
    while n >= 0:
        label = numberToLetterMap[n % 26] + label
        n = (n // 26) - 1
    return label

letters = [get_label(i) for i in range(numCols)]

# important function for correct size texts
def getCenteredText(middleSymbol, sideSymbol, width):
    left = (width - len(middleSymbol))//2 * sideSymbol
    finalText = left + middleSymbol + left
    if len(finalText) == width - 1:
        finalText += sideSymbol
    return finalText

#This is the welcome message
widthOfBoard = (horizontalLength+1)*numCols+1+len(str(numRows))
titleMessage = getCenteredText(message, welcomeSymbol,widthOfBoard)

#game board and logic stuff here
gameBoard = []
for _ in range(numRows):
    gameBoard.append(list(range(numCols)))
for i in range(len(gameBoard)):
    for j in range(len(gameBoard[i])):
        gameBoard[i][j] = placeholderSymbol

#This is printing out the board
middleP1 = getCenteredText(P1Char, space, horizontalLength)
middleP2 = getCenteredText(P2Char, space, horizontalLength)
middleP0 = space * horizontalLength
def getNewPrintBoard(gameBoard):
    board = ""
    lenOfLeftWidth = len(str(numRows))
    board += lenOfLeftWidth*space
    for col in range(numCols):
        board += (verticalSymbol +
                  getCenteredText(letters[col], space, horizontalLength))
    board += verticalSymbol + "\n"
    for row in range(numRows):
        board += lenOfLeftWidth*horizontalSymbol
        for col in range(numCols):
            board += cornerSymbol + horizontalSymbol*horizontalLength
        board += cornerSymbol + "\n"
        for vert in range(verticalLength):
            if vert == yCoordsIndicator:
                board += getCenteredText(str(row+1), space, lenOfLeftWidth)
            else:
                board += lenOfLeftWidth*space
            for col in range(numCols):
                symbolAtCoords = gameBoard[row][col]
                if symbolAtCoords == placeholderSymbol:
                    cell = middleP0
                elif symbolAtCoords == P1Char:
                    cell = middleP1
                else:
                    cell = middleP2
                board += verticalSymbol + cell
            board += verticalSymbol + "\n"
    board += lenOfLeftWidth*horizontalSymbol
    for col in range(numCols):
        board += cornerSymbol + horizontalSymbol*horizontalLength
    board += cornerSymbol
    return board

def updateGameBoard(gameBoard, x, y, symbol):
    gameBoard[x][y] = symbol

def getNumberFromLetter(input):
    lenOfInput = len(input)
    total = 0
    for i in range(lenOfInput):
        total += letterToNumberMap[input[i].upper()]*(26**(lenOfInput-i-1))
    return total

def isValidInput(input):
    if not isinstance(input, str):
        print("Input is not a string")
        return False
    elif not input.isalpha():
        print("Input is not all letters")
        return False
    elif len(input) > len(letters[-1]) or numCols < getNumberFromLetter(input.upper()):
        print("Input is out of bounds")
        return False
    else:
        return True

def getInput(P):
    isNotValid = True
    while isNotValid:
        P1Input = input(f"Player {P}'s turn:")
        isNotValid = not isValidInput(P1Input)
    return P1Input

def getInputCoords(letters):
    num = getNumberFromLetter(letters)
    if isColumnFull(letters):
        print("This column is full. Try again")
        return -1,-1
    elif gameBoard[numRows-1][num] == placeholderSymbol:
        return numRows-1,num
    isNotFound = True
    prev = 0
    next = 1
    while isNotFound:
        if gameBoard[prev][num] == placeholderSymbol and gameBoard[next][num] != placeholderSymbol:
            isNotFound = False
        prev = next
        next += 1
    return prev-1,num

def isColumnFull(letters):
    return gameBoard[0][getNumberFromLetter(letters)] != placeholderSymbol

def playerTurn(P):
    if P == 1:
        PChar = P1Char
    else:
        PChar = P2Char
    isNotValid = True
    while isNotValid:
        PInput = getInput(P)
        inputCoords = getInputCoords(PInput)
        if inputCoords[0] != -1:
            isNotValid = False
    updateGameBoard(gameBoard, inputCoords[0], inputCoords[1], PChar)
    printBoard = getNewPrintBoard(gameBoard)
    print(printBoard)

updateGameBoard(gameBoard, 0,1,P1Char)
printBoard = getNewPrintBoard(gameBoard)
for i in gameBoard:
    print(i)
print(titleMessage + "\n" + printBoard)
while True:
    playerTurn(1)
    playerTurn(2)
