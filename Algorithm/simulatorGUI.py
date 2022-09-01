import dearpygui.dearpygui as dpg

class Robot_Cats_Simulator():
    def __init__(self):
        self.APP_WIDTH = 1280
        self.APP_HEIGHT = 960
        self.GRID_SIZE = 850

        self.main_app = None
        self.grid_app = None
        self.control_app = None
        self.result_app = None


        self.application()
        self.app_configuration()

    def app_configuration(self):
        dpg.create_viewport()
        dpg.set_viewport_width(self.APP_WIDTH)
        dpg.set_viewport_height(self.APP_HEIGHT)
        dpg.set_viewport_resizable(False)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_viewport_title("Robot Cats Simulator")

    def application(self):
        with dpg.font_registry():
            dpg.set_global_font_scale(1.0)

        with dpg.window(label="Robot Cats Simulator") as self.main_app:
            with dpg.child_window(label="Grid", height=self.GRID_SIZE, width=self.GRID_SIZE, border=True, no_scrollbar=True, pos = [0,20]) as self.grid_app:
                pass
            with dpg.child_window(label="Controls", width=450, pos=[self.GRID_SIZE+10, 20]) as self.control_app:
                dpg.add_input_text(tag='instructions_header', default_value="How to set/remove/edit obstacles", readonly=True)
                dpg.add_text("LClick on an empty cell to set obstacle")
                dpg.add_text("LClick on an obstacle to change direction")
                dpg.add_text("RClick on a cell to clear cell")
            with dpg.child_window(label='Robot Info', pos=[self.GRID_SIZE+10, 125]) as robot_info_app:
                dpg.add_input_text(tag='robot_info_header', default_value="Robot Information", readonly=True)
                dpg.add_text("Robot Position:")
                with dpg.group(horizontal=True):
                    dpg.add_text("X:")
                    dpg.add_input_text(tag="robot_x_highlight", default_value=0, width=22, readonly=True)
                    dpg.add_text("Y:")
                    dpg.add_input_text(tag="robot_y_highlight", default_value=0, width=22, readonly=True)
                with dpg.group(horizontal=True):
                    dpg.add_text('Robot Direction:')
                    dpg.add_input_text(tag="robot_direction_highlight", width=45, default_value='North', readonly=True)
            with dpg.child_window(label='Controls', pos=[self.GRID_SIZE+10,225]):
                dpg.add_input_text(tag='controls_header', width=65, default_value='Controls', readonly=True)
                dpg.add_text('')
                dpg.add_checkbox(tag='step_by_step', label='Step-by-step')
                with dpg.group(horizontal=True):
                    dpg.add_button(tag='start', label='Start', width=175, height=50)
                    dpg.add_button(tag='reset', label='Reset', width=175, height=50)
            with dpg.child_window(label='console', pos=[self.GRID_SIZE+10, 360]):
                dpg.add_input_text(tag='console_header', width=57, default_value='Console', readonly=True)
                dpg.add_input_text(tag='console_body', multiline=True, default_value='', width=400, height=1000, readonly=True)

        dpg.set_primary_window(self.main_app, True)




if __name__ == "__main__":
    dpg.create_context()
    app = Robot_Cats_Simulator()

    #dpg.start_dearpygui()
    while dpg.is_dearpygui_running():
        #app.update()
        dpg.render_dearpygui_frame()
