import dearpygui.dearpygui as dpg
from constants import *
from grid import *
from helper import *
from node import *
from obstacle import *
from point_to_point import *
from robot import *
from route import *
from shortest_path import *
from SimulatorGUI import *

class SimulatorManager():
    def __init__(self, result_app):
        r_row, r_col, r_dir = to_indices([0, 0, 1])
        self.robot = Robot(r_row, r_col, r_dir)
        self.obstacles = None
        self.grid = None



