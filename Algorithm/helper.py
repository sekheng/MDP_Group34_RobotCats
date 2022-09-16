from constants import *
from obstacle import Obstacle
from robot import Robot
from route import Route
from queue import Queue

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


def get_stm_commands(route_list: list[Route]):
    stm_route = []
    for route_obj in route_list:
        route = route_obj.route
        count = 1
        for i in range(len(route)):
            if i < len(route) - 1 and route[i] == route[i+1] and route[i] in 'FB':
                count += 1
            else:
                if route[i] == 'F':
                    stm_route.append(f"w{(count*10):03d}")
                elif route[i] == 'B':
                    stm_route.append(f"s{(count*10):03d}")
                elif route[i] == 'L':
                    stm_route.append(f"q{90:03d}")
                elif route[i] == 'R':
                    stm_route.append(f"e{90:03d}")
                # TODO: Stop command?
                count = 1
    return stm_route



