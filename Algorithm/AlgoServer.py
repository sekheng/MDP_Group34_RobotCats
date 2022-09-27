import socket
import json
from grid import *
from helper import *
from obstacle import *
from robot import *
from shortest_path import *
import constants


class AlgoServer:
    def __init__(self):
        self.host = '192.168.34.22'
        self.port = 5560
        # self.input_obstacles = []
        self.algo_obstacles_dict = {}
        self.algo_obstacles = []
        # for o in self.input_obstacles:
        #     row, col, d = to_indices(o)
        #     self.algo_obstacles.append(Obstacle(row, col, d))
        r_row, r_col, r_d = to_indices([1, 1, 1])  # For algorithm robot
        self.algo_robot = Robot(r_row, r_col, r_d)
        self.command_list = None

        # self.algo_grid = Grid(obstacles=self.algo_obstacles, robot=self.algo_robot)
        # self.algo_path = ShortestPath(self.algo_grid)
        # self.algo_path.get_shortest_path()
        # self.str_stm_commands_list = ' '.join(get_stm_commands(self.algo_path.route))
        # print(self.str_stm_commands_list)
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
        print("conn is", conn, "address is", address)
        return conn

    def server_get(self):

        algo_grid = Grid(obstacles=self.algo_obstacles, robot=self.algo_robot)
        algo_path = ShortestPath(algo_grid)
        algo_path.get_shortest_path()

        self.command_list = get_stm_commands(algo_path.route)

        # str_stm_commands_list = ' '.join(get_stm_commands(algo_path.route))
        # print(str_stm_commands_list)


    def server_repeat(self, dataMessage):
        reply = dataMessage[1]
        return reply

    def server_data_transfer(self, server, conn):
        # A big loop that sends/receives data until told not to.
        while True:
            # Receive the data
            data = conn.recv(1024)  # receive the data
            data = data.decode('utf-8')
            command_list_index = 0
            try:
                parsed_data = json.loads(data)
                self.android_to_algo(parsed_data)
                print('added obstacle: ', parsed_data)
            except:
                print('data is not a json string')
                print('data is ' + str(data))
                # Split the data such that you separate the command
                # from the rest of the data.
                dataMessage = data.split(' ', 1)
                print('data message is ' + str(dataMessage))
                command = dataMessage[0]
                if command == 'GET':
                    self.server_get()
                    reply = self.command_list[0]
                elif command == 'REPEAT':
                    reply = self.server_repeat(dataMessage)
                elif command == 'EXIT':
                    print("Our client has left us :(")
                    break
                elif command == 'KILL':
                    print("Our server is shutting down.")
                    server.close()
                    break
                elif command == 'kkkk':
                    try:
                        command_list_index += 1
                        reply = self.command_list[command_list_index]
                    except:
                        reply = 'No more stm commands left.'
                else:
                    reply = 'Unknown Command'
                # Send the reply back to the client
                print('reply is ' + str(reply))
                conn.sendall(reply.encode('utf-8'))
                print("Data has been sent!")
        conn.close()

    def android_to_algo(self, data: dict):
        # Converts obstacle coordinates from Android into coordinates for algorithm

        if "type" in data.keys() and data["type"] == "obstacle":
            x = int(data['x'])
            y = AREA_WIDTH//CELL_SIZE - 1 - int(data['y'])
            d = data["direction"].upper()[0]
            obstacle = [x, y, d]  # Simulator coordinates
            row, col, direction = to_indices(obstacle) # Algorithm coordinates
            self.algo_obstacles.append(Obstacle(row, col, direction))
            # print(self.input_obstacles)

    def main(self):
        s = self.setup_server()
        while True:
            try:
                conn = self.setup_connection(s)
                self.server_data_transfer(s, conn)
            except:
                break


if __name__ == "__main__":
    test_server = AlgoServer()
