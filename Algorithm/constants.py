import math

# grid cell
CELL_SIZE = 10

# area dimensions
AREA_WIDTH = 200
AREA_LENGTH = 200

# robot
CAR_WIDTH = 30
CAR_LENGTH = 30
VIEW_DIST = 30
# TURN_DIST = 30
# TURN_GRIDS = math.ceil(TURN_DIST/CELL_SIZE)
DISP = 10 // CELL_SIZE  # In-place displacement


# directions
# N = 0, E = 1, S = 2, W = 3

# moves
MOVES = ['F', 'L', 'R', 'B', 'IL', 'IR']

# obstacles markings
OBS_MARKINGS = {'N', 'S', 'E', 'W'}

# colors
IMAGE_COL = [100,149,237]
OBSTACLE_COL = [37, 37, 38]