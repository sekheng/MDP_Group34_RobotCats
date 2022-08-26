class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, move=None, position=None):
        self.parent = parent
        self.prev_move = move
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
            return self.f < other.f

    def __repr__(self):
            return str(self.position)