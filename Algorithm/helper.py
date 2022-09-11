from constants import *
from obstacle import Obstacle
from robot import Robot

def to_indices(coords):
    # this method takes in coordinates from input into simulator,
    # returns corresponding row and column number for algorithm to work with

    # new_coords = []
    num_rows = AREA_LENGTH // CELL_SIZE
    # for coord in coords:
    x, y, d = coords
    new_x = num_rows - 1 - y
    new_y = x

    return [new_x, new_y, d]


def obs_indices_internal(obj: Obstacle):
    # swaps between row and col used in algorithm
    # and positions used in simulator
    new_row, new_col = obj.col, obj.row
    return Obstacle(new_row, new_col, obj.direction)

def robot_indices_internal(obj: Robot):
    # swaps between row and col used in algorithm
    # and positions used in simulator
    new_row, new_col = obj.col, obj.row
    return Robot(new_row, new_col, obj.direction)

def set_cells(row, col, direction):
    # obstacle cells
    if direction == 'N':
        return [[row, col], [row, col + 1], [row - 1, col], [row - 1, col + 1]]
    if direction == 'E':
        return [[row, col], [row, col + 1], [row - 1, col], [row - 1, col + 1]]