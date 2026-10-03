history = {}

def isBoardCoordEmpty(pieceX, pieceY, boardState):
    return(not (boardState[pieceY][pieceX]))

def isBoardCoordWithinBounds(coord):
    return not (coord > (boardSize-1) or coord < 0)

def convertMoveToBoardState(newPieceX, newPieceY, oldPieceX, oldPieceY, currentBoardState, colour):

    #newBoardState = copy.deepcopy(currentBoardState)
    newBoardState = [x[:] for x in currentBoardState]

    newBoardState[newPieceY][newPieceX] = getColourRepresentation(colour)
    newBoardState[oldPieceY][oldPieceX] = 0

    return newBoardState

def convertBoardStateToMove(currentBoardState, newBoardState):
    newX = 0
    newY = 0

    oldX = 0
    oldY = 0

    for i in range(boardSize):
        for j in range(boardSize):
            change = (currentBoardState[j][i] ^ newBoardState[j][i])
            if change and currentBoardState[j][i] == 0:
                newX = i
                newY = j
            elif (change):
                oldX = i
                oldY = j

    return newX, newY, oldX, oldY

def evaluateJumpOvers(pieceX, pieceY, boardState):
    jumpOverList = []

    if (isBoardCoordWithinBounds(pieceY-2) and (not (isBoardCoordEmpty(pieceX, pieceY-1, boardState))) and isBoardCoordEmpty(pieceX, pieceY-2, boardState)):
        jumpOverList.append(({"x": pieceX, "y": pieceY-2}))
    
    if (isBoardCoordWithinBounds(pieceX-2) and (not (isBoardCoordEmpty(pieceX-1, pieceY, boardState))) and isBoardCoordEmpty(pieceX-2, pieceY, boardState)):
        jumpOverList.append(({"x": pieceX-2, "y": pieceY}))

    if (isBoardCoordWithinBounds(pieceY+2) and (not (isBoardCoordEmpty(pieceX, pieceY+1, boardState))) and isBoardCoordEmpty(pieceX, pieceY+2, boardState)):
        jumpOverList.append(({"x": pieceX, "y": pieceY+2}))

    if (isBoardCoordWithinBounds(pieceX+2) and (not (isBoardCoordEmpty(pieceX+1, pieceY, boardState))) and isBoardCoordEmpty(pieceX+2, pieceY, boardState)):
        jumpOverList.append(({"x": pieceX+2, "y": pieceY}))

    return jumpOverList

def evaluateAllJumpOvers(pieceX, pieceY, visitedList, boardState):
    jumpOverList = evaluateJumpOvers(pieceX, pieceY, boardState)

    currentPossibleMoves = []

    for i in range(len(jumpOverList)):
        if (isPieceInList(jumpOverList[i], visitedList)):
            continue

        visitedList.append(jumpOverList[i])
        moves = evaluateAllJumpOvers(jumpOverList[i]["x"], jumpOverList[i]["y"], visitedList, boardState)

        currentPossibleMoves.append(jumpOverList[i])
        currentPossibleMoves.extend(moves)

    return currentPossibleMoves


def isPieceInList(piece, listOfPieces):
    for i in listOfPieces:
        if (i == piece):
            return True
    return False

def evaluateAllLegalMoves(pieceX, pieceY, currentBoardState, colour):
    legalMoves = []
    moves = []
    visitedList = [{ "x" : pieceX, "y" : pieceY }]

    if (isBoardCoordWithinBounds(pieceY-1) and isBoardCoordEmpty(pieceX, pieceY-1, currentBoardState)):
        legalMoves.append({ "x" : pieceX, "y" : pieceY-1 })

    if (isBoardCoordWithinBounds(pieceX-1) and isBoardCoordEmpty(pieceX-1, pieceY, currentBoardState)):
        legalMoves.append({ "x" : pieceX-1, "y" : pieceY })

    if (isBoardCoordWithinBounds(pieceY+1) and isBoardCoordEmpty(pieceX, pieceY+1, currentBoardState)):
        legalMoves.append({ "x" : pieceX, "y" : pieceY+1 })

    if (isBoardCoordWithinBounds(pieceX+1) and isBoardCoordEmpty(pieceX+1, pieceY, currentBoardState)):
        legalMoves.append({ "x" : pieceX+1, "y" : pieceY })

    currentPossibleJumpMoves = evaluateAllJumpOvers(pieceX, pieceY, visitedList, currentBoardState)
    legalMoves.extend(currentPossibleJumpMoves)

    for i in legalMoves:
        # Added tuple containing colour for use in move ordering
        moves.append((convertMoveToBoardState(i["x"], i["y"], pieceX, pieceY, currentBoardState, colour), colour))
    
    #print("Moves are: ")
    #print(moves)
    return moves

