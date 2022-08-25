import itertools
import heapq
from constants import *
from node import Node
from route import Route
import helper


class ShortestPath:

    def __init__(self, grid):
        self.grid = grid
        self.start = [18, 1, 1]  # 1: NORTH
        self.distance = float('inf')  # distance of chosen shortest route
        self.route = None

    @staticmethod
    def get_child(curr_node, move):
        curr_pos = curr_node.position
        new_pos = curr_pos[:]
        if move == 'F':
            if curr_pos[2] == 1:  # car facing NORTH
                new_pos[0] -= 1
            elif curr_pos[2] == 3:  # car facing SOUTH
                new_pos[0] += 1
            elif curr_pos[2] == 2:  # car facing EAST
                new_pos[1] += 1
            elif curr_pos[2] == 4:  # car facing WEST
                new_pos[1] -= 1
        elif move == 'B':
            if curr_pos[2] == 1:
                new_pos[0] += 1
            elif curr_pos[2] == 3:
                new_pos[0] -= 1
            elif curr_pos[2] == 2:
                new_pos[1] -= 1
            elif curr_pos[2] == 4:
                new_pos[1] += 1
        elif move == 'L':
            new_pos[2] = (curr_pos[2] + 3) % 4
        elif move == 'R':
            new_pos[2] = (curr_pos[2] + 1) % 4

        child = Node(curr_node, move, new_pos)
        return child

    def is_move_valid(self, curr_pos, new_pos, move):
        if move == 'L' or move == 'R':
            return self.is_turn_valid(curr_pos, move)

        return self.grid.robot_pos_is_valid(new_pos)

    def is_turn_valid(self, curr_pos, move):

        xi, yi, d = curr_pos
        if (d == 1 and move == 'L') or (d == 4 and move == 'R'):
            xn, yn = xi - TURN_GRIDS, yi - TURN_GRIDS
        elif (d == 4 and move == 'L') or (d == 3 and move == 'R'):
            xn, yn = xi + TURN_GRIDS, yi - TURN_GRIDS
        elif (d == 3 and move == 'L') or (d == 2 and move == 'R'):
            xn, yn = xi + TURN_GRIDS, yi + TURN_GRIDS
        elif (d == 2 and move == 'L') or (d == 1 and move == 'R'):
            xn, yn = xi - TURN_GRIDS, yi + TURN_GRIDS

        for x in range(min(xi, xn), max(xi, xn) + 1):
            for y in range(min(yi, yn), max(yi, yn) + 1):
                if not self.grid.robot_pos_is_valid([x, y, None]):
                    return False

        return True

    def get_shortest_path(self):

        cache = {}  # key = (start.id,goal.id)
        # value = point-to-point path and distance
        # already computed point-to-point distances

        viewing_pos = list(obs.viewpos for obs in self.grid.obstacles)
        candidate_routes = list(itertools.permutations(viewing_pos))  # get all path permutations
        chosen_route = (float('inf'), None)  # total distance, path

        possible = True

        for route in candidate_routes:
            total_dist = 0
            paths = []
            start = self.start

            for viewpos in route:

                if total_dist > chosen_route[0]:
                    possible = False
                    break

                pt_to_pt = Route(position=viewpos)

                goal = viewpos

                if (tuple(start), tuple(goal)) not in cache:
                    path = self.astar(start, goal)
                    print(type(path))
                    if len(path['steps']) > 0:
                        print("No path found for this route")
                        possible = False
                        break

                    cache[(start, goal)] = (path['dist'], path['steps'])
                    pt_to_pt.distance = path['dist']
                    total_dist += pt_to_pt.distance
                    pt_to_pt.route = path['steps']
                else:
                    # print("Cache hit")
                    dist, path = cache[(start, goal)]
                    # print(dist, path)
                    pt_to_pt.distance = dist
                    pt_to_pt.route = path

                # paths = paths + ucs.get_path()
                start = goal

                if pt_to_pt.route:
                    paths.append(pt_to_pt)

            if total_dist < chosen_route[0] and possible:
                if len(paths) != len(self.grid.obstacles):
                    print("Not every obstacle is accessible")
                chosen_route = (total_dist, paths)

        self.route = chosen_route[1]
        self.distance = chosen_route[0]

        return self.route

    def astar(self, start, goal):
        # Create start and goal node
        start_node = Node(None, None, start)
        start_node.g = start_node.h = start_node.f = 0
        goal_node = Node(None, None, goal)
        goal_node.g = goal_node.h = goal_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = set()

        # Add the start node
        heapq.heappush(open_list, start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node, pop current off open list
            current_node = heapq.heappop(open_list)

            # Add to closed list
            closed_list.add(tuple(current_node.position))

            # Found the goal
            if current_node.position == goal_node.position:  # == end
                path = []
                dist = 0
                current = current_node
                while current.prev_move is not None:
                    path.append(current.prev_move)
                    dist += current.g
                    current = current.parent
                return {'steps': path[::-1], 'dist': dist}  # Return reversed path and distance

            # Generate children
            children = []
            for move in moves:  # Adjacent squares

                # get new possible child node
                child = self.get_child(current_node, move)
                if move == 'R' or move == 'L':
                    child.g = 30

                if move == 'B':
                    child.g = 10

                # Get node position
                node_position = child.position

                # Make sure within range and valid
                if not self.is_move_valid(current_node.position, node_position, move):
                    continue

                # Append
                children.append(child)

            # Loop through children
            for child in children:

                # Child is on the closed list
                if tuple(child.position) in closed_list:
                    continue

                # Create the f, g, and h values
                child.g += current_node.g + 1
                # Using manhattan distance as heuristic
                child.h = abs(child.position[0] - goal_node.position[0]) + abs(child.position[1] - goal_node.position[1])
                child.f = child.g + child.h

                # If child is already in open list, but has a higher f in open list, update to new (lower) f
                for idx in range(len(open_list)):
                    open_node = open_list[idx]
                    if child.position == open_node.position:
                        if child.f < open_node.f:
                            open_list.pop(idx)
                            open_list.append(child)
                            heapq.heapify(open_list)

                # If child not in either lists (not visited or queued), add child to the open list
                heapq.heappush(open_list, child)
