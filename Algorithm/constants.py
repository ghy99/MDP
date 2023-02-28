import socket

# PyGame settings
SCALING_FACTOR = 3
FRAMES = 50
WINDOW_SIZE = 800, 650

# Connection to RPi
RPI_HOST: str = "192.168.17.1"
RPI_PORT: int = 6000

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
# Please read briefing notes from Imperial
ROBOT_S_FACTOR = ROBOT_LENGTH / ROBOT_TURN_RADIUS
ROBOT_SAFETY_DISTANCE = 10
# Time provided for scanning an obstacle image in seconds.
ROBOT_SCAN_TIME = 0.25

# Grid Attributes
GRID_LENGTH = 200
GRID_CELL_LENGTH = 10
GRID_START_BOX_LENGTH = 30
NO_OF_GRID_CELLS_PER_SIDE = GRID_LENGTH // GRID_CELL_LENGTH
OFFSET = GRID_CELL_LENGTH // 2

# Task 2 30x10 grid
TASK2_LENGTH = 400
TASK2_WIDTH = 150
TASK2_SCALING_FACTOR = 1

BUTTON_LENGTH = 100
BUTTON_WIDTH = 30
# Obstacle Attributes
OBSTACLE_LENGTH = 10
OBSTACLE_SAFETY_WIDTH = 10
# OBSTACLE_SAFETY_WIDTH = ROBOT_SAFETY_DISTANCE // 3 * 4  # With respect to the center of the obstacle

# Path Finding Attributes
PATH_TURN_COST = 999 * ROBOT_SPEED_PER_SECOND * ROBOT_TURN_RADIUS
SPOT_TURN_COST = 999 * ROBOT_SPEED_PER_SECOND * ROBOT_TURN_RADIUS
# NOTE: Higher number == Lower Granularity == Faster Checking.
# Must be an integer more than 0! Number higher than 3 not recommended.
PATH_TURN_CHECK_GRANULARITY = 1

# COLOURS
RED = (242, 0, 0)
GREEN = (26, 255, 0)
BLUE = (6, 46, 250)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (163, 163, 194)

DARK_GREEN = (0, 80, 0)
PLATINUM = (229, 228, 226)
DARK_GRAY = (169, 169, 169)
SILVER = (192, 192, 192)
DARK_YELLOW = (236, 183, 83)
LIGHT_YELLOW = (255, 255, 153)

PINK = (255, 51, 255)
PURPLE = (153, 51, 255)
DARK_BLUE = (51, 51, 255)
ORANGE = (255, 154, 0)

YELLOW = (255, 255, 18)
LIGHT_BLUE = (1, 255, 255)

# TYPE_OF_TURN ___ DIRECTION_TO_TURN ___ ROBOT_INITIAL_DIRECTION ___ FWD/REV

TURN_SMALL_LEFT_TOP_FORWARD = (-10, 40)
TURN_SMALL_LEFT_BOTTOM_FORWARD = (10, -40)
TURN_SMALL_LEFT_RIGHT_FORWARD = (40, 10)
TURN_SMALL_LEFT_LEFT_FORWARD = (-40, -10)

TURN_SMALL_RIGHT_TOP_FORWARD = (10, 40)
TURN_SMALL_RIGHT_BOTTOM_FORWARD = (-10, -40)
TURN_SMALL_RIGHT_RIGHT_FORWARD = (40, -10)
TURN_SMALL_RIGHT_LEFT_FORWARD = (-40, 10)

TURN_MED_LEFT_TOP_FORWARD = (-30, 20)
TURN_MED_LEFT_BOTTOM_FORWARD = (30, -20)
TURN_MED_LEFT_RIGHT_FORWARD = (20, 30)
TURN_MED_LEFT_LEFT_FORWARD = (-20, -30)

TURN_MED_RIGHT_TOP_FORWARD = (30, 20)
TURN_MED_RIGHT_BOTTOM_FORWARD = (-30, -20)
TURN_MED_RIGHT_RIGHT_FORWARD = (20, -30)
TURN_MED_RIGHT_LEFT_FORWARD = (-20, 30)

TURN_SMALL_LEFT_TOP_REVERSE = (-10, -40)
TURN_SMALL_LEFT_BOTTOM_REVERSE = (10, 40)
TURN_SMALL_LEFT_RIGHT_REVERSE = (-40, 10)
TURN_SMALL_LEFT_LEFT_REVERSE = (40, -10)

TURN_SMALL_RIGHT_TOP_REVERSE = (10, -40)
TURN_SMALL_RIGHT_BOTTOM_REVERSE = (-10, 40)
TURN_SMALL_RIGHT_RIGHT_REVERSE = (-40, -10)
TURN_SMALL_RIGHT_LEFT_REVERSE = (40, 10)

TURN_MED_LEFT_TOP_REVERSE = (-20, -30)
TURN_MED_LEFT_BOTTOM_REVERSE = (20, 30)
TURN_MED_LEFT_RIGHT_REVERSE = (-30, 20)
TURN_MED_LEFT_LEFT_REVERSE = (30, -20)

TURN_MED_RIGHT_TOP_REVERSE = (20, -30)
TURN_MED_RIGHT_BOTTOM_REVERSE = (-20, 30)
TURN_MED_RIGHT_RIGHT_REVERSE = (-30, -20)
TURN_MED_RIGHT_LEFT_REVERSE = (30, 20)
