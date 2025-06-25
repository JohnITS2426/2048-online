const API_BASE = "";

async function startGame() {
  const res = await fetch(`${API_BASE}/game/start`, { method: "POST" });
  const state = await res.json();
  updateBoard(state);
}

async function move(direction) {
  const res = await fetch(`${API_BASE}/game/move/${direction}`, { method: "POST" });
  const state = await res.json();
  updateBoard(state);
}

function updateBoard(state) {
  const boardDiv = document.getElementById("board");
  boardDiv.innerHTML = "";

  state.board.flat().forEach(value => {
    const tile = document.createElement("div");
    tile.className = "tile";
    tile.textContent = value === 0 ? "" : value;
    tile.style.backgroundColor = getTileColor(value);
    boardDiv.appendChild(tile);
  });

  document.getElementById("score").textContent = `Punteggio: ${state.score}`;
  document.getElementById("status").textContent =
    state.won ? "🎉 Hai raggiunto 2048!" :
    state.game_over ? "💀 Game Over!" : "";
}

function getTileColor(value) {
  const colors = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e"
  };
  return colors[value] || "#3c3a32";
}

document.addEventListener("keydown", (e) => {
  const dirs = { ArrowLeft: 0, ArrowUp: 1, ArrowRight: 2, ArrowDown: 3 };
  if (dirs[e.key] !== undefined) {
    move(dirs[e.key]);
  }
});

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/static/service-worker.js");
}


window.onload = startGame;
