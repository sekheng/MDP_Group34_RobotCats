import logging
from time import sleep
from robot import Robot
from grid import Grid


class Actions:
    def __init__(self, robot: Robot, algo_grid: Grid):
        self.logger = logging.getLogger("Actions")
        self.robot = robot
        print(self.robot)
        self.obstacles = algo_grid.obstacles
        print(self.obstacles)
        self.routes = None
        self.selected_route = None
        self.is_completed = True

    def enqueue(self, routes):

        if not routes:
            print("No routes")
            self.logger.info("No routes enqueued")
            return

        print("There are routes")
        self.routes = routes
        self.selected_route = None
        self.is_completed = False

    def dequeue(self):

        if self.selected_route:
            if not self.selected_route.route:
                # If no more moves for this route, capture image
                sleep(5)
                # TODO: Only mark as visited when image rec is successful
                for o in self.obstacles:
                    if o.viewpos == self.selected_route.position:
                        o.visited = True  # Mark obstacle as visited
                self.selected_route = None
                return

            sleep(0.5)
            move = self.selected_route.route.pop(0)

            self.logger.debug(f"Current move: {move}")

            if move == 'F':
                self.robot.move('F')
            elif move == 'B':
                self.robot.move('B')
            elif move == 'L':
                # self.skip = True
                self.robot.turn('L')
                sleep(2)
            elif move == 'R':
                # self.skip = True
                self.robot.turn('R')
                sleep(2)

            return self.robot, move

        else:
            self.logger.debug("Nothing left to dequeue in current route.")
            if self.routes:
                print(self.routes)
                self.logger.debug("Moving on to next route...")
                self.selected_route = self.routes.pop(0)
            else:
                self.logger.debug("All routes traversed.")
                self.is_completed = True

    def get_current_route(self):
        return self.selected_route

    def clear(self):
        self.routes = None
        self.selected_route = None
        self.is_completed = True