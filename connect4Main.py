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

#This is the welcome message
widthOfBoard = (horizontalLength+1)*numCols+1
lenOfWelcomeLeft = (widthOfBoard - len(message))//2
titleMessage = welcomeSymbol*lenOfWelcomeLeft + message + welcomeSymbol * lenOfWelcomeLeft
if len(titleMessage) == widthOfBoard-1:
    titleMessage += welcomeSymbol

#This is printing out the board
for row in range(numRows):
    for col in range(numCols):
        board += cornerSymbol + horizontalSymbol*horizontalLength
    board += cornerSymbol + "\n"
    for vert in range(verticalLength):
        for col in range(numCols):
            board += verticalSymbol + space*horizontalLength
        board += verticalSymbol + "\n"
for col in range(numCols):
    board += cornerSymbol + horizontalSymbol*horizontalLength
board += cornerSymbol

print(titleMessage + "\n" + board, end='')