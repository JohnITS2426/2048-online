from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import game
import copy

# Importa il modulo game (assicurati che esista)

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = (BASE_DIR / ".." / "FrontEnd-2048").resolve()

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

# Stato globale del gioco
state = {
    "board": game.new_board(),
    "score": 0,
    "game_over": False,
    "won": False
}

@app.get("/")
def serve_index():
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.post("/game/start")
def start_game():
    state["board"] = game.new_board()
    state["score"] = 0
    state["game_over"] = False
    state["won"] = False
    return state

@app.post("/game/move/{direction}")
def make_move(direction: int):
    if direction < 0 or direction > 3:
        raise HTTPException(status_code=400, detail="Direzione non valida")
    prev_board = copy.deepcopy(state["board"])
    new_board, score_delta = game.move(state["board"], direction)
    if new_board != prev_board:
        state["board"] = new_board
        state["score"] += score_delta
        state["won"] = game.check_won(state["board"])
        state["game_over"] = game.check_game_over(state["board"])
    return state

@app.get("/game/state")
def get_state():
    return state
