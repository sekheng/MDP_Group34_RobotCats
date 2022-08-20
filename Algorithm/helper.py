from constants import *

def to_indices(coords):
# this method takes in coordinates from input into simulator,
# returns corresponding row and column number for algorithm to work with

    # new_coords = []
    num_rows = AREA_LENGTH // CELL_SIZE

    # for coord in coords:
    x, y, dir = coords
    new_x = num_rows - 1 - y
    new_y = x
        # new_coords.append([new_x, new_y, dir])

    return [new_x, new_y, dir]