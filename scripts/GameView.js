'use strict'

class GameView {

    constructor(boardState) {
        this.canvas = document.getElementById('gameCanvas');
        // Checking for canvas support
        if (this.canvas.getContext) {
            this.context = this.canvas.getContext('2d');
        }

        this.boardSizeSelect = document.querySelectorAll('.boardSize');

        this.numOfRowsWithPieces = document.querySelectorAll('.numOfRowsWithPieces');

        this.gameModeSelect = document.querySelectorAll('.gameMode');
        this.colourSelect = document.querySelectorAll('.pieceColour');
        this.whoGoesFirst = document.querySelectorAll('.whoGoesFirst');
        //this.changeSettingsButton = document.getElementById('changeSettingsButton');
        this.tutorialButton = document.querySelector('#topBarButton');
        this.tutorialPara = document.querySelector('#tutorialText');
        this.rightContent = document.querySelector('#rightContent');

        this.boardSize = boardState.length;
        this.distanceBetweenSquares = 1000 / this.boardSize;
        this.distanceToCentreOfSquare = this.distanceBetweenSquares / 2;

        this.board = new ViewBoard(this.canvas, this.context, this.boardSize, this.distanceBetweenSquares, this.distanceToCentreOfSquare);

        this.board.drawBoard();
        this.listOfPieces = [];
        this.translateBoardStateToPieces(boardState);
    }

    getCanvas() {
        return this.canvas;
    }

    retrieveContext() {
        return this.context;
    }

    getBoardSizeSelect() {
        return this.boardSizeSelect;
    }

    getNumOfRowsWithPieces() {
        return this.numOfRowsWithPieces;
    }

    getTutorialButton() {
        return this.tutorialButton;
    }
    getWhoGoesFirst() {
        return this.whoGoesFirst;
    }
    getColourSelect() {
        return this.colourSelect;
    }
    getGameModeSelect() {
        return this.gameModeSelect;
    }

    getBoard() {
        return this.board;
    }

    getPieceList() {
        return this.listOfPieces;
    }

    getPiece(index) {
        return this.listOfPieces[index];
    }

    checkForBoardSizeClick(handler) {
        for (let i = 0; i < this.boardSizeSelect.length; i++) {
            this.getBoardSizeSelect()[i].addEventListener('click', () => handler(i));
        }
    }

    checkForNumOfRowsChange(handler) {
        for (let i = 0; i < this.numOfRowsWithPieces.length; i++) {
            this.getNumOfRowsWithPieces()[i].addEventListener('click', () => handler(i));
        }
    }

    checkForGameModeSelectClick(handler) {
        for (let i = 0; i < this.gameModeSelect.length; i++) {
            this.getGameModeSelect()[i].addEventListener('click', () => handler(i));
        }
    }

    checkForColourSelectClick(handler) {
        for (let i = 0; i < this.colourSelect.length; i++) {
            this.getColourSelect()[i].addEventListener('click', () => handler(i));
        }
    }

    checkForWhoGoesFirstClick(handler) {
        for (let i = 0; i < this.whoGoesFirst.length; i++) {
            this.getWhoGoesFirst()[i].addEventListener('click', () => handler(i));
        }
    }

    checkForTutorialButtonClick(handler) {
        this.getTutorialButton().addEventListener('click', handler);
    }

    checkForCanvasClick(typeOfEvent, handler) {
        this.getCanvas().addEventListener(typeOfEvent, handler);
    }

    removeCanvasEventListener(typeOfEvent, handler) {
        this.getCanvas().removeEventListener(typeOfEvent, handler);
    }

    showCorrectNumOfRowsWithPiecesButtons() {
        for (let i = 0; i < 4; i++) {
            //console.log(view.getNumOfRowsWithPieces()[i].style.display);
            this.getNumOfRowsWithPieces()[i].style.display = "initial";
            //console.log(view.getNumOfRowsWithPieces()[i].style.display);
        }

        for (let i = 0; i < (4 - (this.boardSize/2)); i++) {
            this.getNumOfRowsWithPieces()[3-i].style.display = "none";
        }
    }

