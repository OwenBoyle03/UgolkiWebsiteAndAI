'use strict'
//import GameModel from "../scripts/GameModel";

// Board size must be an even number
// Minimum board size of 2 x 2
// Maximum pieceRowCount is half the board size
// Minimum pieceRowCount is 1
// board size 2 x 2 a piece count of 1

const model = new GameModel();
const view = new GameView(model.getBoardState());

let scaledMousePosition = { x: 0, y: 0 };
let gameMode = "easy";
let whoGoesFirst = "white";
let winner = false;
let p1Colour = "white";
let currentPlayer = "white";
let AIColour = "black";
let clickedPiece;
let pyodide;
let AIMove;
let mouseDownTutorialHandlerBound;


view.checkForBoardSizeClick(changeBoardSize);
view.checkForNumOfRowsChange(changePieceRowCount);
view.checkForGameModeSelectClick(changeGameMode);
view.checkForColourSelectClick(changeColour);
view.checkForWhoGoesFirstClick(changeWhoGoesFirst);
view.checkForTutorialButtonClick(startTutorial);

function changeBoardSize(index) {
    let size = ((index+1)*2);
    view.getCanvas().removeEventListener('mousedown', mouseDownHandler);
    view.getCanvas().removeEventListener('mousedown', mouseDownTutorialHandlerBound);
    model.changeBoardSize(size);
    view.changeBoardSize(model.getBoardState());
    view.showCorrectNumOfRowsWithPiecesButtons();
    view.highlightTheChosenOption(view.getBoardSizeSelect(), index);

    if (model.getPieceRowCount() > (size/2)) {
        view.highlightTheChosenOption(view.getNumOfRowsWithPieces(), (size/2)-1);
    } else {
        view.highlightTheChosenOption(view.getNumOfRowsWithPieces(), model.getPieceRowCount()-1);
    }

    currentPlayer = p1Colour;

    startNewMatch();
}

function changePieceRowCount(index) {
    let number = (index + 1);
    view.getCanvas().removeEventListener('mousedown', mouseDownHandler);
    view.getCanvas().removeEventListener('mousedown', mouseDownTutorialHandlerBound);
    view.highlightTheChosenOption(view.getNumOfRowsWithPieces(), index);
    model.changeRowCount(number);
    currentPlayer = p1Colour;

    startNewMatch();
}

function changeGameMode(index) {
    let mode = view.getGameModeSelect()[index].id;
    view.getCanvas().removeEventListener('mousedown', mouseDownHandler);
    view.getCanvas().removeEventListener('mousedown', mouseDownTutorialHandlerBound);
    view.highlightTheChosenOption(view.getGameModeSelect(), index);
    gameMode = mode;
    currentPlayer = p1Colour;

    if (gameMode !== "local") {
        console.log(mode);
        loadUgolkiAI(locationOfAIs[mode]);
    }

    startNewMatch();
}

function changeColour(index) {
    let colour = view.getColourSelect()[index].id;
    view.getCanvas().removeEventListener('mousedown', mouseDownHandler);
    view.getCanvas().removeEventListener('mousedown', mouseDownTutorialHandlerBound);
    if (colour === "random") {
        colour = getRandomColour();
    }
    view.highlightTheChosenOption(view.getColourSelect(), index);
    p1Colour = colour;
    currentPlayer = colour;
    changeAIColour(colour);
    startNewMatch();
}

function changeWhoGoesFirst(index) {
    let colour = view.getWhoGoesFirst()[index].id;
    view.getCanvas().removeEventListener('mousedown', mouseDownHandler);
    view.getCanvas().removeEventListener('mousedown', mouseDownTutorialHandlerBound);
    view.highlightTheChosenOption(view.getWhoGoesFirst(), index);
    if (colour === "r") {
        colour = getRandomColour();
    } else if (colour === "w") {
        colour = "white";
    } else {
        colour = "black";
    }
    currentPlayer = p1Colour;
    whoGoesFirst = colour;
    startNewMatch();
}

function changeAIColour(playerColour) {
    if (playerColour === "white") {
        AIColour = "black";
    } else {
        AIColour = "white";
    }
}

function getRandomColour() {
    let randomNumber = Math.floor(Math.random() * 2)
    if (randomNumber === 0) {
        return "white";
    }
    return "black";
}


