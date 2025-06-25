from typing import List
from pydantic import BaseModel

class GameState(BaseModel):
    board: List[List[int]]
    score: int
    game_over: bool
    won: bool