    changeBoardSize(boardState) {
        this.boardSize = boardState.length;
        this.distanceBetweenSquares = 1000 / this.boardSize;
        this.distanceToCentreOfSquare = this.distanceBetweenSquares / 2;
        this.retrieveContext().clearRect(0, 0, this.getCanvas().width, this.getCanvas().height);
        this.getBoard().changeBoardSize(boardState.length);
        this.reDrawCanvasForGameRestart(boardState);
    }

    translateBoardStateToPieces(boardState) {
        let boardSquare;
        let canvasX = 0;
        let canvasY = 0;

        for (let i = 0; i < this.boardSize; i++) {
            for (let j = 0; j < this.boardSize; j++) {
                /*
                console.log("Board State:");
                console.log(boardState);
                console.log("i:", i);
                console.log("j:", j);
                console.log(boardState[i][j]);
                 */
                boardSquare = (boardState[i][j]);
                if (boardSquare === 1) {
                    canvasX = this.boardPositionToCanvasPosition(j);
                    canvasY = this.boardPositionToCanvasPosition(i);
                    this.listOfPieces.push(new ViewPiece(canvasX, canvasY, j, i, "black", this.distanceBetweenSquares, this.distanceToCentreOfSquare, this.canvas, this.context));
                } else if (boardSquare === 2) {
                    canvasX = this.boardPositionToCanvasPosition(j);
                    canvasY = this.boardPositionToCanvasPosition(i);
                    this.listOfPieces.push(new ViewPiece(canvasX, canvasY, j, i, "white", this.distanceBetweenSquares, this.distanceToCentreOfSquare, this.canvas, this.context));
                }
            }
        }
    }

    resetPieces(boardState) {
        this.listOfPieces = [];

        this.translateBoardStateToPieces(boardState);
    }

    drawAllPieces() {
        // Loop to add all pieces
        for (let i = 0; i < this.listOfPieces.length; i++) {
            this.getPiece(i).drawPiece();
        }
    }

    boardPositionToCanvasPosition(pos) {
        return ((pos * this.distanceBetweenSquares) + this.distanceToCentreOfSquare);
    }

    /*
    getPieceIndexFromBoardPosition(boardX, boardY) {
        for (let i = 0; i < this.listOfPieces.length; i++) {
            if (this.listOfPieces[i].getBoardX() === boardX && this.listOfPieces[i].getBoardY() === boardY) {
                return i;
            }
        }
    }
     */

    getPieceFromBoardPosition(boardX, boardY) {
        let piece;
        for (let i = 0; i < this.listOfPieces.length; i++) {
            piece = this.listOfPieces[i];
            if (piece.getBoardX() === boardX && piece.getBoardY() === boardY) {
                return piece;
            }
        }
    }

    // This monstrosity can be done better
    closestSquareCentre(mouseX, mouseY) {
        //const listOfSquareCentres = [62.5, 187.5, 312.5, 437.5, 562.5, 687.5, 812.5, 937.5];
        let listOfSquareCentres = [];

        for (let i = 0; i < this.boardSize; i++) {
            listOfSquareCentres.push((this.distanceBetweenSquares * i) + this.distanceToCentreOfSquare);
        }

        console.log(listOfSquareCentres);

        let closestSquareX = 0;
        let closestSquareY = 0;

        let xLowerBound = 0;
        let xUpperBound = 0;
        for (let i = 0; i < listOfSquareCentres.length; i++) {
            if (listOfSquareCentres[i] > mouseX) {
                xUpperBound = listOfSquareCentres[i];
                break;
            }
            xLowerBound = listOfSquareCentres[i];
        }

        let yLowerBound = 0;
        let yUpperBound = 0;
        for (let i = 0; i < listOfSquareCentres.length; i++) {
            if (listOfSquareCentres[i] > mouseY) {
                yUpperBound = listOfSquareCentres[i];
                break;
            }
            yLowerBound = listOfSquareCentres[i];
        }

        //console.log("MouseX, MouseY: " + mouseX + ", " + mouseY);
        //console.log("XLowerBound, XUpperBound: " + xLowerBound + ", " + xUpperBound);
        if ((Math.abs(xLowerBound - mouseX)) < (Math.abs(xUpperBound - mouseX))) {
            closestSquareX = xLowerBound;
        } else {
            closestSquareX = xUpperBound;
        }

        //console.log("YLowerBound, YUpperBound: " + yLowerBound + ", " + yUpperBound);
        if ((Math.abs(yLowerBound - mouseY)) < (Math.abs(yUpperBound - mouseY))) {
            closestSquareY = yLowerBound;
        } else {
            closestSquareY = yUpperBound;
        }

        //console.log("Original Coordinates: " + mouseX + ", " + mouseY);
        closestSquareX = Math.round(closestSquareX / this.distanceBetweenSquares) - 1;
        closestSquareY = Math.round(closestSquareY / this.distanceBetweenSquares) - 1;
        //console.log("'Centered' Coordinates: " + closestSquareX + " " + closestSquareY);

        return { x: closestSquareX, y: closestSquareY };
    }

