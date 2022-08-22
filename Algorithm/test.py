import test
from grid import *
from helper import *
from obstacle import *
from robot import *

if __name__ == "__main__":

    # construct obstacles
    test_obstacles = [[2,19,'S'],[7,13,'N'],[14,3,'N'],[20,10,'W'],[15,18,'S'],[11,8,'W']]
    for idx, o in enumerate(test_obstacles):
        row, col, dir = to_indices(o)
        test_obstacles[idx] = Obstacle(row, col, dir)

    # construct robot
    r_row, r_col, r_dir = to_indices([0, 0, 1])
    test_robot = Robot(r_row, r_col, r_dir)

    test_grid = Grid(test_obstacles, test_robot)
    test_grid.mark_obstacles()
    test_grid.mark_robot()
    test_grid.print_grid()

    print ('------------------------------------------------')

    test_robot.move()
    test_grid.mark_robot()
    test_grid.print_grid()