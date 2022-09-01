import test
from grid import *
from helper import *
from obstacle import *
from robot import *
from shortest_path import *
import constants

if __name__ == "__main__":
    # construct obstacles
    test_obstacles = [[2,9,'S'],[7,13,'N'],[17,2,'N'],[18,10,'W'],[15,18,'S'],[11,8,'W']]
    # print("Test obstacles:")
    for idx, o in enumerate(test_obstacles):
        row, col, dir = to_indices(o)
        test_obstacles[idx] = Obstacle(row, col, dir)
        # print(row, col, dir)

    # construct robot
    r_row, r_col, r_dir = to_indices([0, 0, 1])
    test_robot = Robot(r_row, r_col, r_dir)

    #test_robot = Robot(0, 0, 1)

    test_grid = Grid(test_obstacles, test_robot)
    test_grid.mark_obstacles()
    test_grid.mark_robot()
    test_grid.print_grid()

    test_path = ShortestPath(test_grid)
    test_path.get_shortest_path()
    print(test_path.route)
    # for routes in test_path.route:
    #     print(routes.route)
    # print("Shortest Route:", test_path.route, "Distance travelled =", test_path.distance)

    print ('------------------------------------------------')

    def move_robot_on_grid(shortest_path_object):
        print("Initial direction robot is facing is: " + str(test_robot.direction))
        move_counter = 1
        route_counter = 1
        for routes in shortest_path_object.route:
            print('Route ' + str(route_counter))
            print('Route is ' + str(routes.route))
            print('---------------------------------------')
            for move in routes.route:
                print('Move ' + str(move_counter) + ' is ' + str(move))
                print('---------------------------------------')
                test_grid.delete_cur_robot_position()
                if move == 'F' or move == 'B':
                    test_robot.move(move)
                elif move == 'L' or move == 'R':
                    test_robot.turn(move)

                test_grid.mark_robot()
                test_grid.print_grid()
                move_counter+=1
            route_counter+=1

    move_robot_on_grid(test_path)




