import numpy as np

from constants import *

class Grid:

    def __init__(self, obstacles = None, robot = None):
        self.robot = robot
        self.obstacles = obstacles
        self.num_rows = int(AREA_LENGTH / CELL_SIZE)
        self.num_cols = int(AREA_WIDTH / CELL_SIZE)
        self.matrix = [[0 for _ in range(self.num_rows)] for _ in range(self.num_cols)]

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.mark_obstacles()

    def get_obstacles(self):
        return self.obstacles

    def mark_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.mark(self.matrix)
            obstacle.set_viewpos(self.num_cols, self.num_rows)

    def mark_robot(self):
        self.robot.mark(self.matrix)

    def delete_cur_robot_position(self):
        self.robot.delete_robot_position(self.matrix)

    def pos_is_obstacle(self, x, y):
        return self.matrix[x][y] != 0  # non-zero values are obstacles

    def pos_is_valid(self, x, y):
        return x >= 0 and x <= self.num_rows - 1 and y >= 0 and y <= self.num_cols - 1 and not self.pos_is_obstacle(x, y)

    def robot_pos_is_valid(self, robot_centre):
        x_c, y_c, _ = robot_centre
        for x in range(x_c - 1, x_c + 2):
            for y in range(y_c - 1, y_c + 2):
                if (not self.pos_is_valid(x, y)):
                    return False

        return True

    def print_grid(self):
        for i in self.matrix:
            for j in i:
                print(j, end=" ")
            print()