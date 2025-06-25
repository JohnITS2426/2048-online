from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app import game
from pathlib import Path
import copy

app = FastAPI()

# Stato del gioco
state = {
    "board": game.new_board(),
    "score": 0,
    "game_over": False,
    "won": False
}

frontend_dir = Path(__file__).parent.parent / "FrontEnd-2048"
if not frontend_dir.exists():
    raise RuntimeError(f"Directory {frontend_dir} non trovata")

# Mount frontend
app.mount("/static", StaticFiles(directory="FrontEnd-2048"), name="static")


@app.get("/")
def serve_index():
    index_file = frontend_dir / "/static/index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="index.html non trovato")
    return FileResponse(str(index_file))

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
    new_board = game.move(state["board"], direction)
    if new_board != prev_board:
        state["board"] = new_board
        state["won"] = game.check_won(state["board"])
        state["game_over"] = game.check_game_over(state["board"])
    return state

@app.get("/game/state")
def get_state():
    return state