const locationOfAIs = { "easy" : "./scripts/easyAIUgolkiHeuristicBased.py",
                             "medium" : "./scripts/mediumMinimaxVariantUgolkiAI.py",
                             "hard" : "./scripts/hardMinimaxVariantUgolkiAI.py",
                             "MCTS" : "./scripts/ugolkiMCTSAI.py" };


function startNewMatch() {
    view.clearTutorialText();
    view.displayCurrentPlayersTurn(whoGoesFirst);

    //removeAllEventListenersFromCanvas();

    if (gameMode === "local") {
        resetGame();
        currentPlayer = whoGoesFirst;
        view.getCanvas().addEventListener('mousedown', mouseDownHandler);
    } else if (whoGoesFirst === currentPlayer) {
        resetGame();
        view.getCanvas().addEventListener('mousedown', mouseDownHandler);
    } else {
        resetGame();
        ugolkiAITurn();
    }
}

async function loadUgolkiAI(fileLocation) {
    pyodide = await loadPyodide();
    //console.log(fileLocation);
    await pyodide.runPythonAsync(await (await fetch(fileLocation)).text());
    AIMove = await pyodide.globals.get("AIMove");
    console.log("AI has loaded");
}

/*
async function loadUgolkiAI(fileLocation) {
    // Need to find a way to make this load separately of the page
    pyodide = await loadPyodide();
    //console.log(fileLocation);
    await pyodide.runPython(await (await fetch(fileLocation)).text());
    AIMove = await pyodide.globals.get("AIMove");
    console.log("AI has loaded");
};
*/

function ugolkiAITurn() {

    let boardStateConvertedToPy = pyodide.toPy(model.getBoardState());
    let pieceToMove = AIMove(boardStateConvertedToPy, AIColour);

    let piece = view.getPieceFromBoardPosition(pieceToMove[2], pieceToMove[3]);

    model.movePiece(pieceToMove[0], pieceToMove[1], pieceToMove[2], pieceToMove[3]);
    piece.movePiecePositionBoardXY(pieceToMove[0], pieceToMove[1]);
    view.reDrawCanvas();
    winner = model.checkForWinner();

    if (winner) {
        view.displayWinScreen(winner);
        view.getCanvas().addEventListener('mousedown', resetGame, { once: true });
    } else {
        view.displayCurrentPlayersTurn(currentPlayer);
        view.getCanvas().addEventListener('mousedown', mouseDownHandler);
    }
}

function moveHandler(e) {
    view.setPiecePositionToMousePosition(e, view.getPieceList().indexOf(clickedPiece));
    view.reDrawCanvas();
    model.evaluateAllLegalMoves(clickedPiece.getBoardX(), clickedPiece.getBoardY()).forEach((move) => {
        view.drawPositionPuck(move.x, move.y);
    });
}

function mouseUpHandler(e) {
    view.getCanvas().removeEventListener('mousemove', moveHandler);
    view.getCanvas().removeEventListener('mouseup', mouseUpHandler);

    scaledMousePosition = view.getCanvasScaledMousePosition(e);
    let centreOfSquare = view.closestSquareCentre(scaledMousePosition.x, scaledMousePosition.y);

    if (model.isPieceInList(centreOfSquare, model.evaluateAllLegalMoves(clickedPiece.getBoardX(), clickedPiece.getBoardY()))) {
        model.movePiece(centreOfSquare.x, centreOfSquare.y, clickedPiece.getBoardX(), clickedPiece.getBoardY());
        clickedPiece.movePiecePositionBoardXY(centreOfSquare.x, centreOfSquare.y);
        view.reDrawCanvas();
        winner = model.checkForWinner();

        if (winner) {
            //alert(winner + " has won the game, congratulations!");
            view.displayWinScreen(winner);
            view.getCanvas().addEventListener('mousedown', resetGame, { once: true });

        } else if (gameMode === "local") {
            localChangePlayer();
            view.displayCurrentPlayersTurn(currentPlayer);
            view.getCanvas().addEventListener('mousedown', mouseDownHandler);
        } else {
            //view.getCanvas().removeEventListener('mousedown', mouseDownHandler);
            //ugolkiAITurn();
            //requestAnimationFrame(() => ugolkiAITurn());
            view.displayCurrentPlayersTurn(AIColour);
            // This works because it forces the current stack to empty which lets the canvas render
            setTimeout(() => ugolkiAITurn(), 0);
        }

    } else {
        clickedPiece.movePiecePositionBoardXY(clickedPiece.getBoardX(), clickedPiece.getBoardY());
        view.reDrawCanvas();
        view.getCanvas().addEventListener('mousedown', mouseDownHandler);
    }
}

