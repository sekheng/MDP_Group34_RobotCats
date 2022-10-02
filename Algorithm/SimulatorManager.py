import time

import dearpygui.dearpygui as dpg
from constants import *
from grid import *
from helper import *
from node import *
from obstacle import *
from robot import *
from route import *
from shortest_path import *
from SimulatorGUI import *
from SimulatorGrid import *
from time import perf_counter

# TEST_OBSTACLES = [[2, 15, 'S'], [6, 13, 'E'], [10, 17, 'S'], [15, 7, 'W'],
#                   [18, 18, 'S'], [8, 2, 'N'], [13, 9, 'N'], [18, 6, 'N']]
TEST_OBSTACLES = [[3, 4, 'W']]

class SimulatorManager:
    def __init__(self, result_app):

        self.robot = None
        self.obstacles = []

        # Initialize robot and obstacles for algorithm grid
        algo_obstacles = []
        for o in TEST_OBSTACLES:
            row, col, d = to_indices(o)
            algo_obstacles.append(Obstacle(row, col, d))
        r_row, r_col, r_d = to_indices([1, 1, 1])  # For algorithm robot
        algo_robot = Robot(r_row, r_col, r_d)
        self.algo_grid = Grid(obstacles=algo_obstacles, robot=algo_robot)

        # Convert robot and obstacle coordinates from algorithm coordinates into simulator coordinates
        self.set_robot()
        self.set_obstacles()
        self.grid = SimulatorGrid(grid_app=result_app, obstacles=self.obstacles)

        self.console_clear()

        # self.actions = Actions(self.robot, self.algo_grid)
        self.total_distance = 0
        self.timer = perf_counter() + 500

        dpg.configure_item("start", callback=self.on_click_start)

    def set_robot(self):
        # updates simulator's robot position based on algorithm's robot
        self.robot = robot_indices_internal(self.algo_grid.robot)

    def set_obstacles(self):
        # updates simulator's obstacle positions based on algorithm's obstacles
        self.obstacles.clear()
        for o in self.algo_grid.obstacles:
            sim_obstacle = obs_indices_internal(o)
            sim_obstacle.viewpos = o.viewpos
            self.obstacles.append(sim_obstacle)

    def update(self):
        current_time = perf_counter()
        #print(current_time - self.timer)
        if current_time - self.timer < 360:
            return 1
        else:
            return 0

    def on_click_start(self):

        sp = ShortestPath(self.algo_grid)

        start_time = perf_counter()

        sp.get_shortest_path()
        car = self.algo_grid.robot
        self.console_writeline("Initial direction robot is facing is: " + str(self.robot.direction))
        move_counter = 1
        route_counter = 1
        dist_travelled = 0

        self.timer = perf_counter()
        print(f"\nTo STM: {get_stm_commands(sp.route)}\n")

        for curr_route in sp.route:
            self.console_writeline(f"Route {route_counter} to {curr_route.position}")
            self.console_writeline(f"Moves: {curr_route.route}")

            for move in curr_route.route:
                self.console_writeline(f"Move {move_counter} is {move}")
                if move == 'F' or move == 'B':
                    car.move(move)
                elif move == 'L' or move == 'R':
                    car.turn(move)
                elif move == 'IL' or move == 'IR':
                    car.in_place(move)

                self.set_robot()
                self.redraw()
                time.sleep(0.5)
                move_counter += 1

            # TODO: If obstacle cannot be reached, add route to it at the end of sp.route to try again at the end
            self.console_writeline("Recognizing image...")
            time.sleep(2)  # Capture image
            self.mark_visited(curr_route.position)
            dist_travelled += curr_route.distance
            self.console_writeline(f"Distance travelled = {dist_travelled}")
            route_counter += 1

        self.redraw()
        self.total_distance = sp.distance
        if dist_travelled == self.total_distance:
            end_time = perf_counter()
            self.console_writeline(f"Path complete! Total distance/cost = {self.total_distance}")
            self.console_writeline(f"Time taken: {end_time - start_time:.2f}")

    def mark_visited(self, viewpos):

        for o in self.obstacles:
            if viewpos == o.viewpos:
                o.visited = True
                return
        print("Not found")

    def console_writeline(self, msg):
        self.console += f"{msg}\n"
        dpg.set_value("console_body", self.console)

    def console_clear(self):
        self.console = ""
        dpg.set_value("console_body", self.console)

    def redraw(self):
        # set all colours to white
        for y in range(self.grid.rows):
            for x in range(self.grid.cols):
                self.grid.set_color(x, y)

        for o in self.obstacles:
            self.grid.set_color(o.row,
                                o.col,
                                color=OBSTACLE_COL,
                                flip=True)

        self.grid.configure_obstacles(self.obstacles)
        self.grid.update_robot_position(self.robot.row, self.robot.col, self.robot.direction)

        # update panels
        dpg.set_value("robot_x_highlight", self.robot.row)
        dpg.set_value("robot_y_highlight", self.robot.col)
        dpg.set_value("robot_direction_highlight", self.robot.direction)
