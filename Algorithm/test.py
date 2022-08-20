from grid import *
from helper import *
from obstacle import *

if __name__ == "__main__":

    test_obstacles = [[2,19,'S'],[7,13,'N'],[14,3,'N'],[20,10,'W'],[15,18,'S'],[11,8,'W']]

    for idx, o in enumerate(test_obstacles):
        rol, col, dir = to_indices(o)
        test_obstacles[idx] = Obstacle(rol, col, dir)

    test_grid = Grid(test_obstacles)
    test_grid.mark_obstacles()
    test_grid.print_grid()
