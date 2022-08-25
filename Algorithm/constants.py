import math

# grid cell
CELL_SIZE = 10

# area dimensions
AREA_WIDTH = 200
AREA_LENGTH = 200

# robot
CAR_WIDTH = 30
CAR_LENGTH = 30
VIEW_DIST = 20  # 20cm between camera and image
TURN_RADIUS = 25
TURN_DIST = 30
TURN_GRIDS = math.ceil(TURN_DIST/CELL_SIZE)


# directions
directions = {1: 'N', 2: 'E', 3: 'S', 4: 'W'}

# moves
moves = ['F', 'L', 'R', 'B']