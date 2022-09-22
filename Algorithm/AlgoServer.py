import socket
from grid import *
from helper import *
from obstacle import *
from robot import *
from shortest_path import *
import constants


class AlgoServer:
    def __init__(self):
        self.host = ''
        self.port = 5560
        self.input_obstacles = [[2, 15, 'S'], [6, 13, 'E'], [10, 17, 'S'], [15, 7, 'W'], [18, 18, 'S'], [8, 2, 'N'], [13, 9, 'N'], [18, 6, 'N']]
        self.algo_obstacles = []
        for o in self.input_obstacles:
            row, col, d = to_indices(o)
            self.algo_obstacles.append(Obstacle(row, col, d))
        r_row, r_col, r_d = to_indices([1, 1, 1])  # For algorithm robot
        self.algo_robot = Robot(r_row, r_col, r_d)
        self.algo_grid = Grid(obstacles=self.algo_obstacles, robot=self.algo_robot)

        self.algo_path = ShortestPath(self.algo_grid)
        self.algo_path.get_shortest_path()

        self.stm_commands_list = get_stm_commands(self.algo_path.route)
        self.main()

    def setup_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created.")
        try:
            server.bind((self.host, self.port))
        except socket.error as msg:
            print(msg)
        print("Socket bind complete.")
        return server

    def setup_connection(self, server):
        server.listen(1)
        conn, address = server.accept()
        print("Connected to: " + address[0] + ":" + str(address[1]))
        return conn

    def server_get(self):
        reply = self.stm_commands_list
        return reply

    def server_repeat(self, dataMessage):
        reply = dataMessage[1]
        return reply

    def server_data_transfer(self, server, conn):
        # A big loop that sends/receives data until told not to.
        while True:
            # Receive the data
            data = conn.recv(1024)  # receive the data
            data = data.decode('utf-8')
            # Split the data such that you separate the command
            # from the rest of the data.
            dataMessage = data.split(' ', 1)
            command = dataMessage[0]
            if command == 'GET':
                reply = self.server_get()
            elif command == 'REPEAT':
                reply = self.server_repeat(dataMessage)
            elif command == 'EXIT':
                print("Our client has left us :(")
                break
            elif command == 'KILL':
                print("Our server is shutting down.")
                server.close()
                break
            else:
                reply = 'Unknown Command'
            # Send the reply back to the client
            conn.sendall(str.encode(reply))
            print("Data has been sent!")
        conn.close()

    def main(self):
        s = self.setup_server()
        while True:
            try:
                conn = self.setup_connection(s)
                self.server_data_transfer(s, conn)
            except:
                break

test_server = AlgoServer()