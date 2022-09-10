from constants import *
class Obstacle:
    def __init__(self, row, col, direction):
        # coords always refer to bottom-left cell of entire obstacle
        self.row = row
        self.col = col
        # direction is N,S,E,W
        self.direction = direction
        self.cells = row, col
        self.visited = False

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_direction(self):
        return self.direction

    def get_viewpos(self):
        return self.viewpos

    def set_row(self, row):
        self.row = row

    def set_col(self, col):
        self.col = col

    def set_direction(self, direction):
        self.direction = direction

    def mark(self, matrix):

        # draw obstacle itself
        print(self.row, self.col)
        matrix[self.row][self.col] = self.direction

        # demarcate boundaries around obstacle (10cm)
        for i in range(self.row-1, self.row+2):
            for j in range(self.col-1, self.col+2):
                if (matrix[i][j] != 0):
                    continue
                else:
                    matrix[i][j] = 'X'  # invalid if center of car has to traverse these cells

        return matrix
    def set_viewpos(self, num_cols, num_rows):
        # set the position where car should stop to view image
        optimal_dist = math.ceil(VIEW_DIST/CELL_SIZE)  # min number of cells between car center and image
        v_row, v_col, v_dir = self.row, self.col, self.direction

        if self.direction == 'N':
            v_row -= optimal_dist
            v_dir = 3
        elif self.direction == 'S':
            v_row += optimal_dist
            v_dir = 1
        elif self.direction == 'E':
            v_col += optimal_dist
            v_dir = 4
        elif self.direction == 'W':
            v_col -= optimal_dist
            v_dir = 2

        if v_col >= num_cols - 1 or v_col <= 0 or v_row >= num_rows - 1 or v_row <= 0:
            v_row, v_col = float("-inf"), float("-inf")  # -inf for images that cannot be seen
                                                         # as car will exceed arena boundary

        self.viewpos = [v_row, v_col, v_dir]