def checkForWinner(boardState):
    blackWin = True
    whiteWin = True

    # Nested loop to check all pieces
    for i in range(int(pieceRowCount)):
        for j in range(int(boardSize/2)):
            whiteWin = (whiteWin and (boardState[j][i] == 2))

            blackWin = (blackWin and (boardState[(boardSize-1-j)][(boardSize-1-i)] == 1))

    if (blackWin):
        #print("Black win")
        return - float("inf")
        #return -3
    elif (whiteWin):
        #print("White win")
        return float("inf")
        #return 3

    return 0

def getColourRepresentation(colour):
    if (colour == "black"):
        return 1
    else:
        return 2

def findAllColourPieces(colour, boardState):
    listOfColourPieces = []
    colourRepresentation = getColourRepresentation(colour)
    for i in range(len(boardState[0])):
        for j in range(len(boardState[0])):
            if (boardState[j][i] == colourRepresentation):
                listOfColourPieces.append({ "x" : i, "y" : j })
    
    return listOfColourPieces

def printBoardState(boardState):
    for i in range(boardSize):
        print(boardState[i])
    print("")

def nextLegalMovesForAllPieces(colour, boardState):
    moves = []
    colourPieces = findAllColourPieces(colour, boardState)

    for i in colourPieces:
        moves.extend( evaluateAllLegalMoves(i["x"], i["y"], boardState, colour) )

    # Sorting moves in order to improve alpha beta pruning
    if colour == "black":
        moves.sort(key=totalBoardHeuristic)
    else:
        moves.sort(reverse=True, key=totalBoardHeuristic)

    # Turning into just boardStates for return
    for j in range(len(moves)):
        moves[j] = moves[j][0]
    """
    for j in moves:
        j = j[0]
    """
    
    return moves
    #return sortedMoves

# Known as a manhattan distance
def totalBoardHeuristic(boardStateAndColour):
    # This was done for the sorting in nextLegalMovesForAllPieces
    boardState = boardStateAndColour[0]
    colour = boardStateAndColour[1]

    #maxManhattanScore = findMaxManhattanScore(colour)

    pieces = findAllColourPieces(colour, boardState)
    manhattanScore = 0
    pieceInWinRangeScore = 0
    manhattanDistanceToClosestFreeSquare = 0
    for i in pieces:
        manhattanScore += manhattanDistanceForPiece(i, colour)
        pieceInWinRange = pieceInWinRangeHeuristic(i, colour)
        pieceInWinRangeScore += pieceInWinRange
        if not pieceInWinRange:
            manhattanDistanceToClosestFreeSquare += findClosestFreeGoalSquareToPieceScore(boardState, i, colour)


    # Normalising to score between 0 and 1
    manhattanScore = (manhattanScore/(pieceCount))
    #manhattanScore = (manhattanScore/(maxManhattanScore+1))
    totalScore = manhattanScore + pieceInWinRangeScore + manhattanDistanceToClosestFreeSquare
    #return (score / (pieceCount * boardSize * 2))
    return totalScore

# Known as a manhattan distance
def manhattanDistanceForPiece(piece, colour):
    if colour == "black":
        score = - (abs((0 - piece['x'])) + abs((0 - piece['y'])))
        #score = -(abs((0 - piece['x'])) + abs((0 - piece['y'])))
    else:
        score = abs((boardSize - piece['x'])) + abs((boardSize - piece['y']))
    # Normalising to score between 0 and 1 - got idea from information mining lecture
    return (score/((boardSize-1)*2))

def findMaxManhattanScore(colour):
    winState = generateBoardWinState()
    pieces = findAllColourPieces(colour, winState)

    manhattanScore = 0
    for i in pieces:
        manhattanScore += manhattanDistanceForPiece(i, colour)

    return manhattanScore

def pieceInWinRangeHeuristic(piece, colour):
    if colour == "black":
        score = - (0 + ((piece['x'] >= (boardSize - pieceRowCount)) and (piece['y'] >= (boardSize/2))))
    else:
        score = (0 + ((piece['x'] < (0 + pieceRowCount)) and (piece['y'] < (boardSize/2))))
    return (score * 3)

