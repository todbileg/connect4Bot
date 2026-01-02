import random
from pydoc import describe

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
LETTERSINALPHABET = 26
numberToLetterMap = {i: chr(65 + i) for i in range(LETTERSINALPHABET)}
letterToNumberMap = {value: key for key, value in numberToLetterMap.items()}
connectHowMany = 4
directions = [(1, 0), (0, 1), (1, 1), (-1, 1), (-1, 0), (0, -1), (-1, -1), (1, -1)]
listOfPlayer1Moves = []
listOfPlayer2Moves = []

#for the top row... im doing too much for this stupid thing
def getLetterFromNumber(n):
    label = ""
    while n >= 0:
        label = numberToLetterMap[n % 26] + label
        n = (n // 26) - 1
    return label


# important function for correct size texts
def getCenteredText(middleSymbol, sideSymbol, width):
    left = (width - len(middleSymbol))//2 * sideSymbol
    finalText = left + middleSymbol + left
    if len(finalText) == width - 1:
        finalText += sideSymbol
    return finalText


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


def updateGameBoard(gameBoard, x, y, symbol, P):
    gameBoard[x][y] = symbol
    if P == 1:
        listOfPlayer1Moves.append((x,y))
    else:
        listOfPlayer2Moves.append((x,y))


def getNumberFromLetter(input):
    lenOfInput = len(input)
    total = 0
    for i in range(lenOfInput):
        total += letterToNumberMap[input[i].upper()]*(LETTERSINALPHABET**(lenOfInput-i-1))
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
    return executeMove(P, PInput)


def checkWinner(gameBoard, PSymbol, row, col):
    # These pairs represent opposite directions:
    # (Horizontal), (Vertical), (Diagonal /), (Diagonal \)
    direction_pairs = [
        ((0, 1), (0, -1)),  # Left/Right
        ((1, 0), (-1, 0)),  # Down/Up
        ((1, 1), (-1, -1)),  # Down-Right/Up-Left
        ((-1, 1), (1, -1))  # Down-Left/Up-Right
    ]

    for d1, d2 in direction_pairs:
        # Count matches in the first direction
        matches1 = countMatchesInDirection(gameBoard, row, col, d1[0], d1[1], PSymbol)
        # Count matches in the opposite direction
        matches2 = countMatchesInDirection(gameBoard, row, col, d2[0], d2[1], PSymbol)

        # Add them up + 1 (the piece we just placed)
        total_count = 1 + len(matches1) + len(matches2)

        if total_count >= connectHowMany:
            # Combine all coordinates for the return value
            return True, matches1 + [(row, col)] + matches2

    return False, -1


def countMatchesInDirection(gameBoard, startRow, startCol, dRow, dCol, PSymbol):
    matches = []
    currRow, currCol = startRow + dRow, startCol + dCol

    while 0 <= currRow < numRows and 0 <= currCol < numCols:
        if gameBoard[currRow][currCol] == PSymbol:
            matches.append((currRow, currCol))
            currRow += dRow
            currCol += dCol
        else:
            break
    return matches


def getBotMoveEasy(gameBoard) -> tuple:
    return getLetterFromNumber(random.choice(getNonFullCols(gameBoard)))

def getNonFullCols(gameBoard):
    """
    returns integers [0,1,2,3,4, ... ] where 0 maps to A in another function
    """
    nonFullCols = []
    for i in range(numCols):
        if gameBoard[0][i] == placeholderSymbol:
            nonFullCols.append(i)
    return nonFullCols


def getValidUserInput(prompt, listOfValidItems):
    isNotValid = True
    print(prompt)
    while isNotValid:
        userInput = input("Input: ")
        if userInput in listOfValidItems:
            isNotValid = False
        else:
            print("Not a valid input. Try again.")
    return userInput


def executeMove(P, moveLetter):
    PChar = P1Char if P == 1 else P2Char
    inputCoords = getInputCoords(moveLetter)

    updateGameBoard(gameBoard, inputCoords[0], inputCoords[1], PChar, P)
    isWinner = checkWinner(gameBoard, PChar, inputCoords[0], inputCoords[1])

    print(getNewPrintBoard(gameBoard))

    if isWinner[0]:
        print(f"Player {P} wins!")
        return True
    elif len(getNonFullCols(gameBoard)) == 0:
        print("Board is full!")
        return True
    return False


def getWinningCoords(gameBoard, P, PChar):
    if P == 1:
        listOfPlayerMoves = listOfPlayer1Moves
    else:
        listOfPlayerMoves = listOfPlayer2Moves
    for location in listOfPlayerMoves:
        for d in directions:
            result = getWinningCoordsRec(gameBoard, PChar, d, [location], 1)
            if result != -1:
                return True, result
    return False, -1


def getWinningCoordsRec(gameBoard, PChar, d, listOfLocations, numMatches):
    if numMatches == connectHowMany-1:
        result = movePossibleInDirection(gameBoard, d, listOfLocations[-1])
        if result[0]:
            return result[1]
        else:
            return -1
    latestRow, latestCol = listOfLocations[-1]
    nextRow = latestRow + d[0]
    nextCol = latestCol + d[1]
    if 0 <= nextRow < numRows and 0 <= nextCol < numCols:
        if gameBoard[nextRow][nextCol] == PChar:
            return getWinningCoordsRec(gameBoard, PChar, d, listOfLocations + [(nextRow, nextCol)], numMatches + 1)
    return -1


def movePossibleInDirection(gameBoard, d, tupleOfLocation):
    desiredRow = tupleOfLocation[0] + d[0]
    desiredCol = tupleOfLocation[1] + d[1]
    if 0 <= desiredRow < numRows and 0 <= desiredCol < numCols:
        belowDesiredRow = desiredRow + 1
        if ((belowDesiredRow == numRows or gameBoard[belowDesiredRow][desiredCol] != placeholderSymbol) and
                gameBoard[desiredRow][desiredCol] == placeholderSymbol):
            return True, (desiredRow, desiredCol)

    return False, (-1,-1)


def getBotMoveMedium(gameBoard, humanP, humanChar):
    # determining who is who
    botP = 2 if humanP == 1 else 1
    botChar = P2Char if botP == 2 else P1Char

    # 1. ATTACK: Check if Bot can win right now
    winningColumn = findBestMoveForPlayer(gameBoard, botChar)
    if winningColumn != -1:
        return getLetterFromNumber(winningColumn)

    # 2. DEFENSE: Check if other player is about to win
    blockingColumn = findBestMoveForPlayer(gameBoard, humanChar)
    if blockingColumn != -1:
        return getLetterFromNumber(blockingColumn)

    # 3. Random move if no immediate threats/wins
    return getBotMoveEasy(gameBoard)


def findBestMoveForPlayer(gameBoard, PChar):
    # Check Horizontal Windows
    for r in range(numRows):
        for c in range(numCols - (connectHowMany-1)):
            window = [gameBoard[r][c + i] for i in range(connectHowMany)]
            coords = [(r, c + i) for i in range(connectHowMany)]
            col = checkWindow(window, coords, PChar)
            if col != -1: return col

    # Check Vertical Windows
    for r in range(numRows - (connectHowMany-1)):
        for c in range(numCols):
            window = [gameBoard[r + i][c] for i in range(connectHowMany)]
            coords = [(r + i, c) for i in range(connectHowMany)]
            col = checkWindow(window, coords, PChar)
            if col != -1: return col

    # Check Positive Diagonal Windows (/)
    for r in range(numRows - (connectHowMany-1)):
        for c in range(numCols - (connectHowMany-1)):
            window = [gameBoard[r + (connectHowMany-1) - i][c + i] for i in range(connectHowMany)]
            coords = [(r + (connectHowMany-1) - i, c + i) for i in range(connectHowMany)]
            col = checkWindow(window, coords, PChar)
            if col != -1: return col

    # Check Negative Diagonal Windows (\)
    for r in range(numRows - (connectHowMany-1)):
        for c in range(numCols - (connectHowMany-1)):
            window = [gameBoard[r + i][c + i] for i in range(connectHowMany)]
            coords = [(r + i, c + i) for i in range(connectHowMany)]
            col = checkWindow(window, coords, PChar)
            if col != -1: return col

    return -1


def checkWindow(window, coords, PChar):
    # We are looking for 3 of the player's pieces and 1 empty spot
    if window.count(PChar) == connectHowMany-1 and window.count(placeholderSymbol) == 1:
        emptyIndex = window.index(placeholderSymbol)
        emptySpotCoords = coords[emptyIndex]

        # check if the move is physically possible (gravity)
        r, c = emptySpotCoords

        # Is this spot supported?
        if r == numRows - 1:  # Bottom row is always supported
            return c
        elif gameBoard[r + 1][c] != placeholderSymbol:  # Spot below is occupied
            return c

    return -1

letters = [getLetterFromNumber(i) for i in range(numCols)]

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

printBoard = getNewPrintBoard(gameBoard)
# for i in gameBoard:
#     print(i)
print(titleMessage + "\n" + printBoard)

gameType = getValidUserInput("Input 1 for Player vs Player\nInput 2 for Player vs Bot",
                             ["1","2"])
if gameType == "1":
    while True:
        if playerTurn(1):
            break
        if playerTurn(2):
            break
else:
    #bot here ask which difficulty
    whichPlayer = getValidUserInput("Input 1 to play as player 1\nInput 2 to play as player 2",
                                    ["1", "2"])
    difficultyPrompt = "Input 1 for easy bot\nInput 2 for medium bot\nInput 3 for hard bot"
    botDifficulty = getValidUserInput(difficultyPrompt, ["1", "2", "3"])

    humanTurnNum = int(whichPlayer)
    botTurnNum = 2 if humanTurnNum == 1 else 1

    print(humanTurnNum)
    print(botTurnNum)

    while True:
        if botTurnNum == 1:
            print("Bot's turn...")
            if botDifficulty == "1":
                botMoveLetter = getBotMoveEasy(gameBoard)
            elif botDifficulty == "2":
                botMoveLetter = getBotMoveMedium(gameBoard, humanTurnNum, P2Char)
            # else:
            #     botMoveLetter = getBotMoveHard(gameBoard, humanTurnNum, P2Char)

            if executeMove(1, botMoveLetter):
                break
        else:
            if playerTurn(1):
                break

        if botTurnNum == 2:
            print("Bot's turn...")
            if botDifficulty == "1":
                botMoveLetter = getBotMoveEasy(gameBoard)
            elif botDifficulty == "2":
                botMoveLetter = getBotMoveMedium(gameBoard, humanTurnNum, P1Char)
            # else:
            #     botMoveLetter = getBotMoveHard(gameBoard, humanTurnNum, P1Char)

            if executeMove(2, botMoveLetter):
                break
        else:
            if playerTurn(2):
                break