function mouseDownHandler(e) {
    scaledMousePosition = view.getCanvasScaledMousePosition(e);

    view.getPieceList().forEach((piece) => {
        if (piece.doesPieceIntersect(scaledMousePosition) && piece.getColour() === currentPlayer) {
            clickedPiece = piece;

            view.getCanvas().removeEventListener('mousedown', mouseDownHandler);

            view.getCanvas().addEventListener('mousemove', moveHandler);

            view.getCanvas().addEventListener('mouseup', mouseUpHandler);
        }
    });
}

function startTutorial() {

    view.getCanvas().removeEventListener('mousedown', mouseDownHandler);

    view.highlightTheChosenOption(view.getBoardSizeSelect(), 3);
    model.changeBoardSize(8);
    view.showCorrectNumOfRowsWithPiecesButtons();
    view.changeBoardSize(model.getBoardState());

    view.highlightTheChosenOption(view.getNumOfRowsWithPieces(), 3);
    model.changeRowCount(4);

    view.highlightTheChosenOption(view.getWhoGoesFirst(), 0);
    whoGoesFirst = "white";

    model.setBoardToTutorialStartPosition();
    view.reDrawCanvasForGameRestart(model.getBoardState());

    currentPlayer = "white";
    AIColour = "black";
    view.highlightTheChosenOption(view.getColourSelect(), 0);

    const listOfPiecesToMove = [{x:2, y:5}, {x:2, y:3}, {x:4, y:0}, {x:0, y:4}, {x:1, y:5}, {x:2, y:6}];

    const positionsToMoveTo = [{x:2, y:3}, {x:2, y:2}, {x:0, y:2}, {x:2, y:0}, {x:1, y:3}, {x:2, y:5}];

    const opponentMoves = [  {x:4, y:6}, {x:6, y:6}, {x:6, y:0}, {x:6, y:4}, {x:2, y:4}, {x:1, y:4},
                                                     {x:7, y:1}, {x:7, y:2}, {x:6, y:3}, {x:6, y:5}, {x:5, y:4}, {x:5, y:5}];

    const tutorialText = [  "To win the game and complete the tutorial, move the final piece.",
                                    "Please pick up the final piece.",
                                    "In order to win the game you need to set up your pieces in the same formation " +
                                    "that they started in, but on the opponents corner of the board. Place the piece on square C3.",
                                    "Please pick up the piece on square D3.",
                                    "Jumping over pieces is not limited to only your pieces. You can also jump over " +
                                    "your opponents pieces. Please place your piece on square C1.",
                                    "Please pick up the piece on square A5.",
                                    "If the pieces are aligned properly then jumps can be chained in the same turn. " +
                                    "The piece on square E1 can jump to C1 then to C3 and again into A3. Please place the " +
                                    "piece on square A3.",
                                    "Please pick up the piece on square E1.",
                                    "When there is a piece in front of the piece you wish to move, and there is an empty" +
                                    " space in front of the blocking piece, your piece can jump over it onto the available space. " +
                                    "Please place your piece on square D2.",
                                    "Please pick up the piece on square F2.",
                                    "When you pick a piece up, a number of grey circles show you the possible moves you can make." +
                                    " As you can see, your piece can move in one of four directions. You can move pieces as long as" +
                                    " there is an open space in any of the four directions. Please place the piece down on square F3.",
                                    "Click and hold the white piece on square G3"];

    view.changeTutorialText("Click and hold the white piece on square G3");
    view.getCanvas().addEventListener('mousedown', mouseDownTutorialHandler.bind(null, listOfPiecesToMove, positionsToMoveTo, tutorialText, opponentMoves), { once: true });
}

function mouseDownTutorialHandler(listOfPiecesToMove, positionsToMoveTo, tutorialText, opponentMoves, e) {
    scaledMousePosition = view.getCanvasScaledMousePosition(e);

    let listLength = listOfPiecesToMove.length;
    let piece = view.getPieceFromBoardPosition(listOfPiecesToMove[listLength-1].x, listOfPiecesToMove[listLength-1].y);

    if (piece.doesPieceIntersect(scaledMousePosition) && piece.getColour() === currentPlayer) {
        clickedPiece = piece;

        view.changeTutorialText(tutorialText[tutorialText.length-2]);

        view.getCanvas().addEventListener('mousemove', moveHandler);

        view.getCanvas().addEventListener('mouseup', mouseUpTutorialHandler.bind(null, listOfPiecesToMove, positionsToMoveTo, tutorialText, opponentMoves), { once: true });
    } else {
        view.getCanvas().addEventListener('mousedown', mouseDownTutorialHandler.bind(null, listOfPiecesToMove, positionsToMoveTo, tutorialText, opponentMoves), { once: true });
    }
}

