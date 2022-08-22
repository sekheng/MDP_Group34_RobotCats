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

        # demarcate boundaries around obstacle (15cm)
        for i in range(self.row-4, self.row+4):
            for j in range(self.col-3, self.col+5):
                if (matrix[i][j] != 0) or (matrix[i][j] == 'X'):
                    continue
                if (i == self.row-4) or (i == self.row+3) or (j == self.col-3) or (j == self.col+4):
                    matrix[i][j] = 'Y' # perimeter of boundary that the center of car can still traverse
                    #should we keep it as Y or change it to 0?
                else:
                    matrix[i][j] = 'X' # these cells cannot be traversed

        return matrix

