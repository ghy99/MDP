import socket

# PyGame settings
SCALING_FACTOR = 3
FRAMES = 50
WINDOW_SIZE = 800, 650

# Connection to RPi
RPI_HOST: str = "192.168.45.45"
RPI_PORT: int = 5180

# Connection to PC
PC_HOST: str = socket.gethostbyname(socket.gethostname())
PC_PORT: int = 4161

# Robot Attributes
ROBOT_LENGTH = 20
# ROBOT_X_TURN_RADIUS = 30 * SCALING_FACTOR
# ROBOT_Y_TURN_RADIUS = 30 * SCALING_FACTOR
# ROBOT_AVERAGE_TURN_RADIUS = (ROBOT_X_TURN_RADIUS+ROBOT_Y_TURN_RADIUS)/2
ROBOT_TURN_RADIUS = 30
ROBOT_SPEED_PER_SECOND = 100  # should be 33.3
ROBOT_S_FACTOR = ROBOT_LENGTH / ROBOT_TURN_RADIUS  # Please read briefing notes from Imperial
ROBOT_SAFETY_DISTANCE = 15
ROBOT_SCAN_TIME = 0.25  # Time provided for scanning an obstacle image in seconds.

# Grid Attributes
GRID_LENGTH = 200
GRID_CELL_LENGTH = 10
GRID_START_BOX_LENGTH = 30
NO_OF_GRID_CELLS_PER_SIDE = GRID_LENGTH // GRID_CELL_LENGTH
OFFSET = GRID_CELL_LENGTH // 2

# Obstacle Attributes
OBSTACLE_LENGTH = 10
OBSTACLE_SAFETY_WIDTH = 20
# OBSTACLE_SAFETY_WIDTH = ROBOT_SAFETY_DISTANCE // 3 * 4  # With respect to the center of the obstacle

# Path Finding Attributes
PATH_TURN_COST = 999 * ROBOT_SPEED_PER_SECOND * ROBOT_TURN_RADIUS
SPOT_TURN_COST = 999 * ROBOT_SPEED_PER_SECOND * ROBOT_TURN_RADIUS
# NOTE: Higher number == Lower Granularity == Faster Checking.
# Must be an integer more than 0! Number higher than 3 not recommended.
PATH_TURN_CHECK_GRANULARITY = 1

# COLOURS
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DARK_GREEN = (0, 80, 0)
GREY = (220, 220, 220)
PLATINUM = (229, 228, 226)
DARK_GRAY = (169, 169, 169)
SILVER = (192, 192, 192)
DARK_YELLOW = (236, 183, 83)
LIGHT_YELLOW = (255,255,153)

PINK = (255, 51, 255)
PURPLE = (153, 51, 255)
DARK_BLUE = (51, 51, 255)
ORANGE = (255, 153, 51)