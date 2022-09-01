import dearpygui.dearpygui as dpg
import constants
import grid

class SimulatorGrid():
    def __init__(self, row, col, grid_app):
        self.rows = row
        self.col = col
        self.grid_app = grid_app

        self.grid_app_size = dpg.get_item_height(grid_app)
        self.cell_size = self.grid_app_size/self.rows

        self.min_x_pixels = self.min_y_pixels = 0
        self.max_x_pixels = self.max_y = self.grid_app_size

        self.cells = []
        self.robot_direction = None
        self.obstacles = [(None,None)]
