from robot_stm import STM_communicator
from android_bluetooth import Android_communicator
from imagedetection import *
    
import ast
import time

class SimpleCommunicator:
    
    def __init__(self):
        
        print('Starting Inital Communication')
        
        self.stm = STM_communicator()  # handles connection to STM
        self.android = Android_communicator()  # handles connection to Android
        self.queue = []
        
    def start(self):
        
        try:
            self.stm.connect_stm()
            self.android.connect_android()
            print('Connected to STM and Android')
        except Exception as error:
            self.android.disconnect_all_android()
            print('Error:', error)
            
    def end(self):
        self.android.disconnect_all_android()
        print("Disconnected from android")
            
    def manual_nav(self):
        
        try:
            while True:
                #print(self.queue)
                if len(self.queue) == 0:
                    from_android = ast.literal_eval(self.android.read_android())
                    if from_android is not None:
                        self.queue.append(from_android)
                else:
                    queue_msg = self.queue[0]
                    self.queue.pop(0)
                    to_stm = ""
                    
                    if 'robot_direction' in queue_msg:
                        if queue_msg['robot_direction'] == 'up':
                            to_stm = 'w020'
                        elif queue_msg['robot_direction'] == 'down':
                            to_stm = 's020'
                        elif queue_msg['robot_direction'] == 'left':
                            to_stm = 'a090'
                        elif queue_msg['robot_direction'] == 'right':
                            to_stm = 'd090'
                    
                    if to_stm != "":
                        self.stm.write_stm(to_stm.encode())
                        return_msg = ""
                        while return_msg != "kkkk":
                            return_msg = self.stm.read_stm()
                            print(return_msg)
                        print("Robot finish executing")
        except Exception as error:
            raise error
        
        print("Manual navigation ended!")
            
    def autonav_obstacle(self):
        try:
            self.queue = ['takepic']
            i = 0
            
            while len(self.queue) > 0:
                print(self.queue)
                queue_msg = self.queue[0]
                self.queue.pop(0)
                
                if queue_msg == 'takepic':
                    try:
                        result = ("", 0)
                        while result[1] <= 0.5:
                            img = captureImage()
                            value, confidence, result_image = runModel(img)
                            cv2.imwrite('image{}.jpg'.format(i), result_image)
                            print("Value: ", value, "; Confidence: ", confidence)
                        if result[0] != 'Bullseye':
                            print("Value found!")
                            break
                    except Exception as error:
                        #print(error)
                        print("No value found")
                    i += 1
                    self.queue.extend(['e090', 's010', 'takepic'])
                else:
                    self.stm.write_stm(queue_msg.encode())
                    return_msg = ""
                    while return_msg != "kkkk":
                        return_msg = self.stm.read_stm()
                        print(return_msg)
                    print("Robot finish executing")
                    time.sleep(0.2)
            
        except Exception as error:
            raise error
        
        print("Auto navigation for obstacle complete!")
        
