"""Sudoku Game"""

import pyxel
import random
import numpy as np
from copy import deepcopy

game_won = False

with open('sudoku.csv') as f:
    lines = f.read().splitlines()

# Get one of the puzzles and its corresponding solution
line_number = random.randint(0, len(lines))
line = lines[line_number]
line = line.strip()
puzzle, solution = line.split(',')
print(puzzle, solution)

## Make a board structure to fill in the data with.
empty_board = [[0 for _ in range(9)] for _ in range(9)]
rows = ('{} {} {} | {} {} {} | {} {} {}' + '\n')*3
board = ((rows + '---------------------' + '\n')*2 + rows)
print(board.format(*[unit if unit else ' ' for row in empty_board for unit in row]))

## Fill Board with puzzle data
cage = iter(puzzle)
puzzle_board = [[int(next(cage)) for _ in range(9)] for _ in range(9)] 
solution_cage = iter(solution)
solution_board = [[int(next(solution_cage)) for _ in range(9)] for _ in range(9)]  
print(board.format(*[unit if unit else ' ' for row in puzzle_board for unit in row]))
print(board.format(*[unit if unit else ' ' for row in solution_board for unit in row]))

## Check if the board is valid
def rows_valid(board):
    for row in board:
        if len([unit for unit in row if unit]) == len(set(unit for unit in row if unit)):  
            continue
        else:
            return False
    return True

print(rows_valid(solution_board))

def cols_valid(board):
    is_valid = []
    for col in zip(*board):
        is_valid.append(len(list(filter(bool, col))) == len(set(filter(bool, col))))  
    if all(is_valid):  
        return True
    else:
        return False

print(cols_valid(solution_board))

# The little 3x3 rectangles on a sudoku board are called "boxes" 
# (https://simple.wikipedia.org/wiki/Sudoku)
boxes = [[i]*9 for i in range(1,10)]

def box_valid(board):
    board = np.array(board)
    slices = (slice(0, 3), slice(3, 6), slice(6, 9))
    box_coords = [(slice(0, 3), slice(0, 3)), (slice(3, 6), slice(0, 3)), (slice(6, 9), slice(0, 3))]
    for rows in slices:
        for cols in slices:
            box = board[rows, cols]
            if len(np.unique(box[box != 0])) != box[box != 0].size:
                return False
    return True

print(box_valid(solution_board))
width_size = 156
height_size = 183
pyxel.init(width_size, height_size, title="Sudoku Game")

def board_valid(task_board, solution_board):
    if not (rows_valid(task_board) and cols_valid(task_board) and box_valid(task_board)):
        return False
    
    for pcol, scol in zip(task_board, solution_board):
        for pval, sval in zip(pcol, scol):
            if pval and pval != sval:
                return False
    return True

## change board
selected_value = 1

def update_board(board, row, col, value):
    new_board = deepcopy(board)
    new_board[row][col] = value
    return new_board

cell_coordinates = (0, 0)
print(board.format(*[unit if unit else ' ' for row in puzzle_board for unit in row]))
print(board.format(*[unit if unit else ' ' for row in update_board(puzzle_board, 4, 4, 8) for unit in row]))
pyxel.cls(col=3)
print(pyxel.load('my_resource.pyxres', True, True))
image = pyxel.image(0)
pyxel.mouse(True)
            
def draw_cells():
    global puzzle_board
    global cell_coordinates
    global selected_value

    x_offset = 2
    y_offset = 2
    image_size = 16
    for i, row in enumerate(puzzle_board):
        for j, value in enumerate(row):
            x = i*image_size + i + x_offset
            y = j*image_size + j + y_offset
            u_width = 0
            v_height = value * image_size
            transparent_color = get_cell_transparent_color((i, j))
            pyxel.blt(x, y, 0, u_width, v_height, image_size, image_size, transparent_color)

def get_cell_transparent_color(cell_coordinate):
    global cell_coordinates
    global selected_value

    if cell_coordinate == cell_coordinates:
        transparent_color = 5
    elif selected_value and puzzle_board[cell_coordinate[0]][cell_coordinate[1]] == 0:
        transparent_color = 10
    else:
        transparent_color = 0
    return transparent_color

def draw_board_lines():
    x_offset = 2
    y_offset = 2
    pyxel.rect(x_offset, 50 + y_offset, w=150, h=1, col=0)
    pyxel.rect(x_offset, 100 + y_offset, w=150, h=1, col=0)
    pyxel.rect(50 + x_offset, y_offset, h=150, w=1, col=0)
    pyxel.rect(100 + x_offset, y_offset, h=150, w=1, col=0)
    pyxel.rect(x=0, y=156, h=5, w=200, col=0)

def get_transparent_color(value):
    global selected_value

    if selected_value == value:
        transparent_color = 5
    else:
        transparent_color = 10
    return transparent_color

def draw_selected_value():
    global selected_value

    x_offset = 2
    image_size = 16
    for i in range(9):
        transparent_color = get_transparent_color(i+1)
        pyxel.blt(x = i*image_size + i + x_offset, y=165, img=0, u=0, v = (i+1) * image_size, 
                  w=image_size, h=image_size, colkey=transparent_color)

def draw():
    global game_won

    if game_won:
        pyxel.cls(col=10)
    draw_cells()
    draw_board_lines()
    draw_selected_value()

def get_board_cage(mouse_x, mouse_y):
    return min(int(mouse_x // 20), 8), min(int(mouse_y // 20), 8)

def board_is_full(board):
    for row in board:
        for val in row:
            if val == 0:
                return False
            else:
                return True
            
def control_quit():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def control_left_click():
    global cell_coordinates
    global selected_value
    
    mouse_position = (pyxel.mouse_x, pyxel.mouse_y)
    board_cage = get_board_cage(*mouse_position)
    if mouse_position[1] < width_size:
        cell_coordinates = board_cage
    else:
        selected_value = board_cage[0] + 1
        
def control_right_click():
    global selected_value

    mouse_position = (pyxel.mouse_x, pyxel.mouse_y)
    board_cage = get_board_cage(*mouse_position)
    x, y = board_cage
    cell_value = puzzle_board[x][y]
    if cell_value != selected_value:
        puzzle_board[x][y] = selected_value
    else:
        puzzle_board[x][y] = 0
        
def control_game_state():
    global game_won

    if board_is_full(puzzle_board) and board_valid(puzzle_board, solution_board):
        game_won = True
    else:
        game_won = False
        
def update():
    global puzzle_board
    global solution_board
    global game_won
    
    control_quit()
    if pyxel.btnp(0):
        control_left_click()
    elif pyxel.btnp(1):
        control_right_click()
    control_game_state()

pyxel.run(update, draw)
print("That was fun, why don't we play again?")