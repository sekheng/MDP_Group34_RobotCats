import grid

class Robot:
    #row and col will take bottom left corner of the car as reference
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        #direction is 1,2,3,4 for N,E,S,W
        self.direction = direction
        self.cells = [[row-5, col], [row-5, col+1], [row-5, col+2], [row-5, col+3], [row-5, col+4], [row-5, col+5],
                      [row-4, col], [row-4, col+1], [row-4, col+2], [row-4, col+3], [row-4, col+4], [row-4, col+5],
                      [row-3, col], [row-3, col+1], [row-3, col+2], [row-3, col+3], [row-3, col+4], [row-3, col+5],
                      [row-2, col], [row-2, col+1], [row-2, col+2], [row-2, col+3], [row-2, col+4], [row-2, col+5],
                      [row-1, col], [row-1, col+1], [row-1, col+2], [row-1, col+3], [row-1, col+4], [row-1, col+5],
                      [row, col], [row, col+1], [row, col+2], [row, col+3], [row, col+4], [row, col+5]]
        self.center = [[row-3, col+2], [row-3, col+3],
                      [row-2, col+2], [row-2, col+3]]

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
            matrix[i][j] = self.direction
        return matrix

    def turn(self, turn_direction):
        #direction will be left or right
        if self.direction == 1:
            if turn_direction == 'left':
                self.direction = 4
            elif turn_direction == 'right':
                self.direction = 2
        elif self.direction == 2:
            if turn_direction == 'left':
                self.direction = 1
            elif turn_direction == 'right':
                self.direction = 3
        if self.direction == 3:
            if turn_direction == 'left':
                self.direction = 2
            elif turn_direction == 'right':
                self.direction = 4
        if self.direction == 4:
            if turn_direction == 'left':
                self.direction = 3
            elif turn_direction == 'right':
                self.direction = 1

    def update_cells(self):
        row = self.row
        col = self.col
        self.cells = [[row-5, col], [row-5, col+1], [row-5, col+2], [row-5, col+3], [row-5, col+4], [row-5, col+5],
                      [row-4, col], [row-4, col+1], [row-4, col+2], [row-4, col+3], [row-4, col+4], [row-4, col+5],
                      [row-3, col], [row-3, col+1], [row-3, col+2], [row-3, col+3], [row-3, col+4], [row-3, col+5],
                      [row-2, col], [row-2, col+1], [row-2, col+2], [row-2, col+3], [row-2, col+4], [row-2, col+5],
                      [row-1, col], [row-1, col+1], [row-1, col+2], [row-1, col+3], [row-1, col+4], [row-1, col+5],
                      [row, col], [row, col+1], [row, col+2], [row, col+3], [row, col+4], [row, col+5]]
        self.center = [[row-3, col+2], [row-3, col+3],
                      [row-2, col+2], [row-2, col+3]]

    def check_valid_move(self, new_pos):
        if new_pos[0] > 0:
            if new_pos[0] < 40:
                if new_pos[1] > 0:
                    if new_pos[1] < 40:
                        return True
        else:
            return False

    def move(self):
        if self.direction == 1:
            new_pos = [self.row-1, self.col]
            if self.check_valid_move(new_pos):
               self.set_row(self.row-1)
            else:
                print("Invalid move, new position is outside grid")
        elif self.direction == 2:
            new_pos = [self.row, self.col+1]
            if self.check_valid_move(new_pos):
                self.set_col(self.col+1)
            else:
                print("Invalid move, new position is outside grid")
        elif self.direction == 3:
            new_pos = [self.row+1, self.col]
            if self.check_valid_move(new_pos):
                self.set_row(self.row+1)
            else:
                print("Invalid move, new position is outside grid")
        elif self.direction == 4:
            new_pos = [self.row, self.col-1]
            if self.check_valid_move(new_pos):
                self.set_col(self.col-1)
            else:
                print("Invalid move, new position is outside grid")
        self.update_cells()





