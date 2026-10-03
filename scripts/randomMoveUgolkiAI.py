from random import randint
import math
import copy
import sys


def isBoardCoordEmpty(pieceX, pieceY, boardState):
    return(not (boardState[pieceY][pieceX]))

def isBoardCoordWithinBounds(coord):
    return not (coord > (boardSize-1) or coord < 0)

def convertMoveToBoardState(newPieceX, newPieceY, oldPieceX, oldPieceY, currentBoardState, colour):

    newBoardState = copy.deepcopy(currentBoardState)

    newBoardState[newPieceY][newPieceX] = getColourRepresentation(colour)
    newBoardState[oldPieceY][oldPieceX] = 0

    return newBoardState

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


def evaluateAllJumpOvers(pieceX, pieceY, visitedList, boardState):
    jumpOverList = evaluateJumpOvers(pieceX, pieceY, boardState)

    jumpOverListCopy = jumpOverList.copy()
    currentPossibleMoves = []

    for i in range(len(jumpOverListCopy)):
        if (isPieceInList(jumpOverListCopy[i], visitedList)):
            jumpOverList[i] = 0
            continue

        visitedList.append(jumpOverListCopy[i])
        currentPossibleMoves = evaluateAllJumpOvers(jumpOverListCopy[i]["x"], jumpOverListCopy[i]["y"], visitedList, boardState)

        if (currentPossibleMoves != []):
            jumpOverList.extend(currentPossibleMoves)

    return([x for x in jumpOverList if x != 0])

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
    if (currentPossibleJumpMoves != []):
        legalMoves.extend(currentPossibleJumpMoves)

    for i in legalMoves:
        moves.append(convertMoveToBoardState(i["x"], i["y"], pieceX, pieceY, currentBoardState, colour))
    
    #print("Moves are: ")
    #print(moves)
    return moves

def checkForWinner(boardState):
    blackWin = True
    whiteWin = True

    # Nested loop to check all pieces
    for i in range(int(boardSize/2)):
        for j in range(int(boardSize/2)):
            whiteWin = (whiteWin and (boardState[j][i] == 2))

            blackWin = (blackWin and (boardState[(boardSize-1-j)][(boardSize-1-i)] == 1))

    if (blackWin):
        print("Black win")
        return 1
    elif (whiteWin):
        print("White win")
        return 2

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
    """
    print(boardState[0])
    print(boardState[1])
    print(boardState[2])
    print(boardState[3])
    print(boardState[4])
    print(boardState[5])
    print(boardState[6])
    print(boardState[7])
    """
    print("")

def nextLegalMovesForAllPieces(colour, boardState):
    moves = []
    colourPieces = findAllColourPieces(colour, boardState)

    for i in colourPieces:
        moves.extend(evaluateAllLegalMoves(i["x"], i["y"], boardState, colour))

    for i in moves:
        print("BoardState: ")
        printBoardState(i)
    
    return moves


def chooseRandomMove(boardState, colour):
    moves = nextLegalMovesForAllPieces(colour, boardState)
    return (moves[randint(0, len(moves)-1)])

def AIMoveReturnBoardState(boardState, colour):
    global boardSize
    boardSize = len(boardState)

    result = chooseRandomMove(boardState, colour)
    print("Random AI")
    printBoardState(result)

    return(result)

# Returns an array of length 4 where array[0] is newX, array[1] is newY, array[2] is oldX
# and array[3] is oldY
def AIMove(boardState, colour):
    #print(boardState)
    #return [1, 2, 3, 4]
    #print("I'm here")
    #return minimax_prune(boardState, colour)
    global boardSize
    boardSize = len(boardState)

    result = chooseRandomMove(boardState, colour)

    printBoardState(result)

    newX, newY, oldX, oldY = convertBoardStateToMove(boardState, result)

    return [newX, newY, oldX, oldY]

b =                       [[1,1,1,1,0,0,0,0],
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
                             [0,0,0,1,0,1,1,1],
                             [0,0,0,0,1,1,1,1],
                             [0,0,0,0,1,1,1,1],
                             [0,0,0,0,1,1,1,1]]

b3 =                        [[1,1,1,1,0,0,0,0],
                             [1,1,1,1,0,0,0,0],
                             [1,1,1,1,0,0,0,0],
                             [1,1,1,1,0,2,0,0],
                             [0,0,0,0,2,2,2,2],
                             [0,0,0,0,2,0,2,2],
                             [0,0,0,0,2,2,2,2],
                             [0,0,0,0,2,2,2,2]]

sys.setrecursionlimit(1000000)

#print(b2)

#print(AIMove(b2, "black"))
#theBoardState, thing, otherThing = AIMove(b2, "black")
#printBoardState(AIMove(b2, "black")[1])
#print(AIMove(b3, "black"))

#print(b2)