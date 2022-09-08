import dearpygui.dearpygui as dpg
import math
import constants
import grid

class SimulatorGrid():
    def __init__(self, row, col, grid_app):
        self.rows = row
        self.col = col
        self.grid_app = grid_app

        self.grid_app_size = dpg.get_item_height(grid_app)
        self.cell_size = (self.grid_app_size/self.rows)

        #min x and y coordinate in terms of pixels
        self.min_x_pixels = self.min_y_pixels = 0 #starts at the bottom left corner

        #max x and y coordinate in terms of pixels
        self.max_x_pixels = self.max_y_pixels = self.grid_app_size

        self.cells = []
        self.robot_direction = None
        self.obstacles = [(None,None)]

        self.on_cell_click_callback = None

        self.drawlist = None
        self.initialise_grid()

    def initialise_grid(self):
        if (self.drawlist):
            dpg.delete_item(self.drawlist)
            self.drawlist = None

        self.drawlist = dpg.add_drawlist(parent=self.grid_app, width=self.grid_app_size + 1,
                                         height=self.grid_app_size + 1, show=True)
        #draw cells
        for row in range(self.rows):
            for col in range(self.col):
                dpg.draw_rectangle(
                    # minimum x and y coordinate of the cell based on which col and row the cell belongs in
                    [self.cell_size*col, self.cell_size*row],
                    #maximum x and y coordinate of the cell based on which col and row the cell belongs in
                    [self.cell_size*(col+1), self.cell_size*(row+1)],
                    color = [0,0,0], #black
                    fill = [255,255,255], #white
                    parent=self.drawlist,
                    label='grid'
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

        with dpg.draw_node(tag="robot_direction", parent=self.drawlist) as robot_direction:
            dpg.draw_triangle(
                [0, 850],
                [self.cell_size * 3, 850], #robot size on grid is 3by3, so the three points will be (0,0), (3,0) and (1.5,1.5) if facing north
                [self.cell_size * (3 / 2), 850-(self.cell_size * 3)],
                color=[0, 0, 0],
                fill=[0, 255, 0],
                before='grid'
            )

            self.robot_direction = robot_direction

        #need to add a update_robot_position function
        #self.update_robot_position(0, 0, 'N')

        # configure click events
        with dpg.handler_registry():
            dpg.add_mouse_click_handler(callback=self.cell_clicked)

    def on_cell_click(self, callback):
        self.on_cell_click_callback = callback

    def direction_to_angle(self, direction):
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
            if self.__on_cell_click_callback:
                x, y = self.__get_internal_pos(pos[0], pos[1])
                self.__on_cell_click_callback(x, y)



