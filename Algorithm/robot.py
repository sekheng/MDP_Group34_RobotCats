import grid
from constants import *

class Robot:
    #row and col will take center of the car as reference
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col

        #direction is 1,2,3,4 for N,E,S,W
        self.direction = direction
        self.cells = [[self.row-1, self.col-1], [self.row-1, self.col], [self.row-1, self.col+1],
                      [self.row, self.col-1], [self.row, self.col], [self.row, self.col+1],
                      [self.row+1, self.col-1], [self.row+1, self.col], [self.row+1, self.col+1]
                      ]

    def __str__(self):
        return f"Robot({self.row}, {self.col}, {self.direction})"
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
        # draw robot
        for cell in self.cells:
            i, j = cell
            # print("Robot i, j =", i, j)
            matrix[i][j] = self.direction
        # print(matrix)
        return matrix

    def delete_robot_position(self, matrix):
        for cell in self.cells:
            i, j = cell
            matrix[i][j] = 0
        #print(matrix)
        return matrix

    def update_cells_after_move(self):

        self.cells = [[self.row-1, self.col-1], [self.row-1, self.col], [self.row-1, self.col+1],
                      [self.row, self.col-1], [self.row, self.col], [self.row, self.col+1],
                      [self.row+1, self.col-1], [self.row+1, self.col], [self.row+1, self.col+1]
                      ]

    def check_valid_move(self, new_pos):
        if new_pos[0] >= 0:
            if new_pos[0] < 40:
                if new_pos[1] >= 0:
                    if new_pos[1] < 40:
                        return True
        else:
            return False

    def move(self, move, number_of_moves=1):
        new_pos = [self.row, self.col]
        if self.direction == 1:
            if move == 'F':
                new_pos = [self.row - number_of_moves, self.col]
            elif move == 'B':
                new_pos = [self.row + number_of_moves, self.col]
            else:
                print('Invalid move, nothing happened.')
            if self.check_valid_move(new_pos):
                self.set_row(new_pos[0])
                self.set_col(new_pos[1])
            else:
                print("Invalid move, new position is outside grid")
        elif self.direction == 2:
            if move == 'F':
                new_pos = [self.row, self.col + number_of_moves]
            elif move == 'B':
                new_pos = [self.row, self.col - number_of_moves]
            else:
                print('Invalid move, nothing happened.')
            if self.check_valid_move(new_pos):
                self.set_row(new_pos[0])
                self.set_col(new_pos[1])
            else:
                print("Invalid move, new position is outside grid")
        elif self.direction == 3:
            if move == 'F':
                new_pos = [self.row + number_of_moves, self.col]
            elif move == 'B':
                new_pos = [self.row - number_of_moves, self.col]
            else:
                print('Invalid move, nothing happened.')
            if self.check_valid_move(new_pos):
                self.set_row(new_pos[0])
                self.set_col(new_pos[1])
            else:
                print("Invalid move, new position is outside grid")
        elif self.direction == 4:
            if move == 'F':
                new_pos = [self.row, self.col - number_of_moves]
            elif move == 'B':
                new_pos = [self.row, self.col + number_of_moves]
            else:
                print('Invalid move, nothing happened.')
            if self.check_valid_move(new_pos):
                self.set_row(new_pos[0])
                self.set_col(new_pos[1])
            else:
                print("Invalid move, new position is outside grid")
        self.update_cells_after_move()

    def in_place(self, turn):

        if self.direction == 1:
            if turn == 'IL':
                self.set_direction(4)
            elif turn == 'IR':
                self.set_direction(2)
        elif self.direction == 2:
            if turn == 'IL':
                self.set_direction(1)
            elif turn == 'IR':
                self.set_direction(3)
        elif self.direction == 3:
            if turn == 'IL':
                self.set_direction(2)
            elif turn == 'IR':
                self.set_direction(4)
        elif self.direction == 4:
            if turn == 'IL':
                self.set_direction(3)
            elif turn == 'IR':
                self.set_direction(1)

        self.update_cells_after_move()

    def turn(self, turn_direction):
        # direction will be left or right
        if self.direction == 1:
            if turn_direction == 'L':
                self.set_direction(4)
                self.set_row(self.row - 1)
                self.set_col(self.col - 2)
            elif turn_direction == 'R':
                self.set_direction(2)
                self.set_row(self.row - 1)
                self.set_col(self.col + 2)
        elif self.direction == 2:
            if turn_direction == 'L':
                self.set_direction(1)
                self.set_row(self.row - 2)
                self.set_col(self.col + 1)
            elif turn_direction == 'R':
                self.set_direction(3)
                self.set_row(self.row + 2)
                self.set_col(self.col + 1)
        elif self.direction == 3:
            if turn_direction == 'L':
                self.set_direction(2)
                self.set_row(self.row + 1)
                self.set_col(self.col + 2)
            elif turn_direction == 'R':
                self.set_direction(4)
                self.set_row(self.row + 1)
                self.set_col(self.col - 2)
        elif self.direction == 4:
            if turn_direction == 'L':
                self.set_direction(3)
                self.set_row(self.row + 2)
                self.set_col(self.col - 1)
            elif turn_direction == 'R':
                self.set_direction(1)
                self.set_row(self.row - 2)
                self.set_col(self.col - 1)

        self.update_cells_after_move()

        # def move(self, move):  # coords are in terms of simulator coords
        #     if self.direction == 1:
        #         if move == 'F':
        #             new_pos = [self.row - 1, self.col]
        #         elif move == 'B':
        #             new_pos = [self.row + 1, self.col]
        #         else:
        #             print('Invalid move, nothing happened.')
        #         new_pos.reverse()
        #         if self.check_valid_move(new_pos):
        #             self.set_row(new_pos[0])
        #             self.set_col(new_pos[1])
        #         else:
        #             print(f"{new_pos} Invalid move, new position is outside grid")
        #     elif self.direction == 2:
        #         if move == 'F':
        #             new_pos = [self.row, self.col + 1]
        #         elif move == 'B':
        #             new_pos = [self.row, self.col - 1]
        #         else:
        #             print('Invalid move, nothing happened.')
        #         new_pos.reverse()
        #         if self.check_valid_move(new_pos):
        #             self.set_row(new_pos[0])
        #             self.set_col(new_pos[1])
        #         else:
        #             print(f"{new_pos} Invalid move, new position is outside grid")
        #     elif self.direction == 3:
        #         if move == 'F':
        #             new_pos = [self.row + 1, self.col]
        #         elif move == 'B':
        #             new_pos = [self.row - 1, self.col]
        #         else:
        #             print('Invalid move, nothing happened.')
        #         new_pos.reverse()
        #         if self.check_valid_move(new_pos):
        #             self.set_row(new_pos[0])
        #             self.set_col(new_pos[1])
        #         else:
        #             print(f"{new_pos} Invalid move, new position is outside grid")
        #     elif self.direction == 4:
        #         if move == 'F':
        #             new_pos = [self.row, self.col - 1]
        #         elif move == 'B':
        #             new_pos = [self.row, self.col + 1]
        #         else:
        #             print('Invalid move, nothing happened.')
        #         new_pos.reverse()
        #         if self.check_valid_move(new_pos):
        #             self.set_row(new_pos[0])
        #             self.set_col(new_pos[1])
        #         else:
        #             print(f"{new_pos} Invalid move, new position is outside grid")
        #     self.update_cells_after_move()
        #
        #     # if self.serial_comm:
        #     #     self.serial_comm.write("s")

        # def turn(self, turn_direction):  # coords in terms of simulator coords
        #     #direction will be left or right
        #     if self.direction == 1:
        #         if turn_direction == 'L':
        #             self.set_direction(4)
        #             self.set_col(self.row - TURN_GRIDS)
        #             self.set_row(self.col - TURN_GRIDS)
        #         elif turn_direction == 'R':
        #             self.set_direction(2)
        #             self.set_col(self.row - TURN_GRIDS)
        #             self.set_row(self.col + TURN_GRIDS)
        #     elif self.direction == 2:
        #         if turn_direction == 'L':
        #             self.set_direction(1)
        #             self.set_col(self.row - TURN_GRIDS)
        #             self.set_row(self.col + TURN_GRIDS)
        #         elif turn_direction == 'R':
        #             self.set_direction(3)
        #             self.set_col(self.row + TURN_GRIDS)
        #             self.set_row(self.col + TURN_GRIDS)
        #     elif self.direction == 3:
        #         if turn_direction == 'L':
        #             self.set_direction(2)
        #             self.set_col(self.row + TURN_GRIDS)
        #             self.set_row(self.col + TURN_GRIDS)
        #         elif turn_direction == 'R':
        #             self.set_direction(4)
        #             self.set_col(self.row + TURN_GRIDS)
        #             self.set_row(self.col - TURN_GRIDS)
        #     elif self.direction == 4:
        #         if turn_direction == 'L':
        #             self.set_direction(3)
        #             self.set_col(self.row + TURN_GRIDS)
        #             self.set_row(self.col - TURN_GRIDS)
        #         elif turn_direction == 'R':
        #             self.set_direction(1)
        #             self.set_col(self.row - TURN_GRIDS)
        #             self.set_row(self.col - TURN_GRIDS)
        #
        #     self.update_cells_after_move()
        #
        #     # if self.serial_comm:
        #     #     if direction == "left":
        #     #         self.serial_comm.write("l")
        #     #     if direction == "right":
        #     #         self.serial_comm.write("r")
