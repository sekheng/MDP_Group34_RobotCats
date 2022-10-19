import socket
import json
import time

LOCALE = 'UTF-8'

class Algo_communicator:
    def __init__(self):

        self.port = 8080
        self.host = '192.168.34.11'
        self.socket = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
    
    def connect_algo(self):
        while True:
            retry = False

            try:
                print('Now Builing Wifi connection with Device...')
                ADDR = (self.host,self.port)
                self.socket.connect(ADDR)
                print("Connected to device at", ADDR)
                #self.conn, addr = self.socket.accept()
                
            except Exception as error:
                print("Connection with Device failed: " + str(error))
                retry = True

            if not retry:
                break
            
            time.sleep(3)
            print('Retrying Wifi Connection to Device...')
            
    def disconnect_algo(self):
        self.write_algo("KILL")
        print("Disconnected from device")
        
    def write_algo(self,msg):
        try:
            if msg == 'GET' or msg == 'kkkk':
                message = str(msg).encode(LOCALE)
            else:
                message = json.dumps(msg).encode(LOCALE)
            self.socket.send(message)
        except Exception as error:
            print('Algo write failed: ' + str(error))
            raise error

    def read_algo(self):
        try:
            msg = self.socket.recv(1024).decode(LOCALE).strip()
            #if msg != ' ' or msg != '' or msg != '\n' or msg is not None:
                #print('From Algo:', msg)
                
            if msg is None:
                return None
            
            if len(msg) > 0:
                return msg
                
            return None
        except Exception as error:
            print('Algo read failed: ' + str(error))
            raise error
            
        
