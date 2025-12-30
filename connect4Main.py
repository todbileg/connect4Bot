import time

cornerSymbol = "+"
horizontalSymbol = "-"
verticalSymbol = "|"
space = " "
horizontalLength = 3
verticalLength = 1
numRows = 6
numCols = 7
board = ""
welcomeSymbol = "^"
message = "Play Connect 4!"
P1Char = "X"
P2Char = "O"
minInput = 2
maxInput = 4
yCoordsIndicator = (verticalLength - 1) //2
numberToLetterMap = {i: chr(65 + i) for i in range(26)}

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
widthOfBoard = (horizontalLength+1)*numCols+1
titleMessage = getCenteredText(message, welcomeSymbol,widthOfBoard)

#game board and logic stuff here
gameBoard = []
for _ in range(numRows):
    gameBoard.append(list(range(numCols)))
for i in range(len(gameBoard)):
    for j in range(len(gameBoard[i])):
        gameBoard[i][j] = horizontalSymbol


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
                if symbolAtCoords == horizontalSymbol:
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
"""
def checkInput(input):
    lenOfInput = len(input)
    if lenOfInput < minInput or lenOfInput > maxInput:
"""
updateGameBoard(gameBoard, 0,1,P1Char)
printBoard = getNewPrintBoard(gameBoard)
print(len(str(numRows)))
for i in gameBoard:
    print(i)
print(titleMessage + "\n" + printBoard, end='')
# while True:
#     try:
#         P1Input = input("Player 1's turn:")
#         checkInput(P1Input)
#     except e:
# first need to make the coordinate system
