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

class SimulatorManager():
    def __init__(self, result_app):
        r_row, r_col, r_dir = to_indices([0, 0, 1])
        self.robot = Robot(r_row, r_col, r_dir)
        self.obstacles = [[2,15,'S'], [6, 13,'E'], [10,17,'S'], [15,7,'W'], [18,18,'S'], [8,2,'N'], [13,9,'N'], [18,6,'N']]

        algo_obstacles = []
        for o in self.obstacles:
            row, col, dir = to_indices(o)
            algo_obstacles.append(Obstacle(row, col, dir))
        self.algo_grid = Grid(obstacles=algo_obstacles, robot=self.robot)

        self.grid = SimulatorGrid(grid_app=result_app, obstacles=algo_obstacles)
        self.grid.on_cell_click(callback=self.on_click_cell)
        self.grid.initialise_grid()

        self.console_clear()

        # self.actions = ActionQueue(self.rm)

        self.visited_obstacle = []
        self.total_distance = -1

        self.run_simulation = False
        self.timer = 0

    def update(self):
        self.timer += 0.05

        auto = dpg.get_value("step_by_step")
        # timestep = dpg.get_value("slider_timestep")

        if auto and self.run_simulation:
            self.timer = 0
            # self.on_click_step()

    def on_click_step(self):

        if self.actions.is_completed or not self.mm.obstacle_set:
            self.console_writeline("Nothing left to do..")
            self.redraw()
            return

        if not self.run_simulation:
            self.run_simulation = True
            self.timer = 0

        if self.actions.is_completed:
            self.get_shortest_path()

        if not self.actions.is_completed and self.run_simulation:
            path = self.actions.dequeue()
            if path:
                self.console_writeline(f"({path.x}, {path.y}, {path.orientation}): {path.action}")
            self.redraw()
        else:
            self.console_writeline("Route complete!")
            self.console_writeline(f"Total Distance: {self.total_distance}")
        self.redraw()

    def get_shortest_path(self):
        start_time = perf_counter()
        self.console_writeline("Retrieving shortest path..")

        self.actions.clear()
        self.actions.enqueue(self.mm.get_shortest_path())
        end_time = perf_counter()

        self.console_writeline(f"Time taken: {end_time - start_time:.2f}")

        if not self.actions.is_completed:
            for item in self.actions.obstacle_routes:
                self.total_distance += item.distance

            self.rm.robot.x = 0
            self.rm.robot.y = 0
            self.redraw()
        else:
            self.console_writeline("ERROR! Not all paths are possible")


    def console_writeline(self, msg):
        self.console += f"{msg}\n"
        dpg.set_value("text_console", self.console)

    def console_clear(self):
        self.console = ""
        dpg.set_value("console_body", self.console)

    def delete_obstacle(self, x: int, y: int) -> None:
        # row, col = to_indices(x, y)
        self.algo_grid.remove_obstacle(x, y)

    def get_obstacle(self, x, y):
        # row, col = to_indices(x, y)
        return self.algo_grid.get_obstacle(x, y)

    def rotate_obstacle(self, obstacle):

        self.algo_grid.remove_obstacle(obstacle)

        if obstacle.direction == 'N':
            obstacle.direction = 'E'
        elif obstacle.direction == 'E':
            obstacle.direction = 'S'
        elif obstacle.direction == 'S':
            obstacle.direction = 'W'
        elif obstacle.direction == 'W':
            obstacle.direction = 'N'

        return obstacle

    def on_click_cell(self, x, y):
        clear = True if (dpg.is_mouse_button_down(1)) else False
        obs = self.get_obstacle(x, y)

        if clear and obs:
            self.delete_obstacle(obs)
        elif clear and obs is None:
            print("Unable to remove object, obstacle does not exist.")
        else:
            if obs:
                obs = self.rotate_obstacle(obs)
            self.algo_grid.obstacles.append(obs)

        self.redraw()

    def redraw(self):
        # sell all colours to white
        for y in range(self.grid.rows):
            for x in range(self.grid.cols):
                self.grid.set_color(x, y)

        # draw robot
        for i in range(CAR_LENGTH):
            for j in range(CAR_WIDTH):
                self.grid.set_color(
                    self.robot.row + j,
                    self.robot.col + i,
                    color=[85, 168, 104])

        # draw obstacles
        for obstacle in self.grid.obstacles:
            color = [37, 37, 38]

            if obstacle in self.visited_obstacle:
                color = [85, 168, 104]

            self.grid.set_color(
                    obstacle.x,
                    obstacle.y,
                    color=color)

        # draw obstacle direction
        self.grid.configure_obstacle_direction(self.algo_grid.obstacles, Color.ROBOT.value)
        self.grid.update_robot_position(self.robot.x, self.robot.y, self.rm.robot.orientation)

        # update panels
        dpg.set_value("text_robot_x", self.rm.robot.x)
        dpg.set_value("text_robot_y", self.rm.robot.y)
        dpg.set_value("text_robot_direction", self.rm.robot.orientation)
