import math
import copy
import random
import time

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

    #jumpOverListCopy = jumpOverList.copy()
    #currentPossibleMoves = jumpOverList[:]
    currentPossibleMoves = []

    for i in range(len(jumpOverList)):
        if (isPieceInList(jumpOverList[i], visitedList)):
            #currentPossibleMoves[i] = 0
            continue

        visitedList.append(jumpOverList[i])
        moves = evaluateAllJumpOvers(jumpOverList[i]["x"], jumpOverList[i]["y"], visitedList, boardState)

        currentPossibleMoves.append(jumpOverList[i])
        currentPossibleMoves.extend(moves)
        """
        if (currentPossibleMoves != []):
            currentPossibleMoves.extend(moves)
        """

    # jumpOverList.filter(number => number !== 0)
    #currentPossibleMoves = [x for x in currentPossibleMoves if x != 0]

    return currentPossibleMoves

"""
def evaluateAllJumpOvers(pieceX, pieceY, visitedList, boardState):
    jumpOverList = evaluateJumpOvers(pieceX, pieceY, boardState)

    #jumpOverListCopy = jumpOverList.copy()
    currentPossibleMoves = jumpOverList[:]

    for i in jumpOverList:
        if (isPieceInList(i, visitedList)):
            continue

        visitedList.append(i)
        moves = evaluateAllJumpOvers(i["x"], i["y"], visitedList, boardState)

        if (currentPossibleMoves != []):
            currentPossibleMoves.extend(moves)

    return currentPossibleMoves
"""

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
        return 1
        #return -3
    elif (whiteWin):
        #print("White win")
        return 2
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

def rollout(boardState, colour, baseColour):
    total = 0
    #copyBoardState = copy.deepcopy(boardState)
    copyBoardState = [x[:] for x in boardState]

    # Rollout until terminal node
    #finished = False

    rolloutLength = 10
    node = copyBoardState

    colour = swapColour(colour)

    i = 0

    while i < rolloutLength:
        #printBoardState(node)
        winner = checkForWinner(node)
        if (winner == 1 and baseColour == "black") or (winner == 2 and baseColour == "white"):
            total = 20
            break
        elif (winner == 2 and baseColour == "black") or (winner == 1 and colour == "white"):
            total = -20
            break
        else:
            colour = swapColour(colour)
            succ = nextLegalMovesForAllPieces(colour, node)
            #for i in succ:
                #printBoardState(i)
            #choice = randint(0, len(succ)-1)
            node = succ[random.randint(0, len(succ)-1)]
            i += 1

    if (total == 0):
        total = totalBoardHeuristic((node, colour))

    #print("Got here")
    return total


class monteCarloNode():
    def __init__(self, parentNode, boardState, colour, goalColour):
        self.parentNode = parentNode
        self.boardState = boardState
        self.colour = colour
        self.goalColour = goalColour
        self.totalScore = 0
        self.numberOfVisits = 0
        self.children = []

    def expand(self):
        winner = checkForWinner(self.boardState)
        if winner:
            self.totalScore += 1
            self.numberOfVisits += 1
            self.backpropagate()

        elif self.numberOfVisits == 0:
            newNumberOfVisits = rollout(self.boardState, self.colour, self.goalColour)
            self.totalScore += newNumberOfVisits
            self.numberOfVisits += 1
            self.backpropagate()

        elif self.numberOfVisits == 1:
            self.addChildren()
            child = self.children[0]
            child.expand()
            self.backpropagate()

        else:
            child = self.children[0]
            chosenValue = float("inf")

            for s in self.children:
                value = s.calculateUCB1()

                if value < chosenValue:
                    child = s
                    chosenValue = value
            
            child.expand()
            self.backpropagate()

    def backpropagate(self):
        if self.children == []:
            current = self
            loc = self
        else:
            current = self.children[0]
            loc = self.children[0]

            while loc.parentNode != 0:
                loc = loc.parentNode
                loc.totalScore += current.totalScore
                loc.numberOfVisits += 1

    def calculateUCB1(self):
        numberOfVisits = self.getBaseNumberOfVisits()

        constant = 2

        if self.numberOfVisits == 0:
            return float("inf")
        else:
            UCB1 = int(self.totalScore) + (constant * math.sqrt(math.log(int(numberOfVisits)/int(self.numberOfVisits))))
            return UCB1
    
    def getBaseNumberOfVisits(self):
        currentNode = self
        while currentNode.parentNode:
            currentNode = currentNode.parentNode
        
        return currentNode.numberOfVisits

    def addChildren(self):
        children = nextLegalMovesForAllPieces(self.colour, self.boardState)
        for i in children:
            childNode = monteCarloNode(self, i, swapColour(self.colour), self.goalColour)
            self.children.append(childNode)

def monteCarloTreeSearch(rootBoardState, colour):

    global boardSize
    boardSize = len(rootBoardState)

    global pieceCount
    pieceCount = len(findAllColourPieces("white", rootBoardState))

    global pieceRowCount
    pieceRowCount = pieceCount / (boardSize / 2)

    rootNode = monteCarloNode(0, rootBoardState, colour, colour)
    rootNode.expand()

    seconds = 3

    endOfTimer = time.time() + seconds

    while time.time() < endOfTimer:

        rootNode.expand()
        #leafNode = select(rootBoardState)
        #simulationResult = eval(leafNode)
        #backpropagate(leafNode, simulationResult)

    chosenChild = rootNode.children[0]
    chosenValue = chosenChild.totalScore
    for s in rootNode.children:
        value = s.totalScore

        if value > chosenValue:
            chosenChild = s
            chosenValue = value

    """
    print("Chosen boardState: ")
    printBoardState(chosenChild.boardState)
    print(chosenChild.totalScore)
    print(" ")
    """

    return chosenValue, chosenChild.boardState

# Returns an array of length 4 where array[0] is newX, array[1] is newY, array[2] is oldX
# and array[3] is oldY
def AIMove(boardState, colour):
    #print(boardState)
    #return [1, 2, 3, 4]
    #print("I'm here")
    #return minimax_prune(boardState, colour)

    chosenValue, newBoardState = monteCarloTreeSearch(boardState, colour)

    #printBoardState(chosenValue)

    newX, newY, oldX, oldY = convertBoardStateToMove(boardState, newBoardState)

    return [newX, newY, oldX, oldY]


def AIMoveReturnBoardState(boardState, colour):
    chosenValue, newBoardState = monteCarloTreeSearch(boardState, colour)
    
    print("MCTS AI")
    printBoardState(newBoardState)
    return newBoardState

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

#print(b)

#print(AIMove(testing, "black"))

#print(b)
"""
boardState = b3
colour = "black"
pieceRowCount = 2
boardSize = 4
while not checkForWinner(boardState):
    boardState = AIMoveReturnsBoard(boardState, colour)
    colour = swapColour(colour)
"""

b5 = [[2,0,0,2],
      [2,2,0,0],
      [0,1,0,1],
      [0,0,1,1]]

#print(AIMove(b, "black"))