    // Mouse scaling calculations
    getCanvasScaledMousePosition(e) {
        let bounds = this.canvas.getBoundingClientRect();

        // Raw mouse position
        let mouseX = e.clientX;
        let mouseY = e.clientY;

        // Mouse position account for canvas position
        mouseX = mouseX - bounds.left - scrollX;
        mouseY = mouseY - bounds.top - scrollY;

        // Mouse position normalised for canvas bounds
        mouseX /= bounds.width;
        mouseY /= bounds.height;

        // Mouse position scaled to canvas coordinates
        mouseX *= this.canvas.width;
        mouseY *= this.canvas.height;

        // Since the mouse position is given in terms of pixel and the canvas measurements
        // are a mix of pixel and css scaling the mouse position needs to be scaled as well
        return { x: mouseX, y: mouseY };
    }

    setPiecePositionToMousePosition(e, index) {
        let scaledMousePosition = this.getCanvasScaledMousePosition(e);
        this.getPiece(index).movePiecePosition(scaledMousePosition.x, scaledMousePosition.y);
    }

    // This might need to be an async function
    reDrawCanvas() {
        this.retrieveContext().clearRect(0, 0, this.getCanvas().width, this.getCanvas().height);
        this.getBoard().drawBoard();
        this.drawAllPieces();
    }

    // This might need to be an async function
    reDrawCanvasForGameRestart(boardState) {
        this.retrieveContext().clearRect(0, 0, this.getCanvas().width, this.getCanvas().height);
        this.getBoard().drawBoard();
        this.resetPieces(boardState);
        this.drawAllPieces();
    }

    // Top left board square is boardSquareX = 0, boardSquareY = 0
    drawPositionPuck(x, y) {
        // Sets colour of pieces
        this.context.fillStyle = "grey";

        // Draws piece
        this.context.beginPath();
        // Multiply by 125 to get to the start of the square and add 62.5 to get the centre of square
        // Might need to change the radius for sake of board scaling
        this.context.arc(this.boardPositionToCanvasPosition(x), this.boardPositionToCanvasPosition(y), (this.distanceBetweenSquares * 0.16), 0, 2 * Math.PI);
        this.context.fill();
        this.context.closePath();
        //console.log("Piece has been drawn");
    }

    highlightTheChosenOption(buttonArray, chosenIndex) {
        for (let i = 0; i < buttonArray.length; i++) {
            buttonArray[i].style.color = "initial";
        }
        buttonArray[chosenIndex].style.color = "purple";
    }

    changeTutorialText(text) {
        this.tutorialPara.innerHTML = "<h1>Tutorial</h1><p>" + text + "</p>";
    }

    clearTutorialText() {
        this.tutorialPara.innerHTML = "";
    }

    displayCurrentPlayersTurn(colour) {
        if (colour === "white") {
            this.rightContent.innerHTML = "<h1>White's turn</h1>";
        } else {
            this.rightContent.innerHTML = "<h1>Black's turn</h1>";
        }
    }

    clearCurrentPlayersTurn() {
        this.rightContent.innerHTML = "";
    }

    displayWinScreen(winner) {
        // Sets the font and size of the text
        this.context.font = "" + (50) + "px Arial";

        // Sets the position from which text is positioned
        this.context.textBaseline = "top";

        this.context.fillStyle = 'blue';
        this.context.fillText(( winner + " wins!"), (400), (400));
        this.context.fillStyle = '#d18c47';
    }
}