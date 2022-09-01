import grid
from constants import *

class Robot:
    #row and col will take bottom left corner of the car as reference
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        #direction is 1,2,3,4 for N,E,S,W
        self.direction = direction
        self.cells = [[row-2, col], [row-2, col+1], [row-2, col+2],
                      [row-1, col], [row-1, col+1], [row-1, col+2],
                      [row, col], [row, col+1], [row, col+2]
                      ]
        self.center = [row-1, col+1]

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_direction(self):
        return self.direction

    def set_row(self, row):
        self.row = row

    def set_col(self, col):
        self.col = col

    def set_direction(self, direction):
        self.direction = direction

    def mark(self, matrix):
        old_matrix = matrix
        # draw robot
        for cell in self.cells:
            i, j = cell
            matrix[i][j] = self.direction
        #print(matrix)
        return matrix

    def delete_robot_position(self, matrix):
        for cell in self.cells:
            i, j = cell
            matrix[i][j] = 0
        #print(matrix)
        return matrix

    def turn(self, turn_direction):
        #direction will be left or right
        if self.direction == 1:
            if turn_direction == 'L':
                self.set_direction(4)
                self.set_row(self.row - TURN_GRIDS)
                self.set_col(self.col - TURN_GRIDS)
            elif turn_direction == 'R':
                self.set_direction(2)
                self.set_row(self.row - TURN_GRIDS)
                self.set_col(self.col + TURN_GRIDS)
        elif self.direction == 2:
            if turn_direction == 'L':
                self.set_direction(1)
                self.set_row(self.row - TURN_GRIDS)
                self.set_col(self.col + TURN_GRIDS)
            elif turn_direction == 'R':
                self.set_direction(3)
                self.set_row(self.row + TURN_GRIDS)
                self.set_col(self.col + TURN_GRIDS)
        elif self.direction == 3:
            if turn_direction == 'L':
                self.set_direction(2)
                self.set_row(self.row + TURN_GRIDS)
                self.set_col(self.col + TURN_GRIDS)
            elif turn_direction == 'R':
                self.set_direction(4)
                self.set_row(self.row + TURN_GRIDS)
                self.set_col(self.col - TURN_GRIDS)
        elif self.direction == 4:
            if turn_direction == 'L':
                self.set_direction(3)
                self.set_row(self.row + TURN_GRIDS)
                self.set_col(self.col - TURN_GRIDS)
            elif turn_direction == 'R':
                self.set_direction(1)
                self.set_row(self.row - TURN_GRIDS)
                self.set_col(self.col - TURN_GRIDS)

        self.update_cells_after_move()

    def update_cells_after_move(self):
        row = self.row
        col = self.col
        self.cells = [[row - 2, col], [row - 2, col + 1], [row - 2, col + 2],
                      [row - 1, col], [row - 1, col + 1], [row - 1, col + 2],
                      [row, col], [row, col + 1], [row, col + 2]
                      ]
        self.center = [row - 1, col + 1]

    def check_valid_move(self, new_pos):
        if new_pos[0] >= 0:
            if new_pos[0] < 40:
                if new_pos[1] >= 0:
                    if new_pos[1] < 40:
                        return True
        else:
            return False

    def move(self, move):
        new_pos = [self.row, self.col]
        if self.direction == 1:
            if move == 'F':
                new_pos = [self.row-1, self.col]
            elif move == 'B':
                new_pos = [self.row+1, self.col]
            else:
                print('Invalid move, nothing happened.')
            if self.check_valid_move(new_pos):
               self.set_row(new_pos[0])
               self.set_col(new_pos[1])
            else:
                print("Invalid move, new position is outside grid")
        elif self.direction == 2:
            if move == 'F':
                new_pos = [self.row, self.col+1]
            elif move == 'B':
                new_pos = [self.row, self.col-1]
            else:
                print('Invalid move, nothing happened.')
            if self.check_valid_move(new_pos):
                self.set_row(new_pos[0])
                self.set_col(new_pos[1])
            else:
                print("Invalid move, new position is outside grid")
        elif self.direction == 3:
            if move == 'F':
                new_pos = [self.row+1, self.col]
            elif move == 'B':
                new_pos = [self.row-1, self.col]
            else:
                print('Invalid move, nothing happened.')
            if self.check_valid_move(new_pos):
                self.set_row(new_pos[0])
                self.set_col(new_pos[1])
            else:
                print("Invalid move, new position is outside grid")
        elif self.direction == 4:
            if move == 'F':
                new_pos = [self.row, self.col-1]
            elif move == 'B':
                new_pos = [self.row, self.col + 1]
            else:
                print('Invalid move, nothing happened.')
            if self.check_valid_move(new_pos):
                self.set_row(new_pos[0])
                self.set_col(new_pos[1])
            else:
                print("Invalid move, new position is outside grid")
        self.update_cells_after_move()





