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
        self.port = 8080
        self.input_obstacles = []
        # self.algo_obstacles_dict = {}
        self.algo_obstacles = []

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

        for o in self.input_obstacles:
            row, col, d = to_indices(o)  # Algorithm coordinates
            self.algo_obstacles.append(Obstacle(row, col, d))

        algo_grid = Grid(obstacles=self.algo_obstacles, robot=self.algo_robot)
        print(f"Initial robot {self.algo_robot.get_col()}, {self.algo_robot.get_row()}, {self.algo_robot.get_direction()}")
        algo_path = ShortestPath(algo_grid)
        algo_path.get_shortest_path()
        print("Routes = ", algo_path.route)

        if algo_path.route is not None and len(algo_path.route) != 0:
            self.command_list = get_stm_commands(algo_path.route)
            # self.command_list.insert(0, 'P')  # when we need to bulldoze first obstacle
            print(f"command_list = {self.command_list}")
        else:
            print('No route')

        # str_stm_commands_list = ' '.join(get_stm_commands(algo_path.route))
        # print(str_stm_commands_list)

    def server_repeat(self, dataMessage):
        reply = dataMessage[1]
        return reply

    def server_data_transfer(self, server, conn):
        conn.sendall('Server and client is connected.'.encode('utf-8'))
        # A big loop that sends/receives data until told not to.
        command_list_index = 0
        while True:
            # Receive the data
            data = conn.recv(1024)  # receive the data
            data = data.decode('utf-8')
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
                    print("server_get done")

                    if self.command_list or self.command_list is not None:
                        reply = self.command_list[0]
                        self.update_robot_pos(reply)
                        # Send the reply back to the client
                        print('reply is ' + str(reply))
                        conn.sendall(reply.encode('utf-8'))
                        print("Move has been sent!")

                        # dir = 'NORTH'
                        # if self.get_robot_direction() is None:
                        #     print("robot direction is none")
                        #
                        # if self.get_robot_direction() == 1:
                        #     dir = 'NORTH'
                        # elif self.get_robot_direction() == 2:
                        #     dir = 'EAST'
                        # elif self.get_robot_direction() == 3:
                        #     dir = 'SOUTH'
                        # elif self.get_robot_direction() == 4:
                        #     dir = 'WEST'

                        robot_pos_json = {"type": "robot", "x": str(self.algo_robot.get_col()),
                                          "y": str(self.algo_robot.get_row()), "direction": str(self.get_robot_direction())}
                        reply = json.dumps(robot_pos_json)
                        conn.sendall(reply.encode('utf-8'))
                        print(f"Updated robot position = {reply} has been sent")
                    else:
                        conn.sendall("No path found".encode('utf-8'))

                elif command == 'REPEAT':
                    reply = self.server_repeat(dataMessage)
                    # Send the reply back to the client
                    print('reply is ' + str(reply))
                    conn.sendall(reply.encode('utf-8'))
                    print("Data has been sent!")
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
                        print("index =", command_list_index)
                        reply = self.command_list[command_list_index]

                        if reply != 'P':
                            print('reply is ' + str(reply))
                            conn.sendall(reply.encode('utf-8'))
                            self.update_robot_pos(reply)
                            robot_pos_json = {"type": "robot", "x": str(self.algo_robot.get_col()),
                                              "y": str(self.algo_robot.get_row()),
                                              "direction": str(self.get_robot_direction())}
                            new_pos = json.dumps(robot_pos_json)
                            conn.sendall(new_pos.encode('utf-8'))
                            print(f"Updated robot position = {new_pos} has been sent")

                        elif reply == 'P':
                            print('reply is ' + str(reply))
                            conn.sendall(reply.encode('utf-8'))

                        print("Data has been sent!")

                    except:
                        reply = 'No more stm commands left.'
                else:
                    reply = 'Unknown Command'
                    # Send the reply back to the client
                    print('reply is ' + str(reply))
                    conn.sendall(reply.encode('utf-8'))
                    print("Data has been sent!")
        conn.close()

    def get_robot_direction(self):
        direction = self.algo_robot.direction
        if direction == 1:
            return 'NORTH'
        elif direction == 2:
            return 'EAST'
        elif direction == 3:
            return 'SOUTH'
        elif direction == 4:
            return 'WEST'

    def get_obstacle(self, x1, y1):

        for i, obstacle in enumerate(self.input_obstacles):
            x2, y2, d2 = obstacle
            if x1 == x2 and y1 == y2:
                return i

    def android_to_algo(self, data):
        # Converts obstacle coordinates from Android into coordinates for algorithm

        if "type" in data.keys():
            x = int(data['x'])
            y = AREA_WIDTH//CELL_SIZE - 1 - int(data['y'])

            if "direction" in data.keys():
                d = data["direction"][0]
            else:
                d = 0

            obstacle = [x, y, d]  # Simulator coordinates
            existing = self.get_obstacle(x, y)

            if data["type"] == "obstacle":
                if existing is not None:
                    self.input_obstacles[existing][2] = d
                else:
                    self.input_obstacles.append(obstacle)
            elif data["type"] == "remove_obstacle":
                if existing:
                    self.input_obstacles.pop(existing)
                else:
                    print(f"Obstacle at ({x}, {y}) not found")

    def update_robot_pos(self, command):
        if command[0] == 'w':
            move = 'F'
            grid_distance = int(command[1:4])//10
            self.algo_robot.move(move, grid_distance)
        elif command[0] == 's':
            move = 'B'
            grid_distance = int(command[1:4])//10
            self.algo_robot.move(move, grid_distance)
        elif command[0] == 'q':
            print("Prev pos =", self.algo_robot.get_col(), self.algo_robot.get_row(), self.algo_robot.get_direction())
            move = 'L'
            self.algo_robot.turn(move)
            print("New pos =", self.algo_robot.get_col(), self.algo_robot.get_row(), self.algo_robot.get_direction())
        elif command[0] == 'e':
            print("Prev pos =", self.algo_robot.get_col(), self.algo_robot.get_row(), self.algo_robot.get_direction())
            move = 'R'
            self.algo_robot.turn(move)
            print("New pos =", self.algo_robot.get_col(), self.algo_robot.get_row(), self.algo_robot.get_direction())
        elif command[0] == 'a':
            print("Prev pos =", self.algo_robot.get_col(), self.algo_robot.get_row(), self.algo_robot.get_direction())
            move = 'IL'
            self.algo_robot.in_place(move)
            print("New pos =", self.algo_robot.get_col(), self.algo_robot.get_row(), self.algo_robot.get_direction())
        elif command[0] == 'd':
            print("Prev pos =", self.algo_robot.get_col(), self.algo_robot.get_row(), self.algo_robot.get_direction())
            move = 'IR'
            self.algo_robot.in_place(move)
            print("New pos =", self.algo_robot.get_col(), self.algo_robot.get_row(), self.algo_robot.get_direction())
        elif command[0] == 'z':
            print("Prev pos =", self.algo_robot.get_col(), self.algo_robot.get_row(), self.algo_robot.get_direction())
            move = 'BL'
            self.algo_robot.turn(move)
            print("New pos =", self.algo_robot.get_col(), self.algo_robot.get_row(), self.algo_robot.get_direction())
        elif command[0] == 'c':
            print("Prev pos =", self.algo_robot.get_col(), self.algo_robot.get_row(), self.algo_robot.get_direction())
            move = 'BR'
            self.algo_robot.turn(move)
            print("New pos =", self.algo_robot.get_col(), self.algo_robot.get_row(), self.algo_robot.get_direction())

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
