from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app import game
import os

app = FastAPI()

# Stato del gioco
state = {
    "board": game.new_board(),
    "score": 0,
    "game_over": False,
    "won": False
}

# Mount frontend
app.mount("/static", StaticFiles(directory="FrontEnd-2048"), name="static")

@app.get("/")
def root():
    return FileResponse("FrontEnd-2048/index.html")

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
        return {"error": "direzione non valida"}
    prev_board = [row[:] for row in state["board"]]
    new_board = game.move(state["board"], direction)
    if new_board != prev_board:
        state["board"] = new_board
        state["won"] = game.check_won(state["board"])
        state["game_over"] = game.check_game_over(state["board"])
    return state

@app.get("/game/state")
def get_state():
    return state
