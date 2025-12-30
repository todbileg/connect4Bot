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
for i in gameBoard:
    print(i)

#This is printing out the board
middleP1 = getCenteredText(P1Char, space, horizontalLength)
middleP2 = getCenteredText(P2Char, space, horizontalLength)
middleP0 = space * horizontalLength
def getNewPrintBoard(gameBoard):
    board = ""
    for row in range(numRows):
        for col in range(numCols):
            board += cornerSymbol + horizontalSymbol*horizontalLength
        board += cornerSymbol + "\n"
        for vert in range(verticalLength):
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
    for col in range(numCols):
        board += cornerSymbol + horizontalSymbol*horizontalLength
    board += cornerSymbol
    return board
def updateGameBoard(gameBoard, x, y, symbol):
    gameBoard[x][y] = symbol

updateGameBoard(gameBoard, 1, 5, P1Char)
updateGameBoard(gameBoard, 1, 2, P1Char)
updateGameBoard(gameBoard, 1, 4, P1Char)
updateGameBoard(gameBoard, 0, 0, P1Char)

printBoard = getNewPrintBoard(gameBoard)

print(titleMessage + "\n" + printBoard, end='')