import test
from grid import *
from helper import *
from obstacle import *
from robot import *
from shortest_path import *
from AlgoServer import *
import constants


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
                test_robot.algo_move(move)
            elif move == 'L' or move == 'R':
                test_robot.algo_turn(move)

            test_grid.mark_robot()
            test_grid.print_grid()
            move_counter += 1
        route_counter += 1


def test_obstacle_conversion(server):

    test_json = [{"type": "obstacle", "direction": "south", "symbol": "square", "x": "2", "y": "4"},
                 {"type": "obstacle", "direction": "east", "symbol": "square", "x": "6", "y": "6"},
                 {"type": "obstacle", "direction": "south", "symbol": "square", "x": "10", "y": "2"},
                 {"type": "obstacle", "direction": "west", "symbol": "square", "x": "15", "y": "12"},
                 {"type": "obstacle", "direction": "south", "symbol": "square", "x": "18", "y": "1"},
                 {"type": "obstacle", "direction": "north", "symbol": "square", "x": "8", "y": "17"},
                 {"type": "obstacle", "direction": "north", "symbol": "square", "x": "13", "y": "10"},
                 {"type": "obstacle", "direction": "north", "symbol": "square", "x": "18", "y": "13"}]
    # [[2, 15, 'S'], [6, 13, 'E'], [10, 17, 'S'], [15, 7, 'W'], [18, 18, 'S'], [8, 2, 'N'], [13, 9, 'N'], [18, 6, 'N']]

    for item in test_json:
        server.android_to_algo(item)

    print(server.server_get())


if __name__ == "__main__":
    # test_server = AlgoServer()
    # test_obstacle_conversion(test_server)

    test_obstacles = [[1, 4, 'S']]
    # [[2, 15, 'S'], [6, 13, 'E'], [10, 17, 'S'], [15, 7, 'W'], [18, 18, 'S'], [8, 2, 'N'], [13, 9, 'N'], [18, 6, 'N']]
    for idx, o in enumerate(test_obstacles):
        row, col, dir = to_indices(o)
        test_obstacles[idx] = Obstacle(row, col, dir)
        print(row, col, dir)

    # construct robot
    r_row, r_col, r_dir = to_indices([1, 1, 1])
    test_robot = Robot(r_row, r_col, r_dir)

    test_grid = Grid(test_obstacles, test_robot)
    print(test_grid.robot)

    test_path = ShortestPath(test_grid)
    test_path.get_shortest_path()
    if test_path.route is not None:
        for r in test_path.route:
            print(r.route)
    else:
        print("No routes")
    print("Shortest Route:", test_path.route, "Distance travelled =", test_path.distance)

    print(f'============== TURN_DIST = {TURN_DIST} ==============')

    move_robot_on_grid(test_path)


# TEST_OBSTACLES = [[2, 15, 'S'], [6, 13, 'E'], [10, 17, 'S'], [15, 7, 'W'],
    #                   [18, 18, 'S'], [8, 2, 'N'], [13, 9, 'N'], [18, 6, 'N']]
    # algo_obstacles = []
    # for o in TEST_OBSTACLES:
    #     row, col, d = to_indices(o)
    #     algo_obstacles.append(Obstacle(row, col, d))
    # r_row, r_col, r_d = to_indices([1, 1, 1])  # For algorithm robot
    # algo_robot = Robot(r_row, r_col, r_d)
    # algo_grid = Grid(obstacles=algo_obstacles, robot=algo_robot)
    #
    # algo_path = ShortestPath(algo_grid)
    # algo_path.get_shortest_path()
    #
    # stm_commands_list = get_stm_commands(algo_path.route)
    # print(stm_commands_list)


    # construct obstacles
    # test_obstacles = [[2,9,'S'],[7,13,'N'],[17,2,'N'],[18,10,'W'],[15,18,'S'],[11,8,'W']]
    # test_obstacles = [[8,13,'W'], [11,17,'S'],[15,15,'S'], [17,6,'W'],[2,19,'S'],[11,5,'N']]
    # test_obstacles = [[2,15,'S'], [6, 13,'E'], [10,17,'S'], [15,7,'W'], [18,18,'S'], [8,2,'N'], [13,9,'N'], [18,6,'N']]
    # test_obstacles = [[7,11,'W'],[12,5,'W'], [14,15,'S'], [19,17,'S'],[19,4,'N'],[2,17,'S'],[5,7,'S'],[10,15,'S']]
    # print("Test obstacles:")