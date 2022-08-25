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

    def mark_robot(self):
        self.robot.mark(self.matrix)

    def delete_cur_robot_position(self):
        self.robot.delete_robot_position(self.matrix)

    def print_grid(self):
        for i in self.matrix:
            for j in i:
                print(j, end=" ")
            print()