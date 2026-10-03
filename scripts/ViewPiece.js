'use strict'

class ViewPiece {
    constructor(canvasX, canvasY, boardX, boardY, colour, distanceBetweenSquares, distanceToCentreOfSquare, canvas, context) {
        this.canvasX = canvasX;
        this.canvasY = canvasY;
        this.boardX = boardX;
        this.boardY = boardY;
        this.colour = colour;

        this.distanceBetweenSquares = distanceBetweenSquares;
        this.distanceToCentreOfSquare = distanceToCentreOfSquare;

        this.canvas = canvas;
        this.context = context;

        this.drawPiece();
    }

    getBoardX() {
        return this.boardX;
    }

    getBoardY() {
        return this.boardY;
    }

    getColour() {
        return this.colour;
    }

    // Top left board square is boardSquareX = 0, boardSquareY = 0
    drawPiece() {
        // Sets colour of pieces
        this.context.fillStyle = this.colour;

        // Draws piece
        this.context.beginPath();
        // Multiply by 125 to get to the start of the square and add 62.5 to get the centre of square
        // Might need to change the radius for sake of board scaling
        this.context.arc(this.canvasX, this.canvasY, (this.distanceBetweenSquares * 0.36), 0, 2 * Math.PI);
        this.context.fill();
        this.context.closePath();
        //console.log("Piece has been drawn");
    }

    // Top left board square is boardSquareX = 0, boardSquareY = 0
    drawPieceWithBoardXY(boardSquareX, boardSquareY, colour) {
        // Sets colour of pieces
        this.context.fillStyle = colour;

        // X and Y coordinates of the piece
        this.pieceX = boardSquareX;
        this.pieceY = boardSquareY;

        // Draws piece
        this.context.beginPath();
        // Multiply by 125 to get to the start of the square and add 62.5 to get the centre of square
        // Might need to change the 45
        this.context.arc(((this.pieceX * this.distanceBetweenSquares) + this.distanceToCentreOfSquare), ((this.pieceY * this.distanceBetweenSquares) + this.distanceToCentreOfSquare), (this.distanceBetweenSquares * 0.36), 0, 2 * Math.PI);
        this.context.fill();
    }

    // Mouse intersecting pieces calculation
    doesPieceIntersect(coord) {
        // 45 is used because it's the radius of the game piece
        // Might need to change the 45
        return Math.sqrt((coord.x - this.canvasX) ** 2 + (coord.y - this.canvasY) ** 2) < (this.distanceBetweenSquares * 0.36);
    }

    movePiecePosition(x, y) {
        this.canvasX = x;
        this.canvasY = y;
    }

    movePiecePositionBoardXY(x, y) {
        this.boardX = x;
        this.boardY = y;
        this.canvasX = ((x * this.distanceBetweenSquares) + this.distanceToCentreOfSquare);
        this.canvasY = ((y * this.distanceBetweenSquares) + this.distanceToCentreOfSquare);
    }

}