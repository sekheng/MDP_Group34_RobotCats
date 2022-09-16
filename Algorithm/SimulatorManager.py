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
from actions import *
from SimulatorGUI import *
from SimulatorGrid import *
from time import perf_counter

TEST_OBSTACLES = [[2, 15, 'S'], [6, 13, 'E'], [10, 17, 'S'], [15, 7, 'W'],
                  [18, 18, 'S'], [8, 2, 'N'], [13, 9, 'N'], [18, 6, 'N']]

class SimulatorManager():
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
        self.timer = 0

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
        current_time = time.perf_counter()
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

        self.timer = time.perf_counter()

        for curr_route in sp.route:
            self.console_writeline(f"Route {route_counter} to {curr_route.position}")
            self.console_writeline(f"Moves: {curr_route.route}")

            for move in curr_route.route:
                self.console_writeline(f"Move {move_counter} is {move}")
                if move == 'F' or move == 'B':
                    car.algo_move(move)
                elif move == 'L' or move == 'R':
                    car.algo_turn(move)

                self.set_robot()
                self.redraw()
                sleep(0.5)
                move_counter += 1

            # TODO: Mark obstacle as visited only when image is recognised successfully
            # TODO: If obstacle cannot be reached, add route to it at the end of sp.route to try again at the end
            self.console_writeline("Recognizing image...")
            sleep(2)  # Capture image
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

    # def get_shortest_path(self):
    #     sp = ShortestPath(self.algo_grid)
    #     start_time = perf_counter()
    #     self.console_writeline("Retrieving shortest path..")
    #
    #     self.actions.clear()
    #     sp.get_shortest_path()
    #     self.actions.enqueue(sp.route)
    #     end_time = perf_counter()
    #
    #     self.console_writeline(f"Time taken: {end_time - start_time:.2f}")
    #
    #     if not self.actions.is_completed:
    #         print("Not complete")
    #         for item in self.actions.routes:
    #             self.total_distance += item.distance
    #         self.console_writeline(f"Path found with total distance = {self.total_distance}. Starting simulation...")
    #
    #         self.robot.row = 0
    #         self.robot.col = 0
    #         self.redraw()
    #
    #     else:
    #         self.console_writeline("ERROR! Not all paths are possible")


    # def on_click_start(self):
    #
    #     if self.total_distance == 0:
    #         self.get_shortest_path()
    #
    #     if self.actions.is_completed or not self.obstacles:
    #         self.console_writeline("Nothing left to do.")
    #         self.redraw()
    #         return
    #
    #     if not self.run_simulation:
    #         self.run_simulation = True
    #         self.timer = 0
    #
    #     if not self.actions.is_completed and self.run_simulation:
    #
    #         if not self.actions.dequeue() is None:
    #             print(self.actions.dequeue())
    #             robot_pos, move = self.actions.dequeue()
    #             self.robot = robot_pos
    #             # robot_indices_internal(robot_pos)
    #             self.console_writeline(f"({robot_pos.row}, {robot_pos.col}, {robot_pos.direction}): {move}")
    #         self.redraw()
    #     else:
    #         self.console_writeline("Route complete!")
    #         self.console_writeline(f"Total Distance: {self.total_distance}")
    #     self.redraw()
