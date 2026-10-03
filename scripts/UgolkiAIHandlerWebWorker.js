let pyodide;
let AIMove;

const locationOfAIs = { "easy" : "./scripts/easyAStarUgolkiAI.py",
                             "medium" : "./scripts/mediumMinimaxVariantUgolkiAI.py",
                             "hard" : "./scripts/hardMinimaxVariantUgolkiAI.py",
                             "MCTS" : "./scripts/ugolkiMCTSAI.py" };


let firstMessage = true;

self.onmessage = async (e) => {
    console.log("Message to worker: " + e.data);

    if (firstMessage) {
        await loadUgolkiAI(e.data);

        firstMessage = false;

    } else {
        postMessage(getUgolkiAIMove(e.data[0], e.data[1]));
    }
}

/*
self.addEventListener('load', () => {
    postMessage("loaded");
});
 */

async function loadUgolkiAI(fileLocation) {
    pyodide = await loadPyodide();
    //console.log(fileLocation);
    await pyodide.runPythonAsync(await (await fetch(fileLocation)).text());
    AIMove = await pyodide.globals.get("AIMove");
    console.log("AI has loaded");
}

function getUgolkiAIMove(boardState, AIColour) {

    let boardStateConvertedToPy = pyodide.toPy(boardState);
    return AIMove(boardStateConvertedToPy, AIColour);

}

//setTimeout( () => self.postMessage("loaded"), 1000);

//postMessage("loaded");