def findGoalSquares(colour):
    goalSquareList = []
    if colour == "black":
        for i in range(int(boardSize/2)):
            for j in range(int(boardSize/2)):
                if ((i+(boardSize/2)) >= (boardSize - pieceRowCount)) and ((j+(boardSize/2)) >= (boardSize/2)):
                    goalSquareList.append((int(i+(boardSize/2)), int(j+(boardSize/2))))
    else:
        for i in range(int(boardSize/2)):
            for j in range(int(boardSize/2)):
                if ((i < (0 + pieceRowCount)) and (j < (boardSize/2))):
                    goalSquareList.append((i,j))
    
    return goalSquareList

def findFreeGoalSquares(boardState, colour):
    goalSquareList = findGoalSquares(colour)
    freeGoalSquareList = []

    for i in range(len(goalSquareList)):
        if not boardState[goalSquareList[i][1]][goalSquareList[i][0]]:
            #print(goalSquareList[i])
            #print(boardState[goalSquareList[i][1]][goalSquareList[i][0]])
            freeGoalSquareList.append(goalSquareList[i])

    return freeGoalSquareList

def findClosestFreeGoalSquareToPieceScore(boardState, piece, colour):
    freeGoalSquareList = findFreeGoalSquares(boardState, colour)

    #print(freeGoalSquareList)

    #closestFreeGoalSquare = 0
    manhattanDistanceToClosestFreeSquare = 0
    
    if colour == "black":
        for i in range(len(freeGoalSquareList)):
            score = -(((boardSize-1)*2) - (abs((freeGoalSquareList[i][0] - piece['x'])) + abs((freeGoalSquareList[i][1] - piece['y']))))
            #print("Score: " + str(score))
            if score < manhattanDistanceToClosestFreeSquare:
                manhattanDistanceToClosestFreeSquare = score
                #closestFreeGoalSquare = freeGoalSquareList[i]
    else:
        for i in range(len(freeGoalSquareList)):
            score = (((boardSize-1)*2) - (abs((freeGoalSquareList[i][0] - piece['x'])) + abs((freeGoalSquareList[i][1] - piece['y']))))
            #print("Score: " + str(score))
            if score > manhattanDistanceToClosestFreeSquare:
                manhattanDistanceToClosestFreeSquare = score
    
    #print("Score before normalising: " + str(manhattanDistanceToClosestFreeSquare))
    
    # Normalising to score between 0 and 1 - got idea from information mining lecture
    return (manhattanDistanceToClosestFreeSquare/(boardSize*2))

def MaxValuePrune(boardState, colour, depth, alpha, beta):
    winner = checkForWinner(boardState)
    if winner:
        # History saved as tuple of boardState, colour of move after boardState, evaluation
        history[str((boardState, colour))] = ("", swapColour(colour), winner)
        return winner
    
    if str((boardState, colour)) in history.keys():
        return history[str((boardState, colour))][2]
    
    if depth < 1:
        #printBoardState(boardState)
        eval = totalBoardHeuristic((boardState, colour))
        history[str((boardState, colour))] = ("", swapColour(colour), eval)
        return eval
    
    successors = nextLegalMovesForAllPieces(colour, boardState)
    
    #bestSuccessorState = copy.deepcopy(successors[0])
    bestSuccessorState = successors[0]
    minValue = - float("inf")
    
    for s in successors:
        value = MinValuePrune(s, swapColour(colour), depth-1, alpha, beta)
        
        if value > minValue:
            #print("Max")
            minValue = value
            bestSuccessorState = s
            #bestSuccessorState = copy.deepcopy(s)
        if value >= beta:
            history[str((boardState, colour))] = (bestSuccessorState, swapColour(colour), minValue)
            return minValue
        if value > alpha:
            alpha = value
    
    history[str((boardState, colour))] = (bestSuccessorState, swapColour(colour), minValue)

    return minValue

def MinValuePrune(boardState, colour, depth, alpha, beta):    
    winner = checkForWinner(boardState)
    if winner:
        history[str((boardState, colour))] = ("", swapColour(colour), winner)
        return winner
    
    if str((boardState, colour)) in history.keys():
        return history[str((boardState, colour))][2]
    
    if depth < 1:
        #printBoardState(boardState)
        eval = totalBoardHeuristic((boardState, colour))
        history[str((boardState, colour))] = ("", swapColour(colour), eval)
        return eval
    
    successors = nextLegalMovesForAllPieces(colour, boardState)

    bestSuccessorState = successors[0]
    maxValue = float("inf")

    for s in successors:
        value = MaxValuePrune(s, swapColour(colour), depth-1, alpha, beta)
        
        if value < maxValue:
            #print("Max")
            maxValue = value
            #bestSuccessorState = copy.deepcopy(s)
            bestSuccessorState = s
        if value <= alpha:
            history[str((boardState, colour))] = (bestSuccessorState, swapColour(colour), maxValue)
            return maxValue
        if value < beta:
            beta = value
        
    history[str((boardState, colour))] = (bestSuccessorState, swapColour(colour), maxValue)

    return maxValue

