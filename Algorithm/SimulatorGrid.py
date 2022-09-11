import dearpygui.dearpygui as dpg
import math
from cmath import pi
from constants import *
from helper import *
from obstacle import Obstacle
import grid

class SimulatorGrid():
    def __init__(self, grid_app, obstacles: list[Obstacle]):
        self.rows = AREA_LENGTH//CELL_SIZE
        self.cols = AREA_WIDTH//CELL_SIZE
        self.grid_app = grid_app

        self.grid_app_size = dpg.get_item_height(grid_app)
        self.cell_size = (self.grid_app_size/self.rows)

        #min x and y coordinate in terms of pixels
        self.min_x_pixels = self.min_y_pixels = 0 #starts at the bottom left corner

        #max x and y coordinate in terms of pixels
        self.max_x_pixels = self.max_y_pixels = self.grid_app_size

        self.cells = []
        self.robot_direction = None
        self.obstacles = obstacles

        self.on_cell_click_callback = None

        self.drawlist = None
        self.obstacle_directions = []
        self.initialise_grid()

    def initialise_grid(self):
        if self.drawlist:
            dpg.delete_item(self.drawlist)
            self.drawlist = None

        self.drawlist = dpg.add_drawlist(parent=self.grid_app, width=self.grid_app_size + 1,
                                         height=self.grid_app_size + 1, show=True)
        #draw cells
        for row in range(self.rows):
            for col in range(self.cols):
                dpg.draw_rectangle(
                    # minimum x and y coordinate of the cell based on which col and row the cell belongs in
                    [self.cell_size*col, self.cell_size*row],
                    #maximum x and y coordinate of the cell based on which col and row the cell belongs in
                    [self.cell_size*(col+1), self.cell_size*(row+1)],
                    color = [0,0,0], #black
                    fill = [255,255,255], #white
                    parent=self.drawlist,
                    label='grid',
                    tag=self.get_tag(col, row)
                    )

        #draw grid lines
        for row in range(self.rows):
            dpg.draw_rectangle([self.min_x_pixels, self.cell_size*row],
                               [self.min_x_pixels+(self.rows*self.cell_size), self.cell_size*row],
                               color=[0, 0, 0],
                               fill=[0, 0, 0],
                               thickness=1,
                               parent=self.drawlist
            )

            dpg.draw_rectangle(
                [self.cell_size*row, self.min_y_pixels],
                [self.cell_size*row, self.min_y_pixels + (self.rows*self.cell_size)],
                color=[0, 0, 0],
                fill=[0, 0, 0],
                thickness=1,
                parent=self.drawlist
            )

        with dpg.draw_node(tag="robot_direction", parent=self.drawlist) as item:
            dpg.draw_triangle(
                [0, 0],
                [self.cell_size * 3, 0],
                [self.cell_size * (3 / 2), -self.cell_size * 3],
                # [0, 850],
                # [self.cell_size * 3, 850], #robot size on grid is 3by3, so the three points will be (0,0), (3,0) and (1.5,1.5) if facing north
                # [self.cell_size * (3 / 2), 850-(self.cell_size * 3)],
                color=[0, 0, 0],
                fill=[0, 255, 0],
                before='grid'
            )

            self.robot_direction = item
        self.update_robot_position(1, 1, 1)
        self.configure_obstacles(obstacles=self.obstacles)

        # configure click events
        with dpg.handler_registry():
            dpg.add_mouse_click_handler(callback=self.cell_clicked)

    def set_color(self, x, y, color=[255, 255, 255], flip=False):
        if x < self.cols and y < self.rows:
            dpg.configure_item(self.get_tag(x, y, flip),
                               color=color,
                               fill=color)

        else:
            print(f"Map: set_color unable to set color on position {self.get_tag(x, y, flip=flip)}")

    def update_robot_position(self, x, y, direction):

        x_offset = 0
        y_offset = 0

        if direction == 1:
            x_offset = -self.cell_size
            y_offset = self.cell_size * 2
        elif direction == 3:
            x_offset = self.cell_size * 2
            y_offset = -self.cell_size
        elif direction == 2:
            x_offset = -self.cell_size
            y_offset = -self.cell_size
        elif direction == 4:
            x_offset = self.cell_size * 2
            y_offset = self.cell_size * 2

        angle = pi * self.direction_to_angle(direction) / 180.0
        x, y = self.get_internal_pos(x, y)
        position = [(x * self.cell_size + x_offset), (y * self.cell_size + y_offset)]

        translate = dpg.create_translation_matrix(position)
        rotation = dpg.create_rotation_matrix(angle=-angle, axis=[0, 0, -1])

        dpg.apply_transform(self.robot_direction, translate * rotation)

    def configure_obstacles(self, obstacles):

        # for item in self.obstacle_directions:
        #     print("item =", item)
        #     dpg.delete_item(item)
        #
        # self.obstacle_directions.clear()

        for o in obstacles:
            if not dpg.does_item_exist(str(o)):
                with dpg.draw_node(tag=str(o), parent=self.drawlist) as item:
                    dpg.draw_rectangle(
                        [0, 0],
                        [self.cell_size, 5],
                        color=IMAGE_COL,
                        fill=IMAGE_COL,
                    )

                    # self.obstacle_directions.append(item)

            # apply transform (cause we only create the direction rect when obstacale is added)
            angle = pi * self.direction_to_angle(o.direction) / 180.0
            x_offset = 0
            y_offset = 0

            if o.direction == 'N':
                x_offset = 0
                y_offset = 0
            elif o.direction == 'S':
                x_offset = y_offset = self.cell_size
            elif o.direction == 'E':
                y_offset = self.cell_size
                x_offset = self.cell_size - 5
            elif o.direction == 'W':
                x_offset = 5

            translate = ((o.row * self.cell_size + x_offset), (o.col * self.cell_size + y_offset))
            dpg.apply_transform(str(o), dpg.create_translation_matrix(translate) * dpg.create_rotation_matrix(angle=angle, axis=[0, 0, -1]))

        for o in obstacles:
            print(f"Setting color for {o.row}, {o.col}")
            self.set_color(o.row,
                           o.col,
                           color=OBSTACLE_COL,
                           flip=True)

    # def on_cell_click(self, callback):
    #     self.on_cell_click_callback = callback
    #     print(callback)

    def get_tag(self, x, y, flip=True) -> str:
        return f"{self.get_internal_pos(x, y)}" if flip else f"{(x, y)}"

    def get_internal_pos(self, x, y):
        return (x, self.rows - y - 1)

    def direction_to_angle(self, direction):
        angle = 0
        if direction == 'N':
            angle = 0
        elif direction == 'E':
            angle = 90
        elif direction == 'S':
            angle = 180
        elif direction == 'W':
            angle = 270
        return angle


    #to check if mouse click is within grid
    def cell_clicked(self):
        mouse_pos = dpg.get_mouse_pos()
        mouse_pos[1] -= 1  # account for window padding

        if (\
        mouse_pos[0] > self.max_x_pixels or mouse_pos[0] < 0 or \
        mouse_pos[1] > self.max_y_pixels or mouse_pos[1] < 0 or \
        dpg.get_active_window() != self.grid_app):
            return


        mouse_pos = dpg.get_drawing_mouse_pos()

        within_x = mouse_pos[0] >= 0 and mouse_pos[0] <= self.max_x_pixels
        within_y = mouse_pos[1] >= 0 and mouse_pos[1] <= self.max_y_pixels

        pos = (math.trunc(mouse_pos[0]//self.cell_size), math.trunc(mouse_pos[1]//self.cell_size))

        if (within_x and within_y):
            if self.on_cell_click_callback:
                x, y = self.get_internal_pos(pos[0], pos[1])
                self.on_cell_click_callback(x, y)
