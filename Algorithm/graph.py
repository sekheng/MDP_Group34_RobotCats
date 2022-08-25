import constants

class Graph:

    def __init__(self, grid):
        self.matrix = grid.matrix
        self.num_rows = grid.num_rows
        self.num_cols = grid.num_cols

    def load_graph(self):
        """
        Generate the graph in dictionary
        Key is (Vertex, orientation)
        Value is a list of neighbours in Vertex
        :param matrix: The matrix
        :return:
        """
        for i in range(num_rows):
            for j in range(num_cols):
                for key, value in constants.directions:
                    # for each direction N S E W, construct a vertex with the same coords
                    vertex = Vertex(x=j, y=i, direction=key)
                    # find the vertex's neighbours
                    neighbours = self.__get_neighbours(x=j, y=i,direction=key)

                    # Set the graph

                    neighbour_list: [Vertex] = []
                    # Set the distance
                    for neighbour in neighbours:
                        self.dist[(vertex, neighbour[0])] = neighbour[1]
                        neighbour_list.append(neighbour[0])

                    self.graph[vertex] = neighbour_list

        # print(self.graph)
        # print(self.dist)

    def __get_neighbours(self, x, y, orientation: Direction, matrix) -> list:
        # Possible movement of the robot:
        # Forward, backward, left 90 degree, right 90 degree

        neighbours = []

        left_x_offset, left_y_offset, _ = get_turn_offsets(direction="left", orientation=orientation)
        right_x_offset, right_y_offset, _ = get_turn_offsets(direction="right", orientation=orientation)
        turn_left = (x + left_x_offset, y + left_y_offset)
        turn_right = (x + right_x_offset, y + right_y_offset)

        UNIT = 1

        if orientation == Direction.NORTH:
            forward = (x, y + UNIT)
            backward = (x, y - UNIT)
        elif orientation == Direction.SOUTH:
            forward = (x, y - UNIT)
            backward = (x, y + UNIT)
        elif orientation == Direction.WEST:
            forward = (x - UNIT, y)
            backward = (x + UNIT, y)
        elif orientation == Direction.EAST:
            forward = (x + UNIT, y)
            backward = (x - UNIT, y)
        else:
            return neighbours

        # possible actions to consider
        actions = {
            Action.FORWARD: forward,
            Action.BACKWARD: backward,
            Action.TURN_LEFT_90: turn_left,
            Action.TURN_RIGHT_90: turn_right
        }

        for action, value in actions.items():
            # action -> (x, y)
            if self.__check_bound(x=value[0], y=value[1], matrix=matrix):
                hit = False
                if action in [Action.TURN_LEFT_90, Action.TURN_RIGHT_90]:
                    # Check obstacle in the turning radius
                    # for simplicity, use square area to check
                    x_step = 1 if x < value[0] else -1
                    y_step = 1 if y < value[1] else -1

                    for i in range(y, value[1], y_step):
                        if hit:
                            break
                        for j in range(x, value[0], x_step):
                            if matrix[i][j]:
                                # obstacle detected in the turning path
                                hit = True
                                break
                if not hit:
                    if action == Action.TURN_LEFT_90:
                        new_orientation = Direction((orientation.value - 90) % 360)
                        distance = round((1 / 2) * pi * ROBOT_TURNING_RADIUS, 2)
                    elif action == Action.TURN_RIGHT_90:
                        new_orientation = Direction((orientation.value + 90) % 360)
                        distance = round((1 / 2) * pi * ROBOT_TURNING_RADIUS, 2)
                    else:
                        new_orientation = orientation
                        distance = 1

                    vertex = Vertex(x=value[0], y=value[1], orientation=new_orientation, action=action)
                    neighbours.append((vertex, distance))  # (Vertex, distance to neighbour)
        return neighbours