class AlgoTask2():
    def __init__(self):
        self.DIST_START_OBJECT1 = 0
        self.DIST_OBJECT1_OBJECT2 = 0
        self.stm_command_list = []
        self.reversed_stm_command_list = []
        self.combined_stm_command_list = []
        self.main()

    def main(self):
        self.set_dist_travelled_start_object1()
        self.set_dist_travelled_object1_object2()
        self.stm_command_list.append('w'+str(self.DIST_START_OBJECT1))
        self.capture_image()
        self.stm_command_list.append('w'+str(self.DIST_OBJECT1_OBJECT2))
        self.capture_image()
        #self.reversed_stm_command_list = self.reverse(self.stm_command_list)
        #self.combined_stm_command_list = self.stm_command_list + self.reversed.command_list
        #return combined_stm_command_list



    def set_dist_travelled_start_object1(self):
        input_distance = int(input('Input distance from start point to object 1: '))
        self.DIST_START_OBJECT1 = input_distance - 20

    def set_dist_travelled_object1_object2(self):
        input_distance = int(input('Input distance from start point to object 1: '))
        self.DIST_OBJECT1_OBJECT2 = input_distance - 20 - 30

    def capture_image(self):
        image_rec_result = input('L or R')
        if image_rec_result == 'L':
            self.stm_command_list.append('a090')
            self.stm_command_list.append('e090')
            self.stm_command_list.append('e090')
            self.stm_command_list.append('a090')
        elif image_rec_result == 'R':
            self.stm_command_list.append('d090')
            self.stm_command_list.append('q090')
            self.stm_command_list.append('q090')
            self.stm_command_list.append('d090')




