'use strict'

const GameModel = require("../scripts/GameModel");

const startBoard8x8With4Rows = [[1,1,1,1,0,0,0,0],
                                      [1,1,1,1,0,0,0,0],
                                      [1,1,1,1,0,0,0,0],
                                      [1,1,1,1,0,0,0,0],
                                      [0,0,0,0,2,2,2,2],
                                      [0,0,0,0,2,2,2,2],
                                      [0,0,0,0,2,2,2,2],
                                      [0,0,0,0,2,2,2,2]];

const startBoard2x2With1Rows = [[1,0],
                                      [0,2]];

const testBoard8x8 = [[0,1,0,0,0,1,1,2],
                            [0,0,0,0,0,2,1,2],
                            [1,0,1,1,2,2,2,0],
                            [0,2,0,0,0,1,1,0],
                            [0,0,2,0,2,2,1,0],
                            [0,1,1,1,2,1,2,2],
                            [0,1,0,1,0,0,0,0],
                            [0,0,0,0,2,2,2,0]];

const TestBoard6x6 = [[2,0,1,2,2,0],
                            [2,1,1,1,2,0],
                            [1,0,1,2,0,0],
                            [0,1,2,2,0,0],
                            [1,1,2,0,0,0],
                            [0,0,0,0,0,0]];

describe('GameModel class', () => {

    const testModel = new GameModel(8, 4);

    test('GameModel should be defined', () => {
        expect(testModel).toBeDefined();
    });

    test('GameModel this.boardState should be set properly upon definition', () => {

        expect(testModel.getBoardState()).toEqual(startBoard8x8With4Rows);

    });

    test('movePiece function should work as intended', () => {

        testModel.movePiece(0, 7, 0, 0);
        expect(testModel.getBoardState()[7][0]).toBe(1);
        expect(testModel.getBoardState()[0][0]).toBe(0);

        testModel.movePiece(7, 3, 6, 5);
        expect(testModel.getBoardState()[3][7]).toBe(2);
        expect(testModel.getBoardState()[5][6]).toBe(0);

    });

    test('evaluateAllJumpOvers function should work as intended', () => {
        testModel.changeBoardSize(6);
        testModel.changeRowCount(3);
        testModel.setBoardState(TestBoard6x6);
        //testModel.setBoardToStartPosition(8, 4);
        expect(testModel.getBoardState()).toStrictEqual(TestBoard6x6);

        // Should have 3 in this list in unknown order
        // { x: 1, y: 2 }, { x: 3, y: 4 }, { x: 1, y: 0 }
        console.log(testModel.evaluateAllJumpOvers(3, 2, [{ x: 3, y: 2 }]));

        testModel.changeBoardSize(8);
        testModel.changeRowCount(4);
        testModel.setBoardState(testBoard8x8);
        expect(testModel.getBoardState()).toStrictEqual(testBoard8x8);

        // Should have 6 in this list in this order
        // [{'x': 3, 'y': 4}, {'x': 5, 'y': 6}, {'x': 7, 'y': 4}, {'x': 1, 'y': 4}, {'x': 1, 'y': 2}, {'x': 7, 'y': 6}]
        console.log(testModel.evaluateAllJumpOvers(5, 4, [{ "x" : 5, "y" : 4 }]));
    });

    test('evaluateAllLegalMoves function should work as intended', () => {

        testModel.changeBoardSize(8);
        testModel.changeRowCount(4);
        testModel.setBoardToStartPosition(8, 4);

        expect(testModel.evaluateAllLegalMoves(0, 0)).toEqual([]);

        expect(testModel.evaluateAllLegalMoves(3, 3)).toEqual([{"x":3, "y":4}, {"x":4, "y":3}]);

        expect(testModel.evaluateAllLegalMoves(6, 5)).toEqual([{"x":6, "y":3}]);

        expect(testModel.evaluateAllLegalMoves(5, 5)).toEqual([{"x":5, "y":3}, {"x":3, "y":5}]);

        //expect(testModel.evaluateAllLegalMoves(4, 5)).toEqual([{"x":3, "y":5}, {"x":4, "y":3}]);

    });

    test('setBoardToStartPosition function should work as intended', () => {
        testModel.changeBoardSize(8);
        testModel.changeRowCount(4);
        //testModel.setBoardToStartPosition(8, 4);
        expect(testModel.getBoardState()).toStrictEqual(startBoard8x8With4Rows);

        testModel.changeBoardSize(2);
        testModel.changeRowCount(1);
        //testModel.setBoardToStartPosition(2, 1);
        expect(testModel.getBoardState()).toStrictEqual(startBoard2x2With1Rows);
    });

});