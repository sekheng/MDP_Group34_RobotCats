import json
import time
import ast
from multiprocessing import Process, Queue, Value

from robot_stm import STM_communicator
from android_bluetooth import Android_communicator
from algo_wifi import Algo_communicator

from imagedetection import *
from image_postproc import *

'''
New structure for multiprocessing to have only 2 queues
Image Recognition process to run in main program
'''

class MultiCommunicator:
    def __init__(self):
        
        print('Initializing Multiprocessing Communication')
        
        self.android = Android_communicator()
        self.stm = STM_communicator()
        
        #print('\nEnter IP address for connected device to network:')
        #hostaddr = input()
        self.algo = Algo_communicator()

        self.msg_queue = Queue()
        self.imagecount = Value('i',0)
        
    def start(self):
        try:
            self.android.connect_android()
            self.stm.connect_stm()
            self.algo.connect_algo()

            Process(target=self.read_android, args=(self.msg_queue,)).start()
            Process(target=self.read_stm, args=(self.msg_queue,)).start()
            Process(target=self.read_algo, args=(self.msg_queue,)).start()
            
            Process(target=self.write_target, args=(self.msg_queue,)).start()

            print('Multiprocess Communication Session Started')

        except KeyboardInterrupt:
            self.android.disconnect_all_android()
            self.algo.disconnect_algo()
            print('Disconnected by user interrupt')
        except Exception as error:
            self.android.disconnect_all_android()
            self.algo.disconnect_algo()
            print('Error:', error)
        
    def sendImages(self):
        return

    def end(self):
        self.android.disconnect_all_android()
        print('Multiprocess Communication Session Ended')

    def read_android(self, msg_queue):
        while True:
            try:
                msg = ast.literal_eval(self.android.read_android())
                if msg is not None:
                    print('Read Android: ' + str(msg))
                    if 'robot_direction' in msg:
                        print('Send to STM')
                        direction = msg['robot_direction']
                        if direction == 'up':
                            msg_robot = 'w010'
                        elif direction == 'down':
                            msg_robot = 's010'
                        elif direction =='left':
                            msg_robot = 'a010'
                        elif direction =='right':
                            msg_robot = 'd010'
                        elif direction =='right diagonal up':
                            msg_robot = 'e090'
                        elif direction =='left diagonal up':
                            msg_robot = 'q090'
                        elif direction =='right diagonal down':
                            msg_robot = 'c090'
                        elif direction =='left diagonal down':
                            msg_robot = 'z090'
                        msg_queue.put_nowait(self.format_for('STM', msg_robot))
                    else:
                        print('Send to Algo')
                        if 'status' in msg:
                            if msg['status'] == 'exploring':
                                msg_queue.put_nowait(self.format_for('ALG', 'GET'))
                            elif msg['status'] == 'idle':
                                print(str(self.imagecount.value)+' values captured')
                                stitch_pic(self.imagecount.value)
                                print('Pictures stitched')
                                msg_queue.put_nowait(self.format_for('ALG', 'EXIT'))
                        else:
                            msg_queue.put_nowait(self.format_for('ALG', msg))
                    
            except Exception as error:
                print('Android read failed: ', error)
                self.android.connect_android()
                raise error

    def read_stm(self, msg_queue):
        while True:
            msg = self.stm.read_stm()
            if msg is not None and msg == 'kkkk':
                print('Read STM: ' + str(msg))
                time.sleep(0.5)
                msg_queue.put_nowait(self.format_for('ALG', msg))

    
    def read_algo(self, msg_queue):
        while True:
            try:
                msg = self.algo.read_algo()
                if msg is not None:
                    print('Read Algo: ' + str(msg))
                    if msg == 'DONE':
                        print('=== Path Complete ===')
                        print(str(self.imagecount.value)+' values captured')
                        stitch_pic(self.imagecount.value)
                        print('Pictures stitched')
                        and_status = json.dumps({"status":"idle"})
                        msg_queue.put_nowait(self.format_for('AND', and_status))
                    elif msg[0] == 'P':
                        for i in range(3):
                            try:
                                img = captureImage()
                                value, confidence, image = runModel(img)
                                if confidence >=0.5 and value != 'bullseye':
                                    filename = './images/image'+str(self.imagecount.value)+'.jpg'
                                    cv2.imwrite(filename, image)
                                    print("Image Result: ", value, " (", confidence, ")")
                                    with self.imagecount.get_lock():
                                        self.imagecount.value += 1
                                    print(str(self.imagecount.value) + ' values captured')
                                    obstacle = json.loads(msg[1:])
                                    obstacle["symbol"] = value
                                    new_msg = json.dumps(obstacle)
                                    msg_queue.put_nowait(self.format_for('AND', new_msg))
                                    break
                            except Exception as error:
                                print('Image Capture Error: ', error)
                        msg_queue.put_nowait(self.format_for('ALG', 'kkkk'))
                    elif msg != 'Unknown Command':
                        if len(msg) == 4:
                            msg_queue.put_nowait(self.format_for('STM', msg))
                        else:
                            msg_queue.put_nowait(self.format_for('AND', msg))
            except Exception as error:
                print('Error:', error)
                raise error

    def write_target(self, msg_queue):
        while True:
            if not msg_queue.empty():
                msg = msg_queue.get_nowait()
                msg = json.loads(msg)
                payload = msg['payload']

                
                if msg['target'] == 'ALG':
                    print('Write Algo:' + str(payload))
                    self.algo.write_algo(payload)
                
                elif msg['target'] == 'AND':
                    print('Write Android:' + str(payload))
                    self.android.write_android(payload)

                elif msg['target'] == 'STM':
                    print('Write STM:' + str(payload))
                    self.stm.write_stm(payload)
                    
    def format_for(self, target, payload):
        return json.dumps({
            'target': target,
            'payload': payload
        })
