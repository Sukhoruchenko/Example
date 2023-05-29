"""Sudoku Game"""

game_won = False

## Read sudoku data
f = open('sudoku.csv')
text = f.read()
import random
lines = text.splitlines()

# Get one of the puzzles and its corresponding solution
# line_number = 20
# line_number = 1
# line_number = 600
line_number = random.randint(0, len(lines))
line = lines[line_number]
line = line.strip()
puzzle, solution = line.split(',')
print(puzzle, solution)

def generate_random_puzzle():
    pass

## Make a board structure to fill in the data with.
empty_board = [[0 for _ in range(9)] for _ in range(9)]

print("""
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
---------------------
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
---------------------
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
""".format(*[val if val else ' ' for row in empty_board for val in row]))


## Fill Board with puzzle data
spots = iter(puzzle)
puzzle_board = [[int(next(spots)) for _ in range(9)] for _ in range(9)] # change from a string to a list of list of ints

solution_spots = iter(solution)
solution_board = [[int(next(solution_spots)) for _ in range(9)] for _ in range(9)]  # change form a string to a list of list of ints

print("""
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
---------------------
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
---------------------
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
""".format(*[val if val else ' ' for row in puzzle_board for val in row]))


print("""
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
---------------------
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
---------------------
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
""".format(*[val if val else ' ' for row in solution_board for val in row]))

## Check if the board is valid.

def rowsValid(board):
    for row in board:
        if len([val for val in row if val]) == len(set(val for val in row if val)):  # check if the values are all unique, not counting zeroes
            continue
        else:
            return False
    return True

print(rowsValid(solution_board))


def cols_vald(board):
    is_valid = []
    for col in zip(*board):
        is_valid.append(len(list(filter(bool, col))) == len(set(filter(bool, col))))   # check if the column contains unique values, not counting zeroes
    if all(is_valid):  # if all the columns are valid
        return True
    else:
        return False

print(cols_vald(solution_board))

import os
from os import path


# The little 3x3 rectangles on a sudoku board are called "boxes" (https://simple.wikipedia.org/wiki/Sudoku)
boxes = [
    [1, 1, 1, 2, 2, 2, 3, 3, 3],
    [1, 1, 1, 2, 2, 2, 3, 3, 3],
    [1, 1, 1, 2, 2, 2, 3, 3, 3],
    [4, 4, 4, 5, 5, 5, 6, 6, 6],
    [4, 4, 4, 5, 5, 5, 6, 6, 6],
    [4, 4, 4, 5, 5, 5, 6, 6, 6],
    [7, 7, 7, 8, 8, 8, 9, 9, 9],
    [7, 7, 7, 8, 8, 8, 9, 9, 9],
    [7, 7, 7, 8, 8, 8, 9, 9, 9],
]

import numpy as np

invalid_puzzle = generate_random_puzzle()


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


import pyxel
pyxel.init(156, 183, caption="Sudoku Game")

def board_valid(problem_board, solution_board):
    # all the rules of sudoku haven't been broken
    if rowsValid(problem_board):
        if cols_vald(problem_board):
            if box_valid(problem_board):
                pass
            else:
                return False
        else:
                return False
    else:
                return False

    # the board matches the solution board so far.
    for pcol, scol in zip(problem_board, solution_board):
        for pval, sval in zip(pcol, scol):
            if pval:
                if pval == sval:
                    continue
                else:
                    return False
    return True



import itertools as it

## change board
selected_value = 1
from copy import deepcopy

def update_board(board, row, col, value):
    new_board = deepcopy(board)
    new_board[row][col] = value
    return new_board

cell_selected = (0, 0)

print("""
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
---------------------
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
---------------------
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
""".format(*[val if val else ' ' for row in puzzle_board for val in row]))


print("""
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
---------------------
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
---------------------
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
""".format(*[val if val else ' ' for row in update_board(puzzle_board, 4, 4, 8) for val in row]))


pyxel.cls(3)
pyxel.text(1, 1, "8", 0)
# pyxel.show()

is_valid = True
print(pyxel.load('my_resource.pyxres', True, True))
image = pyxel.image(0)
print(dir(image))




pyxel.mouse(True)




def draw():
    global puzzle_board
    global solution_board
    global is_valid
    global cell_selected
    global selected_value
    global game_won
    if game_won:
        pyxel.cls(10)  # Make bakcground yellow if game is won
    # Draw each space
    for i, row in enumerate(puzzle_board):
        for j, value in enumerate(row):
            x_offset = 2
            y_offset = 2
            x = i * 16 + i + x_offset# where to put the subimage

            y = j * 16 + j + y_offset# where to put the subimage
            image_size = 16
            w = image_size

            h = image_size
            u = 0
            v = value * 16
            if cell_selected == (i, j):
                transparent_color = 7
            else:
                transparent_color = 10

            pyxel.blt(x, y, 0, u, v, w, h, transparent_color)  # copy part of image from resource file to the screen.
    # Draw the lines of the board
    lines_col = 0
    pyxel.rect(0+x_offset,50+y_offset,w=16*9+8,h=1,col=lines_col)
    pyxel.rect(0 + x_offset, 101 + y_offset, w=16 * 9 + 8, h=1, col=lines_col)
    pyxel.rect(50 + x_offset, 0 + y_offset, h=16 *9 +8, w=1, col=lines_col)
    pyxel.rect(101 +x_offset, 0+ y_offset, h=16 * 9+ 8, w=1, col=lines_col)


    pyxel.rect(0, 156, h=7, w=200, col=0)

    for idx in range(9):
        if selected_value == idx + 1:
            transparent_color = 7
        else:
            transparent_color = 10
        pyxel.blt(idx*16+idx+x_offset,165,0,u=0,v=(idx + 1)*16,w=image_size,h=image_size,colkey=transparent_color)  #copy part of image from resource file to the screen.

def get_board_spot(mouse_x, mouse_y):
    return min(int(mouse_x // 17), 8), min(int(mouse_y // 17), 8)

def update():
    global puzzle_board
    global solution_board
    global is_valid
    global cell_selected
    global selected_value
    global game_won
    import pyxel
    if pyxel.btnp(pyxel.KEY_Q):
             pyxel.quit()

    # select the board spot when the player clicks the left mouse button
    if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
        mouse_pos = (pyxel.mouse_x,pyxel.mouse_y)
        print(mouse_pos)
        board_spot = get_board_spot(*mouse_pos)
        if mouse_pos[1]<155:
          cell_selected=board_spot
        else:
             selected_value=board_spot[0]+1
             print('selected value:',selected_value)
    # update the board spot when the player clicks the right mouse button
    if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON):
        mouse_pos = (pyxel.mouse_x, pyxel.mouse_y)
        print(mouse_pos)
        board_spot = get_board_spot(*mouse_pos)
        x, y = board_spot
        cell_value = puzzle_board[x][y]
        if cell_value != selected_value:
               puzzle_board[x][y] = selected_value
        else:
            puzzle_board[x][y] = 0

    is_valid = board_valid(puzzle_board, solution_board)

    if board_is_full(puzzle_board):
        print('full')
        if board_valid(puzzle_board):
                     print('hi')
                     game_won=True
        else:
         game_won=False
    else:
           game_won = False
def board_is_full(board):
    for row in board:
          for val in row:
            if val == 0:
                    return False
    else:
          return True


###start the game###
pyxel.run(update, draw)










print("That was fun, why don't we play again?")

