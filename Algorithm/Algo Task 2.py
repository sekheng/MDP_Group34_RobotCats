class AlgoTask2():
    def __init__(self):
        self.DIST_START_OBJECT1 = 0
        self.DIST_OBJECT1_OBJECT2 = 0
        self.stm_command_list = []
        self.main()


    def main(self):
        #commands for moving forward
        self.set_dist_travelled_start_object1()
        self.set_dist_travelled_object1_object2()
        self.stm_command_list.append('w'+str(self.DIST_START_OBJECT1-20))
        self.stm_command_list.append('P')
        self.capture_image(1)
        self.stm_command_list.append('w'+str(self.DIST_OBJECT1_OBJECT2-50))
        #commands for moving back to start point
        self.stm_command_list.append('P')
        second_obstacle_turn = self.capture_image(2)
        self.return_path(second_obstacle_turn)
        print(self.stm_command_list)

    def set_dist_travelled_start_object1(self):
        input_distance = int(input('Input distance from start point to object 1: '))
        self.DIST_START_OBJECT1 = input_distance

    def set_dist_travelled_object1_object2(self):
        input_distance = int(input('Input distance from start point to object 1: '))
        self.DIST_OBJECT1_OBJECT2 = input_distance

    def capture_image(self, obstacle_no):
        print(obstacle_no)
        image_rec_result = input('L or R: ')
        if image_rec_result == 'L' and obstacle_no == 1:
            self.stm_command_list.append('a090')
            self.stm_command_list.append('e090')
            self.stm_command_list.append('e090')
            self.stm_command_list.append('a090')
        elif image_rec_result == 'R' and obstacle_no == 1:
            self.stm_command_list.append('d090')
            self.stm_command_list.append('q090')
            self.stm_command_list.append('q090')
            self.stm_command_list.append('d090')
        elif image_rec_result == 'L' and obstacle_no == 2:
            self.stm_command_list.append('a090')
            self.stm_command_list.append('w020')
            self.stm_command_list.append('e090')
            self.stm_command_list.append('e090')
            self.stm_command_list.append('w020')
        elif image_rec_result == 'R' and obstacle_no == 2:
            self.stm_command_list.append('d090')
            self.stm_command_list.append('w020')
            self.stm_command_list.append('q090')
            self.stm_command_list.append('q090')
            self.stm_command_list.append('w020')
        return image_rec_result

    def return_path(self, second_obstacle_turn):
        if second_obstacle_turn == 'L':
            self.stm_command_list.append('w020')
            self.stm_command_list.append('e090')
            self.stm_command_list.append('w' + str(self.DIST_OBJECT1_OBJECT2+10))
            self.stm_command_list.append('e090')
            self.stm_command_list.append('w020')
            self.stm_command_list.append('a090')
            #-20 because distance between robot and obstacle,
            # +50 because need to park inside the car
            self.stm_command_list.append('w' + str(self.DIST_START_OBJECT1-20+50))
        elif second_obstacle_turn == 'R':
            self.stm_command_list.append('w020')
            self.stm_command_list.append('q090')
            self.stm_command_list.append('w' + str(self.DIST_OBJECT1_OBJECT2+10))
            self.stm_command_list.append('q090')
            self.stm_command_list.append('w020')
            self.stm_command_list.append('d090')
            #-20 because distance between robot and obstacle,
            # +50 because need to park inside the car
            self.stm_command_list.append('w' + str(self.DIST_START_OBJECT1-20+50))

test = AlgoTask2()