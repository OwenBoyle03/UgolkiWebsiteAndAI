import randomMoveUgolkiAI
import easyAIUgolkiHeuristicBased as easyAI
import mediumMinimaxVariantUgolkiAI  as mediumAI
import hardMinimaxVariantUgolkiAI as hardAI
import ugolkiMCTSAI as MCTS
from numpy import random
import time

def checkForWinner(boardState, boardSize, pieceRowCount):
    blackWin = True
    whiteWin = True

    # Nested loop to check all pieces
    for i in range(int(pieceRowCount)):
        for j in range(int(boardSize/2)):
            whiteWin = (whiteWin and (boardState[j][i] == 2))

            blackWin = (blackWin and (boardState[(boardSize-1-j)][(boardSize-1-i)] == 1))

    if (blackWin):
        return - 1
    elif (whiteWin):
        return 1

    return 0

def swapColour(colour):
    if colour == "black":
        return "white"
    else:
        return "black"

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

def generateRandomBoardState():
    initialBoardState = [   [1,1,1,1,0,0,0,0],
                            [1,1,1,1,0,0,0,0],
                            [1,1,1,1,0,0,0,0],
                            [1,1,1,1,0,0,0,0],
                            [0,0,0,0,2,2,2,2],
                            [0,0,0,0,2,2,2,2],
                            [0,0,0,0,2,2,2,2],
                            [0,0,0,0,2,2,2,2]]
    # Randomly swaps number from the above board
    # to give a random board
    for i in range((8*8)):
        rand1 = random.randint(0,7)
        rand2 = random.randint(0,7)
        rand3 = random.randint(0,7)
        rand4 = random.randint(0,7)

        pieceHolder = initialBoardState[rand1][rand2]
        initialBoardState[rand1][rand2] = initialBoardState[rand3][rand4]
        initialBoardState[rand3][rand4] = pieceHolder
    print(initialBoardState)
    return initialBoardState

def timeDecisionMaking(AI):
    timeDiff = []

    for i in range(10):
        state = generateRandomBoardState()
        timer = time.time()
        AI.AIMoveReturnBoardState(state, "black")
        timeDiff.append(time.time() - timer)
        print("AI took this long to make a move: " + str(timeDiff[i]) + " seconds")
    
    averageTime = 0
    for i in range(10):
        averageTime += timeDiff[i]

    return averageTime




boardState8x8 = [           [1,1,1,1,0,0,0,0],
                            [1,1,1,1,0,0,0,0],
                            [1,1,1,1,0,0,0,0],
                            [1,1,1,1,0,0,0,0],
                            [0,0,0,0,2,2,2,2],
                            [0,0,0,0,2,2,2,2],
                            [0,0,0,0,2,2,2,2],
                            [0,0,0,0,2,2,2,2]]

boardState6x6 = [           [1,1,1,0,0,0],
                            [1,1,1,0,0,0],
                            [1,1,1,0,0,0],
                            [0,0,0,2,2,2],
                            [0,0,0,2,2,2],
                            [0,0,0,2,2,2]]


def comparingAIs(AI1, AI2, startBoardState):
    boardState = startBoardState
    boardSize = len(boardState)

    pieces = findAllColourPieces("white", boardState)
    pieceCount = len(pieces)

    pieceRowCount = pieceCount / (boardSize / 2)

    winner = 0

    rand = random.randint(0,1)

    if rand:
        colour = "black"
    else:
        colour = "white"

    print("Start colour: " + colour)

    rand = random.randint(0,1)
    
    if rand:
        print("AI 1 went first")
        while not winner:
            boardState = AI1.AIMoveReturnBoardState(boardState, colour)

            if checkForWinner(boardState, boardSize, pieceRowCount):
                winner = 1
                print("AI 1 wins")
                continue
            
            #print(boardState)
            print("")
            colour = swapColour(colour)
            
            boardState = AI2.AIMoveReturnBoardState(boardState, colour)

            if checkForWinner(boardState, boardSize, pieceRowCount):
                winner = 2
                print("AI 2 wins")
                continue
            
            colour = swapColour(colour)
            #print(boardState)
    else:
        print("AI 2 went first")
        while not winner:
            boardState = AI2.AIMoveReturnBoardState(boardState, colour)

            if checkForWinner(boardState, boardSize, pieceRowCount):
                winner = 2
                print("AI 2 wins")
                continue

            #print(boardState)
            print("")
            colour = swapColour(colour)
            
            boardState = AI1.AIMoveReturnBoardState(boardState, colour)

            if checkForWinner(boardState, boardSize, pieceRowCount):
                winner = 1
                print("AI 1 wins")
                continue
            
            colour = swapColour(colour)
            #print(boardState)
    
    return winner

"""
easyWin = 0
hardWinAgainstEasy = 0
for i in range(100):
    winner = comparingAIs(easyAI, hardAI, boardState6x6)
    if winner == 1:
        easyWin += 1
    else:
        hardWinAgainstEasy += 1

print("After 100 games easy wins against hard this many times: " + str(easyWin))

mediumWin = 0
hardWinAgainstMedium = 0
for i in range(100):
    winner = comparingAIs(mediumAI, hardAI, boardState6x6)
    if winner == 1:
        mediumWin += 1
    else:
        hardWinAgainstMedium += 1

print("After 100 games medium wins against hard this many times: " + str(mediumWin))




MCTSWin = 0
hardWinAgainstMCTS = 0
for i in range(100):
    winner = comparingAIs(MCTS, hardAI, boardState6x6)
    if winner == 1:
        MCTSWin += 1
    else:
        hardWinAgainstMCTS += 1

print("After 100 games MCTS wins against hard this many times: " + str(MCTSWin))

print("")

print("After 100 games hard wins against easy this many times: " + str(hardWinAgainstEasy))
print("After 100 games hard wins against medium this many times: " + str(hardWinAgainstMedium))
print("After 100 games hard wins against MCTS this many times: " + str(hardWinAgainstMCTS))
"""

def whoWinsMost():

    easyWin = 0
    hardWinAgainstEasy = 0
    for i in range(20):
        winner = comparingAIs(easyAI, hardAI, boardState6x6)
        if winner == 1:
            easyWin += 1
        else:
            hardWinAgainstEasy += 1

    print("After 20 games easy wins against hard this many times: " + str(easyWin))

    mediumWin = 0
    hardWinAgainstMedium = 0
    for i in range(20):
        winner = comparingAIs(mediumAI, hardAI, boardState6x6)
        if winner == 1:
            mediumWin += 1
        else:
            hardWinAgainstMedium += 1

    print("After 20 games medium wins against hard this many times: " + str(mediumWin))




    MCTSWin = 0
    hardWinAgainstMCTS = 0
    """
    for i in range(10):
        winner = comparingAIs(MCTS, hardAI, boardState6x6)
        if winner == 1:
            MCTSWin += 1
        else:
            hardWinAgainstMCTS += 1
    """

    print("After 20 games MCTS wins against hard this many times: " + str(MCTSWin))

    print("")

    print("After 20 games hard wins against easy this many times: " + str(hardWinAgainstEasy))
    print("After 20 games hard wins against medium this many times: " + str(hardWinAgainstMedium))
    print("After 20 games hard wins against MCTS this many times: " + str(hardWinAgainstMCTS)) 

#whoWinsMost()
timeDecisionMaking(hardAI)



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