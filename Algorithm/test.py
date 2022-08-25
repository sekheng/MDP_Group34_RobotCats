import test
from grid import *
from helper import *
from obstacle import *
from robot import *

if __name__ == "__main__":

    # construct obstacles
    test_obstacles = [[2,9,'S'],[7,13,'N'],[14,3,'N'],[18,10,'W'],[15,18,'S'],[11,8,'W']]
    for idx, o in enumerate(test_obstacles):
        row, col, dir = to_indices(o)
        test_obstacles[idx] = Obstacle(row, col, dir)

    # construct robot
    r_row, r_col, r_dir = to_indices([0, 0, 1])
    test_robot = Robot(r_row, r_col, r_dir)

    #test_robot = Robot(0, 0, 1)

    test_grid = Grid(test_obstacles, test_robot)
    test_grid.mark_obstacles()
    test_grid.mark_robot()
    test_grid.print_grid()

    print ('------------------------------------------------')

    def move_robot_on_grid():
        while True:
            print("Current direction robot is facing is: " + str(test_robot.direction))
            move_cfm_input = input('Confirm movement? Y/N: ')
            if move_cfm_input.lower() == 'y':
                test_grid.delete_cur_robot_position()
                test_robot.move()
                test_grid.mark_robot()
                test_grid.print_grid()
                break
            elif move_cfm_input.lower() == 'n':
                break
            else:
                print("Incorrect input, try again! (Y/N)")

    move_robot_on_grid()




