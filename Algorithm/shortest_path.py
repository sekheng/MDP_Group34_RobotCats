import itertools
import heapq
from constants import *
from node import Node
from route import Route
import helper
from point_to_point import PointToPoint


class ShortestPath:

    def __init__(self, grid):
        self.grid = grid
        self.start = helper.to_indices([1, 1, 1])  # 1: NORTH
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
            if curr_pos[2] == 1:  # N
                new_pos[2] = 4  # W
            elif curr_pos[2] == 2:  # E
                new_pos[2] = 1  # N
            elif curr_pos[2] == 3:  # S
                new_pos[2] = 2  # E
            elif curr_pos[2] == 4:  # W
                new_pos[2] = 3  # S
            # new_pos[2] = (curr_pos[2] + 3) % 4
        elif move == 'R':
            if curr_pos[2] == 1:  # N
                new_pos[2] = 2 # E
            elif curr_pos[2] == 2:  # E
                new_pos[2] = 3  # S
            elif curr_pos[2] == 3:  # S
                new_pos[2] = 4  # W
            elif curr_pos[2] == 4:  # W
                new_pos[2] = 1  # N
            # new_pos[2] = (curr_pos[2] + 1) % 4

        child = Node(curr_node, move, new_pos)
        # print("Child", new_pos)
        return child

    def is_move_valid(self, curr_pos, new_pos, move):
        # if move == 'L' or move == 'R':
        #     return self.is_turn_valid(curr_pos, move)

        return self.grid.robot_pos_is_valid(new_pos)

    def is_turn_valid(self, curr_pos, move):

        xi, yi, d = curr_pos

        # print("d =", d, ",move =", move)

        if (d == 1 and move == 'L') or (d == 4 and move == 'R'):
            xn, yn = xi - TURN_GRIDS, yi - TURN_GRIDS
            # print("xn =", xn)
        elif (d == 4 and move == 'L') or (d == 3 and move == 'R'):
            xn, yn = xi + TURN_GRIDS, yi - TURN_GRIDS
            # print("xn =", xn)
        elif (d == 3 and move == 'L') or (d == 2 and move == 'R'):
            xn, yn = xi + TURN_GRIDS, yi + TURN_GRIDS
            # print("xn =", xn)
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
        print("Viewing positions:", viewing_pos)
        candidate_routes = list(itertools.permutations(viewing_pos))  # get all path permutations
        chosen_route = (float('inf'), None)  # total distance, path

        possible = True

        # print("candidate routes =", candidate_routes)
        for i, route in enumerate(candidate_routes):
            # if i == 4:
            #     break
            # print("route =", route)
            total_dist = 0
            paths = []
            start = self.start

            # print("---------------------------------")

            for viewpos in route:

                # print("viewpos =", viewpos)

                if total_dist > chosen_route[0]:
                    possible = False
                    break

                pt_to_pt = Route(position=viewpos)

                goal = viewpos

                if start == goal:
                    continue

                # print("start =", start, "goal =", goal)

                if (tuple(start), tuple(goal)) not in cache:
                    path = self.astar(start, goal)
                    if path is None:
                        print("No path found for this route")
                        possible = False
                        break

                    cache[(tuple(start), tuple(goal))] = (path.distance, path.route)
                    pt_to_pt.distance = path.distance
                    total_dist += pt_to_pt.distance
                    pt_to_pt.route = path.route
                else:
                    # print("Cache hit")
                    dist, path = cache[(tuple(start), tuple(goal))]
                    # print(dist, path)
                    pt_to_pt.distance = dist
                    pt_to_pt.route = path
                    total_dist += pt_to_pt.distance

                # paths = paths + ucs.get_path()
                start = goal

                if pt_to_pt.route:
                    paths.append(pt_to_pt)

            if total_dist < chosen_route[0] and possible:
                if len(paths) != len(self.grid.obstacles):
                    print("Not every obstacle is accessible")
                    continue
                chosen_route = (total_dist, paths)

        self.route = chosen_route[1]
        self.distance = chosen_route[0]

    def astar(self, start, goal):
        # Create start and goal node
        start_node = Node(None, None, start)
        start_node.g = start_node.h = start_node.f = 0
        goal_node = Node(None, None, goal)
        goal_node.g = goal_node.h = goal_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        heapq.heappush(open_list, start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node, pop current off open list
            current_node = heapq.heappop(open_list)
            # print("current node =", current_node.position)

            # Add to closed list
            closed_list.append(tuple(current_node.position))

            # Found the goal
            if current_node.position == goal_node.position:  # == end
                print("goal found", current_node.position)
                pt_to_pt = PointToPoint()
                current = current_node
                while current.prev_move is not None:
                    pt_to_pt.route.insert(0, current.prev_move)
                    pt_to_pt.distance += current.g
                    current = current.parent
                return pt_to_pt  # Return reversed path and distance

            # Generate children
            children = []
            for move in moves:  # Adjacent squares

                # get new possible child node
                child = self.get_child(current_node, move)
                if move == 'R' or move == 'L':
                    child.g = 1

                if move == 'B':
                    child.g = 1

                # Get node position
                node_position = child.position

                # Make sure within range and valid
                if not self.is_move_valid(current_node.position, node_position, move):
                    # print("Invalid move from", current_node.position, "to", node_position)
                    continue

                # Append
                children.append(child)

            # print("Children =", children)
            # Loop through children
            for child in children:

                # print("child", child)

                # Child is on the closed list
                if tuple(child.position) in closed_list:
                    continue

                # Create the f, g, and h values
                child.g += current_node.g + 1
                # Using manhattan distance as heuristic
                child.h = abs(child.position[0] - goal_node.position[0]) + abs(child.position[1] - goal_node.position[1])
                child.f = child.g + child.h

                # If child is already in open list, but has a higher f in open list, update to new (lower) f
                exists = False
                for idx in range(len(open_list)):
                    open_node = open_list[idx]
                    if child.position == open_node.position:
                        # print(child.position, "already exists")
                        exists = True
                        if child.f < open_node.f:
                            open_list.pop(idx)
                            open_list.append(child)
                            heapq.heapify(open_list)
                            break

                # If child not in either lists (not visited or queued), add child to the open list
                if not exists:
                    heapq.heappush(open_list, child)


        # print("closed list=", closed_list)