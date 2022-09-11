from constants import *
from obstacle import *

class Grid:

    def __init__(self, obstacles=[], robot = None):
        self.robot = robot
        self.obstacles = obstacles
        self.num_rows = int(AREA_LENGTH / CELL_SIZE)
        self.num_cols = int(AREA_WIDTH / CELL_SIZE)
        self.matrix = [[0 for _ in range(self.num_rows)] for _ in range(self.num_cols)]
        self.mark_robot()
        self.mark_obstacles()
        self.print_grid()

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        # self.mark_obstacles()

    def get_obstacle(self, x, y):
        for obstacle in self.obstacles:
            if x == obstacle.row and y == obstacle.col:
                return obstacle

    def remove_obstacle(self, obstacle):
        self.obstacles.remove(obstacle)

    def mark_obstacles(self):
        for i, obstacle in enumerate(self.obstacles):
            obstacle.mark(self.matrix)
            obstacle.set_viewpos(self.num_cols, self.num_rows)
            print(f"Algo obstacle {i} = {obstacle.cells}, Algo viewpos {i} = {obstacle.viewpos}")

    def mark_robot(self):
        self.robot.mark(self.matrix)

    def delete_cur_robot_position(self):
        self.robot.delete_robot_position(self.matrix)

    def pos_is_obstacle(self, x, y):
        return self.matrix[x][y] in OBS_MARKINGS  # obstacles and their boundaries are N S E W or X

    def pos_is_valid(self, x, y):
        return 0 <= x <= self.num_rows - 1 and 0 <= y <= self.num_cols - 1 and not self.pos_is_obstacle(x, y)

    def robot_pos_is_valid(self, robot_centre):
        x_c, y_c, _ = robot_centre
        for x in range(x_c - 1, x_c + 2):
            for y in range(y_c - 1, y_c + 2):
                # print("Checking", x, y)
                if (not self.pos_is_valid(x, y)):
                    # print("Pos is not valid")
                    return False

        return True

    def print_grid(self):
        for i in self.matrix:
            for j in i:
                print(j, end=" ")
            print()