def swapColour(colour):
    if colour == "black":
        return "white"
    else:
        return "black"

def generateBoardWinState():
    state = []

    for i in range(boardSize):
        state.append([])
        for j in range(boardSize):
            state[i].append(0)

    for i in range(int(pieceRowCount)):
        for j in range(int(boardSize/2)):
            state[j][i] = 2
            state[(boardSize-1-j)][(boardSize-1-i)] = 1

    return state

"""
# This version is minimax with alpha beta pruning, move sorting based on a heuristic,
# and a search history
"""
def minimaxPrune(boardState, colour):
    global history

    # If this is not here then the history is saved between game moves
    # however that sometimes causes the game to return with a blank move
    history = {}

    alpha = -1 * float("inf")
    beta = float("inf")

    global boardSize
    boardSize = len(boardState)

    pieces = findAllColourPieces(colour, boardState)

    global pieceCount
    pieceCount = len(pieces)

    global pieceRowCount
    pieceRowCount = pieceCount / (boardSize / 2)

    depth = 2
    print("Depth:", depth)

    """
    noOfPiecesInWinRange = 0

    for i in range(pieceCount):
        noOfPiecesInWinRange += (abs(pieceInWinRangeHeuristic(pieces[i], colour))/3)
        print(noOfPiecesInWinRange)

    if noOfPiecesInWinRange > (pieceCount * 0.85):
        depth *= 2
        print("The depth is:", depth)"
    """

    if colour == "white":
        return MaxValuePrune(boardState, colour, depth, alpha, beta)
        #return MinValue(boardState, colour, depth)
    
    return MinValuePrune(boardState, colour, depth, alpha, beta)
    #return MaxValue(boardState, colour, depth)

def reconstructPath(boardState, colour):
    path = []
    currentState = history[str((boardState, colour))]

    path.append(currentState)

    while currentState[0] != "":
        currentState = history[str((currentState[0], currentState[1]))]
        path.append(currentState)

    return path

# Returns an array of length 4 where array[0] is newX, array[1] is newY, array[2] is oldX
# and array[3] is oldY

def AIMoveReturnBoardState(boardState, colour):
    minimaxPrune(boardState, colour)
    
    newBoardState = history[str((boardState, colour))]

    print("Medium AI")
    printBoardState(newBoardState[0])

    return newBoardState[0]

def AIMove(boardState, colour):
    
    minimaxPrune(boardState, colour)
    
    newBoardState = history[str((boardState, colour))]
    
    return convertBoardStateToMove(boardState, newBoardState[0])

b =                        [[1,1,1,1,0,0,0,0],
                            [1,1,1,1,0,0,0,0],
                            [1,1,1,1,0,0,0,0],
                            [1,1,1,1,0,0,0,0],
                            [0,0,0,0,2,2,2,2],
                            [0,0,0,2,2,0,2,2],
                            [0,0,0,0,2,2,2,2],
                            [0,0,0,0,2,2,2,2]]

b2 =                        [[2,2,2,2,2,2,2,2],
                             [2,2,2,2,2,2,2,2],
                             [0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0],
                             [0,0,0,0,1,1,1,1],
                             [0,0,0,0,1,1,1,1],
                             [0,0,0,0,1,1,1,1],
                             [0,0,0,1,1,0,1,1]]

b3 = [[1,1,0,0],
      [1,1,0,0],
      [0,0,2,2],
      [0,0,2,2]]

b4 = [[1,0],
      [0,2]]

testing =                  [[1,0,0,0,1,0,2,1],
                            [0,1,1,1,1,0,2,0],
                            [0,0,0,1,1,0,0,0],
                            [1,1,1,1,2,0,0,2],
                            [1,0,0,1,2,2,0,2],
                            [0,2,2,0,0,0,0,0],
                            [0,0,0,1,0,2,2,2],
                            [0,0,0,0,2,2,2,2]]

#sys.setrecursionlimit(1000000)

b5 = [[2,0,0,2],
      [2,2,0,0],
      [0,1,0,1],
      [0,0,1,1]]

#print(AIMove(testing, "black"))



#pieceRowCount = 4
#boardSize = 8

#print(findFreeGoalSquares(b2, "black"))

#print(findClosestFreeGoalSquareToPieceScore(b2, {'x':4, 'y':3}, "black"))