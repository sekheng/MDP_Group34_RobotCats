class Obstacle:
    def __init__(self, row, col, direction):
        # coords always refer to bottom-left cell of entire obstacle
        self.row = row
        self.col = col
        #direction is N,S,E,W
        self.direction = direction
        self.cells = [[row, col], [row, col+1], [row-1, col], [row-1, col+1]]
                    # bottom-left, bottom-right, top-left, top-right cells of obstacle

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

        # draw obstacle itself
        for cell in self.cells:
            i, j = cell
            matrix[i][j] = self.direction

        # demarcate boundaries around obstacle (10cm)
        for i in range(self.row-3, self.row+3):
            for j in range(self.col-2, self.col+4):
                if (matrix[i][j] != 0):
                    continue
                else:
                    matrix[i][j] = 'X' # invalid if center of car has to traverse these cells

        return matrix

