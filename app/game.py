import random

GRID_SIZE = 5

def new_board():
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_random_tile(board)
    add_random_tile(board)
    return board

def add_random_tile(board):
    empty = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == 0]
    if not empty:
        return
    i, j = random.choice(empty)
    board[i][j] = 2 if random.random() < 0.9 else 4

def slide_row(row):
    new_row = [i for i in row if i != 0]
    merged = []
    skip = False
    for i in range(len(new_row)):
        if skip:
            skip = False
            continue
        if i + 1 < len(new_row) and new_row[i] == new_row[i+1]:
            merged.append(new_row[i] * 2)
            skip = True
        else:
            merged.append(new_row[i])
    merged += [0] * (GRID_SIZE - len(merged))
    return merged

def move(board, direction):
    rotated = board
    for _ in range(direction):  # 0 = left, 1 = up, 2 = right, 3 = down
        rotated = [list(row) for row in zip(*rotated[::-1])]

    moved = [slide_row(row) for row in rotated]

    for _ in range((4 - direction) % 4):
        moved = [list(row) for row in zip(*moved[::-1])]

    if moved != board:
        add_random_tile(moved)
    
    return moved

def check_won(board):
    return any(cell == 2048 for row in board for cell in row)

def check_game_over(board):
    for direction in range(4):
        if move([row[:] for row in board], direction) != board:
            return False
    return True
