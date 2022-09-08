import dearpygui.dearpygui as dpg
import constants
import grid

class SimulatorGrid():
    def __init__(self, row, col, grid_app):
        self.rows = row
        self.col = col
        self.grid_app = grid_app

        self.grid_app_size = dpg.get_item_height(grid_app)
        self.cell_size = (self.grid_app_size/self.rows) - 0.5

        #min x and y coordinate in terms of pixels
        self.min_x_pixels = self.min_y_pixels = 0 #starts at the bottom left corner

        #max x and y coordinate in terms of pixels
        self.max_x_pixels = self.max_y = self.grid_app_size

        self.cells = []
        self.robot_direction = None
        self.obstacles = [(None,None)]

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
                    color = [0,0,0,0], #black
                    fill = [255,255,255,255], #white
                    parent=self.drawlist
                    )

        #draw grid lines
        for row in range(self.rows):
            dpg.draw_rectangle([self.min_x_pixels, self.cell_size*row],
                               [self.min_x_pixels+(self.rows*self.cell_size), self.cell_size*row],
                               color=[0, 0, 0, 255],
                               fill=[0, 0, 0, 0],
                               thickness=1,
                               parent=self.drawlist
            )

            dpg.draw_rectangle(
                [self.cell_size*row, self.min_y_pixels],
                [self.cell_size*row, self.min_y_pixels + (self.rows*self.cell_size)],
                color=[0, 0, 0, 255],
                fill=[0, 0, 0, 0],
                thickness=1,
                parent=self.drawlist
            )

