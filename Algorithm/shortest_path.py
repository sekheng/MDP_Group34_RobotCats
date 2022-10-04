import itertools
from constants import *
from node import Node
from route import Route
import helper
from math import sqrt
from queue import PriorityQueue

class ShortestPath:

    def __init__(self, grid):
        self.grid = grid
        self.start = helper.to_indices([1, 1, 1])  # 1: NORTH
        self.distance = float('inf')  # distance of chosen shortest route
        self.route = []

    @staticmethod
    def get_child(curr_node, move):
        curr_pos = curr_node.pos
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
                new_pos[0], new_pos[1] = curr_pos[0] - 1, curr_pos[1] - 2
                new_pos[2] = 4  # W
            elif curr_pos[2] == 2:  # E
                new_pos[0], new_pos[1] = curr_pos[0] - 2, curr_pos[1] + 1
                new_pos[2] = 1  # N
            elif curr_pos[2] == 3:  # S
                new_pos[0], new_pos[1] = curr_pos[0] + 1, curr_pos[1] + 2
                new_pos[2] = 2  # E
            elif curr_pos[2] == 4:  # W
                new_pos[0], new_pos[1] = curr_pos[0] + 2, curr_pos[1] - 1
                new_pos[2] = 3  # S
            # new_pos[2] = (curr_pos[2] + 3) % 4
        elif move == 'R':
            if curr_pos[2] == 1:  # N
                new_pos[0], new_pos[1] = curr_pos[0] - 1, curr_pos[1] + 2
                new_pos[2] = 2 # E
            elif curr_pos[2] == 2:  # E
                new_pos[0], new_pos[1] = curr_pos[0] + 2, curr_pos[1] + 1
                new_pos[2] = 3  # S
            elif curr_pos[2] == 3:  # S
                new_pos[0], new_pos[1] = curr_pos[0] + 1, curr_pos[1] - 2
                new_pos[2] = 4  # W
            elif curr_pos[2] == 4:  # W
                new_pos[0], new_pos[1] = curr_pos[0] - 2, curr_pos[1] - 1
                new_pos[2] = 1  # N
            # new_pos[2] = (curr_pos[2] + 1) % 4
        elif move == 'IL':
            if curr_pos[2] == 1:  # N
                new_pos[2] = 4  # W
            elif curr_pos[2] == 2:  # E
                new_pos[2] = 1  # N
            elif curr_pos[2] == 3:  # S
                new_pos[2] = 2  # E
            elif curr_pos[2] == 4:  # W
                new_pos[2] = 3  # S
        elif move == 'IR':
            if curr_pos[2] == 1:  # N
                new_pos[2] = 2  # E
            elif curr_pos[2] == 2:  # E
                new_pos[2] = 3  # S
            elif curr_pos[2] == 3:  # S
                new_pos[2] = 4  # W
            elif curr_pos[2] == 4:  # W
                new_pos[2] = 1  # N
        elif move == 'BL':
            if curr_pos[2] == 1:  # N
                new_pos[0], new_pos[1] = curr_pos[0] + 2, curr_pos[1] - 1
                new_pos[2] = 2 # E
            elif curr_pos[2] == 2:  # E
                new_pos[0], new_pos[1] = curr_pos[0] - 1, curr_pos[1] - 2
                new_pos[2] = 3  # S
            elif curr_pos[2] == 3:  # S
                new_pos[0], new_pos[1] = curr_pos[0] - 2, curr_pos[1] + 1
                new_pos[2] = 4  # W
            elif curr_pos[2] == 4:  # W
                new_pos[0], new_pos[1] = curr_pos[0] + 1, curr_pos[1] + 2
                new_pos[2] = 1  # N
        elif move == 'BR':
            if curr_pos[2] == 1:  # N
                new_pos[0], new_pos[1] = curr_pos[0] + 2, curr_pos[1] + 1
                new_pos[2] = 4  # W
            elif curr_pos[2] == 2:  # E
                new_pos[0], new_pos[1] = curr_pos[0] + 1, curr_pos[1] - 2
                new_pos[2] = 1  # N
            elif curr_pos[2] == 3:  # S
                new_pos[0], new_pos[1] = curr_pos[0] - 2, curr_pos[1] - 1
                new_pos[2] = 2  # E
            elif curr_pos[2] == 4:  # W
                new_pos[0], new_pos[1] = curr_pos[0] - 1, curr_pos[1] + 2
                new_pos[2] = 3  # S

        child = Node(curr_node, move, new_pos)
        return child

    def is_move_valid(self, curr_pos, new_pos, move):
        if move in ['L', 'R', 'BL', 'BR']:
            return self.is_turn_valid(curr_pos, move)

        if move in ['IL', 'IR']:
            return self.is_in_place_valid(curr_pos)

        return self.grid.robot_pos_is_valid(new_pos)

    def is_in_place_valid(self, curr_pos):

        xi, yi, d = curr_pos

        if d == 1:  # North
            xm, ym = xi - DISP, yi
        elif d == 2:  # East
            xm, ym = xi, yi + DISP
        elif d == 3:  # South
            xm, ym = xi + DISP, yi
        elif d == 4:  # West
            xm, ym = xi, yi - DISP

        if not self.grid.robot_pos_is_valid([xm, ym, None]):
            return False

        return True

    def is_turn_valid(self, curr_pos, move):

        xi, yi, d = curr_pos
        # x is row, y is column

        if d == 1:  # North
            if move == 'L':
                xn, yn = xi - 1, yi - 2
            elif move == 'R':
                xn, yn = xi - 1, yi + 2
            elif move == 'BL':
                xn, yn = xi + 2, yi - 1
            elif move == 'BR':
                xn, yn = xi + 2, yi + 1
            xm, ym = xn, yi
        elif d == 2:  # East
            if move == 'L':
                xn, yn = xi - 2, yi + 1
            elif move == 'R':
                xn, yn = xi + 2, yi + 1
            elif move == 'BL':
                xn, yn = xi - 1, yi - 2
            elif move == 'BR':
                xn, yn = xi + 1, yi - 2
            xm, ym = xi, yn
        elif d == 3:  # South
            if move == 'L':
                xn, yn = xi + 1, yi + 2
            elif move == 'R':
                xn, yn = xi + 1, yi - 2
            elif move == 'BL':
                xn, yn = xi - 2, yi + 1
            elif move == 'BR':
                xn, yn = xi - 2, yi - 1
            xm, ym = xn, yi
        elif d == 4:  # West
            if move == 'L':
                xn, yn = xi + 2, yi - 1
            elif move == 'R':
                xn, yn = xi - 2, yi - 1
            elif move == 'BL':
                xn, yn = xi + 1, yi + 2
            elif move == 'BR':
                xn, yn = xi - 1, yi + 2
            xm, ym = xi, yn

        to_check = [[xm, ym, d], [xn, yn, d]]

        for pos in to_check:
            if not self.grid.robot_pos_is_valid(pos):
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

        for i, route in enumerate(candidate_routes):
            # if i == 2:
            #     break
            # print("Route", i, route)
            total_dist = 0
            paths = []
            prev = self.start

            possible = True

            for viewpos in route:

                if float('-inf') in viewpos:
                    print("Inaccessible obstacle")
                    return

                if total_dist > chosen_route[0]:
                    possible = False
                    break

                pt_to_pt = Route(position=viewpos)

                start = prev
                goal = viewpos

                # print("start =", start, "goal =", goal)

                if (tuple(start), tuple(goal)) not in cache:

                    if self.aStar(start, goal) is None:
                        print("No path found for", start, "to", goal)
                        possible = False
                        break

                    res_route, res_dist = self.aStar(start, goal)
                    cache[(tuple(start), tuple(goal))] = (res_route, res_dist)
                    pt_to_pt.route = res_route
                    pt_to_pt.distance = res_dist
                    total_dist += res_dist
                else:
                    # print("Cache hit")
                    route, dist = cache[(tuple(start), tuple(goal))]
                    pt_to_pt.route = route
                    pt_to_pt.distance = dist
                    total_dist += dist

                # paths = paths + ucs.get_path()
                prev = goal

                if pt_to_pt.route:
                    paths.append(pt_to_pt)

            if total_dist < chosen_route[0] and possible:
                if len(paths) != len(self.grid.obstacles):
                    print("Not every obstacle is accessible")
                    continue
                chosen_route = (total_dist, paths)

            # print("Total dist =", total_dist, "Possible =", possible)
            # print()

        self.route = chosen_route[1]
        self.distance = chosen_route[0]
        # print("Chosen shortest route =", self.route, "Cost =", self.distance)

    @staticmethod
    def h(cell1, cell2):

        x1, y1, d = cell1
        x2, y2, d = cell2
        # Manhattan distance between source to goal
        return abs(x1 - x2) + abs(y1 - y2)

        # Euclidean
        # return sqrt( ((x1 - x2)**2) + ((y1 - y2)**2) )

    def aStar(self, start, goal):

        start = Node(None, None, start)
        goal = Node(None, None, goal)
        start.f = start.h = self.h(start.pos, goal.pos)
        open = PriorityQueue()
        open.put((start.f, start.h, start))
        # parents = {}
        f_score = {}
        for row in range(self.grid.num_rows):
            for col in range(self.grid.num_cols):
                for d in range(1, 5):
                    f_score[(row, col, d)] = float('inf')

        while not open.empty():

            curr = open.get()[2]

            # if there is a shorter path to this position, don't expand this cell
            if curr.f > f_score[tuple(curr.pos)]:
                continue

            # if goal is reached, return path and distance
            if curr.pos == goal.pos:
                path = []
                current = curr
                dist = curr.g

                if current.move is None:  # if car is already at viewpos from the start +_+
                    path.append('X')

                while current.move is not None:
                    path.append(current.move)
                    current = current.parent
                return path[::-1], dist

            for move in MOVES:
                child = self.get_child(curr, move)

                if move in ['R', 'L', 'BL', 'BR']:
                    child.g = 15

                elif move in ['IL', 'IR']:
                    child.g = 30

                if not self.is_move_valid(curr.pos, child.pos, move):
                    continue

                child.g += curr.g + 10
                child.h = self.h(child.pos, goal.pos)
                child.f = child.g + child.h

                if child.f < f_score[tuple(child.pos)]:
                    f_score[tuple(child.pos)] = child.f
                    open.put((child.f, child.h, child))