function mouseUpTutorialHandler(listOfPiecesToMove, positionsToMoveTo, tutorialText, opponentMoves, e) {
    view.getCanvas().removeEventListener('mousemove', moveHandler);

    scaledMousePosition = view.getCanvasScaledMousePosition(e);
    let centreOfSquare = view.closestSquareCentre(scaledMousePosition.x, scaledMousePosition.y);

    let listLength = listOfPiecesToMove.length;
    let desiredMoveXY = {   x: positionsToMoveTo[listLength-1].x,
                                         y: positionsToMoveTo[listLength-1].y };


    if (JSON.stringify(centreOfSquare) === JSON.stringify(desiredMoveXY)) {

        model.movePiece(centreOfSquare.x, centreOfSquare.y, clickedPiece.getBoardX(), clickedPiece.getBoardY());
        clickedPiece.movePiecePositionBoardXY(centreOfSquare.x, centreOfSquare.y);
        view.reDrawCanvas();

        tutorialText.pop();
        tutorialText.pop();
        view.changeTutorialText(tutorialText[tutorialText.length-1]);

        winner = model.checkForWinner();
        if (winner) {
            view.changeTutorialText("Congratulations on finishing the tutorial. You now know everything you" +
                " need to know about Ugolki. Good luck in your future matches!");

            // Need to wait for some kind of input or some delay before starting a new match

            view.displayWinScreen(winner);

            view.getCanvas().addEventListener('mousedown', startNewMatch, { once: true });

        } else {

            listOfPiecesToMove.pop();
            positionsToMoveTo.pop();

            let opponentMovesLength = opponentMoves.length;

            console.log((opponentMoves[(opponentMovesLength-1)].x + ", " + opponentMoves[(opponentMovesLength-1)].y));

            model.movePiece(opponentMoves[(opponentMovesLength-2)].x, opponentMoves[(opponentMovesLength-2)].y, opponentMoves[(opponentMovesLength-1)].x, opponentMoves[(opponentMovesLength-1)].y);
            view.getPieceFromBoardPosition(opponentMoves[(opponentMovesLength-1)].x, opponentMoves[(opponentMovesLength-1)].y).movePiecePositionBoardXY(opponentMoves[(opponentMovesLength-2)].x, opponentMoves[(opponentMovesLength-2)].y);
            view.reDrawCanvas();

            opponentMoves.pop();
            opponentMoves.pop();

            mouseDownTutorialHandlerBound = mouseDownTutorialHandler.bind(null, listOfPiecesToMove, positionsToMoveTo, tutorialText, opponentMoves);

            view.getCanvas().addEventListener('mousedown', mouseDownTutorialHandlerBound, { once: true });
        }

    } else {
        clickedPiece.movePiecePositionBoardXY(clickedPiece.getBoardX(), clickedPiece.getBoardY());
        view.reDrawCanvas();
        view.changeTutorialText(tutorialText[tutorialText.length-1]);
        view.getCanvas().addEventListener('mousedown', mouseDownTutorialHandler.bind(null, listOfPiecesToMove, positionsToMoveTo, tutorialText, opponentMoves), { once: true });

    }
}

function localChangePlayer() {
    if (currentPlayer === "white") {
        currentPlayer = "black";
    } else {
        currentPlayer = "white";
    }
}

function resetGame() {
    model.setBoardToStartPosition();
    view.reDrawCanvasForGameRestart(model.getBoardState());
    winner = false;
}

function setMatchDefaults() {
    view.highlightTheChosenOption(view.getBoardSizeSelect(), 3);
    view.highlightTheChosenOption(view.getNumOfRowsWithPieces(), 3);
    view.highlightTheChosenOption(view.getGameModeSelect(), 1);
    view.highlightTheChosenOption(view.getColourSelect(), 0);
    view.highlightTheChosenOption(view.getWhoGoesFirst(), 0);
}

setMatchDefaults();
loadUgolkiAI(locationOfAIs["easy"]).then(startNewMatch);