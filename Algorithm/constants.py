import math

# grid cell
CELL_SIZE = 10

# area dimensions
AREA_WIDTH = 200
AREA_LENGTH = 200

# robot
CAR_WIDTH = 30
CAR_LENGTH = 30
VIEW_DIST = 20 + 10 + 5 # 20cm between camera and image + 10cm car border
TURN_RADIUS = 25
TURN_DIST = 20
TURN_GRIDS = math.ceil(TURN_DIST/CELL_SIZE)


# directions
# N = 0, E = 1, S = 2, W = 3

# moves
MOVES = ['F', 'L', 'R', 'B']

# obstacles markings
OBS_MARKINGS = {'N', 'S', 'E', 'W', 'X'}