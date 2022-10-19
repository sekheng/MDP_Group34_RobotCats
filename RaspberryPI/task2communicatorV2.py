import json
import time
import ast
from multiprocessing import Process, Queue, Value

from robot_stm import STM_communicator
from android_bluetooth import Android_communicator

from imagedetection import *
from image_postproc2 import *

'''
New structure for multiprocessing to have only 2 queues
Image Recognition process to run in main program
'''

class Task2CommunicatorV2:
    def __init__(self):
        
        print('Initializing Task 2 Multiprocessing Communication')
        
        self.android = Android_communicator()
        self.stm = STM_communicator()

        self.msg_queue = Queue()
        self.state = Value('i',-1)
        self.action1 = Value('i',0)
        self.action2 = Value('i',0)
        
    def start(self):
        try:
            self.android.connect_android()
            self.stm.connect_stm()

            Process(target=self.read_android, args=(self.msg_queue,)).start()
            Process(target=self.read_stm, args=(self.msg_queue,)).start()
                        
            Process(target=self.write_target, args=(self.msg_queue,)).start()
            print('Multiprocess Communication Session Started')
            
            while True:
                try:
                    value = ""
                    if self.state.value == 0 or self.state.value == 1:
                        value = self.runImageModel()
                    if value != "":
                        if self.state.value == 0:
                            if value == 'Left':
                                with self.action1.get_lock():
                                    self.action1.value = 1
                            elif value == 'Right':
                                with self.action1.get_lock():
                                    self.action1.value = 2
                        elif self.state.value == 1:
                            if value == 'Left':
                                with self.action2.get_lock():
                                    self.action2.value = 1
                            elif value == 'Right':
                                with self.action2.get_lock():
                                    self.action2.value = 2 
                except Exception as error:
                    print('Image Capture Error: ', error)
        
        except KeyboardInterrupt:
            self.android.disconnect_all_android()
            print('Disconnected by user interrupt')
        except Exception as error:
            self.android.disconnect_all_android()
            print('Error:', error)

    def end(self):
        self.android.disconnect_all_android()
        print('Multiprocess Communication Session Ended')

    def read_android(self, msg_queue):
        while True:
            try:
                msg = ast.literal_eval(self.android.read_android())
                if msg is not None:
                    print('Read Android: ' + str(msg))
                    print('Send to STM')
                    if 'status' in msg:
                        if msg['status'] == 'fastest':
                            with self.state.get_lock():
                                self.state.value = 0
                            msg_queue.put_nowait(self.format_for('STM', 'o000'))
                        elif msg['status'] == 'idle':
                            print(str(self.state.value)+' values captured')
                            print(str(min(self.state.value,2))+' pictures to stitch')
                            stitch_pic(min(self.state.value, 2))
                            print('Pictures stitched')
                            with self.state.get_lock():
                                self.state.value = -1
                            print('State reset')
            except Exception as error:
                print('Android read failed: ', error)
                self.android.connect_android()
                raise error

    def read_stm(self, msg_queue):
        while True:
            msg = self.stm.read_stm()
            if msg is not None and msg == 'kkkk':
                print('Read STM: ' + str(msg))
                if self.state.value <= 1:
                    if self.state.value == 0:
                        if self.action1.value == 1:
                            msg_queue.put_nowait(self.format_for('STM', 'k000'))
                        elif self.action1.value == 2:
                            msg_queue.put_nowait(self.format_for('STM', 'l000'))
                        else:
                            value = self.runImageModel()
                            if value == 'Left':
                                msg_queue.put_nowait(self.format_for('STM', 'k000'))
                            elif value == 'Right':
                                msg_queue.put_nowait(self.format_for('STM', 'l000'))
                                
                    elif self.state.value == 1:
                        if self.action2.value == 1:
                            msg_queue.put_nowait(self.format_for('STM', 'n000'))
                        elif self.action2.value == 2:
                            msg_queue.put_nowait(self.format_for('STM', 'm000'))
                        else:
                            value = self.runImageModel()
                            if value == 'Left':
                                msg_queue.put_nowait(self.format_for('STM', 'n000'))
                            elif value == 'Right':
                                msg_queue.put_nowait(self.format_for('STM', 'm000'))
                    
                    with self.state.get_lock():
                        self.state.value += 1

    def write_target(self, msg_queue):
        while True:
            if not msg_queue.empty():
                msg = msg_queue.get_nowait()
                msg = json.loads(msg)
                payload = msg['payload']
                
                if msg['target'] == 'AND':
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
    
    def runImageModel(self):
        value = ""
        print('Capturing image')
        img = captureImage()
        value, confidence, image = runModel(img)
        if confidence >=0.5 and (value == 'Left' or value == 'Right'):
            filename = './images2/image'+str(self.state.value)+'.jpg'
            cv2.imwrite(filename, image)
            print("Image Result: ", value, " (", confidence, ")")
        return value