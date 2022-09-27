import socket
import json

class Algo_comm:
    def __init__(self, host='192.168.34.22', port=5560):

        self.port = port
        self.host = host
        self.socket = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect_algo(self):
        ADDR = (self.host,self.port)
        self.socket.connect(ADDR)
    
    def send_to_algo(self,msg):
        FORMAT = 'utf-8'
        message = msg.encode(FORMAT)
        self.socket.send(message)

    def read_from_algo(self):
        conn, addr = self.socket.accept()
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode()
        print(f"[{addr}] {msg}")
    


        




